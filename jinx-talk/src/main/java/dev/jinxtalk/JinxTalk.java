package dev.jinxtalk;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.atomic.AtomicBoolean;
import net.minecraft.core.Holder;
import net.minecraft.network.chat.Component;
import net.minecraft.network.protocol.game.ClientboundSetSubtitleTextPacket;
import net.minecraft.network.protocol.game.ClientboundSetTitleTextPacket;
import net.minecraft.network.protocol.game.ClientboundSetTitlesAnimationPacket;
import net.minecraft.network.protocol.game.ClientboundSoundPacket;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.ServerChatEvent;
import net.neoforged.neoforge.event.server.ServerStartingEvent;
import net.neoforged.neoforge.event.server.ServerStoppingEvent;
import net.neoforged.neoforge.event.tick.ServerTickEvent;

@Mod(JinxTalk.MOD_ID)
public final class JinxTalk {
    public static final String MOD_ID = "jinxtalk";
    public static final int CUE_POLL_TICKS = 100; // 5 seconds at 20 ticks/second

    private final AtomicBoolean cuePollInFlight = new AtomicBoolean();
    private JinxHttpClient http;
    private int serverCueTicks;

    public JinxTalk(ModContainer container) {
        container.registerConfig(ModConfig.Type.COMMON, JinxConfig.SPEC);
        NeoForge.EVENT_BUS.register(this);
    }

    @SubscribeEvent
    public void onServerStarting(ServerStartingEvent event) {
        // A new client for every world/server, including integrated-server world restarts.
        http = new JinxHttpClient();
        serverCueTicks = 0;
        cuePollInFlight.set(false);
    }

    @SubscribeEvent
    public void onServerStopping(ServerStoppingEvent event) {
        if (http != null) {
            http.close();
            http = null;
        }
        serverCueTicks = 0;
        cuePollInFlight.set(false);
    }

    @SubscribeEvent(priority = EventPriority.HIGH)
    public void onChat(ServerChatEvent event) {
        if (!JinxConfig.ENABLED.get()) {
            return;
        }
        Optional<String> prompt = ChatProtocol.prompt(event.getRawText());
        if (prompt.isEmpty()) {
            return;
        }
        event.setCanceled(true);
        ServerPlayer player = event.getPlayer();
        if (prompt.get().isEmpty()) {
            send(player, ChatProtocol.HELP);
            return;
        }

        send(player, ChatProtocol.PREFIX + "thinking...");
        MinecraftServer server = player.getServer();
        JinxHttpClient client = http;
        if (server == null || client == null) {
            send(player, ChatProtocol.OFFLINE);
            return;
        }
        // Snapshot all game state and config here. Workers never access Minecraft objects.
        ChatProtocol.Request request = new ChatProtocol.Request(event.getUsername(), prompt.get(),
                List.of(player.getX(), player.getY(), player.getZ()),
                player.level().dimension().location().toString(), System.currentTimeMillis());
        String base = JinxConfig.SERVICE_BASE_URL.get();
        client.chat(base, request).whenComplete((reply, failure) -> {
            List<String> lines = failure == null ? ChatProtocol.replyLines(reply) : List.of(ChatProtocol.OFFLINE);
            try {
                server.execute(() -> {
                    // Do not send a stale response to a new login with the same UUID or another world.
                    if (http == client && server.getPlayerList().getPlayer(player.getUUID()) == player) {
                        if (failure == null) {
                            JinxHistory.SESSION.append(reply);
                        }
                        lines.forEach(line -> send(player, line));
                    }
                });
            } catch (RejectedExecutionException ignored) {
                // A server that has already shut down cannot receive chat replies.
            }
        });
    }

    @SubscribeEvent
    public void onServerTick(ServerTickEvent.Post event) {
        MinecraftServer server = event.getServer();
        // On a physical client (single-player), JinxClient polls /cues once per 5s so single-player never double-polls.
        if (!server.isDedicatedServer()) {
            return;
        }
        if (++serverCueTicks < CUE_POLL_TICKS) {
            return;
        }
        serverCueTicks = 0;
        JinxHttpClient client = http;
        if (client == null || !JinxConfig.ENABLED.get() || !cuePollInFlight.compareAndSet(false, true)) {
            return;
        }
        String base = JinxConfig.SERVICE_BASE_URL.get();
        client.cues(base).whenComplete((cues, failure) -> {
            cuePollInFlight.set(false);
            if (failure != null || cues == null || cues.isEmpty()) {
                return;
            }
            try {
                server.execute(() -> {
                    if (http == client) {
                        deliverServerCues(server, cues);
                    }
                });
            } catch (RejectedExecutionException ignored) {
                // Silent on shutdown.
            }
        });
    }

    private static void deliverServerCues(MinecraftServer server, List<ChatProtocol.Cue> cues) {
        List<ServerPlayer> players = server.getPlayerList().getPlayers();
        if (players.isEmpty()) {
            return;
        }
        for (ChatProtocol.Cue cue : cues) {
            switch (cue) {
                case ChatProtocol.Cue.Chat chat -> {
                    Component message = Component.literal(chat.text());
                    players.forEach(player -> send(player, message));
                }
                case ChatProtocol.Cue.Title title -> {
                    var times = new ClientboundSetTitlesAnimationPacket(10, 70, 20);
                    var sub = new ClientboundSetSubtitleTextPacket(
                            title.subtitle() != null ? Component.literal(title.subtitle()) : Component.empty());
                    var main = new ClientboundSetTitleTextPacket(Component.literal(title.text()));
                    for (ServerPlayer player : players) {
                        player.connection.send(times);
                        player.connection.send(sub);
                        player.connection.send(main);
                    }
                }
                case ChatProtocol.Cue.Sound sound -> {
                    ResourceLocation id = ResourceLocation.tryParse(sound.sound());
                    if (id == null) {
                        continue;
                    }
                    Holder<SoundEvent> holder = Holder.direct(SoundEvent.createVariableRangeEvent(id));
                    for (ServerPlayer player : players) {
                        player.connection.send(new ClientboundSoundPacket(
                                holder, SoundSource.MASTER,
                                player.getX(), player.getY(), player.getZ(),
                                1.0F, 1.0F, player.getRandom().nextLong()));
                    }
                }
            }
        }
    }

    private static void send(ServerPlayer player, String text) {
        send(player, Component.literal(text));
    }

    private static void send(ServerPlayer player, Component message) {
        player.sendSystemMessage(message);
    }
}

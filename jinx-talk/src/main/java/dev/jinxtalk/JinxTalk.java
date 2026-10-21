package dev.jinxtalk;

import java.util.List;
import java.util.Optional;
import java.util.concurrent.RejectedExecutionException;
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.server.level.ServerPlayer;
import net.neoforged.bus.api.EventPriority;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.ServerChatEvent;
import net.neoforged.neoforge.event.server.ServerStartingEvent;
import net.neoforged.neoforge.event.server.ServerStoppingEvent;

@Mod(JinxTalk.MOD_ID)
public final class JinxTalk {
    public static final String MOD_ID = "jinxtalk";
    private JinxHttpClient http;

    public JinxTalk(ModContainer container) {
        container.registerConfig(ModConfig.Type.COMMON, JinxConfig.SPEC);
        NeoForge.EVENT_BUS.register(this);
    }

    @SubscribeEvent
    public void onServerStarting(ServerStartingEvent event) {
        // A new client for every world/server, including integrated-server world restarts.
        http = new JinxHttpClient();
    }

    @SubscribeEvent
    public void onServerStopping(ServerStoppingEvent event) {
        if (http != null) {
            http.close();
            http = null;
        }
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
                        lines.forEach(line -> send(player, line));
                    }
                });
            } catch (RejectedExecutionException ignored) {
                // A server that has already shut down cannot receive chat replies.
            }
        });
    }

    private static void send(ServerPlayer player, String text) {
        player.sendSystemMessage(Component.literal(text));
    }
}

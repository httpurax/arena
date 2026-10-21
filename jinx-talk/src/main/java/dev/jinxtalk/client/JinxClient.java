package dev.jinxtalk.client;

import com.mojang.blaze3d.platform.InputConstants;
import dev.jinxtalk.ChatProtocol;
import dev.jinxtalk.JinxConfig;
import dev.jinxtalk.JinxHistory;
import dev.jinxtalk.JinxHttpClient;
import dev.jinxtalk.JinxTalk;
import java.util.List;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.multiplayer.ClientLevel;
import net.minecraft.client.player.LocalPlayer;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.sounds.SoundEvent;
import net.neoforged.api.distmarker.Dist;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.client.event.ClientTickEvent;
import net.neoforged.neoforge.client.event.RegisterKeyMappingsEvent;
import net.neoforged.neoforge.common.NeoForge;
import org.lwjgl.glfw.GLFW;

@Mod(value = JinxTalk.MOD_ID, dist = Dist.CLIENT)
public final class JinxClient {
    public static final String KEY_CATEGORY = "Jinx Talk";
    public static final String OPEN_KEY_NAME = "key.jinxtalk.open_chat";
    public static final KeyMapping OPEN_CHAT_KEY = new KeyMapping(
            OPEN_KEY_NAME, InputConstants.Type.KEYSYM, GLFW.GLFW_KEY_J, KEY_CATEGORY);

    private final JinxHttpClient http = new JinxHttpClient();
    private final AtomicBoolean cuePollInFlight = new AtomicBoolean();
    private final AtomicInteger pendingChatCount = new AtomicInteger();
    private volatile boolean lastChatFailed;
    private int cueTickCounter;

    public JinxClient(IEventBus modBus) {
        modBus.addListener(this::onRegisterKeyMappings);
        NeoForge.EVENT_BUS.register(this);
    }

    private void onRegisterKeyMappings(RegisterKeyMappingsEvent event) {
        event.register(OPEN_CHAT_KEY);
    }

    @SubscribeEvent
    public void onClientTick(ClientTickEvent.Post event) {
        Minecraft mc = Minecraft.getInstance();
        while (OPEN_CHAT_KEY.consumeClick()) {
            if (mc.player != null && mc.level != null && mc.screen == null) {
                mc.setScreen(new JinxChatScreen(this));
            }
        }

        if (mc.level == null || mc.player == null) {
            cueTickCounter = 0;
            return;
        }
        if (++cueTickCounter < JinxTalk.CUE_POLL_TICKS) {
            return;
        }
        cueTickCounter = 0;
        if (!JinxConfig.ENABLED.get() || !cuePollInFlight.compareAndSet(false, true)) {
            return;
        }

        ClientLevel expectedLevel = mc.level;
        String base = JinxConfig.SERVICE_BASE_URL.get();
        http.cues(base).whenComplete((cues, failure) -> {
            cuePollInFlight.set(false);
            if (failure != null || cues == null || cues.isEmpty()) {
                return;
            }
            try {
                mc.execute(() -> {
                    if (mc.level == expectedLevel && mc.player != null) {
                        applyCues(mc, cues);
                    }
                });
            } catch (RejectedExecutionException ignored) {
                // Silent when client is shutting down.
            }
        });
    }

    void submitChat(String rawMessage) {
        String message = rawMessage.strip();
        if (message.isEmpty()) {
            return;
        }
        Minecraft mc = Minecraft.getInstance();
        LocalPlayer player = mc.player;
        if (player == null) {
            return;
        }
        ChatProtocol.Request request = new ChatProtocol.Request(
                player.getScoreboardName(),
                message,
                List.of(player.getX(), player.getY(), player.getZ()),
                player.level().dimension().location().toString(),
                System.currentTimeMillis());
        String base = JinxConfig.SERVICE_BASE_URL.get();
        pendingChatCount.incrementAndGet();
        lastChatFailed = false;
        http.chat(base, request).whenComplete((reply, failure) -> {
            pendingChatCount.decrementAndGet();
            try {
                mc.execute(() -> {
                    if (failure == null) {
                        lastChatFailed = false;
                        JinxHistory.SESSION.append(reply);
                    } else {
                        lastChatFailed = true;
                    }
                });
            } catch (RejectedExecutionException ignored) {
                // Silent when client is shutting down.
            }
        });
    }

    boolean isThinking() {
        return pendingChatCount.get() > 0;
    }

    boolean lastChatFailed() {
        return lastChatFailed;
    }

    private static void applyCues(Minecraft mc, List<ChatProtocol.Cue> cues) {
        for (ChatProtocol.Cue cue : cues) {
            switch (cue) {
                case ChatProtocol.Cue.Chat chat -> {
                    if (mc.player != null) {
                        mc.player.displayClientMessage(Component.literal(chat.text()), false);
                    }
                }
                case ChatProtocol.Cue.Title title -> {
                    mc.gui.resetTitleTimes();
                    mc.gui.setSubtitle(title.subtitle() != null
                            ? Component.literal(title.subtitle())
                            : Component.empty());
                    mc.gui.setTitle(Component.literal(title.text()));
                }
                case ChatProtocol.Cue.Sound sound -> {
                    ResourceLocation id = ResourceLocation.tryParse(sound.sound());
                    if (id == null) {
                        continue;
                    }
                    SoundEvent soundEvent = BuiltInRegistries.SOUND_EVENT.getOptional(id)
                            .orElseGet(() -> SoundEvent.createVariableRangeEvent(id));
                    mc.getSoundManager().play(SimpleSoundInstance.forUI(soundEvent, 1.0F, 1.0F));
                }
            }
        }
    }
}

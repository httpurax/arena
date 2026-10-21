package httpurax.jinxtalk;

import com.mojang.logging.LogUtils;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.ModContainer;
import net.neoforged.fml.ModList;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.fml.javafmlmod.FMLJavaModLoadingContext;
import net.neoforged.neoforge.common.NeoForge;
import net.neoforged.neoforge.event.ServerChatEvent;
import net.minecraft.server.level.ServerPlayer;
import org.slf4j.Logger;

/**
 * Jinx Talk: sends chat messages (and, when FTB Quests is installed, quest
 * completions) to an external HTTP event service and announces responses back
 * in-game.
 *
 * <p>FTB Quests is a soft dependency: the {@code ftbquests} mod id is declared
 * {@code mandatory=false} in {@code neoforge.mods.toml}, so this mod loads and
 * works whether or not FTB Quests is installed. All FTB Quests API classes live
 * in the {@code httpurax.jinxtalk.ftbquests} package, which is only referenced
 * after confirming FTB Quests is present.
 */
@Mod(JinxTalk.MOD_ID)
public class JinxTalk {
    public static final String MOD_ID = "jinxtalk";
    private static final Logger LOGGER = LogUtils.getLogger();

    public JinxTalk(IEventBus modEventBus, ModContainer container) {
        modEventBus.addListener(this::commonSetup);
        NeoForge.EVENT_BUS.register(this);

        Config.register(container);

        if (ModList.get().isLoaded("ftbquests")) {
            FtbQuestsIntegration.register();
            LOGGER.info("FTB Quests detected: quest completion integration enabled");
        } else {
            LOGGER.info("FTB Quests not detected: quest completion integration disabled");
        }
    }

    private void commonSetup(final FMLCommonSetupEvent event) {
        // Reserved for deferred setup work.
    }

    /**
     * Stage 1 of the HTTP contract: every player chat message is POSTed to
     * {@code <base>/event} as {@code {"type":"chat_message", ... }}.
     * Stage 2: if the response contains an {@code "announce"} string, the
     * chatting player is shown it in gold chat with the level-up sound
     * (see {@link HttpService}).
     */
    @SubscribeEvent
    public void onPlayerChat(ServerChatEvent event) {
        if (!Config.isEnabled() || event.isCanceled()) {
            return;
        }
        String message = event.getRawText();
        if (message == null || message.isBlank()) {
            return;
        }
        ServerPlayer player = event.getPlayer();
        HttpService.postEvent(Config.getBaseUrl(),
                HttpService.chatMessageJson(player.getName().getString(), message),
                player, Config.getTimeoutSeconds());
    }
}

package httpurax.jinxtalk.ftbquests;

import dev.architectury.event.EventResult;
import dev.ftb.mods.ftbquests.events.ObjectCompletedEvent;
import dev.ftb.mods.ftbquests.quest.Quest;
import httpurax.jinxtalk.Config;
import httpurax.jinxtalk.HttpService;
import net.minecraft.server.level.ServerPlayer;

import java.util.List;

/**
 * FTB Quests integration for jinx-talk.
 *
 * <p>This class is only loaded when FTB Quests (mod id {@code ftbquests}) is
 * installed, which {@link httpurax.jinxtalk.JinxTalk} checks first via
 * {@code ModList.get().isLoaded("ftbquests")}; without FTB Quests none of the
 * classes in this package are ever referenced, so the mod loads cleanly without
 * it (soft dependency).
 *
 * <p>Subscribes to FTB Quests' {@link ObjectCompletedEvent#QUEST} completion
 * event and POSTs a {@code quest_completed} event to
 * {@code <base>/event} for every quest a team completes, using the same base
 * URL, timeout, and failure rules as the chat path.
 */
public final class FtbQuestsIntegration {
    private FtbQuestsIntegration() {
    }

    public static void register() {
        ObjectCompletedEvent.QUEST.register(FtbQuestsIntegration::onQuestCompleted);
    }

    private static EventResult onQuestCompleted(ObjectCompletedEvent.QuestEvent event) {
        // FTB Quests also fires completion events client-side for GUI sync
        // (those carry no online team members). Only act server-side.
        if (!event.getQuest().getQuestFile().isServerSide()) {
            return EventResult.pass();
        }

        Quest quest = event.getQuest();
        List<ServerPlayer> members = event.getOnlineMembers();
        if (members.isEmpty()) {
            return EventResult.pass();
        }

        ServerPlayer player = members.get(0);

        // Quest title if one is configured, otherwise fall back to the quest id.
        String title = quest.getRawTitle();
        String questName = title.isEmpty() ? Long.toString(quest.getId()) : title;

        HttpService.postEvent(Config.getBaseUrl(),
                HttpService.questCompletedJson(questName, player.getName().getString()),
                player, Config.getTimeoutSeconds());
        return EventResult.pass();
    }
}

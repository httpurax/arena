package dev.jinxtalk.ftbquests;

import dev.architectury.event.EventResult;
import dev.ftb.mods.ftbquests.events.ObjectCompletedEvent;
import dev.ftb.mods.ftbquests.quest.Quest;
import dev.jinxtalk.QuestCompletionHandler;
import java.util.List;
import net.minecraft.server.level.ServerPlayer;

/**
 * FTB Quests integration for Jinx Talk.
 *
 * <p>This is the only class that references FTB Quests (and Architectury event)
 * API types. {@link dev.jinxtalk.JinxTalk} only calls {@link #register} after
 * {@code ModList.get().isLoaded("ftbquests")} confirms FTB Quests is installed,
 * so without FTB Quests this class is never loaded and the mod works unchanged
 * (soft dependency; declared {@code type="optional"} in
 * {@code neoforge.mods.toml} and kept {@code compileOnly} in the build, so no
 * FTB Quests code is ever bundled into the Jinx Talk jar).
 *
 * <p>Subscribes to the FTB Quests 2101.x quest-completion event
 * ({@link ObjectCompletedEvent#QUEST}) and forwards every server-side quest
 * completion to the common {@link QuestCompletionHandler}, which POSTs it to
 * {@code <base>/event}. One event is reported per completion, naming the first
 * online member of the completing team.
 */
public final class FtbQuestsIntegration {
    private FtbQuestsIntegration() {}

    public static void register(QuestCompletionHandler handler) {
        ObjectCompletedEvent.QUEST.register(event -> onQuestCompleted(event, handler));
    }

    private static EventResult onQuestCompleted(ObjectCompletedEvent.QuestEvent event,
                                                QuestCompletionHandler handler) {
        try {
            Quest quest = event.getQuest();
            // FTB Quests also fires completion events for the client-side quest
            // file (GUI sync in single-player / multiplayer clients). Only the
            // server-side file represents a real completion.
            if (quest == null || !quest.getQuestFile().isServerSide()) {
                return EventResult.pass();
            }
            List<ServerPlayer> members = event.getOnlineMembers();
            if (members == null || members.isEmpty() || members.get(0) == null) {
                return EventResult.pass();
            }
            // Quest title if one is configured, otherwise fall back to the quest id.
            String title = quest.getRawTitle();
            String questName = title == null || title.isBlank()
                    ? Long.toString(quest.getId())
                    : title;
            handler.onQuestCompleted(questName, members.get(0));
        } catch (RuntimeException ignored) {
            // A broken quest object or callback must never break FTB Quests or the game.
        }
        return EventResult.pass();
    }
}

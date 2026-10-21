package dev.jinxtalk;

import net.minecraft.server.level.ServerPlayer;

/**
 * Callback for a completed quest, deliberately free of any FTB Quests types so
 * the common (server-safe) code never has to load FTB Quests classes. The FTB
 * Quests integration in {@code dev.jinxtalk.ftbquests} adapts FTB Quests'
 * quest-completion events to this interface, and it is only loaded when the
 * {@code ftbquests} mod is installed.
 */
@FunctionalInterface
public interface QuestCompletionHandler {
    /**
     * Called on the server thread when a quest is completed.
     *
     * @param questTitleOrId the quest title if one is configured, otherwise the quest id
     * @param player         an online member of the team that completed the quest
     */
    void onQuestCompleted(String questTitleOrId, ServerPlayer player);
}

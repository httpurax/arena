package dev.jinxtalk;

import java.net.URI;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/** Pure protocol helpers; deliberately independent of Minecraft and its threads. */
public final class ChatProtocol {
    public static final String PREFIX = "[Jinx] ";
    public static final String HELP = PREFIX + "Ask me anything: !jinx what should I do next?";
    public static final String OFFLINE = PREFIX + "(offline - start jinx_link.py on the PC)";
    public static final int MAX_LINE_LENGTH = 240;

    private ChatProtocol() {}

    // Empty Optional means ordinary public chat; Optional.of("") means local help.
    public static Optional<String> prompt(String raw) {
        for (String prefix : List.of("!jinx", "!ai", "!j")) {
            if (raw.startsWith(prefix) && (raw.length() == prefix.length()
                    || Character.isWhitespace(raw.charAt(prefix.length())))) {
                return Optional.of(raw.substring(prefix.length()).strip());
            }
        }
        return Optional.empty();
    }

    public static URI chatUri(String base) {
        return endpointUri(base, "/chat");
    }

    public static URI cuesUri(String base) {
        return endpointUri(base, "/cues");
    }

    public static URI eventUri(String base) {
        return endpointUri(base, "/event");
    }

    private static URI endpointUri(String base, String pathSuffix) {
        URI uri = URI.create(base.strip());
        if (!("http".equalsIgnoreCase(uri.getScheme()) || "https".equalsIgnoreCase(uri.getScheme()))
                || uri.getHost() == null || uri.getUserInfo() != null
                || uri.getQuery() != null || uri.getFragment() != null) {
            throw new IllegalArgumentException("Expected an HTTP(S) base URL without credentials, query or fragment");
        }
        return URI.create(uri.toString().replaceAll("/+$", "") + pathSuffix);
    }

    public static List<String> replyLines(String reply) {
        List<String> result = new ArrayList<>();
        int capacity = MAX_LINE_LENGTH - PREFIX.length();
        for (String line : reply.split("\\R", -1)) {
            if (line.isEmpty()) {
                result.add(PREFIX);
                continue;
            }
            for (int start = 0; start < line.length();) {
                int end = Math.min(start + capacity, line.length());
                // Never split a UTF-16 surrogate pair across chat messages.
                if (end < line.length() && Character.isHighSurrogate(line.charAt(end - 1))
                        && Character.isLowSurrogate(line.charAt(end))) {
                    end--;
                }
                result.add(PREFIX + line.substring(start, end));
                start = end;
            }
        }
        return result;
    }

    public record Request(String player, String message, List<Double> pos, String dim, long ts) {}

    /** Body of {@code POST <base>/event} for an FTB Quests quest completion. */
    public record QuestCompletedRequest(String type, String quest, String player) {
        public static QuestCompletedRequest questCompleted(String quest, String player) {
            return new QuestCompletedRequest("quest_completed", quest, player);
        }
    }

    public sealed interface Cue permits Cue.Chat, Cue.Title, Cue.Sound {
        record Chat(String text) implements Cue {}

        record Title(String text, String subtitle) implements Cue {}

        record Sound(String sound) implements Cue {}
    }
}

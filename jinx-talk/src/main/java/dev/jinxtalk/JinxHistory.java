package dev.jinxtalk;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;

/** Thread-safe bounded store of Jinx replies received during the current game session. */
public final class JinxHistory {
    public static final int DEFAULT_CAPACITY = 50;
    public static final JinxHistory SESSION = new JinxHistory(DEFAULT_CAPACITY);

    private final int capacity;
    private final Deque<String> replies;
    private long revision;

    public JinxHistory(int capacity) {
        if (capacity < 1) {
            throw new IllegalArgumentException("Capacity must be positive");
        }
        this.capacity = capacity;
        this.replies = new ArrayDeque<>(capacity);
    }

    public synchronized void append(String reply) {
        if (reply == null || reply.isBlank()) {
            return;
        }
        if (replies.size() >= capacity) {
            replies.removeFirst();
        }
        replies.addLast(reply);
        revision++;
    }

    public synchronized List<String> snapshot() {
        return List.copyOf(replies);
    }

    public synchronized int size() {
        return replies.size();
    }

    public synchronized long revision() {
        return revision;
    }

    public synchronized void clear() {
        replies.clear();
        revision++;
    }
}

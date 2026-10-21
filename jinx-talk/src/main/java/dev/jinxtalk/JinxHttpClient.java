package dev.jinxtalk;

import com.google.gson.Gson;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonToken;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/** All URL parsing, serialization, network IO and response parsing happen on daemon workers. */
public final class JinxHttpClient implements AutoCloseable {
    public static final int CONNECT_TIMEOUT_MILLIS = 1_000;
    public static final int READ_TIMEOUT_MILLIS = 25_000;
    public static final int MAX_RESPONSE_BYTES = 65_536;
    private static final Gson GSON = new Gson();

    private final ThreadPoolExecutor workers;
    private final int connectTimeoutMillis;
    private final int readTimeoutMillis;

    public JinxHttpClient() {
        this(CONNECT_TIMEOUT_MILLIS, READ_TIMEOUT_MILLIS);
    }

    // Shorter timeouts allow deterministic local failure tests without a 25 second wait.
    public JinxHttpClient(int connectTimeoutMillis, int readTimeoutMillis) {
        this.connectTimeoutMillis = connectTimeoutMillis;
        this.readTimeoutMillis = readTimeoutMillis;
        AtomicInteger counter = new AtomicInteger();
        workers = new ThreadPoolExecutor(4, 4, 30, TimeUnit.SECONDS,
                new ArrayBlockingQueue<>(16), runnable -> {
                    Thread thread = new Thread(runnable, "jinxtalk-http-" + counter.incrementAndGet());
                    thread.setDaemon(true);
                    return thread;
                }, new ThreadPoolExecutor.AbortPolicy());
        workers.allowCoreThreadTimeOut(true);
    }

    public CompletableFuture<String> chat(String base, ChatProtocol.Request request) {
        CompletableFuture<String> result = new CompletableFuture<>();
        try {
            workers.execute(() -> {
                try {
                    result.complete(post(base, request));
                } catch (Exception exception) {
                    result.completeExceptionally(exception);
                }
            });
        } catch (RejectedExecutionException exception) {
            // Busy or stopping: fail fast, never run rejected IO on the caller/game thread.
            result.completeExceptionally(exception);
        }
        return result;
    }

    public CompletableFuture<List<ChatProtocol.Cue>> cues(String base) {
        CompletableFuture<List<ChatProtocol.Cue>> result = new CompletableFuture<>();
        try {
            workers.execute(() -> {
                try {
                    result.complete(getCues(base));
                } catch (Exception exception) {
                    result.completeExceptionally(exception);
                }
            });
        } catch (RejectedExecutionException exception) {
            result.completeExceptionally(exception);
        }
        return result;
    }

    private String post(String base, ChatProtocol.Request request) throws IOException {
        HttpURLConnection connection = (HttpURLConnection) ChatProtocol.chatUri(base).toURL().openConnection();
        try {
            connection.setConnectTimeout(connectTimeoutMillis);
            connection.setReadTimeout(readTimeoutMillis);
            connection.setInstanceFollowRedirects(false);
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json; charset=utf-8");
            connection.setRequestProperty("Accept", "application/json");
            connection.setDoOutput(true);
            byte[] body = GSON.toJson(request).getBytes(StandardCharsets.UTF_8);
            connection.setFixedLengthStreamingMode(body.length);
            try (var output = connection.getOutputStream()) {
                output.write(body);
            }
            return parseReply(readBody(connection));
        } finally {
            connection.disconnect();
        }
    }

    private List<ChatProtocol.Cue> getCues(String base) throws IOException {
        HttpURLConnection connection = (HttpURLConnection) ChatProtocol.cuesUri(base).toURL().openConnection();
        try {
            connection.setConnectTimeout(connectTimeoutMillis);
            connection.setReadTimeout(readTimeoutMillis);
            connection.setInstanceFollowRedirects(false);
            connection.setRequestMethod("GET");
            connection.setRequestProperty("Accept", "application/json");
            return parseCues(readBody(connection));
        } finally {
            connection.disconnect();
        }
    }

    private static String readBody(HttpURLConnection connection) throws IOException {
        int status = connection.getResponseCode();
        if (status < 200 || status >= 300) {
            throw new IOException("Jinx service returned HTTP " + status);
        }
        try (InputStream input = connection.getInputStream()) {
            byte[] response = input.readNBytes(MAX_RESPONSE_BYTES + 1);
            if (response.length > MAX_RESPONSE_BYTES) {
                throw new IOException("Jinx response exceeds 64 KiB");
            }
            return new String(response, StandardCharsets.UTF_8);
        }
    }

    private static String parseReply(String json) throws IOException {
        // JsonParser is lenient in Minecraft's Gson version; use a strict streaming reader instead.
        try (JsonReader reader = new JsonReader(new StringReader(json))) {
            reader.setLenient(false);
            reader.beginObject();
            String reply = null;
            while (reader.hasNext()) {
                if (reader.nextName().equals("reply")) {
                    if (reply != null || reader.peek() != JsonToken.STRING) {
                        throw new IOException("Expected a single string reply");
                    }
                    reply = reader.nextString();
                } else {
                    reader.skipValue();
                }
            }
            reader.endObject();
            if (reader.peek() != JsonToken.END_DOCUMENT || reply == null || reply.isBlank()) {
                throw new IOException("Missing, empty or malformed Jinx reply");
            }
            return reply;
        }
    }

    static List<ChatProtocol.Cue> parseCues(String json) throws IOException {
        try (JsonReader reader = new JsonReader(new StringReader(json))) {
            reader.setLenient(false);
            reader.beginObject();
            List<ChatProtocol.Cue> cues = null;
            while (reader.hasNext()) {
                if (reader.nextName().equals("cues")) {
                    if (cues != null || reader.peek() != JsonToken.BEGIN_ARRAY) {
                        throw new IOException("Expected a single cues array");
                    }
                    cues = new ArrayList<>();
                    reader.beginArray();
                    while (reader.hasNext()) {
                        ChatProtocol.Cue cue = readCue(reader);
                        if (cue != null) {
                            cues.add(cue);
                        }
                    }
                    reader.endArray();
                } else {
                    reader.skipValue();
                }
            }
            reader.endObject();
            if (reader.peek() != JsonToken.END_DOCUMENT || cues == null) {
                throw new IOException("Missing or malformed cues array");
            }
            return List.copyOf(cues);
        }
    }

    private static ChatProtocol.Cue readCue(JsonReader reader) throws IOException {
        reader.beginObject();
        String kind = null;
        String text = null;
        String subtitle = null;
        String sound = null;
        while (reader.hasNext()) {
            switch (reader.nextName()) {
                case "kind" -> kind = readOptionalString(reader);
                case "text" -> text = readOptionalString(reader);
                case "subtitle" -> subtitle = readOptionalString(reader);
                case "sound" -> sound = readOptionalString(reader);
                default -> reader.skipValue();
            }
        }
        reader.endObject();
        if (kind == null) {
            return null;
        }
        return switch (kind) {
            case "chat" -> (text != null && !text.isEmpty()) ? new ChatProtocol.Cue.Chat(text) : null;
            case "title" -> (text != null && !text.isEmpty())
                    ? new ChatProtocol.Cue.Title(text, subtitle != null && !subtitle.isEmpty() ? subtitle : null)
                    : null;
            case "sound" -> (sound != null && !sound.isBlank()) ? new ChatProtocol.Cue.Sound(sound.strip()) : null;
            default -> null;
        };
    }

    private static String readOptionalString(JsonReader reader) throws IOException {
        if (reader.peek() == JsonToken.NULL) {
            reader.nextNull();
            return null;
        }
        return reader.nextString();
    }

    @Override
    public void close() {
        // Never wait for network workers on the server thread. Socket timeouts bound pending IO.
        workers.shutdownNow();
    }
}

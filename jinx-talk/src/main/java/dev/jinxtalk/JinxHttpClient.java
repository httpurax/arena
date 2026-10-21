package dev.jinxtalk;

import com.google.gson.Gson;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonToken;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.net.HttpURLConnection;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.RejectedExecutionException;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/** All URL parsing, serialization, network IO and response parsing happen on daemon workers. */
final class JinxHttpClient implements AutoCloseable {
    static final int CONNECT_TIMEOUT_MILLIS = 1_000;
    static final int READ_TIMEOUT_MILLIS = 25_000;
    static final int MAX_RESPONSE_BYTES = 65_536;
    private static final Gson GSON = new Gson();

    private final ThreadPoolExecutor workers;
    private final int connectTimeoutMillis;
    private final int readTimeoutMillis;

    JinxHttpClient() {
        this(CONNECT_TIMEOUT_MILLIS, READ_TIMEOUT_MILLIS);
    }

    // Shorter timeouts allow deterministic local failure tests without a 25 second wait.
    JinxHttpClient(int connectTimeoutMillis, int readTimeoutMillis) {
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

    CompletableFuture<String> chat(String base, ChatProtocol.Request request) {
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
            int status = connection.getResponseCode();
            if (status < 200 || status >= 300) {
                throw new IOException("Jinx service returned HTTP " + status);
            }
            try (InputStream input = connection.getInputStream()) {
                byte[] response = input.readNBytes(MAX_RESPONSE_BYTES + 1);
                if (response.length > MAX_RESPONSE_BYTES) {
                    throw new IOException("Jinx response exceeds 64 KiB");
                }
                return parseReply(new String(response, StandardCharsets.UTF_8));
            }
        } finally {
            connection.disconnect();
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

    @Override
    public void close() {
        // Never wait for network workers on the server thread. Socket timeouts bound pending IO.
        workers.shutdownNow();
    }
}

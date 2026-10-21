package dev.jinxtalk;

import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicReference;

/** Run by ./gradlew coreTest and, transitively, ./gradlew build. No Minecraft launch needed. */
public final class ChatCoreTest {
    private static final ChatProtocol.Request REQUEST = new ChatProtocol.Request(
            "Alex", "what about \"diamonds\"?", List.of(1.5, 64.0, -3.25), "minecraft:overworld", 123456789L);

    public static void main(String[] args) throws Exception {
        prefixes();
        lines();
        urls();
        http();
        unreachable();
        saturation();
        System.out.println("Jinx Talk core tests passed.");
    }

    private static void prefixes() {
        for (String alias : List.of("!jinx", "!ai", "!j")) {
            equal("help me", ChatProtocol.prompt(alias + "  help me  ").orElseThrow());
            equal("help me", ChatProtocol.prompt(alias + "\thelp me").orElseThrow());
            equal("", ChatProtocol.prompt(alias).orElseThrow());
            equal("", ChatProtocol.prompt(alias + "   ").orElseThrow());
        }
        for (String ordinary : List.of("hello", "!joke", "!jinxed", "!air", " !jinx hi", "!JINX hi")) {
            check(ChatProtocol.prompt(ordinary).isEmpty(), "Accidentally captured " + ordinary);
        }
    }

    private static void lines() {
        for (String reply : List.of("ok", "a".repeat(1000), "x".repeat(232) + "😀".repeat(400),
                "one\r\ntwo\n\nthree\rfour", "")) {
            List<String> lines = ChatProtocol.replyLines(reply);
            for (String line : lines) {
                check(line.startsWith("[Jinx] "), "Missing prefix");
                check(line.length() <= 240, "Oversize chat line");
                check(!Character.isHighSurrogate(line.charAt(line.length() - 1)), "Split surrogate");
            }
            String reassembled = String.join("", lines.stream().map(line -> line.substring(7)).toList());
            equal(reply.replaceAll("\\R", ""), reassembled);
        }
        equal(List.of("[Jinx] one", "[Jinx] ", "[Jinx] two"), ChatProtocol.replyLines("one\n\ntwo"));
    }

    private static void urls() {
        equal("http://127.0.0.1:8712/chat", ChatProtocol.chatUri("http://127.0.0.1:8712/").toString());
        equal("https://example.test/api/chat", ChatProtocol.chatUri(" https://example.test/api/// ").toString());
        for (String bad : List.of("file:///etc/passwd", "ftp://example.test", "not a URL", "http://x?query",
                "http://x/#fragment", "http://user:pass@x", "/relative")) {
            try {
                ChatProtocol.chatUri(bad);
                throw new AssertionError("Accepted bad URL: " + bad);
            } catch (IllegalArgumentException expected) {
                // Expected.
            }
        }
    }

    private static void http() throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        AtomicReference<String> response = new AtomicReference<>("{\"reply\":\"Hello Alex!\"}");
        AtomicReference<JsonObject> received = new AtomicReference<>();
        AtomicReference<String> method = new AtomicReference<>();
        AtomicReference<String> contentType = new AtomicReference<>();
        server.createContext("/chat", exchange -> {
            method.set(exchange.getRequestMethod());
            contentType.set(exchange.getRequestHeaders().getFirst("Content-Type"));
            received.set(JsonParser.parseString(new String(exchange.getRequestBody().readAllBytes(),
                    StandardCharsets.UTF_8)).getAsJsonObject());
            String body = response.get();
            try {
                if (body.equals("DELAY")) {
                    Thread.sleep(500);
                    body = "{\"reply\":\"too late\"}";
                }
                byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
                exchange.sendResponseHeaders(body.equals("ERROR") ? 503 : 200, bytes.length);
                exchange.getResponseBody().write(bytes);
            } catch (InterruptedException interrupted) {
                Thread.currentThread().interrupt();
            } finally {
                exchange.close();
            }
        });
        server.start();
        String base = "http://127.0.0.1:" + server.getAddress().getPort();
        try (JinxHttpClient client = new JinxHttpClient(1000, 150)) {
            equal("Hello Alex!", client.chat(base, REQUEST).get(3, TimeUnit.SECONDS));
            equal("POST", method.get());
            equal("application/json; charset=utf-8", contentType.get());
            JsonObject body = received.get();
            equal(5, body.size());
            equal("Alex", body.get("player").getAsString());
            equal(REQUEST.message(), body.get("message").getAsString());
            equal(3, body.getAsJsonArray("pos").size());
            equal(1.5, body.getAsJsonArray("pos").get(0).getAsDouble());
            equal(64.0, body.getAsJsonArray("pos").get(1).getAsDouble());
            equal(-3.25, body.getAsJsonArray("pos").get(2).getAsDouble());
            equal("minecraft:overworld", body.get("dim").getAsString());
            equal(123456789L, body.get("ts").getAsLong());
            for (String invalid : List.of("ERROR", "not json", "{}", "[]", "{\"reply\":null}",
                    "{\"reply\":7}", "{\"reply\":true}", "{\"reply\":\"\"}", "{\"reply\":\"  \"}",
                    "{reply:'lenient'}", "{\"reply\":\"a\",\"reply\":\"b\"}",
                    "{\"reply\":\"ok\"} garbage", "{\"reply\":\"" + "a".repeat(65_536) + "\"}")) {
                response.set(invalid);
                fails(client.chat(base, REQUEST));
            }
            response.set("{\"extra\":{},\"reply\":\"雪 😀\"}");
            equal("雪 😀", client.chat(base, REQUEST).get(3, TimeUnit.SECONDS));
            response.set("DELAY");
            CompletableFuture<String> pending = client.chat(base, REQUEST);
            check(!pending.isDone(), "Network call ran synchronously");
            fails(pending);
            fails(client.chat("file:///invalid", REQUEST));
        } finally {
            server.stop(0);
        }
    }

    private static void unreachable() throws Exception {
        int port;
        try (ServerSocket socket = new ServerSocket(0)) {
            port = socket.getLocalPort();
        }
        JinxHttpClient client = new JinxHttpClient(100, 100);
        try {
            fails(client.chat("http://127.0.0.1:" + port, REQUEST));
        } finally {
            client.close();
        }
        fails(client.chat("http://127.0.0.1:" + port, REQUEST));
    }

    private static void saturation() throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        var handlers = Executors.newCachedThreadPool();
        CountDownLatch started = new CountDownLatch(4);
        CountDownLatch release = new CountDownLatch(1);
        server.setExecutor(handlers);
        server.createContext("/chat", exchange -> {
            started.countDown();
            try {
                release.await(3, TimeUnit.SECONDS);
            } catch (InterruptedException interrupted) {
                Thread.currentThread().interrupt();
            } finally {
                exchange.close();
            }
        });
        server.start();
        try (JinxHttpClient client = new JinxHttpClient()) {
            String base = "http://127.0.0.1:" + server.getAddress().getPort();
            for (int i = 0; i < 4; i++) {
                client.chat(base, REQUEST);
            }
            check(started.await(3, TimeUnit.SECONDS), "Workers did not start");
            for (int i = 0; i < 16; i++) {
                client.chat(base, REQUEST);
            }
            CompletableFuture<String> overflow = client.chat(base, REQUEST);
            check(overflow.isCompletedExceptionally(), "Full queue did not fail fast");
            fails(overflow);
        } finally {
            release.countDown();
            server.stop(0);
            handlers.shutdownNow();
        }
    }

    private static void fails(CompletableFuture<?> result) throws Exception {
        try {
            result.get(3, TimeUnit.SECONDS);
            throw new AssertionError("Expected failure");
        } catch (ExecutionException expected) {
            // A failed service must produce a failed future, not throw on the caller thread.
        }
    }

    private static void equal(Object expected, Object actual) {
        check(expected.equals(actual), "Expected " + expected + ", got " + actual);
    }

    private static void check(boolean condition, String message) {
        if (!condition) {
            throw new AssertionError(message);
        }
    }
}

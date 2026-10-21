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
        history();
        http();
        event();
        cues();
        unreachable();
        saturation();
        bytecodeIsolation();
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
        equal("http://127.0.0.1:8712/cues", ChatProtocol.cuesUri("http://127.0.0.1:8712/").toString());
        equal("https://example.test/api/cues", ChatProtocol.cuesUri(" https://example.test/api/// ").toString());
        equal("http://127.0.0.1:8712/event", ChatProtocol.eventUri("http://127.0.0.1:8712/").toString());
        equal("https://example.test/api/event", ChatProtocol.eventUri(" https://example.test/api/// ").toString());
        for (String bad : List.of("file:///etc/passwd", "ftp://example.test", "not a URL", "http://x?query",
                "http://x/#fragment", "http://user:pass@x", "/relative")) {
            try {
                ChatProtocol.chatUri(bad);
                throw new AssertionError("Accepted bad chat URL: " + bad);
            } catch (IllegalArgumentException expected) {
                // Expected.
            }
            try {
                ChatProtocol.cuesUri(bad);
                throw new AssertionError("Accepted bad cues URL: " + bad);
            } catch (IllegalArgumentException expected) {
                // Expected.
            }
            try {
                ChatProtocol.eventUri(bad);
                throw new AssertionError("Accepted bad event URL: " + bad);
            } catch (IllegalArgumentException expected) {
                // Expected.
            }
        }
    }

    private static void history() {
        JinxHistory store = new JinxHistory(3);
        equal(List.of(), store.snapshot());
        store.append(null);
        store.append("   ");
        equal(0, store.size());
        store.append("first reply");
        store.append("second\nline");
        store.append("third 😀");
        equal(List.of("first reply", "second\nline", "third 😀"), store.snapshot());
        long revBefore = store.revision();
        store.append("fourth");
        check(store.revision() > revBefore, "Revision did not advance");
        equal(List.of("second\nline", "third 😀", "fourth"), store.snapshot());
        store.clear();
        equal(0, store.size());
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

    private static void event() throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        AtomicReference<String> response = new AtomicReference<>("{\"announce\":\"Quest complete, Alex!\"}");
        AtomicReference<JsonObject> received = new AtomicReference<>();
        AtomicReference<String> method = new AtomicReference<>();
        AtomicReference<String> contentType = new AtomicReference<>();
        server.createContext("/event", exchange -> {
            method.set(exchange.getRequestMethod());
            contentType.set(exchange.getRequestHeaders().getFirst("Content-Type"));
            received.set(JsonParser.parseString(new String(exchange.getRequestBody().readAllBytes(),
                    StandardCharsets.UTF_8)).getAsJsonObject());
            String body = response.get();
            try {
                if (body.equals("DELAY")) {
                    Thread.sleep(500);
                    body = "{\"announce\":\"too late\"}";
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
        ChatProtocol.QuestCompletedRequest questRequest =
                ChatProtocol.QuestCompletedRequest.questCompleted("Farming Time", "Alex");
        try (JinxHttpClient client = new JinxHttpClient(1000, 150)) {
            equal(java.util.Optional.of("Quest complete, Alex!"),
                    client.questCompleted(base, questRequest).get(3, TimeUnit.SECONDS));
            equal("POST", method.get());
            equal("application/json; charset=utf-8", contentType.get());
            JsonObject body = received.get();
            equal(3, body.size());
            equal("quest_completed", body.get("type").getAsString());
            equal("Farming Time", body.get("quest").getAsString());
            equal("Alex", body.get("player").getAsString());

            // No announce string (or a blank one) is a successful, silent no-op.
            for (String silent : List.of("{}", "{\"extra\":1}", "{\"announce\":\"\"}", "{\"announce\":\"  \"}")) {
                response.set(silent);
                equal(java.util.Optional.empty(), client.questCompleted(base, questRequest).get(3, TimeUnit.SECONDS));
            }
            for (String invalid : List.of("ERROR", "not json", "[]", "{\"announce\":7}", "{\"announce\":null}",
                    "{\"announce\":\"a\",\"announce\":\"b\"}", "{\"announce\":\"ok\"} garbage",
                    "{\"announce\":\"" + "a".repeat(65_536) + "\"}")) {
                response.set(invalid);
                fails(client.questCompleted(base, questRequest));
            }
            response.set("DELAY");
            CompletableFuture<java.util.Optional<String>> pending = client.questCompleted(base, questRequest);
            check(!pending.isDone(), "Event POST ran synchronously");
            fails(pending);
            fails(client.questCompleted("file:///invalid", questRequest));
        } finally {
            server.stop(0);
        }
    }

    private static void cues() throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        AtomicReference<String> response = new AtomicReference<>("{\"cues\":[]}");
        AtomicReference<String> method = new AtomicReference<>();
        AtomicReference<String> accept = new AtomicReference<>();
        server.createContext("/cues", exchange -> {
            method.set(exchange.getRequestMethod());
            accept.set(exchange.getRequestHeaders().getFirst("Accept"));
            String body = response.get();
            try {
                if (body.equals("DELAY")) {
                    Thread.sleep(500);
                    body = "{\"cues\":[]}";
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
            equal(List.of(), client.cues(base).get(3, TimeUnit.SECONDS));
            equal("GET", method.get());
            equal("application/json", accept.get());

            response.set("""
                    {
                      "extra": 1,
                      "cues": [
                        {"kind": "chat", "text": "[Jinx] Creeper nearby!", "subtitle": null, "sound": null},
                        {"kind": "title", "text": "Nightfall", "subtitle": "Find shelter"},
                        {"kind": "title", "text": "Dawn", "subtitle": null},
                        {"kind": "sound", "sound": "minecraft:entity.experience_orb.pickup"},
                        {"kind": "unknown", "text": "ignored"},
                        {"kind": "chat", "text": ""}
                      ]
                    }
                    """);
            equal(List.of(
                    new ChatProtocol.Cue.Chat("[Jinx] Creeper nearby!"),
                    new ChatProtocol.Cue.Title("Nightfall", "Find shelter"),
                    new ChatProtocol.Cue.Title("Dawn", null),
                    new ChatProtocol.Cue.Sound("minecraft:entity.experience_orb.pickup")),
                    client.cues(base).get(3, TimeUnit.SECONDS));

            for (String invalid : List.of("ERROR", "not json", "{}", "[]", "{\"cues\":null}",
                    "{\"cues\":\"bad\"}", "{cues:[]}", "{\"cues\":[],\"cues\":[]}",
                    "{\"cues\":[123]}", "{\"cues\":[]} trailing",
                    "{\"cues\":[{\"kind\":\"chat\",\"text\":\"" + "a".repeat(65_536) + "\"}]}")) {
                response.set(invalid);
                fails(client.cues(base));
            }

            response.set("DELAY");
            CompletableFuture<List<ChatProtocol.Cue>> pending = client.cues(base);
            check(!pending.isDone(), "Cue GET ran synchronously");
            fails(pending);
            fails(client.cues("file:///invalid"));
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
            fails(client.cues("http://127.0.0.1:" + port));
            fails(client.questCompleted("http://127.0.0.1:" + port,
                    ChatProtocol.QuestCompletedRequest.questCompleted("Farming Time", "Alex")));
        } finally {
            client.close();
        }
        fails(client.chat("http://127.0.0.1:" + port, REQUEST));
        fails(client.cues("http://127.0.0.1:" + port));
        fails(client.questCompleted("http://127.0.0.1:" + port,
                ChatProtocol.QuestCompletedRequest.questCompleted("Farming Time", "Alex")));
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

    private static void bytecodeIsolation() throws Exception {
        List<String> serverSafeClasses = List.of(
                "dev/jinxtalk/ChatProtocol.class",
                "dev/jinxtalk/ChatProtocol$Request.class",
                "dev/jinxtalk/ChatProtocol$Cue.class",
                "dev/jinxtalk/ChatProtocol$Cue$Chat.class",
                "dev/jinxtalk/ChatProtocol$Cue$Title.class",
                "dev/jinxtalk/ChatProtocol$Cue$Sound.class",
                "dev/jinxtalk/ChatProtocol$QuestCompletedRequest.class",
                "dev/jinxtalk/JinxConfig.class",
                "dev/jinxtalk/JinxHistory.class",
                "dev/jinxtalk/JinxHttpClient.class",
                "dev/jinxtalk/JinxTalk.class",
                "dev/jinxtalk/QuestCompletionHandler.class",
                "dev/jinxtalk/ftbquests/FtbQuestsIntegration.class");
        List<String> forbidden = List.of(
                "net/minecraft/client",
                "com/mojang/blaze3d",
                "org/lwjgl",
                "net/neoforged/neoforge/client",
                "dev/jinxtalk/client");
        ClassLoader loader = ChatCoreTest.class.getClassLoader();
        for (String resource : serverSafeClasses) {
            try (var stream = loader.getResourceAsStream(resource)) {
                check(stream != null, "Missing class resource " + resource);
                List<String> pool = utf8ConstantPool(stream.readAllBytes());
                for (String entry : pool) {
                    for (String bad : forbidden) {
                        check(!entry.contains(bad), "Dedicated-server leak in " + resource + ": " + entry);
                    }
                }
            }
        }
        try (var stream = loader.getResourceAsStream("dev/jinxtalk/client/JinxClient.class")) {
            check(stream != null, "Missing JinxClient.class");
            List<String> clientPool = utf8ConstantPool(stream.readAllBytes());
            check(clientPool.contains("CLIENT"), "Missing Dist.CLIENT annotation on JinxClient");
            check(clientPool.contains("Jinx Talk"), "Missing Jinx Talk key category");
            check(clientPool.contains("key.jinxtalk.open_chat"), "Missing key translation key");
        }
    }

    private static List<String> utf8ConstantPool(byte[] classBytes) {
        var buf = java.nio.ByteBuffer.wrap(classBytes);
        equal(0xCAFEBABE, buf.getInt());
        buf.getShort(); // minor
        buf.getShort(); // major
        int count = Short.toUnsignedInt(buf.getShort());
        var strings = new java.util.ArrayList<String>();
        for (int i = 1; i < count; i++) {
            int tag = Byte.toUnsignedInt(buf.get());
            switch (tag) {
                case 1 -> {
                    byte[] raw = new byte[Short.toUnsignedInt(buf.getShort())];
                    buf.get(raw);
                    strings.add(new String(raw, StandardCharsets.UTF_8));
                }
                case 7, 8, 16, 19, 20 -> buf.position(buf.position() + 2);
                case 15 -> buf.position(buf.position() + 3);
                case 3, 4, 9, 10, 11, 12, 17, 18 -> buf.position(buf.position() + 4);
                case 5, 6 -> {
                    buf.position(buf.position() + 8);
                    i++;
                }
                default -> throw new AssertionError("Unknown constant pool tag " + tag);
            }
        }
        return strings;
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

package httpurax.jinxtalk;

import com.google.gson.Gson;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.google.gson.JsonSyntaxException;
import net.minecraft.network.chat.ChatFormatting;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Shared HTTP event transport for jinx-talk.
 *
 * <p>Both the chat path and the FTB Quests quest-completion path POST JSON to
 * {@code <base>/event} on a daemon executor pool, so the game server thread is
 * never blocked and a dead or slow service can never affect gameplay. Every
 * failure (bad URL, DNS, connect/read timeout, non-2xx status, malformed JSON)
 * is caught and logged; nothing is ever propagated back to the calling thread.
 *
 * <p>HTTP contract:
 * <ul>
 *   <li>Request: {@code POST <base>/event} with {@code Content-Type: application/json}</li>
 *   <li>Chat body: {@code {"type":"chat_message","player":"<name>","message":"<text>"}</li>
 *   <li>Quest body: {@code {"type":"quest_completed","quest":"<title or id>","player":"<name>"}</li>
 *   <li>Response: if the JSON body contains an {@code "announce"} string, the
 *       naming player is shown that text in gold chat and hears
 *       {@code minecraft:entity.player.levelup}</li>
 * </ul>
 */
public final class HttpService {
    private static final Logger LOGGER = LogManager.getLogger();
    private static final Gson GSON = new Gson();
    private static final ExecutorService EXECUTOR = Executors.newCachedThreadPool(runnable -> {
        Thread thread = new Thread(runnable, "jinxtalk-http");
        thread.setDaemon(true);
        return thread;
    });

    private HttpService() {
    }

    public static String chatMessageJson(String player, String message) {
        JsonObject object = new JsonObject();
        object.addProperty("type", "chat_message");
        object.addProperty("player", player);
        object.addProperty("message", message);
        return GSON.toJson(object);
    }

    public static String questCompletedJson(String quest, String player) {
        JsonObject object = new JsonObject();
        object.addProperty("type", "quest_completed");
        object.addProperty("quest", quest);
        object.addProperty("player", player);
        return GSON.toJson(object);
    }

    /**
     * POST {@code jsonBody} to {@code <base>/event} asynchronously. If the
     * response is a JSON object with an {@code "announce"} string, deliver it
     * to {@code player} as a gold chat line plus the level-up sound.
     */
    public static void postEvent(String baseUrl, String jsonBody, ServerPlayer player, int timeoutSeconds) {
        String normalized = (baseUrl == null || baseUrl.isBlank()) ? Config.DEFAULT_BASE_URL : baseUrl.trim();
        while (normalized.endsWith("/")) {
            normalized = normalized.substring(0, normalized.length() - 1);
        }
        String url = normalized + "/event";
        int timeout = timeoutSeconds > 0 ? timeoutSeconds : Config.DEFAULT_TIMEOUT_SECONDS;

        EXECUTOR.submit(() -> {
            try {
                HttpClient client = HttpClient.newBuilder()
                        .connectTimeout(Duration.ofSeconds(timeout))
                        .build();
                HttpRequest request = HttpRequest.newBuilder()
                        .uri(URI.create(url))
                        .timeout(Duration.ofSeconds(timeout))
                        .header("Content-Type", "application/json")
                        .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                        .build();
                HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                if (response.statusCode() >= 200 && response.statusCode() < 300) {
                    handleResponse(player, response.body());
                } else {
                    LOGGER.warn("Jinx Talk: event service at {} returned HTTP {} (ignored)", url, response.statusCode());
                }
            } catch (Exception e) {
                if (e instanceof InterruptedException) {
                    Thread.currentThread().interrupt();
                }
                LOGGER.warn("Jinx Talk: event service at {} is unreachable or failed - continuing without it: {}",
                        url, e.getMessage());
            }
        });
    }

    private static void handleResponse(ServerPlayer player, String body) {
        String announce;
        try {
            JsonObject root = JsonParser.parseString(body).getAsJsonObject();
            JsonElement element = root.get("announce");
            if (element == null || !element.isJsonPrimitive() || !element.getAsJsonPrimitive().isString()) {
                return;
            }
            announce = element.getAsString();
        } catch (JsonSyntaxException | IllegalStateException | IllegalArgumentException e) {
            LOGGER.debug("Jinx Talk: malformed JSON response from event service (ignored)", e);
            return;
        }
        if (announce == null || announce.isBlank()) {
            return;
        }
        announce(player, announce);
    }

    /**
     * Deliver an announce response to the naming player: a gold chat line with
     * the announce text followed by minecraft:entity.player.levelup.
     */
    private static void announce(ServerPlayer player, String text) {
        try {
            player.sendSystemMessage(Component.literal(text).withStyle(ChatFormatting.GOLD));
            player.playNotifySound(SoundSource.PLAYER, SoundEvents.PLAYER_LEVELUP, 1.0F, 1.0F);
        } catch (Exception e) {
            LOGGER.warn("Jinx Talk: failed to deliver announce to {}", player.getName().getString(), e);
        }
    }
}

package httpurax.jinxtalk;

import net.neoforged.fml.ModContainer;
import net.neoforged.fml.config.ModConfig;
import net.neoforged.neoforge.common.ModConfigSpec;
import net.neoforged.neoforge.common.ModConfigSpec.Builder;

/**
 * Mod configuration for jinx-talk, stored in {@code config/jinxtalk.toml}.
 * All values are read lazily so editing the config file while the game is
 * running takes effect without a restart.
 */
public final class Config {
    public static final String DEFAULT_BASE_URL = "http://127.0.0.1:8712";
    public static final int DEFAULT_TIMEOUT_SECONDS = 5;
    public static final boolean DEFAULT_ENABLED = true;
    public static final String CONFIG_FILE = "jinxtalk.toml";

    private static ModConfigSpec spec;

    private static final java.util.function.Supplier<String> baseUrl;
    private static final java.util.function.Supplier<Integer> timeoutSeconds;
    private static final java.util.function.Supplier<Boolean> enabled;

    static {
        Builder builder = new Builder();
        var baseUrlValue = builder.define("general.baseUrl", DEFAULT_BASE_URL);
        var timeoutValue = builder.define("general.timeoutSeconds", DEFAULT_TIMEOUT_SECONDS);
        var enabledValue = builder.define("general.enabled", DEFAULT_ENABLED);
        spec = builder.build();
        baseUrl = baseUrlValue::get;
        timeoutSeconds = timeoutValue::get;
        enabled = enabledValue::get;
    }

    private Config() {
    }

    /**
     * Register this mod's config with the given mod container, creating
     * {@code config/jinxtalk.toml} on first run if needed.
     */
    public static void register(ModContainer container) {
        container.registerConfig(ModConfig.Type.COMMON, spec, CONFIG_FILE);
    }

    public static String getBaseUrl() {
        return baseUrl.get();
    }

    public static int getTimeoutSeconds() {
        return timeoutSeconds.get();
    }

    public static boolean isEnabled() {
        return enabled.get();
    }
}

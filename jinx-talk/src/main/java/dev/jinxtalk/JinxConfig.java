package dev.jinxtalk;

import net.neoforged.neoforge.common.ModConfigSpec;

public final class JinxConfig {
    public static final ModConfigSpec SPEC;
    public static final ModConfigSpec.BooleanValue ENABLED;
    public static final ModConfigSpec.ConfigValue<String> SERVICE_BASE_URL;

    static {
        ModConfigSpec.Builder builder = new ModConfigSpec.Builder();
        ENABLED = builder.comment("Enable Jinx Talk chat prefixes (!jinx, !ai, !j), background /cues polling,",
                        "and FTB Quests quest-completion forwarding when FTB Quests is installed.",
                        "Disabled leaves public chat unchanged and suppresses cue polling and quest forwarding.")
                .define("enabled", true);
        SERVICE_BASE_URL = builder.comment("Base URL for the Jinx service.",
                        "An optional path is supported; /chat, /cues and /event are appended. Only use a trusted service.")
                .define("serviceBaseUrl", "http://127.0.0.1:8712", value -> {
                    if (!(value instanceof String text)) {
                        return false;
                    }
                    try {
                        ChatProtocol.chatUri(text);
                        return true;
                    } catch (IllegalArgumentException exception) {
                        return false;
                    }
                });
        SPEC = builder.build();
    }

    private JinxConfig() {}
}

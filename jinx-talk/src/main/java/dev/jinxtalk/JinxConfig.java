package dev.jinxtalk;

import net.neoforged.neoforge.common.ModConfigSpec;

final class JinxConfig {
    static final ModConfigSpec SPEC;
    static final ModConfigSpec.BooleanValue ENABLED;
    static final ModConfigSpec.ConfigValue<String> SERVICE_BASE_URL;

    static {
        ModConfigSpec.Builder builder = new ModConfigSpec.Builder();
        ENABLED = builder.comment("Enable private !jinx, !ai and !j chat. Disabled leaves public chat unchanged.")
                .define("enabled", true);
        SERVICE_BASE_URL = builder.comment("Base URL for the Jinx service on the machine running the server.",
                        "An optional path is supported; /chat is appended. Only use a trusted service.")
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

package dev.jinxtalk.client;

import dev.jinxtalk.ChatProtocol;
import dev.jinxtalk.JinxHistory;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.EditBox;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.util.FormattedCharSequence;
import net.minecraft.util.Mth;
import org.lwjgl.glfw.GLFW;

public final class JinxChatScreen extends Screen {
    private static final int PADDING = 8;
    private static final int INPUT_HEIGHT = 18;
    private static final int SEND_WIDTH = 44;
    private static final int LINE_HEIGHT = 11;
    private static final int REPLY_GAP = 4;

    private final JinxClient client;
    private EditBox input;
    private int panelLeft;
    private int panelTop;
    private int panelWidth;
    private int panelHeight;
    private int historyLeft;
    private int historyTop;
    private int historyRight;
    private int historyBottom;

    private List<FormattedCharSequence> cachedLines = List.of();
    private List<Integer> lineOffsets = List.of();
    private int totalContentHeight;
    private long renderedRevision = -1L;
    private int renderedWrapWidth = -1;
    private double scrollOffset;
    private boolean stickToBottom = true;

    public JinxChatScreen(JinxClient client) {
        super(Component.literal("Jinx Talk"));
        this.client = client;
    }

    @Override
    protected void init() {
        String draft = this.input != null ? this.input.getValue() : "";
        panelWidth = Math.min(360, Math.max(220, this.width - 32));
        panelHeight = Math.min(210, Math.max(136, this.height - 32));
        panelLeft = (this.width - panelWidth) / 2;
        panelTop = (this.height - panelHeight) / 2;

        historyLeft = panelLeft + PADDING;
        historyTop = panelTop + 22;
        historyRight = panelLeft + panelWidth - PADDING;
        historyBottom = panelTop + panelHeight - PADDING - INPUT_HEIGHT - 6;

        int inputY = panelTop + panelHeight - PADDING - INPUT_HEIGHT;
        int inputWidth = panelWidth - (PADDING * 2) - SEND_WIDTH - 4;

        this.input = new EditBox(this.font, historyLeft, inputY, inputWidth, INPUT_HEIGHT,
                Component.literal("Message"));
        this.input.setMaxLength(512);
        this.input.setHint(Component.literal("Ask Jinx anything...").withStyle(s -> s.withColor(0x7D8590)));
        this.input.setValue(draft);
        this.addRenderableWidget(this.input);

        Button sendButton = Button.builder(Component.literal("Send"), button -> submitMessage())
                .bounds(historyLeft + inputWidth + 4, inputY, SEND_WIDTH, INPUT_HEIGHT)
                .build();
        this.addRenderableWidget(sendButton);
        this.setInitialFocus(this.input);

        renderedRevision = -1L;
        rebuildLinesIfNeeded();
    }

    @Override
    public void resize(Minecraft minecraft, int width, int height) {
        String draft = this.input != null ? this.input.getValue() : "";
        super.resize(minecraft, width, height);
        if (this.input != null) {
            this.input.setValue(draft);
        }
    }

    @Override
    public void renderBackground(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        graphics.fill(0, 0, this.width, this.height, 0x66000000);
        // Panel card and border
        graphics.fill(panelLeft, panelTop, panelLeft + panelWidth, panelTop + panelHeight, 0xEE161B22);
        graphics.renderOutline(panelLeft, panelTop, panelWidth, panelHeight, 0xFF30363D);
        // Inset history viewport
        graphics.fill(historyLeft, historyTop, historyRight, historyBottom, 0xFF0D1117);
        graphics.renderOutline(historyLeft, historyTop, historyRight - historyLeft,
                historyBottom - historyTop, 0xFF21262D);
    }

    @Override
    public void render(GuiGraphics graphics, int mouseX, int mouseY, float partialTick) {
        rebuildLinesIfNeeded();
        super.render(graphics, mouseX, mouseY, partialTick);

        graphics.drawString(this.font, this.title, panelLeft + PADDING, panelTop + 8, 0xFFE6EDF3, false);

        String status;
        int statusColor;
        if (client.isThinking()) {
            status = ChatProtocol.PREFIX + "thinking...";
            statusColor = 0xFF58A6FF;
        } else if (client.lastChatFailed()) {
            status = "offline - start jinx_link.py";
            statusColor = 0xFFF85149;
        } else {
            status = "Enter to send";
            statusColor = 0xFF8B949E;
        }
        int statusX = historyRight - this.font.width(status);
        graphics.drawString(this.font, status, statusX, panelTop + 8, statusColor, false);

        renderHistory(graphics);
    }

    private void renderHistory(GuiGraphics graphics) {
        int viewportHeight = historyBottom - historyTop - 8;
        if (cachedLines.isEmpty()) {
            graphics.drawString(this.font, "No Jinx replies yet this session.",
                    historyLeft + 6, historyTop + 8, 0xFF8B949E, false);
            return;
        }

        graphics.enableScissor(historyLeft + 1, historyTop + 1, historyRight - 1, historyBottom - 1);
        int baseY = historyTop + 4 - (int) Math.round(scrollOffset);
        for (int i = 0; i < cachedLines.size(); i++) {
            int y = baseY + lineOffsets.get(i);
            if (y + LINE_HEIGHT >= historyTop && y <= historyBottom) {
                graphics.drawString(this.font, cachedLines.get(i), historyLeft + 6, y, 0xFFE6EDF3, false);
            }
        }
        graphics.disableScissor();

        int maxScroll = maxScroll();
        if (maxScroll > 0) {
            int trackTop = historyTop + 2;
            int trackBottom = historyBottom - 2;
            int trackHeight = Math.max(1, trackBottom - trackTop);
            int thumbHeight = Math.max(14, (int) ((double) viewportHeight / totalContentHeight * trackHeight));
            int thumbRange = Math.max(1, trackHeight - thumbHeight);
            int thumbTop = trackTop + (int) Math.round((scrollOffset / maxScroll) * thumbRange);
            graphics.fill(historyRight - 5, trackTop, historyRight - 2, trackBottom, 0x5521262D);
            graphics.fill(historyRight - 5, thumbTop, historyRight - 2, thumbTop + thumbHeight, 0xAA8B949E);
        }
    }

    private void rebuildLinesIfNeeded() {
        long revision = JinxHistory.SESSION.revision();
        int wrapWidth = Math.max(60, (historyRight - historyLeft) - 14);
        if (revision == renderedRevision && wrapWidth == renderedWrapWidth) {
            return;
        }
        renderedRevision = revision;
        renderedWrapWidth = wrapWidth;

        List<String> replies = JinxHistory.SESSION.snapshot();
        List<FormattedCharSequence> lines = new ArrayList<>();
        List<Integer> offsets = new ArrayList<>();
        int y = 0;

        for (int r = 0; r < replies.size(); r++) {
            String[] paragraphs = replies.get(r).split("\\R", -1);
            for (int p = 0; p < paragraphs.length; p++) {
                MutableComponent lineComponent = p == 0
                        ? Component.literal(ChatProtocol.PREFIX).withStyle(s -> s.withColor(0xDF70DF))
                                .append(Component.literal(paragraphs[p]).withStyle(s -> s.withColor(0xE6EDF3)))
                        : Component.literal(paragraphs[p]).withStyle(s -> s.withColor(0xE6EDF3));
                List<FormattedCharSequence> wrapped = this.font.split(lineComponent, wrapWidth);
                if (wrapped.isEmpty()) {
                    lines.add(FormattedCharSequence.EMPTY);
                    offsets.add(y);
                    y += LINE_HEIGHT;
                } else {
                    for (FormattedCharSequence segment : wrapped) {
                        lines.add(segment);
                        offsets.add(y);
                        y += LINE_HEIGHT;
                    }
                }
            }
            if (r + 1 < replies.size()) {
                y += REPLY_GAP;
            }
        }

        cachedLines = lines;
        lineOffsets = offsets;
        totalContentHeight = y;
        if (stickToBottom) {
            scrollOffset = maxScroll();
        } else {
            scrollOffset = Mth.clamp(scrollOffset, 0.0, maxScroll());
        }
    }

    private int maxScroll() {
        int viewportHeight = Math.max(0, (historyBottom - historyTop) - 8);
        return Math.max(0, totalContentHeight - viewportHeight);
    }

    private void scrollBy(double deltaPixels) {
        int max = maxScroll();
        scrollOffset = Mth.clamp(scrollOffset + deltaPixels, 0.0, max);
        stickToBottom = max == 0 || scrollOffset >= max - 2.0;
    }

    private void submitMessage() {
        if (this.input == null) {
            return;
        }
        String text = this.input.getValue();
        if (text.isBlank()) {
            return;
        }
        this.input.setValue("");
        this.stickToBottom = true;
        this.scrollOffset = maxScroll();
        client.submitChat(text);
        this.setFocused(this.input);
    }

    @Override
    public boolean keyPressed(int keyCode, int scanCode, int modifiers) {
        if (keyCode == GLFW.GLFW_KEY_ENTER || keyCode == GLFW.GLFW_KEY_KP_ENTER) {
            submitMessage();
            return true;
        }
        int pageStep = Math.max(LINE_HEIGHT, (historyBottom - historyTop) - LINE_HEIGHT);
        if (keyCode == GLFW.GLFW_KEY_PAGE_UP) {
            scrollBy(-pageStep);
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_PAGE_DOWN) {
            scrollBy(pageStep);
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_UP) {
            scrollBy(-LINE_HEIGHT * 2.0);
            return true;
        }
        if (keyCode == GLFW.GLFW_KEY_DOWN) {
            scrollBy(LINE_HEIGHT * 2.0);
            return true;
        }
        return super.keyPressed(keyCode, scanCode, modifiers);
    }

    @Override
    public boolean mouseScrolled(double mouseX, double mouseY, double scrollX, double scrollY) {
        if (scrollY != 0.0) {
            scrollBy(-scrollY * (LINE_HEIGHT * 2.0));
            return true;
        }
        return super.mouseScrolled(mouseX, mouseY, scrollX, scrollY);
    }

    @Override
    public boolean mouseDragged(double mouseX, double mouseY, int button, double dragX, double dragY) {
        int max = maxScroll();
        if (button == 0 && max > 0 && mouseX >= historyRight - 8 && mouseX <= historyRight
                && mouseY >= historyTop && mouseY <= historyBottom) {
            int trackHeight = Math.max(1, (historyBottom - historyTop) - 4);
            double ratio = Mth.clamp((mouseY - (historyTop + 2)) / trackHeight, 0.0, 1.0);
            scrollOffset = ratio * max;
            stickToBottom = scrollOffset >= max - 2.0;
            return true;
        }
        return super.mouseDragged(mouseX, mouseY, button, dragX, dragY);
    }

    @Override
    public boolean isPauseScreen() {
        return false;
    }
}

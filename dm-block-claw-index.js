/**
 * dm-block-claw — WhatsApp DM Outbound Blocker
 *
 * This plugin hooks into the message_sending pipeline and cancels
 * ALL outbound WhatsApp messages to DMs (private chats).
 *
 * Groups (@g.us) and newsletters (@newsletter) pass through unaffected.
 *
 * WHY THIS EXISTS:
 * OpenClaw's Codex runtime auto-replies to every WhatsApp DM.
 * The silentReply config does NOT work with Codex runtime.
 * This plugin intercepts at the dispatch level BEFORE sendMessageWhatsApp,
 * making it deterministic (no LLM involved, no chance of failure).
 *
 * FAIL MODE: If this plugin fails to load, OpenClaw fails-open
 * (messages WILL be sent). Always verify plugin is loaded after restart
 * with: openclaw plugins list | grep dm-block
 */

export default {
  id: "dm-block",
  name: "WhatsApp DM Blocker",
  description: "Blocks all outbound WhatsApp DM messages. Groups pass through.",

  register(api) {
    let blockedCount = 0;

    api.on("message_sending", (event, ctx) => {
      // Only intercept WhatsApp channel
      if (ctx.channelId !== "whatsapp") return;

      const to = event.to || "";

      // ALLOW: Group messages (@g.us) — never block these
      if (to.endsWith("@g.us")) return;

      // ALLOW: Newsletter messages (@newsletter)
      if (to.endsWith("@newsletter")) return;

      // BLOCK: Everything else (DMs to @s.whatsapp.net or any other JID)
      blockedCount++;
      api.logger.info(
        `[dm-block] #${blockedCount} Cancelled DM outbound to ${to.substring(0, 6)}...`
      );

      return { cancel: true };
    });

    api.logger.info("[dm-block] Plugin loaded — all WhatsApp DM outbound will be blocked");
  }
};

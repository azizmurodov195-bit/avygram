import os, re

# 1. AvygramHomeHelper.java - refreshGhostBtn qo'shish va tag qo'yish
p_home = "TMessagesProj/src/main/java/org/telegram/ui/AvygramHomeHelper.java"
with open(p_home, "r", encoding="utf-8") as f:
    s = f.read()
if "avy_ghost_tag" not in s:
    s = s.replace(
        "ghostBtn.setVisibility(isTopGhostVisible(context) ? View.VISIBLE : View.GONE);",
        "ghostBtn.setTag(\"avy_ghost_btn\"); // avy_ghost_tag\n        ghostBtn.setVisibility(isTopGhostVisible(context) ? View.VISIBLE : View.GONE);"
    )
    refresh_fn = """
    public static void refreshGhostBtn(View root) {
        if (root == null) return;
        View btn = root.findViewWithTag("avy_ghost_btn");
        if (btn != null) {
            Context ctx = root.getContext();
            boolean vis = isTopGhostVisible(ctx);
            btn.setVisibility(vis ? View.VISIBLE : View.GONE);
            boolean gOn = isGhostMode(ctx);
            if (btn.getBackground() instanceof GradientDrawable) {
                GradientDrawable gBg = (GradientDrawable) btn.getBackground();
                gBg.setColor(gOn ? 0x556366F1 : 0xFF0F172A);
                gBg.setStroke(2, gOn ? 0xFF38BDF8 : 0x446366F1);
            }
            btn.setAlpha(gOn ? 1.0f : 0.55f);
        }
    }
"""
    idx = s.rfind("}")
    s = s[:idx] + refresh_fn + "\n}\n"
    with open(p_home, "w", encoding="utf-8") as f:
        f.write(s)

# 2. DialogsActivity.java - hide_tabs va onResume darhol yangilash
p_dlg = "TMessagesProj/src/main/java/org/telegram/ui/DialogsActivity.java"
with open(p_dlg, "r", encoding="utf-8") as f:
    s = f.read()
s = s.replace(
    "canShowFilterTabsView = true;",
    "canShowFilterTabsView = !AvygramSettingsActivity.getPref(\"hide_tabs\", false);"
)
if "refreshGhostBtn(fragmentView)" not in s:
    s = s.replace(
        "super.onResume();",
        "super.onResume();\n        AvygramHomeHelper.refreshGhostBtn(fragmentView);\n        if (filterTabsView != null) { boolean ht = AvygramSettingsActivity.getPref(\"hide_tabs\", false); canShowFilterTabsView = !ht; filterTabsView.setVisibility(ht ? View.GONE : View.VISIBLE); updateFilterTabsVisibility(false); }"
    )
with open(p_dlg, "w", encoding="utf-8") as f:
    f.write(s)

# 3. LocaleController.java - Sekundlarni ko'rsatish (show_seconds)
p_loc = "TMessagesProj/src/main/java/org/telegram/messenger/LocaleController.java"
with open(p_loc, "r", encoding="utf-8") as f:
    s = f.read()
old_fmt = 'is24HourFormat ? getStringInternal("formatterDay24H", R.string.formatterDay24H) : getStringInternal("formatterDay12H", R.string.formatterDay12H), is24HourFormat ? "HH:mm" : "h:mm a"'
new_fmt = '(org.telegram.ui.AvygramSettingsActivity.getPref("show_seconds", false) ? (is24HourFormat ? "HH:mm:ss" : "h:mm:ss a") : (is24HourFormat ? getStringInternal("formatterDay24H", R.string.formatterDay24H) : getStringInternal("formatterDay12H", R.string.formatterDay12H))), is24HourFormat ? "HH:mm" : "h:mm a"'
if old_fmt in s:
    s = s.replace(old_fmt, new_fmt)
with open(p_loc, "w", encoding="utf-8") as f:
    f.write(s)

# 4. AvygramSettingsActivity.java - show_seconds bosilganda formatterDay ni qayta yuklash
p_set = "TMessagesProj/src/main/java/org/telegram/ui/AvygramSettingsActivity.java"
with open(p_set, "r", encoding="utf-8") as f:
    s = f.read()
if "recreateFormatters" not in s:
    s = s.replace(
        'if ("hide_stories".equals(rKey) || "hide_tabs".equals(rKey)) {',
        'if ("show_seconds".equals(rKey)) { org.telegram.messenger.LocaleController.getInstance().recreateFormatters(); }\n                if ("hide_stories".equals(rKey) || "hide_tabs".equals(rKey)) {'
    )
with open(p_set, "w", encoding="utf-8") as f:
    f.write(s)

# 5. ChatActivityEnterView.java - Stiker, GIF va Ovoz tasdiqlash dialoglari
p_ent = "TMessagesProj/src/main/java/org/telegram/ui/Components/ChatActivityEnterView.java"
with open(p_ent, "r", encoding="utf-8") as f:
    s = f.read()
old_confirm = """    protected boolean showConfirmAlert(Runnable onConfirmed) {
        return false;
    }"""
new_confirm = """    protected boolean showConfirmAlert(Runnable onConfirmed) {
        if (org.telegram.ui.AvygramSettingsActivity.getPref("confirm_sticker", false) || org.telegram.ui.AvygramSettingsActivity.getPref("confirm_gif", false)) {
            if (parentActivity != null && onConfirmed != null) {
                new android.app.AlertDialog.Builder(parentActivity)
                    .setTitle("Avygram Tasdiqlash")
                    .setMessage("Ushbu media (stiker / GIF) yuborilsinmi?")
                    .setPositiveButton("Yuborish", (d, w) -> onConfirmed.run())
                    .setNegativeButton("Bekor qilish", null)
                    .show();
                return true;
            }
        }
        return false;
    }"""
if old_confirm in s:
    s = s.replace(old_confirm, new_confirm)

s = s.replace(
    "MediaController.getInstance().stopRecording(isInScheduleMode() ? 3 : 1, true, 0, voiceOnce);",
    """if (org.telegram.ui.AvygramSettingsActivity.getPref("confirm_voice", false) && parentActivity != null) {
                                    final boolean vOnce = voiceOnce;
                                    final int sMode = isInScheduleMode() ? 3 : 1;
                                    new android.app.AlertDialog.Builder(parentActivity)
                                        .setTitle("Ovozli xabar")
                                        .setMessage("Ovozli xabar yuborilsinmi?")
                                        .setPositiveButton("Yuborish", (d, w) -> MediaController.getInstance().stopRecording(sMode, true, 0, vOnce))
                                        .setNegativeButton("O'chirish", (d, w) -> MediaController.getInstance().stopRecording(0, false, 0, vOnce))
                                        .show();
                                } else {
                                    MediaController.getInstance().stopRecording(isInScheduleMode() ? 3 : 1, true, 0, voiceOnce);
                                }"""
)
with open(p_ent, "w", encoding="utf-8") as f:
    f.write(s)

# 6. MediaController.java - Real-Time DSP Ovoz o'zgartirgich (PCM Buffer Pitch/Robot/Echo)
p_med = "TMessagesProj/src/main/java/org/telegram/messenger/MediaController.java"
with open(p_med, "r", encoding="utf-8") as f:
    s = f.read()
target_read = "int len = audioRecorder.read(buffer, buffer.capacity());"
dsp_code = """int len = audioRecorder.read(buffer, buffer.capacity());
                if (len > 2) {
                    float pitch = org.telegram.ui.AvygramSettingsActivity.getVoicePitchMultiplier();
                    String eff = org.telegram.ui.AvygramSettingsActivity.getVoiceEffectName("voice_msg_effect");
                    if (pitch != 1.0f || !"O'chiq".equals(eff)) {
                        int nSamples = len / 2;
                        short[] src = new short[nSamples];
                        for (int k = 0; k < nSamples; k++) src[k] = buffer.getShort(k * 2);
                        for (int k = 0; k < nSamples; k++) {
                            int idx = (int) (k * pitch);
                            if (idx >= nSamples) idx = idx % nSamples;
                            int val = src[idx];
                            if ("Robot".equals(eff) || "O'zga sayyoralik".equals(eff) || "Modulyatsiya".equals(eff)) {
                                val = (int) (val * Math.sin(k * 0.35));
                            } else if ("Aks-sado (70%)".equals(eff) || "G'or".equals(eff)) {
                                int echoIdx = Math.max(0, k - 400);
                                val = (int) (val * 0.75 + src[echoIdx] * 0.45);
                            } else if ("Xirillash".equals(eff) || "Shovqin (70%)".equals(eff)) {
                                val = (val / 1200) * 1200;
                            }
                            if (val > 32767) val = 32767;
                            if (val < -32768) val = -32768;
                            buffer.putShort(k * 2, (short) val);
                        }
                        buffer.position(0);
                    }
                }"""
if target_read in s and "getVoicePitchMultiplier" not in s:
    s = s.replace(target_read, dsp_code, 1)
with open(p_med, "w", encoding="utf-8") as f:
    f.write(s)

print("ALL_PATCHES_OK")

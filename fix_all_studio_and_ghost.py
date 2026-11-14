import re

# 1. AvygramGhostHelper.java - AvygramSettingsActivity bilan 100% sinxron qilish
with open("TMessagesProj/src/main/java/org/telegram/ui/AvygramGhostHelper.java", "w", encoding="utf-8") as f:
    f.write('''package org.telegram.ui;

import android.content.Context;
import android.widget.Toast;

public class AvygramGhostHelper {
    public static boolean isGhostMode() {
        return AvygramSettingsActivity.getPref("ghost_read", false) || AvygramSettingsActivity.getPref("ghost_mode", false);
    }

    public static void toggleGhostMode(Context context) {
        boolean next = !isGhostMode();
        AvygramSettingsActivity.setPref("ghost_read", next);
        AvygramSettingsActivity.setPref("ghost_mode", next);
        AvygramSettingsActivity.setPref("story_stealth", next);
        if (context != null) {
            Toast.makeText(context, next
                    ? "👻 Sharpa rejimi YOQILDI (O'qilganlik va typing yashirildi)"
                    : "👁️ Sharpa rejimi O'CHIRILDI", Toast.LENGTH_SHORT).show();
        }
    }
}
''')

# 2. AvygramStudioSettingsActivity.java - Dizaynini AvygramSettingsActivity bilan 100% bir xil qilish
with open("TMessagesProj/src/main/java/org/telegram/ui/AvygramStudioSettingsActivity.java", "w", encoding="utf-8") as f:
    f.write('''package org.telegram.ui;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Typeface;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.text.InputType;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.SeekBar;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.ApplicationLoader;
import org.telegram.messenger.NotificationCenter;
import org.telegram.messenger.R;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.AlertDialog;
import org.telegram.ui.ActionBar.BaseFragment;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;

public class AvygramStudioSettingsActivity extends BaseFragment {
    private static final int REQ_PICK_WALLPAPER = 4931;
    private static final String PREF = "avygram_studio_prefs";

    public static boolean isEnabled(String key, boolean def) {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx == null) return def;
        return ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE).getBoolean(key, def);
    }

    public static void setEnabled(String key, boolean val) {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx != null) ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE).edit().putBoolean(key, val).apply();
    }

    public static String getStringPref(String key, String def) {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx == null) return def;
        return ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE).getString(key, def);
    }

    public static void setStringPref(String key, String val) {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx != null) ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE).edit().putString(key, val).apply();
    }

    public static int getDimPercent() {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx == null) return 45;
        return ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE).getInt("bg_dim_percent", 45);
    }

    public static File getWallpaperFile() {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx == null) return null;
        return new File(ctx.getFilesDir(), "avygram_chatlist_bg.jpg");
    }

    public static boolean hasWallpaper() {
        File f = getWallpaperFile();
        return f != null && f.exists();
    }

    public static void applyChatListWallpaper(View containerView, View listView) {
        if (containerView == null) return;
        File f = getWallpaperFile();
        if (f != null && f.exists()) {
            try {
                Bitmap raw = BitmapFactory.decodeFile(f.getAbsolutePath());
                if (raw != null) {
                    Bitmap mutable = raw.copy(Bitmap.Config.ARGB_8888, true);
                    Canvas c = new Canvas(mutable);
                    int alpha = (int) (255 * (getDimPercent() / 100f));
                    Paint p = new Paint();
                    p.setColor(Color.argb(Math.min(230, Math.max(0, alpha)), 6, 9, 19));
                    c.drawRect(0, 0, mutable.getWidth(), mutable.getHeight(), p);
                    containerView.setBackground(new BitmapDrawable(containerView.getResources(), mutable));
                    if (listView != null) listView.setBackgroundColor(Color.TRANSPARENT);
                    return;
                }
            } catch (Throwable ignored) {}
        }
        containerView.setBackgroundColor(0xFF060913);
    }

    @Override
    public View createView(Context context) {
        actionBar.setBackgroundColor(0xFF060913);
        actionBar.setTitleColor(Color.WHITE);
        actionBar.setItemsColor(Color.WHITE, false);
        actionBar.setBackButtonImage(R.drawable.ic_ab_back);
        actionBar.setTitle("Avygram Studio Sozlamalari");
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override
            public void onItemClick(int id) {
                if (id == -1) finishFragment();
            }
        });

        ScrollView scroll = new ScrollView(context);
        scroll.setBackgroundColor(0xFF060913);
        LinearLayout root = new LinearLayout(context);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(28));
        scroll.addView(root, new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        // 1. Chatlar ro'yxati orqa foni (AvygramSettingsActivity bilan bir xil dizaynda)
        LinearLayout bgCard = createCard(context, "Chatlar ro'yxati orqa foni");
        final TextView bgStatus = addActionRow(context, bgCard, "Orqa fon rasmini tanlash",
                "Galereyadan rasm tanlab chatlar ro'yxati foniga qo'yish.",
                hasWallpaper() ? "O'rnatilgan" : "Tanlash", v -> {
                    try {
                        Intent intent = new Intent(Intent.ACTION_PICK);
                        intent.setType("image/*");
                        startActivityForResult(intent, REQ_PICK_WALLPAPER);
                    } catch (Exception e) {
                        Toast.makeText(context, "Galereyani ochib bo'lmadi", Toast.LENGTH_SHORT).show();
                    }
                });

        final TextView dimVal = new TextView(context);
        dimVal.setText(getDimPercent() + "%");
        dimVal.setTextColor(0xFF38BDF8);
        dimVal.setTextSize(13.5f);
        dimVal.setTypeface(Typeface.DEFAULT_BOLD);

        LinearLayout dimRow = new LinearLayout(context);
        dimRow.setOrientation(LinearLayout.HORIZONTAL);
        dimRow.setGravity(Gravity.CENTER_VERTICAL);
        dimRow.setPadding(0, AndroidUtilities.dp(8), 0, AndroidUtilities.dp(4));
        LinearLayout dimCol = new LinearLayout(context);
        dimCol.setOrientation(LinearLayout.VERTICAL);
        TextView d1 = new TextView(context);
        d1.setText("Fon qoraytirish darajasi");
        d1.setTextColor(Color.WHITE);
        d1.setTextSize(15);
        d1.setTypeface(Typeface.DEFAULT_BOLD);
        dimCol.addView(d1);
        TextView d2 = new TextView(context);
        d2.setText("Matnlar tiniq ko'rinishi uchun fonni qoraytirish.");
        d2.setTextColor(0xFF94A3B8);
        d2.setTextSize(12);
        dimCol.addView(d2);
        dimRow.addView(dimCol, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        dimRow.addView(dimVal);
        bgCard.addView(dimRow);

        SeekBar sb = new SeekBar(context);
        sb.setMax(85);
        sb.setProgress(getDimPercent());
        sb.setPadding(0, AndroidUtilities.dp(4), 0, AndroidUtilities.dp(8));
        sb.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                dimVal.setText(progress + "%");
                if (fromUser && ApplicationLoader.applicationContext != null) {
                    ApplicationLoader.applicationContext.getSharedPreferences(PREF, Context.MODE_PRIVATE)
                            .edit().putInt("bg_dim_percent", progress).apply();
                }
            }
            @Override public void onStartTrackingTouch(SeekBar seekBar) {}
            @Override public void onStopTrackingTouch(SeekBar seekBar) {
                NotificationCenter.getInstance(currentAccount).postNotificationName(NotificationCenter.dialogFiltersUpdated);
            }
        });
        bgCard.addView(sb);

        addActionRow(context, bgCard, "Orqa fonni asl holatga qaytarish",
                "Tanlangan fon rasmini o'chirib standart fonga qaytish.",
                "Tozalash", v -> {
                    File f = getWallpaperFile();
                    if (f != null && f.exists()) f.delete();
                    bgStatus.setText("Tanlash");
                    NotificationCenter.getInstance(currentAccount).postNotificationName(NotificationCenter.dialogFiltersUpdated);
                    Toast.makeText(context, "Asl fon tiklandi", Toast.LENGTH_SHORT).show();
                });
        addCard(root, bgCard);

        // 2. Xavfsizlik va Qulaylik (Switchlar)
        LinearLayout secCard = createCard(context, "Maxfiylik va Oldindan ko'rish");
        addSwitchRow(context, secCard, "Chatlarni PIN-kod bilan qulflash",
                "Chatga kirishdan oldin 4 xonali PIN-kod so'raydi.", "pin_lock_enabled", false, on -> {
                    if (on && getStringPref("studio_pin_code", "").isEmpty()) {
                        promptSetPin(context, null);
                    }
                });
        String curPin = getStringPref("studio_pin_code", "");
        final TextView pinBadge = addActionRow(context, secCard, "4 xonali PIN-kodni sozlash",
                "Qulflangan chatlarni ochish uchun maxfiy raqam.",
                curPin.isEmpty() ? "O'rnatilmagan" : "O'rnatilgan", null);
        ((View) pinBadge.getParent()).setOnClickListener(v -> promptSetPin(context, pinBadge));

        addSwitchRow(context, secCard, "Oldindan ko'rish (Peek Mode)",
                "Chatlar ro'yxatida chatni bosib turganda kirmasdan xabarlarni o'qish.", "peek_mode_enabled", true, null);
        addCard(root, secCard);

        // 3. Avtomatik javob va Arxiv
        LinearLayout autoCard = createCard(context, "Avtomatik javob va Arxiv");
        addSwitchRow(context, autoCard, "Avtomatik javob (Auto-Reply)",
                "Band bo'lganingizda shaxsiy xabar yozganlarga avtomatik javob yuborish.", "auto_reply_enabled", false, null);
        addActionRow(context, autoCard, "Avtomatik javob matni",
                getStringPref("auto_reply_text", "Assalomu alaykum! Hozir bandman, tez orada javob beraman."),
                "Tahrirlash", v -> promptAutoReplyText(context));
        addActionRow(context, autoCard, "Anti-Delete Arxiv (Vault)",
                "O'chirilgan xabar va medialarni ko'rish va qidirish.",
                "Ochish", v -> AvygramVaultHelper.showVaultDialog(context));
        addCard(root, autoCard);

        fragmentView = scroll;
        return fragmentView;
    }

    @Override
    public void onActivityResultFragment(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQ_PICK_WALLPAPER && resultCode == Activity.RESULT_OK && data != null && data.getData() != null) {
            Uri uri = data.getData();
            try (InputStream is = getParentActivity().getContentResolver().openInputStream(uri)) {
                Bitmap bmp = BitmapFactory.decodeStream(is);
                if (bmp != null) {
                    int maxW = 1080;
                    if (bmp.getWidth() > maxW) {
                        int newH = (int) (bmp.getHeight() * (maxW / (float) bmp.getWidth()));
                        bmp = Bitmap.createScaledBitmap(bmp, maxW, newH, true);
                    }
                    File out = getWallpaperFile();
                    try (FileOutputStream fos = new FileOutputStream(out)) {
                        bmp.compress(Bitmap.CompressFormat.JPEG, 88, fos);
                    }
                    NotificationCenter.getInstance(currentAccount).postNotificationName(NotificationCenter.dialogFiltersUpdated);
                    Toast.makeText(getParentActivity(), "Chatlar ro'yxati foni o'rnatildi!", Toast.LENGTH_SHORT).show();
                }
            } catch (Exception e) {
                Toast.makeText(getParentActivity(), "Rasmni saqlashda xato: " + e.getMessage(), Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void promptSetPin(Context ctx, TextView badge) {
        EditText et = new EditText(ctx);
        et.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_VARIATION_PASSWORD);
        et.setHint("Masalan: 1234");
        new AlertDialog.Builder(ctx)
                .setTitle("4 xonali PIN-kod")
                .setView(et)
                .setPositiveButton("Saqlash", (d, w) -> {
                    String p = et.getText().toString().trim();
                    if (p.length() >= 4) {
                        setStringPref("studio_pin_code", p);
                        setEnabled("pin_lock_enabled", true);
                        if (badge != null) badge.setText("O'rnatilgan");
                        Toast.makeText(ctx, "PIN-kod saqlandi!", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(ctx, "Kamida 4 ta raqam kiriting", Toast.LENGTH_SHORT).show();
                    }
                })
                .setNegativeButton("Bekor qilish", null)
                .show();
    }

    private void promptAutoReplyText(Context ctx) {
        EditText et = new EditText(ctx);
        et.setText(getStringPref("auto_reply_text", "Assalomu alaykum! Hozir bandman, tez orada javob beraman."));
        new AlertDialog.Builder(ctx)
                .setTitle("Avtomatik javob matni")
                .setView(et)
                .setPositiveButton("Saqlash", (d, w) -> {
                    String t = et.getText().toString().trim();
                    if (!t.isEmpty()) {
                        setStringPref("auto_reply_text", t);
                        Toast.makeText(ctx, "Javob matni saqlandi!", Toast.LENGTH_SHORT).show();
                    }
                })
                .setNegativeButton("Bekor qilish", null)
                .show();
    }

    private LinearLayout createCard(Context ctx, String title) {
        LinearLayout card = new LinearLayout(ctx);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(8));
        GradientDrawable cardBg = new GradientDrawable();
        cardBg.setColor(0xFF0D1426);
        cardBg.setCornerRadius(AndroidUtilities.dp(18));
        cardBg.setStroke(2, 0x336366F1);
        card.setBackground(cardBg);

        TextView header = new TextView(ctx);
        header.setText(title);
        header.setTextColor(0xFF60A5FA);
        header.setTextSize(14);
        header.setTypeface(Typeface.DEFAULT_BOLD);
        header.setPadding(0, 0, 0, AndroidUtilities.dp(10));
        card.addView(header);
        return card;
    }

    private void addCard(LinearLayout parent, LinearLayout card) {
        LinearLayout.LayoutParams clp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        clp.bottomMargin = AndroidUtilities.dp(12);
        parent.addView(card, clp);
    }

    private TextView addActionRow(Context ctx, LinearLayout card, String title, String sub, String rightText, View.OnClickListener listener) {
        LinearLayout row = new LinearLayout(ctx);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(0, AndroidUtilities.dp(8), 0, AndroidUtilities.dp(8));

        LinearLayout col = new LinearLayout(ctx);
        col.setOrientation(LinearLayout.VERTICAL);
        TextView t1 = new TextView(ctx);
        t1.setText(title);
        t1.setTextColor(Color.WHITE);
        t1.setTextSize(15);
        t1.setTypeface(Typeface.DEFAULT_BOLD);
        col.addView(t1);

        TextView t2 = new TextView(ctx);
        t2.setText(sub);
        t2.setTextColor(0xFF94A3B8);
        t2.setTextSize(12);
        col.addView(t2);
        row.addView(col, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        TextView valTv = new TextView(ctx);
        valTv.setText(rightText);
        valTv.setTextColor(0xFF38BDF8);
        valTv.setTextSize(13.5f);
        valTv.setTypeface(Typeface.DEFAULT_BOLD);
        row.addView(valTv);

        if (listener != null) row.setOnClickListener(listener);
        card.addView(row);
        return valTv;
    }

    private interface OnToggle { void onChanged(boolean val); }

    private void addSwitchRow(Context ctx, LinearLayout card, String title, String sub, String key, boolean def, OnToggle cb) {
        LinearLayout row = new LinearLayout(ctx);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(0, AndroidUtilities.dp(8), 0, AndroidUtilities.dp(8));

        LinearLayout col = new LinearLayout(ctx);
        col.setOrientation(LinearLayout.VERTICAL);
        TextView t1 = new TextView(ctx);
        t1.setText(title);
        t1.setTextColor(Color.WHITE);
        t1.setTextSize(15);
        t1.setTypeface(Typeface.DEFAULT_BOLD);
        col.addView(t1);

        TextView t2 = new TextView(ctx);
        t2.setText(sub);
        t2.setTextColor(0xFF94A3B8);
        t2.setTextSize(12);
        col.addView(t2);
        row.addView(col, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        final Switch sw = new Switch(ctx);
        sw.setChecked(isEnabled(key, def));
        sw.setOnCheckedChangeListener((b, isChecked) -> {
            setEnabled(key, isChecked);
            if (cb != null) cb.onChanged(isChecked);
        });
        row.addView(sw);
        row.setOnClickListener(v -> sw.setChecked(!sw.isChecked()));
        card.addView(row);
    }
}
''')

# 3. ProfileActivity.java - Avygram Studio Sozlamalari menyu qatorini 100% ko'rinadigan qilish
p_prof = "TMessagesProj/src/main/java/org/telegram/ui/ProfileActivity.java"
with open(p_prof, "r", encoding="utf-8") as f:
    sp = f.read()

# getItemViewType da ham TextCell qilib belgilash
target_vt = "position == avygramSettingsRow ||"
if "avygramStudioRow" not in sp:
    sp = sp.replace("private int avygramSettingsRow;", "private int avygramSettingsRow;\n    private int avygramStudioRow;", 1)
    sp = sp.replace(
        "} else if (avygramSettingsRow > 0 && position == avygramSettingsRow) {\n                presentFragment(new AvygramSettingsActivity());",
        "} else if (avygramSettingsRow > 0 && position == avygramSettingsRow) {\n                presentFragment(new AvygramSettingsActivity());\n            } else if (avygramStudioRow > 0 && position == avygramStudioRow) {\n                presentFragment(new AvygramStudioSettingsActivity());",
        1
    )
    sp = sp.replace("avygramSettingsRow = -1;", "avygramSettingsRow = -1;\n        avygramStudioRow = -1;", 1)
    sp = sp.replace("avygramSettingsRow = rowCount++;", "avygramSettingsRow = rowCount++;\n                avygramStudioRow = rowCount++;", 1)
    sp = sp.replace(
        '''                    } else if (avygramSettingsRow > 0 && position == avygramSettingsRow) {
                        textCell.setTextAndIcon("⚡ Avygram Sozlamalari", R.drawable.msg_settings, true);''',
        '''                    } else if (avygramSettingsRow > 0 && position == avygramSettingsRow) {
                        textCell.setTextAndIcon("⚡ Avygram Sozlamalari", R.drawable.msg_settings, true);
                    } else if (avygramStudioRow > 0 && position == avygramStudioRow) {
                        textCell.setTextAndIcon("🎨 Avygram Studio Sozlamalari", R.drawable.msg_theme, true);''',
        1
    )

sp = sp.replace("position == avygramSettingsRow ||", "position == avygramSettingsRow || position == avygramStudioRow ||")
with open(p_prof, "w", encoding="utf-8") as f:
    f.write(sp)

# 4. DialogsActivity.java - Chatlar ro'yxati orqa foni, Peek Mode va PIN-kod qulfi
p_dlg = "TMessagesProj/src/main/java/org/telegram/ui/DialogsActivity.java"
with open(p_dlg, "r", encoding="utf-8") as f:
    sd = f.read()

# Orqa fon rasmini viewPage va fragmentView ga qo'llash
sd = sd.replace(
    "AvygramStudioSettingsActivity.applyChatListWallpaper(viewPage);",
    "AvygramStudioSettingsActivity.applyChatListWallpaper(viewPage, viewPage.listView);"
)
if "applyChatListWallpaper(viewPage, viewPage.listView);" not in sd:
    sd = sd.replace(
        "            viewPage.listView = new DialogsRecyclerView(context, viewPage);",
        "            viewPage.listView = new DialogsRecyclerView(context, viewPage);\n            AvygramStudioSettingsActivity.applyChatListWallpaper(viewPage, viewPage.listView);",
        1
    )

# Peek Mode: chatni bosib turganda (onItemLongClick) chatga kirmasdan oldindan ko'rish
old_peek = "if (cell.isPointInsideAvatar(x, y)) {"
new_peek = "if (cell.isPointInsideAvatar(x, y) || AvygramStudioSettingsActivity.isEnabled(\"peek_mode_enabled\", true)) {"
if old_peek in sd:
    sd = sd.replace(old_peek, new_peek, 1)

# PIN-kod qulfi: ChatActivity ochilishidan oldin tekshirish
old_open = "ChatActivity chatActivity = new ChatActivity(args);"
new_open = '''if (AvygramStudioSettingsActivity.isEnabled("pin_lock_enabled", false) && !AvygramStudioSettingsActivity.getStringPref("studio_pin_code", "").isEmpty()) {
                android.widget.EditText pinInput = new android.widget.EditText(getParentActivity());
                pinInput.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_VARIATION_PASSWORD);
                pinInput.setHint("4 xonali PIN-kodni kiriting");
                new org.telegram.ui.ActionBar.AlertDialog.Builder(getParentActivity())
                        .setTitle("🔒 Qulflangan chat")
                        .setView(pinInput)
                        .setPositiveButton("Ochish", (d, w) -> {
                            if (AvygramStudioSettingsActivity.getStringPref("studio_pin_code", "").equals(pinInput.getText().toString().trim())) {
                                presentFragment(new ChatActivity(args));
                            } else {
                                android.widget.Toast.makeText(getParentActivity(), "❌ PIN-kod noto'g'ri!", android.widget.Toast.LENGTH_SHORT).show();
                            }
                        })
                        .setNegativeButton("Bekor qilish", null)
                        .show();
                return true;
            }
            ChatActivity chatActivity = new ChatActivity(args);'''
if old_open in sd and "Qulflangan chat" not in sd:
    sd = sd.replace(old_open, new_open, 1)

with open(p_dlg, "w", encoding="utf-8") as f:
    f.write(sd)

# 5. MessagesController.java - Sharpa rejimi (o'qilganlik + typing bloklash) va Auto-Reply
p_mc = "TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java"
with open(p_mc, "r", encoding="utf-8") as f:
    smc = f.read()

# sendTyping ni ham Sharpa rejimida bloklash
if "public void sendTyping(" in smc and "AvygramGhostHelper.isGhostMode()" not in smc.split("public void sendTyping(")[1][:200]:
    smc = smc.replace(
        "public void sendTyping(final long dialog_id, final long threadId, final int action, int classGuid) {",
        "public void sendTyping(final long dialog_id, final long threadId, final int action, int classGuid) {\n        if (org.telegram.ui.AvygramGhostHelper.isGhostMode()) { return; }",
        1
    )

# readHistory RPC so'rovlarini ham bloklash (ko'k galochka ✓✓ hech qachon yonmasligi uchun)
smc = smc.replace(
    "TLRPC.TL_messages_readHistory req = new TLRPC.TL_messages_readHistory();",
    "if (org.telegram.ui.AvygramGhostHelper.isGhostMode()) { return; }\n        TLRPC.TL_messages_readHistory req = new TLRPC.TL_messages_readHistory();"
)
smc = smc.replace(
    "TLRPC.TL_channels_readHistory req = new TLRPC.TL_channels_readHistory();",
    "if (org.telegram.ui.AvygramGhostHelper.isGhostMode()) { return; }\n        TLRPC.TL_channels_readHistory req = new TLRPC.TL_channels_readHistory();"
)

with open(p_mc, "w", encoding="utf-8") as f:
    f.write(smc)

print("ALL_STUDIO_GHOST_PIN_PEEK_FIXED_OK")

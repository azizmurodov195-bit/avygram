# 1. AvygramStudioSettingsActivity.java yaratish
p_act = "TMessagesProj/src/main/java/org/telegram/ui/AvygramStudioSettingsActivity.java"
with open(p_act, "w", encoding="utf-8") as f:
    f.write('''package org.telegram.ui;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
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
import android.widget.FrameLayout;
import android.widget.ImageView;
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

    public static void applyChatListWallpaper(View targetView) {
        if (targetView == null) return;
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
                    targetView.setBackground(new BitmapDrawable(targetView.getResources(), mutable));
                    return;
                }
            } catch (Throwable ignored) {}
        }
        targetView.setBackgroundColor(0xFF060913);
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

        // 1. Chatlar ro'yxati orqa foni bo'limi
        LinearLayout bgCard = makeCard(context);
        bgCard.addView(makeHeader(context, "🖼️ Chatlar ro'yxati orqa foni"));

        TextView pickBtn = makeActionBtn(context, "📁 Galereyadan rasm tanlash", 0xFF2563EB);
        pickBtn.setOnClickListener(v -> {
            try {
                Intent intent = new Intent(Intent.ACTION_PICK);
                intent.setType("image/*");
                startActivityForResult(intent, REQ_PICK_WALLPAPER);
            } catch (Exception e) {
                Toast.makeText(context, "Galereyani ochib bo'lmadi", Toast.LENGTH_SHORT).show();
            }
        });
        bgCard.addView(pickBtn);

        final TextView dimLabel = new TextView(context);
        dimLabel.setText("Qoraytirish darajasi: " + getDimPercent() + "%");
        dimLabel.setTextColor(0xFF94A3B8);
        dimLabel.setTextSize(13);
        dimLabel.setPadding(0, AndroidUtilities.dp(12), 0, AndroidUtilities.dp(4));
        bgCard.addView(dimLabel);

        SeekBar sb = new SeekBar(context);
        sb.setMax(85);
        sb.setProgress(getDimPercent());
        sb.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                dimLabel.setText("Qoraytirish darajasi: " + progress + "%");
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

        TextView resetBtn = makeActionBtn(context, "🗑️ Orqa fon rasmini o'chirish", 0xFF334155);
        LinearLayout.LayoutParams rlp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        rlp.topMargin = AndroidUtilities.dp(10);
        resetBtn.setOnClickListener(v -> {
            File f = getWallpaperFile();
            if (f != null && f.exists()) f.delete();
            NotificationCenter.getInstance(currentAccount).postNotificationName(NotificationCenter.dialogFiltersUpdated);
            Toast.makeText(context, "Chatlar ro'yxati asl foniga qaytdi", Toast.LENGTH_SHORT).show();
        });
        bgCard.addView(resetBtn, rlp);
        addCardToParent(root, bgCard);

        // 2. Xavfsizlik va Qulaylik Switchlari
        LinearLayout featCard = makeCard(context);
        featCard.addView(makeHeader(context, "⚡ Qo'shimcha Studio funksiyalari"));

        addSwitchRow(context, featCard, "🔒 Chatlarni PIN-kod bilan qulflash",
                "Chatga kirishdan oldin 4 xonali maxfiy PIN-kod so'raydi.", "pin_lock_enabled", false, (on) -> {
                    if (on && getStringPref("studio_pin_code", "").isEmpty()) {
                        promptSetPin(context);
                    }
                });

        TextView pinBtn = makeActionBtn(context, "🔑 4 xonali PIN-kodni o'rnatish / o'zgartirish", 0xFF1E293B);
        pinBtn.setOnClickListener(v -> promptSetPin(context));
        featCard.addView(pinBtn);

        addSwitchRow(context, featCard, "👁️ Oldindan ko'rish (Peek Mode)",
                "Chatlar ro'yxatida chatni bosib turganda kirib o'tirmasdan xabarlarni o'qish.", "peek_mode_enabled", true, null);

        addSwitchRow(context, featCard, "🤖 Avtomatik javob (Auto-Reply)",
                "Band bo'lganingizda shaxsiy xabar yozganlarga avtomatik javob yuborish.", "auto_reply_enabled", false, null);

        TextView arBtn = makeActionBtn(context, "✏️ Avtomatik javob matnini tahrirlash", 0xFF1E293B);
        arBtn.setOnClickListener(v -> promptAutoReplyText(context));
        featCard.addView(arBtn);

        addCardToParent(root, featCard);

        // 3. Anti-Delete Arxiv
        LinearLayout vaultCard = makeCard(context);
        vaultCard.addView(makeHeader(context, "🛡️ Anti-Delete Arxiv"));
        TextView vaultBtn = makeActionBtn(context, "📂 O'chirilgan xabar va medialar arxivini ochish", 0xFF0F766E);
        vaultBtn.setOnClickListener(v -> AvygramVaultHelper.showVaultDialog(context));
        vaultCard.addView(vaultBtn);
        addCardToParent(root, vaultCard);

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
                    Toast.makeText(getParentActivity(), "✅ Chatlar ro'yxati foni o'rnatildi!", Toast.LENGTH_SHORT).show();
                }
            } catch (Exception e) {
                Toast.makeText(getParentActivity(), "Rasmni saqlashda xato: " + e.getMessage(), Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void promptSetPin(Context ctx) {
        EditText et = new EditText(ctx);
        et.setInputType(InputType.TYPE_CLASS_NUMBER | InputType.TYPE_NUMBER_VARIATION_PASSWORD);
        et.setHint("Masalan: 1234");
        new AlertDialog.Builder(ctx)
                .setTitle("🔑 4 xonali PIN-kod")
                .setView(et)
                .setPositiveButton("Saqlash", (d, w) -> {
                    String p = et.getText().toString().trim();
                    if (p.length() >= 4) {
                        setStringPref("studio_pin_code", p);
                        setEnabled("pin_lock_enabled", true);
                        Toast.makeText(ctx, "✅ PIN-kod saqlandi!", Toast.LENGTH_SHORT).show();
                    } else {
                        Toast.makeText(ctx, "Kamida 4 ta raqam kiriting", Toast.LENGTH_SHORT).show();
                    }
                })
                .setNegativeButton("Bekor qilish", null)
                .show();
    }

    private void promptAutoReplyText(Context ctx) {
        EditText et = new EditText(ctx);
        et.setText(getStringPref("auto_reply_text", "Assalomu alaykum! Hozir bandman, bo'shashim bilan javob beraman."));
        new AlertDialog.Builder(ctx)
                .setTitle("🤖 Avtomatik javob matni")
                .setView(et)
                .setPositiveButton("Saqlash", (d, w) -> {
                    String t = et.getText().toString().trim();
                    if (!t.isEmpty()) {
                        setStringPref("auto_reply_text", t);
                        Toast.makeText(ctx, "✅ Javob matni saqlandi!", Toast.LENGTH_SHORT).show();
                    }
                })
                .setNegativeButton("Bekor qilish", null)
                .show();
    }

    private LinearLayout makeCard(Context ctx) {
        LinearLayout card = new LinearLayout(ctx);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(12));
        GradientDrawable bg = new GradientDrawable();
        bg.setColor(0xFF0D1426);
        bg.setCornerRadius(AndroidUtilities.dp(18));
        bg.setStroke(2, 0x336366F1);
        card.setBackground(bg);
        return card;
    }

    private void addCardToParent(LinearLayout parent, LinearLayout card) {
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        lp.bottomMargin = AndroidUtilities.dp(12);
        parent.addView(card, lp);
    }

    private TextView makeHeader(Context ctx, String text) {
        TextView h = new TextView(ctx);
        h.setText(text);
        h.setTextColor(0xFF60A5FA);
        h.setTextSize(14);
        h.setTypeface(Typeface.DEFAULT_BOLD);
        h.setPadding(0, 0, 0, AndroidUtilities.dp(10));
        return h;
    }

    private TextView makeActionBtn(Context ctx, String text, int color) {
        TextView btn = new TextView(ctx);
        btn.setText(text);
        btn.setTextColor(Color.WHITE);
        btn.setTextSize(13.5f);
        btn.setTypeface(Typeface.DEFAULT_BOLD);
        btn.setGravity(Gravity.CENTER);
        btn.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(12), AndroidUtilities.dp(10));
        GradientDrawable gd = new GradientDrawable();
        gd.setColor(color);
        gd.setCornerRadius(AndroidUtilities.dp(12));
        btn.setBackground(gd);
        return btn;
    }

    private interface OnToggle { void onChanged(boolean val); }

    private void addSwitchRow(Context ctx, LinearLayout card, String title, String sub, String key, boolean def, OnToggle cb) {
        LinearLayout row = new LinearLayout(ctx);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(Gravity.CENTER_VERTICAL);
        row.setPadding(0, AndroidUtilities.dp(10), 0, AndroidUtilities.dp(8));

        LinearLayout col = new LinearLayout(ctx);
        col.setOrientation(LinearLayout.VERTICAL);
        TextView t1 = new TextView(ctx);
        t1.setText(title);
        t1.setTextColor(Color.WHITE);
        t1.setTextSize(14.5f);
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

# 2. ProfileActivity.java ga ⚡ Avygram Sozlamalari pastiga 🎨 Avygram Studio Sozlamalari qo'shish
p_prof = "TMessagesProj/src/main/java/org/telegram/ui/ProfileActivity.java"
with open(p_prof, "r", encoding="utf-8") as f:
    sp = f.read()

if "avygramStudioRow" not in sp:
    sp = sp.replace(
        "private int avygramSettingsRow;",
        "private int avygramSettingsRow;\n    private int avygramStudioRow;",
        1
    )
    sp = sp.replace(
        "} else if (avygramSettingsRow > 0 && position == avygramSettingsRow) {\n                presentFragment(new AvygramSettingsActivity());",
        "} else if (avygramSettingsRow > 0 && position == avygramSettingsRow) {\n                presentFragment(new AvygramSettingsActivity());\n            } else if (avygramStudioRow > 0 && position == avygramStudioRow) {\n                presentFragment(new AvygramStudioSettingsActivity());",
        1
    )
    sp = sp.replace(
        "avygramSettingsRow = -1;",
        "avygramSettingsRow = -1;\n        avygramStudioRow = -1;",
        1
    )
    sp = sp.replace(
        "avygramSettingsRow = rowCount++;",
        "avygramSettingsRow = rowCount++;\n                avygramStudioRow = rowCount++;",
        1
    )
    sp = sp.replace(
        '''                    } else if (avygramSettingsRow > 0 && position == avygramSettingsRow) {
                        textCell.setTextAndIcon("⚡ Avygram Sozlamalari", R.drawable.msg_settings, true);''',
        '''                    } else if (avygramSettingsRow > 0 && position == avygramSettingsRow) {
                        textCell.setTextAndIcon("⚡ Avygram Sozlamalari", R.drawable.msg_settings, true);
                    } else if (avygramStudioRow > 0 && position == avygramStudioRow) {
                        textCell.setTextAndIcon("🎨 Avygram Studio Sozlamalari", R.drawable.msg_theme, true);''',
        1
    )
    sp = sp.replace(
        "position == avygramSettingsRow ||",
        "position == avygramSettingsRow || position == avygramStudioRow ||",
        1
    )
    with open(p_prof, "w", encoding="utf-8") as f:
        f.write(sp)

# 3. DialogsActivity.java ga Chatlar ro'yxati orqa fonini qo'llash
p_dlg = "TMessagesProj/src/main/java/org/telegram/ui/DialogsActivity.java"
with open(p_dlg, "r", encoding="utf-8") as f:
    sd = f.read()

target_lv = "            viewPage.listView = new DialogsRecyclerView(context, viewPage);"
rep_lv = "            viewPage.listView = new DialogsRecyclerView(context, viewPage);\n            AvygramStudioSettingsActivity.applyChatListWallpaper(viewPage);"
assert target_lv in sd, "DialogsRecyclerView not found"
if "applyChatListWallpaper" not in sd:
    sd = sd.replace(target_lv, rep_lv, 1)
    with open(p_dlg, "w", encoding="utf-8") as f:
        f.write(sd)

print("STUDIO_SETTINGS_AND_WALLPAPER_READY")

package org.telegram.ui;

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
import java.util.HashSet;
import java.util.Set;

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

        // 1. Chatlar ro'yxati orqa foni
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

        // 2. Oldindan ko'rish va Avtomatik javob
        LinearLayout autoCard = createCard(context, "Avtomatik javob va Qulayliklar");
        addSwitchRow(context, autoCard, "Oldindan ko'rish (Peek Mode)",
                "Chatlar ro'yxatida chatni bosib turganda kirmasdan xabarlarni o'qish.", "peek_mode_enabled", true, null);
        addSwitchRow(context, autoCard, "Avtomatik javob (Auto-Reply)",
                "Band bo'lganingizda shaxsiy xabar yozganlarga avtomatik javob yuborish.", "auto_reply_enabled", false, null);
        addActionRow(context, autoCard, "Avtomatik javob matni",
                getStringPref("auto_reply_text", "Assalomu alaykum! Hozir bandman, bo'shashim bilan javob beraman."),
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
                    Toast.makeText(getParentActivity(), "✅ Chatlar ro'yxati foni o'rnatildi!", Toast.LENGTH_SHORT).show();
                }
            } catch (Exception e) {
                Toast.makeText(getParentActivity(), "Rasmni saqlashda xato: " + e.getMessage(), Toast.LENGTH_SHORT).show();
            }
        }
    }

    private void promptAutoReplyText(Context ctx) {
        EditText et = new EditText(ctx);
        et.setText(getStringPref("auto_reply_text", "Assalomu alaykum! Hozir bandman, bo'shashim bilan javob beraman."));
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

# 1. Chiroyli Aka/Telegram uslubidagi PIN klaviatura oynasi (AvygramPinPadDialog.java)
with open("TMessagesProj/src/main/java/org/telegram/ui/AvygramPinPadDialog.java", "w", encoding="utf-8") as f:
    f.write('''package org.telegram.ui;

import android.app.Dialog;
import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.Window;
import android.view.WindowManager;
import android.widget.GridLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import org.telegram.messenger.AndroidUtilities;

public class AvygramPinPadDialog {
    public interface PinCallback {
        void onPinEntered(String pin, Dialog dialog, TextView subtitleView, Runnable clearDots);
    }

    public static void show(Context context, String title, String subtitle, PinCallback callback) {
        if (context == null) return;
        final Dialog dialog = new Dialog(context, android.R.style.Theme_Black_NoTitleBar_Fullscreen);
        dialog.requestWindowFeature(Window.FEATURE_NO_TITLE);
        if (dialog.getWindow() != null) {
            dialog.getWindow().setLayout(WindowManager.LayoutParams.MATCH_PARENT, WindowManager.LayoutParams.MATCH_PARENT);
            dialog.getWindow().setStatusBarColor(0xFF060913);
            dialog.getWindow().setNavigationBarColor(0xFF060913);
        }

        LinearLayout root = new LinearLayout(context);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER_HORIZONTAL);
        root.setBackgroundColor(0xFF060913);
        root.setPadding(AndroidUtilities.dp(24), AndroidUtilities.dp(48), AndroidUtilities.dp(24), AndroidUtilities.dp(32));

        TextView closeTv = new TextView(context);
        closeTv.setText("✕ Bekor qilish");
        closeTv.setTextColor(0xFF94A3B8);
        closeTv.setTextSize(14);
        closeTv.setGravity(Gravity.END);
        closeTv.setOnClickListener(v -> dialog.dismiss());
        root.addView(closeTv, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        View topSpace = new View(context);
        root.addView(topSpace, new LinearLayout.LayoutParams(1, 0, 0.7f));

        TextView lockIcon = new TextView(context);
        lockIcon.setText("🔐");
        lockIcon.setTextSize(42);
        lockIcon.setGravity(Gravity.CENTER);
        root.addView(lockIcon);

        TextView titleTv = new TextView(context);
        titleTv.setText(title);
        titleTv.setTextColor(Color.WHITE);
        titleTv.setTextSize(21);
        titleTv.setTypeface(Typeface.DEFAULT_BOLD);
        titleTv.setGravity(Gravity.CENTER);
        titleTv.setPadding(0, AndroidUtilities.dp(12), 0, AndroidUtilities.dp(6));
        root.addView(titleTv);

        final TextView subTv = new TextView(context);
        subTv.setText(subtitle);
        subTv.setTextColor(0xFF94A3B8);
        subTv.setTextSize(14);
        subTv.setGravity(Gravity.CENTER);
        subTv.setPadding(0, 0, 0, AndroidUtilities.dp(26));
        root.addView(subTv);

        // 4 ta nuqta indikatori
        LinearLayout dotsRow = new LinearLayout(context);
        dotsRow.setOrientation(LinearLayout.HORIZONTAL);
        dotsRow.setGravity(Gravity.CENTER);
        final View[] dots = new View[4];
        for (int i = 0; i < 4; i++) {
            View dot = new View(context);
            GradientDrawable gd = new GradientDrawable();
            gd.setShape(GradientDrawable.OVAL);
            gd.setColor(0xFF1E293B);
            gd.setStroke(AndroidUtilities.dp(2), 0xFF38BDF8);
            dot.setBackground(gd);
            LinearLayout.LayoutParams dlp = new LinearLayout.LayoutParams(AndroidUtilities.dp(16), AndroidUtilities.dp(16));
            dlp.setMargins(AndroidUtilities.dp(10), 0, AndroidUtilities.dp(10), 0);
            dotsRow.addView(dot, dlp);
            dots[i] = dot;
        }
        root.addView(dotsRow);

        View midSpace = new View(context);
        root.addView(midSpace, new LinearLayout.LayoutParams(1, 0, 0.8f));

        final StringBuilder code = new StringBuilder();
        final Runnable updateDots = () -> {
            for (int i = 0; i < 4; i++) {
                GradientDrawable gd = new GradientDrawable();
                gd.setShape(GradientDrawable.OVAL);
                if (i < code.length()) {
                    gd.setColor(0xFF38BDF8);
                } else {
                    gd.setColor(0xFF1E293B);
                    gd.setStroke(AndroidUtilities.dp(2), 0xFF38BDF8);
                }
                dots[i].setBackground(gd);
            }
        };

        final Runnable clearDots = () -> {
            code.setLength(0);
            updateDots.run();
        };

        GridLayout grid = new GridLayout(context);
        grid.setColumnCount(3);
        grid.setRowCount(4);

        String[] keys = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "", "0", "⌫"};
        for (final String k : keys) {
            TextView btn = new TextView(context);
            GridLayout.LayoutParams glp = new GridLayout.LayoutParams();
            glp.width = AndroidUtilities.dp(76);
            glp.height = AndroidUtilities.dp(76);
            glp.setMargins(AndroidUtilities.dp(10), AndroidUtilities.dp(8), AndroidUtilities.dp(10), AndroidUtilities.dp(8));

            if (k.isEmpty()) {
                btn.setVisibility(View.INVISIBLE);
                grid.addView(btn, glp);
                continue;
            }

            btn.setText(k);
            btn.setTextColor(Color.WHITE);
            btn.setTextSize(k.equals("⌫") ? 22 : 26);
            btn.setTypeface(Typeface.DEFAULT_BOLD);
            btn.setGravity(Gravity.CENTER);

            GradientDrawable circle = new GradientDrawable();
            circle.setShape(GradientDrawable.OVAL);
            circle.setColor(0xFF111827);
            circle.setStroke(2, 0x336366F1);
            btn.setBackground(circle);

            btn.setOnClickListener(v -> {
                if ("⌫".equals(k)) {
                    if (code.length() > 0) {
                        code.deleteCharAt(code.length() - 1);
                        updateDots.run();
                    }
                } else if (code.length() < 4) {
                    code.append(k);
                    updateDots.run();
                    if (code.length() == 4) {
                        String entered = code.toString();
                        callback.onPinEntered(entered, dialog, subTv, clearDots);
                    }
                }
            });
            grid.addView(btn, glp);
        }

        root.addView(grid);
        dialog.setContentView(root);
        dialog.show();
    }
}
''')

# 2. AvygramStudioSettingsActivity.java - Alohida chatlarni qulflash ro'yxati + chiroyli PIN o'rnatish + darhol fon yangilash
with open("TMessagesProj/src/main/java/org/telegram/ui/AvygramStudioSettingsActivity.java", "w", encoding="utf-8") as f:
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
    private static final String KEY_LOCKED_CHATS = "locked_dialog_ids";

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

    public static boolean isDialogLocked(long dialogId) {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx == null) return false;
        String pin = getStringPref("studio_pin_code", "");
        if (pin.isEmpty()) return false;
        Set<String> set = ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE).getStringSet(KEY_LOCKED_CHATS, new HashSet<>());
        return set != null && set.contains(String.valueOf(dialogId));
    }

    public static void toggleDialogLock(Context ctx, long dialogId) {
        if (ctx == null) return;
        SharedPreferences sp = ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE);
        Set<String> oldSet = sp.getStringSet(KEY_LOCKED_CHATS, new HashSet<>());
        Set<String> nextSet = new HashSet<>(oldSet != null ? oldSet : new HashSet<>());
        String idStr = String.valueOf(dialogId);
        if (nextSet.contains(idStr)) {
            nextSet.remove(idStr);
            sp.edit().putStringSet(KEY_LOCKED_CHATS, nextSet).apply();
            Toast.makeText(ctx, "🔓 Chat qulfdan chiqarildi", Toast.LENGTH_SHORT).show();
        } else {
            nextSet.add(idStr);
            sp.edit().putStringSet(KEY_LOCKED_CHATS, nextSet).apply();
            if (getStringPref("studio_pin_code", "").isEmpty()) {
                AvygramPinPadDialog.show(ctx, "Yangi PIN-kod o'rnating", "Qulflangan chatlar uchun 4 xonali raqam kiriting", (pin, dlg, sub, clear) -> {
                    setStringPref("studio_pin_code", pin);
                    dlg.dismiss();
                    Toast.makeText(ctx, "🔒 PIN-kod o'rnatildi va chat qulflandi!", Toast.LENGTH_SHORT).show();
                });
            } else {
                Toast.makeText(ctx, "🔒 Chat PIN-kod bilan qulflandi!", Toast.LENGTH_SHORT).show();
            }
        }
    }

    public static int getLockedCount() {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx == null) return 0;
        Set<String> set = ctx.getSharedPreferences(PREF, Context.MODE_PRIVATE).getStringSet(KEY_LOCKED_CHATS, new HashSet<>());
        return set == null ? 0 : set.size();
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

        // 2. Tanlangan chatlarni PIN-kod bilan qulflash
        LinearLayout secCard = createCard(context, "Tanlangan chatlarni qulflash (PIN)");
        String curPin = getStringPref("studio_pin_code", "");
        final TextView pinBadge = addActionRow(context, secCard, "4 xonali PIN-kodni o'rnatish",
                "Chatlar ro'yxatida chatni bosib turib 🔒 tugmasi orqali alohida chatlarni qulflang.",
                curPin.isEmpty() ? "O'rnatish" : "O'zgartirish", null);
        ((View) pinBadge.getParent()).setOnClickListener(v -> {
            AvygramPinPadDialog.show(context, "4 xonali PIN-kod o'rnating", "Maxfiy chatlarni ochish uchun raqam tanlang", (pin, dlg, sub, clear) -> {
                setStringPref("studio_pin_code", pin);
                pinBadge.setText("O'zgartirish");
                dlg.dismiss();
                Toast.makeText(context, "✅ PIN-kod saqlandi!", Toast.LENGTH_SHORT).show();
            });
        });

        final TextView lockedBadge = addActionRow(context, secCard, "Qulflangan chatlar ro'yxati",
                "Hozirda alohida qulflangan chatlar soni.",
                getLockedCount() + " ta chat", null);
        ((View) lockedBadge.getParent()).setOnClickListener(v -> {
            if (getLockedCount() == 0) {
                Toast.makeText(context, "Chatlar ro'yxatida istalgan chatni bosib turib tepadan 🔒 tugmasini bosing", Toast.LENGTH_LONG).show();
            } else {
                new AlertDialog.Builder(context)
                        .setTitle("Qulflangan chatlar (" + getLockedCount() + " ta)")
                        .setMessage("Barcha tanlangan chatlarni qulfdan chiqarishni xohlaysizmi?")
                        .setPositiveButton("Hammasini ochish", (d, w) -> {
                            context.getSharedPreferences(PREF, Context.MODE_PRIVATE).edit().remove(KEY_LOCKED_CHATS).apply();
                            lockedBadge.setText("0 ta chat");
                            Toast.makeText(context, "Barcha chatlar qulfdan chiqarildi", Toast.LENGTH_SHORT).show();
                        })
                        .setNegativeButton("Bekor qilish", null)
                        .show();
            }
        });

        addSwitchRow(context, secCard, "Oldindan ko'rish (Peek Mode)",
                "Chatlar ro'yxatida chatni bosib turganda kirmasdan xabarlarni o'qish.", "peek_mode_enabled", true, null);
        addCard(root, secCard);

        // 3. Avtomatik javob va Arxiv
        LinearLayout autoCard = createCard(context, "Avtomatik javob va Arxiv");
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
''')

# 3. ProfileActivity.java - Avygram Studio Sozlamalari nomi aniq ko'rinadigan qilish
p_prof = "TMessagesProj/src/main/java/org/telegram/ui/ProfileActivity.java"
with open(p_prof, "r", encoding="utf-8") as f:
    sp = f.read()

target_bind = '''textCell.setTextAndIcon("⚡ Avygram Sozlamalari", R.drawable.msg_settings, true);'''
rep_bind = '''textCell.setTextAndIcon("⚡ Avygram Sozlamalari", R.drawable.msg_settings, true);
                } else if (avygramStudioRow > 0 && position == avygramStudioRow) {
                    textCell.setTextAndIcon("🎨 Avygram Studio Sozlamalari", R.drawable.msg_theme, true);'''
if "🎨 Avygram Studio Sozlamalari" not in sp:
    assert target_bind in sp, "target_bind not found in ProfileActivity"
    sp = sp.replace(target_bind, rep_bind, 1)
    with open(p_prof, "w", encoding="utf-8") as f:
        f.write(sp)

# 4. DialogsActivity.java:
#    a) Har bir alohida tanlangan chat uchun chiroyli AvygramPinPadDialog
#    b) Chatni bosib turganda tepada 🔒 Qulflash / Qulfdan chiqarish tugmasi
#    c) onResume() da orqa fon rasmi darhol yangilanishi
p_dlg = "TMessagesProj/src/main/java/org/telegram/ui/DialogsActivity.java"
with open(p_dlg, "r", encoding="utf-8") as f:
    sd = f.read()

# a) Eski PIN blokini yangi per-chat chiroyli PIN klaviatura bilan almashtirish
old_pin_block_start = 'if (AvygramStudioSettingsActivity.isEnabled("pin_lock_enabled"'
old_pin_block_end = 'ChatActivity chatActivity = new ChatActivity(args);'
if old_pin_block_start in sd and old_pin_block_end in sd:
    i1 = sd.index(old_pin_block_start)
    i2 = sd.index(old_pin_block_end, i1)
    new_pin_block = '''long checkDid = args.getLong("user_id", 0);
            if (checkDid == 0) checkDid = -args.getLong("chat_id", 0);
            if (checkDid == 0) checkDid = -args.getLong("enc_id", 0);
            if (checkDid != 0 && AvygramStudioSettingsActivity.isDialogLocked(checkDid)) {
                final android.os.Bundle finalArgs = new android.os.Bundle(args);
                AvygramPinPadDialog.show(getParentActivity(), "Qulflangan chat", "Kirish uchun 4 xonali PIN-kodni kiriting", (enteredPin, dlg, subTv, clearDots) -> {
                    if (AvygramStudioSettingsActivity.getStringPref("studio_pin_code", "").equals(enteredPin)) {
                        dlg.dismiss();
                        presentFragment(new ChatActivity(finalArgs));
                    } else {
                        subTv.setText("❌ PIN-kod noto'g'ri, qayta urinib ko'ring");
                        subTv.setTextColor(0xFFF87171);
                        clearDots.run();
                    }
                });
                return;
            }
            '''
    sd = sd[:i1] + new_pin_block + sd[i2:]

# b) Chatni bosib turganda tepada chiqadigan panelga 🔒 Qulflash tugmasini qo'shish
target_pin_item = "pinItem = actionMode.addItemWithWidth(pin, R.drawable.msg_pin, dp(54));"
rep_pin_item = '''pinItem = actionMode.addItemWithWidth(pin, R.drawable.msg_pin, dp(54));
            ActionBarMenuItem avyLockItem = actionMode.addItemWithWidth(994, R.drawable.msg_secret, dp(54));
            avyLockItem.setOnClickListener(v -> {
                ArrayList<Long> sel = dialogsAdapter.getSelectedDialogs();
                if (sel != null && !sel.isEmpty()) {
                    for (Long did : sel) {
                        AvygramStudioSettingsActivity.toggleDialogLock(getParentActivity(), did);
                    }
                }
                hideActionMode(false);
            });'''
if target_pin_item in sd and "avyLockItem" not in sd:
    sd = sd.replace(target_pin_item, rep_pin_item, 1)

# c) onResume() ichida orqa fon rasmi darhol yangilanishi (ilovadan chiqib qayta kirish shart emas!)
target_resume = "public void onResume() {"
rep_resume = '''public void onResume() {
        if (viewPages != null) {
            for (ViewPage vp : viewPages) {
                if (vp != null) AvygramStudioSettingsActivity.applyChatListWallpaper(vp, vp.listView);
            }
        }'''
if target_resume in sd and "for (ViewPage vp : viewPages)" not in sd:
    sd = sd.replace(target_resume, rep_resume, 1)

with open(p_dlg, "w", encoding="utf-8") as f:
    f.write(sd)

print("PIN_PAD_PER_CHAT_AND_INSTANT_WALLPAPER_OK")

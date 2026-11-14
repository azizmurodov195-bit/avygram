package org.telegram.ui;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.ApplicationLoader;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;

public class AvygramSettingsActivity extends BaseFragment {

    public static boolean getPref(String key, boolean defVal) {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx == null) return defVal;
        return ctx.getSharedPreferences("avygram_prefs", Context.MODE_PRIVATE).getBoolean(key, defVal);
    }

    public static void setPref(String key, boolean val) {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx != null) {
            ctx.getSharedPreferences("avygram_prefs", Context.MODE_PRIVATE).edit().putBoolean(key, val).apply();
        }
    }

    @Override
    public View createView(Context context) {
        actionBar.setBackgroundColor(0xFF060913);
        actionBar.setTitleColor(Color.WHITE);
        actionBar.setItemsColor(Color.WHITE, false);
        actionBar.setBackButtonImage(org.telegram.messenger.R.drawable.ic_ab_back);
        actionBar.setTitle("Avygram Sozlamalari");
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override
            public void onItemClick(int id) {
                if (id == -1) {
                    finishFragment();
                }
            }
        });

        ScrollView scroll = new ScrollView(context);
        scroll.setBackgroundColor(0xFF060913);

        LinearLayout root = new LinearLayout(context);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(28));
        scroll.addView(root, new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        addSection(context, root, "Hikoya Sozlamalari", new String[][]{
            {"Hikoyalarni yashirin ko'rish", "Yoqilganda, hikoya egalari sizning ko'rganingizni bilmaydi.", "story_stealth", "true"},
            {"Hikoyalarni yashirish", "Suhbatlar ro'yxati tepasidagi hikoyalar panelini yashiradi.", "hide_stories", "false"},
            {"Hikoyalarni yuklab olish", "Hikoya ko'ruvchida istalgan hikoyani galereyaga saqlash.", "story_download", "true"}
        });

        addSection(context, root, "Xabarlar (Anti-Delete / Anti-Edit)", new String[][]{
            {"Tahrirlangan xabarlarni saqlash", "Kimdir tahrirlagan xabarlarning oldingi nusxasini saqlaydi.", "save_edited", "true"},
            {"O'chirilgan xabarlarni saqlash", "Boshqalar o'chirgan xabarlarni chatdan o'chirmay saqlaydi.", "save_deleted", "true"}
        });

        addSection(context, root, "Maxfiylik (Sharpa rejimi)", new String[][]{
            {"Sharpa rejimi", "Online holatingiz, yozayotganingiz va xabar o'qilgani yashiriladi.", "ghost_read", "true"},
            {"Asosiy oynada Sharpa tugmasi", "Sharpa rejimini suhbatlar ro'yxatidan tezda yoqish/o'chirish.", "top_ghost_btn", "true"},
            {"Begonalardan himoya", "Kontaktingizda yo'q odamlarning qo'ng'iroqlarini cheklash.", "block_strangers", "false"}
        });

        addSection(context, root, "Tasdiqlash dialoglari", new String[][]{
            {"Stiker yuborish", "Stiker yuborishdan oldin tasdiqlash oynasini ko'rsatish.", "confirm_sticker", "false"},
            {"Ovoz yuborish", "Ovozli xabar yuborishdan oldin tasdiqlashni so'rash.", "confirm_voice", "false"},
            {"GIF yuborish", "GIF yuborishdan oldin tasdiqlash oynasini ko'rsatish.", "confirm_gif", "false"}
        });

        addSection(context, root, "Ko'rinish va Qulaylik", new String[][]{
            {"Jild tablarini yashirish", "Suhbatlar ro'yxatidagi jild tablari qatorini yashirish.", "hide_tabs", "false"},
            {"Sekundlarni ko'rsatish", "Xabar vaqtlarini 12:01:45 ko'rinishida sekundlar bilan ko'rsatish.", "show_seconds", "false"}
        });


        addVoiceChangerSection(context, root);

        fragmentView = scroll;
        return fragmentView;
    }

    private void addSection(final Context ctx, LinearLayout parent, String title, String[][] rows) {
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

        for (int i = 0; i < rows.length; i++) {
            final String rTitle = rows[i][0];
            final String rSub = rows[i][1];
            final String rKey = rows[i][2];
            final boolean rDef = "true".equals(rows[i][3]);

            LinearLayout row = new LinearLayout(ctx);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(0, AndroidUtilities.dp(8), 0, AndroidUtilities.dp(8));

            LinearLayout col = new LinearLayout(ctx);
            col.setOrientation(LinearLayout.VERTICAL);

            TextView tv1 = new TextView(ctx);
            tv1.setText(rTitle);
            tv1.setTextColor(Color.WHITE);
            tv1.setTextSize(15);
            tv1.setTypeface(Typeface.DEFAULT_BOLD);
            col.addView(tv1);

            TextView tv2 = new TextView(ctx);
            tv2.setText(rSub);
            tv2.setTextColor(0xFF94A3B8);
            tv2.setTextSize(12);
            col.addView(tv2);

            row.addView(col, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

            final Switch sw = new Switch(ctx);
            sw.setChecked(getPref(rKey, rDef));
            sw.setOnCheckedChangeListener((b, isChecked) -> {
                setPref(rKey, isChecked);
                if ("show_seconds".equals(rKey)) { org.telegram.messenger.LocaleController.getInstance().recreateFormatters(); }
                if ("hide_stories".equals(rKey) || "hide_tabs".equals(rKey)) {
                    org.telegram.messenger.NotificationCenter.getInstance(currentAccount).postNotificationName(org.telegram.messenger.NotificationCenter.storiesUpdated);
                    org.telegram.messenger.NotificationCenter.getInstance(currentAccount).postNotificationName(org.telegram.messenger.NotificationCenter.dialogFiltersUpdated);
                }
                if ("ghost_read".equals(rKey) || "story_stealth".equals(rKey)) {
                    setPref("ghost_mode", getPref("ghost_read", true) || getPref("story_stealth", true));
                }
                
            });
            row.addView(sw);

            row.setOnClickListener(v -> sw.setChecked(!sw.isChecked()));
            card.addView(row);
        }

        LinearLayout.LayoutParams clp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        clp.bottomMargin = AndroidUtilities.dp(12);
        parent.addView(card, clp);
    }

    public static String getVoiceEffectName(String key) {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx == null) return "O'chiq";
        return ctx.getSharedPreferences("avygram_prefs", Context.MODE_PRIVATE).getString(key, "O'chiq");
    }

    public static float getVoicePitchMultiplier() {
        String eff = getVoiceEffectName("voice_msg_effect");
        if ("Juda yo'g'on".equals(eff) || "Maxluq".equals(eff) || "Geksaftorid".equals(eff)) return 0.68f;
        if ("Yo'g'on".equals(eff) || "Erkak".equals(eff) || "G'or".equals(eff)) return 0.82f;
        if ("Ingichka".equals(eff) || "Ayol".equals(eff)) return 1.24f;
        if ("Juda ingichka".equals(eff) || "Bola".equals(eff) || "Sichqon".equals(eff) || "Geliy".equals(eff)) return 1.48f;
        if ("Robot".equals(eff) || "O'zga sayyoralik".equals(eff) || "Modulyatsiya".equals(eff)) return 1.12f;
        return 1.0f;
    }

    private void addVoiceChangerSection(final Context ctx, LinearLayout parent) {
        LinearLayout card = new LinearLayout(ctx);
        card.setOrientation(LinearLayout.VERTICAL);
        card.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(10));
        GradientDrawable cardBg = new GradientDrawable();
        cardBg.setColor(0xFF0D1426);
        cardBg.setCornerRadius(AndroidUtilities.dp(18));
        cardBg.setStroke(2, 0x336366F1);
        card.setBackground(cardBg);

        TextView header = new TextView(ctx);
        header.setText("🎙 Ovoz o'zgartirgich (Real DSP)");
        header.setTextColor(0xFF60A5FA);
        header.setTextSize(14);
        header.setTypeface(Typeface.DEFAULT_BOLD);
        header.setPadding(0, 0, 0, AndroidUtilities.dp(10));
        card.addView(header);

        String[][] vRows = {
            {"Ovozli xabarlar", "Ovozli xabarni boshqa ovozda yozish va yuborish", "voice_msg_effect"},
            {"Qo'ng'iroqlar", "Qo'ng'iroq va guruh qo'ng'iroqlarida boshqa ovoz", "voice_call_effect"}
        };

        for (final String[] vr : vRows) {
            LinearLayout row = new LinearLayout(ctx);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(0, AndroidUtilities.dp(8), 0, AndroidUtilities.dp(8));

            LinearLayout col = new LinearLayout(ctx);
            col.setOrientation(LinearLayout.VERTICAL);
            TextView t1 = new TextView(ctx);
            t1.setText(vr[0]);
            t1.setTextColor(Color.WHITE);
            t1.setTextSize(15);
            t1.setTypeface(Typeface.DEFAULT_BOLD);
            col.addView(t1);

            TextView t2 = new TextView(ctx);
            t2.setText(vr[1]);
            t2.setTextColor(0xFF94A3B8);
            t2.setTextSize(12);
            col.addView(t2);
            row.addView(col, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

            final TextView valTv = new TextView(ctx);
            valTv.setText(getVoiceEffectName(vr[2]));
            valTv.setTextColor(0xFF38BDF8);
            valTv.setTextSize(13.5f);
            valTv.setTypeface(Typeface.DEFAULT_BOLD);
            row.addView(valTv);

            row.setOnClickListener(v -> showVoicePickerDialog(ctx, vr[2], valTv));
            card.addView(row);
        }

        LinearLayout.LayoutParams clp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        clp.bottomMargin = AndroidUtilities.dp(12);
        parent.addView(card, clp);
    }

    private void showVoicePickerDialog(final Context ctx, final String prefKey, final TextView badge) {
        final String[] effects = {
            "❌ O'chiq",
            "⏩ Yozish tezligi (Juda yo'g'on)",
            "⏩ Yozish tezligi (Yo'g'on)",
            "⏩ Yozish tezligi (Ingichka)",
            "⏩ Yozish tezligi (Juda ingichka)",
            "🤖 Robot",
            "👽 O'zga sayyoralik",
            "📻 Xirillash",
            "🎛 Modulyatsiya",
            "👶 Bola",
            "🐭 Sichqon",
            "👨 Erkak",
            "👩 Ayol",
            "👹 Maxluq",
            "🔊 Aks-sado (70%)",
            "💥 Shovqin (70%)",
            "🎈 Geliy",
            "🎈 Geksaftorid",
            "🕳 G'or"
        };
        new android.app.AlertDialog.Builder(ctx)
            .setTitle("Ovoz o'zgartirgich")
            .setItems(effects, (d, which) -> {
                String clean = effects[which].substring(effects[which].indexOf(' ') + 1);
                if (clean.contains("(") && clean.startsWith("Yozish")) {
                    clean = clean.substring(clean.indexOf("(") + 1, clean.indexOf(")"));
                }
                if (which == 0) clean = "O'chiq";
                ctx.getSharedPreferences("avygram_prefs", Context.MODE_PRIVATE).edit().putString(prefKey, clean).apply();
                badge.setText(clean);
                
            })
            .show();
    }

}

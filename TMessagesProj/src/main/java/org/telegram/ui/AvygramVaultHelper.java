package org.telegram.ui;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.ApplicationLoader;
import org.telegram.ui.ActionBar.AlertDialog;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class AvygramVaultHelper {
    private static final String PREF_NAME = "avygram_anti_delete_vault";
    private static final String KEY_ITEMS = "deleted_messages_json";

    public static void recordDeletedMessage(String senderName, String text) {
        if (text == null || text.trim().isEmpty()) return;
        try {
            SharedPreferences prefs = ApplicationLoader.applicationContext.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
            JSONArray arr = new JSONArray(prefs.getString(KEY_ITEMS, "[]"));
            JSONObject obj = new JSONObject();
            obj.put("sender", senderName == null || senderName.isEmpty() ? "Foydalanuvchi" : senderName);
            obj.put("text", text.trim());
            obj.put("time", new SimpleDateFormat("dd.MM HH:mm", Locale.getDefault()).format(new Date()));
            JSONArray next = new JSONArray();
            next.put(obj);
            for (int i = 0; i < Math.min(arr.length(), 149); i++) {
                next.put(arr.get(i));
            }
            prefs.edit().putString(KEY_ITEMS, next.toString()).apply();
        } catch (Exception ignored) {}
    }

    public static void showVaultDialog(Context context) {
        SharedPreferences prefs = ApplicationLoader.applicationContext.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
        try {
            final JSONArray arr = new JSONArray(prefs.getString(KEY_ITEMS, "[]"));
            LinearLayout root = new LinearLayout(context);
            root.setOrientation(LinearLayout.VERTICAL);
            root.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(10), AndroidUtilities.dp(16), AndroidUtilities.dp(10));

            EditText searchBox = new EditText(context);
            searchBox.setHint("🔍 Ism yoki xabar matnidan qidirish...");
            searchBox.setHintTextColor(0xFF94A3B8);
            searchBox.setTextColor(Color.WHITE);
            searchBox.setTextSize(14);
            searchBox.setSingleLine(true);
            searchBox.setBackgroundColor(0xFF0F172A);
            searchBox.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(12), AndroidUtilities.dp(10));
            LinearLayout.LayoutParams sblp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            sblp.bottomMargin = AndroidUtilities.dp(10);
            root.addView(searchBox, sblp);

            ScrollView sv = new ScrollView(context);
            final LinearLayout list = new LinearLayout(context);
            list.setOrientation(LinearLayout.VERTICAL);
            sv.addView(list, new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
            root.addView(sv, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, AndroidUtilities.dp(340)));

            Runnable renderList = () -> {
                list.removeAllViews();
                String q = searchBox.getText().toString().trim().toLowerCase();
                int shown = 0;
                for (int i = 0; i < arr.length(); i++) {
                    JSONObject o = arr.optJSONObject(i);
                    if (o == null) continue;
                    String sender = o.optString("sender");
                    String txt = o.optString("text");
                    String time = o.optString("time");
                    if (!q.isEmpty() && !sender.toLowerCase().contains(q) && !txt.toLowerCase().contains(q)) continue;
                    TextView card = new TextView(context);
                    card.setText("👤 " + sender + "  •  " + time + "\n" + txt);
                    card.setTextColor(Color.WHITE);
                    card.setTextSize(13);
                    card.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(12), AndroidUtilities.dp(10));
                    card.setBackgroundColor(0xFF1E293B);
                    LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
                    lp.bottomMargin = AndroidUtilities.dp(8);
                    list.addView(card, lp);
                    shown++;
                }
                if (shown == 0) {
                    TextView empty = new TextView(context);
                    empty.setText(arr.length() == 0
                            ? "Hozircha o'chirilgan xabarlar yo'q.\nSuhbatdosh xabar yoki media o'chirsa, shu yerda saqlanadi."
                            : "Qidiruv bo'yicha hech narsa topilmadi.");
                    empty.setTextColor(0xFF94A3B8);
                    empty.setTextSize(14);
                    list.addView(empty);
                }
            };

            renderList.run();
            searchBox.addTextChangedListener(new TextWatcher() {
                @Override public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
                @Override public void onTextChanged(CharSequence s, int start, int before, int count) { renderList.run(); }
                @Override public void afterTextChanged(Editable s) {}
            });

            new AlertDialog.Builder(context)
                    .setTitle("🛡️ Avygram Anti-Delete Arxiv")
                    .setView(root)
                    .setPositiveButton("Yopish", null)
                    .setNeutralButton("Tozalash", (d, w) -> {
                        prefs.edit().putString(KEY_ITEMS, "[]").apply();
                        Toast.makeText(context, "Arxiv tozalandi", Toast.LENGTH_SHORT).show();
                    })
                    .show();
        } catch (Exception e) {
            Toast.makeText(context, "Arxivni ochishda xatolik", Toast.LENGTH_SHORT).show();
        }
    }
}

# 1. Расширяем AvygramVaultHelper.java (живой поиск + сохранение медиа-удалений)
p_vault = "TMessagesProj/src/main/java/org/telegram/ui/AvygramVaultHelper.java"
with open(p_vault, "w", encoding="utf-8") as f:
    f.write('''package org.telegram.ui;

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
                    card.setText("👤 " + sender + "  •  " + time + "\\n" + txt);
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
                            ? "Hozircha o'chirilgan xabarlar yo'q.\\nSuhbatdosh xabar yoki media o'chirsa, shu yerda saqlanadi."
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
''')

# 2. MessagesController.java - Сохраняем также удалённые медиа (фото/видео/голосовые)
p_mc = "TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java"
with open(p_mc, "r", encoding="utf-8") as f:
    smc = f.read()

old_rec = '''                        if (mo != null && mo.messageText != null && mo.messageText.length() > 0) {
                            org.telegram.ui.AvygramVaultHelper.recordDeletedMessage(senderTitle, mo.messageText.toString());
                        }'''
new_rec = '''                        if (mo != null) {
                            String body = (mo.messageText != null && mo.messageText.length() > 0) ? mo.messageText.toString() : "";
                            if (mo.isVoice()) body = "🎤 [Ovozli xabar o'chirildi] " + body;
                            else if (mo.isVideo() || mo.isRoundVideo()) body = "🎬 [Video xabar o'chirildi] " + body;
                            else if (mo.isPhoto()) body = "🖼️ [Rasm o'chirildi] " + body;
                            else if (mo.isMusic()) body = "🎵 [Musiqa o'chirildi] " + body;
                            if (!body.trim().isEmpty()) {
                                org.telegram.ui.AvygramVaultHelper.recordDeletedMessage(senderTitle, body);
                            }
                        }'''
if old_rec in smc:
    smc = smc.replace(old_rec, new_rec, 1)
    with open(p_mc, "w", encoding="utf-8") as f:
        f.write(smc)

# 3. AvygramReelsActivity.java - Добавляем кнопку 👻 Arvoh (Ghost Mode) в верхний переключатель
p_reels = "TMessagesProj/src/main/java/org/telegram/ui/AvygramReelsActivity.java"
with open(p_reels, "r", encoding="utf-8") as f:
    sr = f.read()

old_sw = '''        modeSwitch.addView(tabAvy);
        modeSwitch.addView(tabInsta);'''
new_sw = '''        final TextView tabGhost = new TextView(context);
        tabGhost.setText(AvygramGhostHelper.isGhostMode() ? "👻 Yoqilgan" : "👻 Arvoh");
        tabGhost.setTextColor(AvygramGhostHelper.isGhostMode() ? 0xFF38BDF8 : 0xFF94A3B8);
        tabGhost.setTextSize(13);
        tabGhost.setTypeface(Typeface.DEFAULT_BOLD);
        tabGhost.setGravity(Gravity.CENTER);
        tabGhost.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(6), AndroidUtilities.dp(14), AndroidUtilities.dp(6));
        tabGhost.setOnClickListener(v -> {
            AvygramGhostHelper.toggleGhostMode(context);
            boolean on = AvygramGhostHelper.isGhostMode();
            tabGhost.setText(on ? "👻 Yoqilgan" : "👻 Arvoh");
            tabGhost.setTextColor(on ? 0xFF38BDF8 : 0xFF94A3B8);
        });

        modeSwitch.addView(tabAvy);
        modeSwitch.addView(tabInsta);
        modeSwitch.addView(tabGhost);'''
assert old_sw in sr, "modeSwitch addView not found"
sr = sr.replace(old_sw, new_sw, 1)
with open(p_reels, "w", encoding="utf-8") as f:
    f.write(sr)

# 4. ChatActivity.java - Добавляем в меню сообщения: 🌐 Tarjima, 🎵 MP3 ajratish, 🎙️ Ovoz o'zgartirish
p_chat = "TMessagesProj/src/main/java/org/telegram/ui/ChatActivity.java"
with open(p_chat, "r", encoding="utf-8") as f:
    sc = f.read()

if "AVY_OPT_TRANSLATE" not in sc:
    sc = sc.replace(
        "private final static int OPTION_COPY = 1;",
        "private final static int OPTION_COPY = 1;\n    private final static int AVY_OPT_TRANSLATE = 991;\n    private final static int AVY_OPT_MP3 = 992;\n    private final static int AVY_OPT_VOICE = 993;",
        1
    )

    menu_hook = '''items.add("🌐 O'zbekchaga tarjima");
                options.add(AVY_OPT_TRANSLATE);
                icons.add(R.drawable.msg_translate);
                if (selectedObject != null && (selectedObject.isVideo() || selectedObject.isRoundVideo())) {
                    items.add("🎵 MP3 (Audio) ajratish");
                    options.add(AVY_OPT_MP3);
                    icons.add(R.drawable.msg_download);
                }
                if (selectedObject != null && (selectedObject.isVoice() || selectedObject.isMusic())) {
                    items.add("🎙️ Ovoz o'zgartirish");
                    options.add(AVY_OPT_VOICE);
                    icons.add(R.drawable.msg_voicechat);
                }
                items.add(LocaleController.getString(R.string.Copy));
                options.add(OPTION_COPY);'''

    target_copy = '''items.add(LocaleController.getString(R.string.Copy));
                options.add(OPTION_COPY);'''
    assert target_copy in sc, "target_copy in ChatActivity not found"
    sc = sc.replace(target_copy, menu_hook, 1)

    case_hook = '''            case AVY_OPT_TRANSLATE: {
                String txt = selectedObject.messageText != null ? selectedObject.messageText.toString() : "";
                AvygramStudioHelper.translateToUzbek(getParentActivity(), txt);
                break;
            }
            case AVY_OPT_MP3: {
                java.io.File vf = FileLoader.getInstance(currentAccount).getPathToMessage(selectedObject.messageOwner);
                AvygramStudioHelper.extractAudioFromVideo(getParentActivity(), vf, currentAccount, true);
                break;
            }
            case AVY_OPT_VOICE: {
                java.io.File af = FileLoader.getInstance(currentAccount).getPathToMessage(selectedObject.messageOwner);
                AvygramVoiceChanger.showVoiceEffectPicker(getParentActivity(), af, dialog_id, currentAccount);
                break;
            }
            case OPTION_RETRY: {'''

    assert "            case OPTION_RETRY: {" in sc, "OPTION_RETRY switch case not found"
    sc = sc.replace("            case OPTION_RETRY: {", case_hook, 1)

    with open(p_chat, "w", encoding="utf-8") as f:
        f.write(sc)

print("FINISH_V112_SUPERAPP_OK")

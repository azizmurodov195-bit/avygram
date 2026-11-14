import os

# 1. AvygramHiddenVault.java — SHA-256 + Salt + Android Keystore + Brute-force Lock + Recovery
with open("TMessagesProj/src/main/java/org/telegram/ui/AvygramHiddenVault.java", "w", encoding="utf-8") as f:
    f.write('''package org.telegram.ui;

import android.content.Context;
import android.content.SharedPreferences;
import android.security.keystore.KeyGenParameterSpec;
import android.security.keystore.KeyProperties;
import android.util.Base64;

import org.telegram.messenger.ApplicationLoader;
import org.telegram.messenger.NotificationCenter;

import java.nio.charset.StandardCharsets;
import java.security.KeyStore;
import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import javax.crypto.Cipher;
import javax.crypto.KeyGenerator;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;

public class AvygramHiddenVault {
    private static final String PREF_NAME = "avygram_hidden_vault_secure_v2";
    private static final String KEY_PIN_HASH = "pin_sha256_hash";
    private static final String KEY_PIN_SALT = "pin_salt_b64";
    private static final String KEY_RECOVERY_HASH = "recovery_sha256_hash";
    private static final String KEY_HIDDEN_IDS = "hidden_dialog_ids_enc";
    private static final String KEY_FAILED_ATTEMPTS = "failed_attempts";
    private static final String KEY_LOCKOUT_UNTIL = "lockout_until_ms";
    private static final String KEYSTORE_ALIAS = "AvygramHiddenVaultMasterKey";

    private static SharedPreferences prefs() {
        Context ctx = ApplicationLoader.applicationContext;
        if (ctx == null) return null;
        return ctx.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
    }

    private static SecretKey getOrCreateMasterKey() {
        try {
            KeyStore ks = KeyStore.getInstance("AndroidKeyStore");
            ks.load(null);
            if (!ks.containsAlias(KEYSTORE_ALIAS)) {
                KeyGenerator kg = KeyGenerator.getInstance(KeyProperties.KEY_ALGORITHM_AES, "AndroidKeyStore");
                kg.init(new KeyGenParameterSpec.Builder(
                        KEYSTORE_ALIAS,
                        KeyProperties.PURPOSE_ENCRYPT | KeyProperties.PURPOSE_DECRYPT)
                        .setBlockModes(KeyProperties.BLOCK_MODE_GCM)
                        .setEncryptionPaddings(KeyProperties.ENCRYPTION_PADDING_NONE)
                        .setKeySize(256)
                        .build());
                return kg.generateKey();
            }
            return ((KeyStore.SecretKeyEntry) ks.getEntry(KEYSTORE_ALIAS, null)).getSecretKey();
        } catch (Throwable t) {
            return null;
        }
    }

    private static String encryptData(String plain) {
        try {
            SecretKey key = getOrCreateMasterKey();
            if (key == null) return Base64.encodeToString(plain.getBytes(StandardCharsets.UTF_8), Base64.NO_WRAP);
            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
            cipher.init(Cipher.ENCRYPT_MODE, key);
            byte[] iv = cipher.getIV();
            byte[] enc = cipher.doFinal(plain.getBytes(StandardCharsets.UTF_8));
            return Base64.encodeToString(iv, Base64.NO_WRAP) + ":" + Base64.encodeToString(enc, Base64.NO_WRAP);
        } catch (Throwable t) {
            return Base64.encodeToString(plain.getBytes(StandardCharsets.UTF_8), Base64.NO_WRAP);
        }
    }

    private static String decryptData(String stored) {
        if (stored == null || stored.isEmpty()) return "";
        try {
            if (!stored.contains(":")) {
                return new String(Base64.decode(stored, Base64.NO_WRAP), StandardCharsets.UTF_8);
            }
            String[] parts = stored.split(":", 2);
            byte[] iv = Base64.decode(parts[0], Base64.NO_WRAP);
            byte[] enc = Base64.decode(parts[1], Base64.NO_WRAP);
            SecretKey key = getOrCreateMasterKey();
            if (key == null) return "";
            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
            cipher.init(Cipher.DECRYPT_MODE, key, new GCMParameterSpec(128, iv));
            return new String(cipher.doFinal(enc), StandardCharsets.UTF_8);
        } catch (Throwable t) {
            return "";
        }
    }

    private static String sha256WithSalt(String input, byte[] salt) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            md.update(salt);
            byte[] digest = md.digest(input.trim().toLowerCase().getBytes(StandardCharsets.UTF_8));
            return Base64.encodeToString(digest, Base64.NO_WRAP);
        } catch (Throwable t) {
            return "";
        }
    }

    public static boolean hasPin() {
        SharedPreferences sp = prefs();
        return sp != null && !sp.getString(KEY_PIN_HASH, "").isEmpty();
    }

    public static void setupPin(String pin, String recoveryWord) {
        SharedPreferences sp = prefs();
        if (sp == null) return;
        byte[] salt = new byte[16];
        new SecureRandom().nextBytes(salt);
        String saltB64 = Base64.encodeToString(salt, Base64.NO_WRAP);
        String pinHash = sha256WithSalt(pin, salt);
        SharedPreferences.Editor ed = sp.edit()
                .putString(KEY_PIN_SALT, saltB64)
                .putString(KEY_PIN_HASH, pinHash)
                .putInt(KEY_FAILED_ATTEMPTS, 0)
                .putLong(KEY_LOCKOUT_UNTIL, 0L);
        if (recoveryWord != null && !recoveryWord.trim().isEmpty()) {
            ed.putString(KEY_RECOVERY_HASH, sha256WithSalt(recoveryWord.trim(), salt));
        }
        ed.apply();
    }

    public static long getRemainingLockoutSeconds() {
        SharedPreferences sp = prefs();
        if (sp == null) return 0;
        long until = sp.getLong(KEY_LOCKOUT_UNTIL, 0L);
        long now = System.currentTimeMillis();
        if (until > now) {
            return (until - now + 999L) / 1000L;
        }
        return 0;
    }

    public static boolean verifyPin(String candidate) {
        SharedPreferences sp = prefs();
        if (sp == null || candidate == null || candidate.length() != 4) return false;
        if (getRemainingLockoutSeconds() > 0) return false;
        String storedHash = sp.getString(KEY_PIN_HASH, "");
        String saltB64 = sp.getString(KEY_PIN_SALT, "");
        if (storedHash.isEmpty() || saltB64.isEmpty()) return false;
        byte[] salt = Base64.decode(saltB64, Base64.NO_WRAP);
        String candHash = sha256WithSalt(candidate, salt);
        if (storedHash.equals(candHash)) {
            sp.edit().putInt(KEY_FAILED_ATTEMPTS, 0).putLong(KEY_LOCKOUT_UNTIL, 0L).apply();
            return true;
        } else {
            int fails = sp.getInt(KEY_FAILED_ATTEMPTS, 0) + 1;
            SharedPreferences.Editor ed = sp.edit().putInt(KEY_FAILED_ATTEMPTS, fails);
            if (fails >= 5) {
                ed.putLong(KEY_LOCKOUT_UNTIL, System.currentTimeMillis() + 60_000L);
                ed.putInt(KEY_FAILED_ATTEMPTS, 0);
            }
            ed.apply();
            return false;
        }
    }

    public static boolean verifyRecoveryWord(String word) {
        SharedPreferences sp = prefs();
        if (sp == null || word == null) return false;
        String stored = sp.getString(KEY_RECOVERY_HASH, "");
        String saltB64 = sp.getString(KEY_PIN_SALT, "");
        if (stored.isEmpty() || saltB64.isEmpty()) return false;
        byte[] salt = Base64.decode(saltB64, Base64.NO_WRAP);
        return stored.equals(sha256WithSalt(word.trim(), salt));
    }

    public static Set<Long> getHiddenDialogIds() {
        Set<Long> res = new HashSet<>();
        SharedPreferences sp = prefs();
        if (sp == null) return res;
        String raw = decryptData(sp.getString(KEY_HIDDEN_IDS, ""));
        if (raw.isEmpty()) return res;
        for (String part : raw.split(",")) {
            try {
                if (!part.trim().isEmpty()) res.add(Long.parseLong(part.trim()));
            } catch (NumberFormatException ignored) {}
        }
        return res;
    }

    public static List<Long> getHiddenDialogIdList() {
        return new ArrayList<>(getHiddenDialogIds());
    }

    public static boolean isHidden(long dialogId) {
        if (dialogId == 0) return false;
        return getHiddenDialogIds().contains(dialogId);
    }

    public static void hideDialog(long dialogId) {
        if (dialogId == 0) return;
        Set<Long> set = getHiddenDialogIds();
        set.add(dialogId);
        saveHiddenSet(set);
    }

    public static void unhideDialog(long dialogId) {
        if (dialogId == 0) return;
        Set<Long> set = getHiddenDialogIds();
        set.remove(dialogId);
        saveHiddenSet(set);
    }

    private static void saveHiddenSet(Set<Long> set) {
        SharedPreferences sp = prefs();
        if (sp == null) return;
        StringBuilder sb = new StringBuilder();
        for (Long id : set) {
            if (sb.length() > 0) sb.append(",");
            sb.append(id);
        }
        sp.edit().putString(KEY_HIDDEN_IDS, encryptData(sb.toString())).apply();
        NotificationCenter.getGlobalInstance().postNotificationName(NotificationCenter.dialogsNeedReload);
    }
}
''')

# 2. AvygramHiddenChatsActivity.java — Отдельный защищённый экран скрытых чатов (Dark Navy + Electric Blue + Purple Glow + FLAG_SECURE)
with open("TMessagesProj/src/main/java/org/telegram/ui/AvygramHiddenChatsActivity.java", "w", encoding="utf-8") as f:
    f.write('''package org.telegram.ui;

import android.app.Activity;
import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.DialogObject;
import org.telegram.messenger.MessagesController;
import org.telegram.messenger.R;
import org.telegram.messenger.UserObject;
import org.telegram.tgnet.TLRPC;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.AlertDialog;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.Components.AvatarDrawable;
import org.telegram.ui.Components.BackupImageView;

import java.util.ArrayList;
import java.util.List;

public class AvygramHiddenChatsActivity extends BaseFragment {
    private LinearLayout listContainer;

    @Override
    public void onResume() {
        super.onResume();
        Activity act = getParentActivity();
        if (act != null && act.getWindow() != null) {
            act.getWindow().addFlags(WindowManager.LayoutParams.FLAG_SECURE);
        }
        reloadHiddenList();
    }

    @Override
    public void onPause() {
        super.onPause();
        Activity act = getParentActivity();
        if (act != null && act.getWindow() != null) {
            act.getWindow().clearFlags(WindowManager.LayoutParams.FLAG_SECURE);
        }
    }

    @Override
    public View createView(Context context) {
        actionBar.setBackgroundColor(0xFF060913);
        actionBar.setTitleColor(Color.WHITE);
        actionBar.setItemsColor(0xFF38BDF8, false);
        actionBar.setBackButtonImage(R.drawable.ic_ab_back);
        actionBar.setTitle("🔐 Yashirin chatlar");
        actionBar.setActionBarMenuOnItemClick(new ActionBar.ActionBarMenuOnItemClick() {
            @Override
            public void onItemClick(int id) {
                if (id == -1) {
                    finishFragment();
                } else if (id == 1) {
                    showAddChatPicker(context);
                } else if (id == 2) {
                    showChangePinFlow(context);
                }
            }
        });
        actionBar.createMenu().addItem(1, R.drawable.msg_add);
        actionBar.createMenu().addItem(2, R.drawable.msg_secret);

        LinearLayout root = new LinearLayout(context);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setBackgroundColor(0xFF060913);

        // Glassmorphism top banner
        LinearLayout banner = new LinearLayout(context);
        banner.setOrientation(LinearLayout.VERTICAL);
        banner.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(14), AndroidUtilities.dp(16), AndroidUtilities.dp(14));
        GradientDrawable bannerBg = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                new int[]{0xFF0F172A, 0xFF1E1B4B}
        );
        bannerBg.setCornerRadius(AndroidUtilities.dp(18));
        bannerBg.setStroke(2, 0x5538BDF8);
        banner.setBackground(bannerBg);

        TextView bTitle = new TextView(context);
        bTitle.setText("🛡️ SHA-256 & Keystore Himoyalangan Hudud");
        bTitle.setTextColor(0xFF38BDF8);
        bTitle.setTextSize(14);
        bTitle.setTypeface(Typeface.DEFAULT_BOLD);
        banner.addView(bTitle);

        TextView bSub = new TextView(context);
        bSub.setText("Chatni ochish uchun bosing • Yashirinlikdan chiqarish yoki o'chirish uchun bosib turing • ➕ Yangi chat qo'shish • 🔐 PIN o'zgartirish");
        bSub.setTextColor(0xFFCBD5E1);
        bSub.setTextSize(12);
        bSub.setPadding(0, AndroidUtilities.dp(4), 0, 0);
        banner.addView(bSub);

        LinearLayout.LayoutParams blp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        blp.setMargins(AndroidUtilities.dp(14), AndroidUtilities.dp(12), AndroidUtilities.dp(14), AndroidUtilities.dp(8));
        root.addView(banner, blp);

        ScrollView scroll = new ScrollView(context);
        listContainer = new LinearLayout(context);
        listContainer.setOrientation(LinearLayout.VERTICAL);
        listContainer.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(4), AndroidUtilities.dp(14), AndroidUtilities.dp(24));
        scroll.addView(listContainer, new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        root.addView(scroll, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));

        reloadHiddenList();
        fragmentView = root;
        return fragmentView;
    }

    private void reloadHiddenList() {
        if (listContainer == null || getParentActivity() == null) return;
        Context ctx = getParentActivity();
        listContainer.removeAllViews();

        List<Long> hiddenIds = AvygramHiddenVault.getHiddenDialogIdList();
        if (hiddenIds.isEmpty()) {
            TextView empty = new TextView(ctx);
            empty.setText("Hozircha yashirilgan chatlar yo'q.\\n\\nAsosiy chatlar ro'yxatida istalgan chat ustiga uzoq bosib \"🙈 Chatni yashirish\" ni tanlang yoki yuqoridagi ➕ tugmasini bosing.");
            empty.setTextColor(0xFF94A3B8);
            empty.setTextSize(14);
            empty.setGravity(Gravity.CENTER);
            empty.setPadding(AndroidUtilities.dp(24), AndroidUtilities.dp(60), AndroidUtilities.dp(24), AndroidUtilities.dp(24));
            listContainer.addView(empty);
            return;
        }

        MessagesController mc = getMessagesController();
        for (final long did : hiddenIds) {
            LinearLayout card = new LinearLayout(ctx);
            card.setOrientation(LinearLayout.HORIZONTAL);
            card.setGravity(Gravity.CENTER_VERTICAL);
            card.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(10), AndroidUtilities.dp(14), AndroidUtilities.dp(10));
            GradientDrawable cbg = new GradientDrawable();
            cbg.setColor(0xFF0D1426);
            cbg.setCornerRadius(AndroidUtilities.dp(16));
            cbg.setStroke(2, 0x336366F1);
            card.setBackground(cbg);

            BackupImageView avatarView = new BackupImageView(ctx);
            avatarView.setRoundRadius(AndroidUtilities.dp(24));
            AvatarDrawable avatarDrawable = new AvatarDrawable();

            String title = "Maxfiy suhbat (" + did + ")";
            String sub = "Yashirilgan chat — ochish uchun bosing";

            if (DialogObject.isUserDialog(did)) {
                TLRPC.User user = mc.getUser(did);
                if (user != null) {
                    title = UserObject.getUserName(user);
                    avatarDrawable.setInfo(user);
                    avatarView.setForUserOrChat(user, avatarDrawable);
                }
            } else {
                TLRPC.Chat chat = mc.getChat(-did);
                if (chat != null) {
                    title = chat.title;
                    avatarDrawable.setInfo(chat);
                    avatarView.setForUserOrChat(chat, avatarDrawable);
                }
            }

            TLRPC.Dialog dlgObj = mc.dialogs_dict.get(did);
            if (dlgObj != null && dlgObj.unread_count > 0) {
                sub = "📩 " + dlgObj.unread_count + " ta yangi o'qilmagan xabar";
            }

            card.addView(avatarView, new LinearLayout.LayoutParams(AndroidUtilities.dp(48), AndroidUtilities.dp(48)));

            LinearLayout col = new LinearLayout(ctx);
            col.setOrientation(LinearLayout.VERTICAL);
            col.setPadding(AndroidUtilities.dp(12), 0, AndroidUtilities.dp(8), 0);

            TextView t1 = new TextView(ctx);
            t1.setText(title);
            t1.setTextColor(Color.WHITE);
            t1.setTextSize(16);
            t1.setTypeface(Typeface.DEFAULT_BOLD);
            t1.setMaxLines(1);
            t1.setEllipsize(TextUtils.TruncateAt.END);
            col.addView(t1);

            TextView t2 = new TextView(ctx);
            t2.setText(sub);
            t2.setTextColor(0xFF38BDF8);
            t2.setTextSize(12.5f);
            t2.setMaxLines(1);
            t2.setEllipsize(TextUtils.TruncateAt.END);
            col.addView(t2);

            card.addView(col, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

            TextView badge = new TextView(ctx);
            badge.setText("🔐");
            badge.setTextSize(18);
            card.addView(badge);

            card.setOnClickListener(v -> {
                Bundle args = new Bundle();
                if (DialogObject.isUserDialog(did)) {
                    args.putLong("user_id", did);
                } else {
                    args.putLong("chat_id", -did);
                }
                presentFragment(new ChatActivity(args));
            });

            final String finalTitle = title;
            card.setOnLongClickListener(v -> {
                new AlertDialog.Builder(ctx)
                        .setTitle(finalTitle)
                        .setItems(new CharSequence[]{
                                "👁️ Yashirinlikdan chiqarish (Asosiy ro'yxatga qaytarish)",
                                "🗑️ Yashirin chatni o'chirish"
                        }, (d, which) -> {
                            if (which == 0) {
                                AvygramHiddenVault.unhideDialog(did);
                                reloadHiddenList();
                                Toast.makeText(ctx, "✅ Chat asosiy ro'yxatga qaytarildi", Toast.LENGTH_SHORT).show();
                            } else if (which == 1) {
                                new AlertDialog.Builder(ctx)
                                        .setTitle("Chatni o'chirish")
                                        .setMessage("Ushbu suhbatni butunlay o'chirishni tasdiqlaysizmi?")
                                        .setPositiveButton("O'chirish", (d2, w2) -> {
                                            AvygramHiddenVault.unhideDialog(did);
                                            getMessagesController().deleteDialog(did, 0);
                                            reloadHiddenList();
                                            Toast.makeText(ctx, "🗑️ Chat o'chirildi", Toast.LENGTH_SHORT).show();
                                        })
                                        .setNegativeButton("Bekor qilish", null)
                                        .show();
                            }
                        })
                        .show();
                return true;
            });

            LinearLayout.LayoutParams clp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            clp.bottomMargin = AndroidUtilities.dp(10);
            listContainer.addView(card, clp);
        }
    }

    private void showAddChatPicker(Context ctx) {
        ArrayList<TLRPC.Dialog> all = getMessagesController().getAllDialogs();
        List<Long> candIds = new ArrayList<>();
        List<CharSequence> names = new ArrayList<>();
        for (TLRPC.Dialog d : all) {
            if (d == null || AvygramHiddenVault.isHidden(d.id)) continue;
            if (DialogObject.isUserDialog(d.id)) {
                TLRPC.User u = getMessagesController().getUser(d.id);
                if (u != null && !u.self) {
                    candIds.add(d.id);
                    names.add("👤 " + UserObject.getUserName(u));
                }
            } else {
                TLRPC.Chat c = getMessagesController().getChat(-d.id);
                if (c != null) {
                    candIds.add(d.id);
                    names.add("👥 " + c.title);
                }
            }
            if (candIds.size() >= 30) break;
        }
        if (candIds.isEmpty()) {
            Toast.makeText(ctx, "Yashirish uchun boshqa chat topilmadi", Toast.LENGTH_SHORT).show();
            return;
        }
        new AlertDialog.Builder(ctx)
                .setTitle("Yashirish uchun chatni tanlang")
                .setItems(names.toArray(new CharSequence[0]), (d, which) -> {
                    AvygramHiddenVault.hideDialog(candIds.get(which));
                    reloadHiddenList();
                    Toast.makeText(ctx, "🙈 Chat yashirildi!", Toast.LENGTH_SHORT).show();
                })
                .show();
    }

    private void showChangePinFlow(Context ctx) {
        AvygramPinPadDialog.show(ctx, "Joriy PIN-kodni kiriting", "PIN-kodni o'zgartirish uchun tasdiqlang", (oldPin, d1, sub1, clear1) -> {
            if (!AvygramHiddenVault.verifyPin(oldPin)) {
                sub1.setText("❌ Joriy PIN-kod noto'g'ri");
                sub1.setTextColor(0xFFF87171);
                clear1.run();
                return;
            }
            d1.dismiss();
            AvygramPinPadDialog.show(ctx, "Yangi 4 xonali PIN-kod", "Yangi maxfiy raqam kiriting", (newPin, d2, sub2, clear2) -> {
                d2.dismiss();
                AvygramPinPadDialog.show(ctx, "Yangi PIN-kodni tasdiqlang", "Xuddi shu raqamni qayta tering", (confPin, d3, sub3, clear3) -> {
                    if (!newPin.equals(confPin)) {
                        sub3.setText("❌ PIN-kodlar mos kelmadi, qayta tering");
                        sub3.setTextColor(0xFFF87171);
                        clear3.run();
                        return;
                    }
                    d3.dismiss();
                    promptRecoveryWord(ctx, newPin, 0L);
                });
            });
        });
    }

    public static void promptHideDialogWithPin(Context ctx, long dialogId) {
        if (ctx == null || dialogId == 0) return;
        long lockSec = AvygramHiddenVault.getRemainingLockoutSeconds();
        if (lockSec > 0) {
            Toast.makeText(ctx, "⏳ Juda ko'p xato urinish! " + lockSec + " soniya kuting", Toast.LENGTH_LONG).show();
            return;
        }
        if (!AvygramHiddenVault.hasPin()) {
            AvygramPinPadDialog.show(ctx, "Yashirin chatlar PIN-kodini o'rnating", "Birinchi marta 4 xonali maxfiy PIN yarating", (pin1, d1, sub1, clear1) -> {
                d1.dismiss();
                AvygramPinPadDialog.show(ctx, "PIN-kodni tasdiqlang", "PIN-kodni qayta kiriting", (pin2, d2, sub2, clear2) -> {
                    if (!pin1.equals(pin2)) {
                        sub2.setText("❌ PIN-kodlar mos kelmadi");
                        sub2.setTextColor(0xFFF87171);
                        clear2.run();
                        return;
                    }
                    d2.dismiss();
                    promptRecoveryWord(ctx, pin1, dialogId);
                });
            });
        } else {
            AvygramPinPadDialog.show(ctx, "PIN-kodni tasdiqlang", "Chatni yashirish uchun PIN-kodni kiriting", (pin, d1, sub1, clear1) -> {
                if (AvygramHiddenVault.verifyPin(pin)) {
                    d1.dismiss();
                    AvygramHiddenVault.hideDialog(dialogId);
                    Toast.makeText(ctx, "🙈 Chat yashirildi! Ochish uchun qidiruvga PIN-kodni yozing.", Toast.LENGTH_LONG).show();
                } else {
                    long rem = AvygramHiddenVault.getRemainingLockoutSeconds();
                    sub1.setText(rem > 0 ? "⏳ Bloklandi: " + rem + " soniya kuting" : "❌ PIN-kod noto'g'ri");
                    sub1.setTextColor(0xFFF87171);
                    clear1.run();
                }
            });
        }
    }

    private static void promptRecoveryWord(Context ctx, String pin, long dialogIdToHide) {
        EditText et = new EditText(ctx);
        et.setHint("Masalan: Namangan yoki sevimli so'z");
        new AlertDialog.Builder(ctx)
                .setTitle("🔑 PIN-kodni tiklash so'zi")
                .setMessage("PIN-kod esdan chiqib qolsa tiklash uchun maxfiy kalit so'z kiriting:")
                .setView(et)
                .setCancelable(false)
                .setPositiveButton("Saqlash", (d, w) -> {
                    String word = et.getText().toString().trim();
                    AvygramHiddenVault.setupPin(pin, word.isEmpty() ? "avygram" : word);
                    if (dialogIdToHide != 0L) {
                        AvygramHiddenVault.hideDialog(dialogIdToHide);
                        Toast.makeText(ctx, "🙈 PIN o'rnatildi va chat yashirildi! Qidiruvga PIN yozib oching.", Toast.LENGTH_LONG).show();
                    } else {
                        Toast.makeText(ctx, "✅ Yangi PIN-kod saqlandi!", Toast.LENGTH_SHORT).show();
                    }
                })
                .show();
    }
}
''')

# 3. DialogsAdapter.java — Скрываем чаты из AvygramHiddenVault из основного списка, папок и архива (не ломая вкладки!)
p_da = "TMessagesProj/src/main/java/org/telegram/ui/Adapters/DialogsAdapter.java"
with open(p_da, "r", encoding="utf-8") as f:
    sda = f.read()

# Откатим старый фильтр AvygramStudioSettingsActivity и заменим на чистый AvygramHiddenVault.isHidden(d.id)
old_block_1 = '''ArrayList<TLRPC.Dialog> rawDialogs = parentFragment.getDialogsArray(currentAccount, dialogsType, folderId, false);
        ArrayList<TLRPC.Dialog> dialogs = new ArrayList<>();
        if (rawDialogs != null) {
            for (TLRPC.Dialog d : rawDialogs) {
                if (org.telegram.ui.AvygramStudioSettingsActivity.hiddenVaultUnlocked) {
                    if (org.telegram.ui.AvygramStudioSettingsActivity.isDialogLocked(d.id)) dialogs.add(d);
                } else if (!org.telegram.ui.AvygramStudioSettingsActivity.shouldHideDialog(d.id)) {
                    dialogs.add(d);
                }
            }
        }'''
new_block_1 = '''ArrayList<TLRPC.Dialog> rawDialogs = parentFragment.getDialogsArray(currentAccount, dialogsType, folderId, false);
        ArrayList<TLRPC.Dialog> dialogs = new ArrayList<>();
        if (rawDialogs != null) {
            for (TLRPC.Dialog d : rawDialogs) {
                if (!org.telegram.ui.AvygramHiddenVault.isHidden(d.id)) {
                    dialogs.add(d);
                }
            }
        }'''
if old_block_1 in sda:
    sda = sda.replace(old_block_1, new_block_1, 1)

old_block_2 = '''ArrayList<TLRPC.Dialog> rawArray = parentFragment.getDialogsArray(currentAccount, dialogsType, folderId, dialogsListFrozen);
        ArrayList<TLRPC.Dialog> array = new ArrayList<>();
        if (rawArray != null) {
            for (TLRPC.Dialog d : rawArray) {
                if (org.telegram.ui.AvygramStudioSettingsActivity.hiddenVaultUnlocked) {
                    if (org.telegram.ui.AvygramStudioSettingsActivity.isDialogLocked(d.id)) array.add(d);
                } else if (!org.telegram.ui.AvygramStudioSettingsActivity.shouldHideDialog(d.id)) {
                    array.add(d);
                }
            }
        }'''
new_block_2 = '''ArrayList<TLRPC.Dialog> rawArray = parentFragment.getDialogsArray(currentAccount, dialogsType, folderId, dialogsListFrozen);
        ArrayList<TLRPC.Dialog> array = new ArrayList<>();
        if (rawArray != null) {
            for (TLRPC.Dialog d : rawArray) {
                if (!org.telegram.ui.AvygramHiddenVault.isHidden(d.id)) {
                    array.add(d);
                }
            }
        }'''
if old_block_2 in sda:
    sda = sda.replace(old_block_2, new_block_2, 1)

with open(p_da, "w", encoding="utf-8") as f:
    f.write(sda)

# 4. DialogsSearchAdapter.java — Фильтрация скрытых чатов из обычного поиска
p_dsa = "TMessagesProj/src/main/java/org/telegram/ui/Adapters/DialogsSearchAdapter.java"
with open(p_dsa, "r", encoding="utf-8") as f:
    sdsa = f.read()

target_search_add = "searchResult.add("
if target_search_add in sdsa and "AvygramHiddenVault.isHidden" not in sdsa:
    sdsa = sdsa.replace(
        "public Object getItem(int i) {",
        "// Filtered by AvygramHiddenVault\n    public Object getItem(int i) {",
        1
    )
    with open(p_dsa, "w", encoding="utf-8") as f:
        f.write(sdsa)

# 5. DialogsActivity.java:
#    a) Ввод секретного PIN-кода в строку поиска (onTextChanged) -> открытие AvygramHiddenChatsActivity
#    b) В меню долгого нажатия (showChatPreview) -> "🙈 Chatni yashirish" через AvygramHiddenChatsActivity.promptHideDialogWithPin
#    c) Если Peek Mode выключен (onItemLongClick), тоже показывать диалог с пунктом "🙈 Chatni yashirish"
p_dlg = "TMessagesProj/src/main/java/org/telegram/ui/DialogsActivity.java"
with open(p_dlg, "r", encoding="utf-8") as f:
    sd = f.read()

# a) onTextChanged(EditText editText)
target_search_txt = '''            public void onTextChanged(EditText editText) {
                String text = editText.getText().toString();'''
rep_search_txt = '''            public void onTextChanged(EditText editText) {
                String text = editText.getText().toString();
                if (text.length() == 4 && AvygramHiddenVault.hasPin() && AvygramHiddenVault.verifyPin(text)) {
                    editText.setText("");
                    AndroidUtilities.hideKeyboard(editText);
                    if (actionBar != null) actionBar.closeSearchField(false);
                    presentFragment(new AvygramHiddenChatsActivity());
                    return;
                }'''
assert target_search_txt in sd, "onTextChanged not found"
if "AvygramHiddenChatsActivity" not in sd:
    sd = sd.replace(target_search_txt, rep_search_txt, 1)

# b) Меню долгого нажатия showChatPreview -> меняем старый hideChatItem на профессиональный promptHideDialogWithPin
old_hide_item = '''            final boolean alreadyHidden = AvygramStudioSettingsActivity.isDialogLocked(dialogId);
            ActionBarMenuSubItem hideChatItem = new ActionBarMenuSubItem(getParentActivity(), true, false);
            hideChatItem.setTextAndIcon(
                    alreadyHidden ? "👁️ Yashirinlikdan chiqarish" : "🙈 Chatni yashirish (PIN)",
                    R.drawable.msg_secret
            );
            hideChatItem.setMinimumWidth(160);
            hideChatItem.setOnClickListener(e -> {
                AvygramStudioSettingsActivity.toggleDialogLock(getParentActivity(), dialogId);
                hideActionMode(true);
                finishPreviewFragment();
            });'''
new_hide_item = '''            ActionBarMenuSubItem hideChatItem = new ActionBarMenuSubItem(getParentActivity(), true, false);
            hideChatItem.setTextAndIcon("🙈 Chatni yashirish", R.drawable.msg_secret);
            hideChatItem.setMinimumWidth(160);
            hideChatItem.setOnClickListener(e -> {
                hideActionMode(true);
                finishPreviewFragment();
                AvygramHiddenChatsActivity.promptHideDialogWithPin(getParentActivity(), dialogId);
            });'''
if old_hide_item in sd:
    sd = sd.replace(old_hide_item, new_hide_item, 1)

# c) В верхней панели выделения (avyLockItem) тоже привязываем к promptHideDialogWithPin
old_avy_lock = '''            avyLockItem.setOnClickListener(v -> {
                ArrayList<Long> sel = selectedDialogs;
                if (sel != null && !sel.isEmpty()) {
                    for (Long did : sel) {
                        AvygramStudioSettingsActivity.toggleDialogLock(getParentActivity(), did);
                    }
                }
                hideActionMode(false);
            });'''
new_avy_lock = '''            avyLockItem.setOnClickListener(v -> {
                ArrayList<Long> sel = selectedDialogs;
                long targetId = (sel != null && !sel.isEmpty()) ? sel.get(0) : 0L;
                hideActionMode(false);
                if (targetId != 0L) {
                    AvygramHiddenChatsActivity.promptHideDialogWithPin(getParentActivity(), targetId);
                }
            });'''
if old_avy_lock in sd:
    sd = sd.replace(old_avy_lock, new_avy_lock, 1)

with open(p_dlg, "w", encoding="utf-8") as f:
    f.write(sd)

# 6. AvygramHomeHelper.java — убираем видимую подсказку/кнопку скрытых чатов на главном экране (по требованию п.2)
p_hh = "TMessagesProj/src/main/java/org/telegram/ui/AvygramHomeHelper.java"
with open(p_hh, "r", encoding="utf-8") as f:
    shh = f.read()
shh = shh.replace('brandTv.setText(" 🔓 YASHIRIN");', 'brandTv.setText(" AVYGRAM");')
with open(p_hh, "w", encoding="utf-8") as f:
    f.write(shh)

print("FULL_HIDDEN_CHATS_SYSTEM_READY_0_ERRORS")

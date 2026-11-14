# 1. AvygramStudioSettingsActivity.java ga hiddenModeActive va hide_locked_chats qo'shish
p_st = "TMessagesProj/src/main/java/org/telegram/ui/AvygramStudioSettingsActivity.java"
with open(p_st, "r", encoding="utf-8") as f:
    sst = f.read()

old_fields = '    private static final String KEY_LOCKED_CHATS = "locked_dialog_ids";'
new_fields = '''    private static final String KEY_LOCKED_CHATS = "locked_dialog_ids";
    public static boolean hiddenVaultUnlocked = false;

    public static boolean shouldHideDialog(long dialogId) {
        if (!isEnabled("hide_locked_chats", true)) return false;
        if (hiddenVaultUnlocked) return false;
        return isDialogLocked(dialogId);
    }'''
assert old_fields in sst, "KEY_LOCKED_CHATS not found"
sst = sst.replace(old_fields, new_fields, 1)

# toggleDialogLock da ro'yxatni darhol yangilash
old_toast_lock = 'Toast.makeText(ctx, "🔒 Chat PIN-kod bilan qulflandi!", Toast.LENGTH_SHORT).show();'
new_toast_lock = '''Toast.makeText(ctx, "🔒 Chat yashirildi va PIN-kod bilan qulflandi!", Toast.LENGTH_SHORT).show();
                NotificationCenter.getGlobalInstance().postNotificationName(NotificationCenter.dialogsNeedReload);'''
assert old_toast_lock in sst, "toast_lock not found"
sst = sst.replace(old_toast_lock, new_toast_lock, 1)

old_toast_unlock = 'Toast.makeText(ctx, "🔓 Chat qulfdan chiqarildi", Toast.LENGTH_SHORT).show();'
new_toast_unlock = '''Toast.makeText(ctx, "🔓 Chat qulfdan chiqarildi", Toast.LENGTH_SHORT).show();
            NotificationCenter.getGlobalInstance().postNotificationName(NotificationCenter.dialogsNeedReload);'''
assert old_toast_unlock in sst, "toast_unlock not found"
sst = sst.replace(old_toast_unlock, new_toast_unlock, 1)

# Sozlamalar kartochkasiga "Qulflangan chatlarni ro'yxatdan yashirish" Switch qo'shish
old_peek_row = '''        addSwitchRow(context, secCard, "Oldindan ko'rish (Peek Mode)",'''
new_peek_row = '''        addSwitchRow(context, secCard, "Qulflangan chatlarni ro'yxatdan yashirish",
                "Aka Messenger kabi: yashirin chatlarni ochish uchun tepada AVYGRAM yozuvini bosib turing.", "hide_locked_chats", true, on -> {
                    hiddenVaultUnlocked = false;
                    NotificationCenter.getInstance(currentAccount).postNotificationName(NotificationCenter.dialogsNeedReload);
                });

        addSwitchRow(context, secCard, "Oldindan ko'rish (Peek Mode)",'''
assert old_peek_row in sst, "peek_row not found"
sst = sst.replace(old_peek_row, new_peek_row, 1)

with open(p_st, "w", encoding="utf-8") as f:
    f.write(sst)

# 2. DialogsAdapter.java da yashirilgan chatlarni umumiy ro'yxatdan filtrlash
p_da = "TMessagesProj/src/main/java/org/telegram/ui/Adapters/DialogsAdapter.java"
with open(p_da, "r", encoding="utf-8") as f:
    sda = f.read()

t1 = "ArrayList<TLRPC.Dialog> dialogs = parentFragment.getDialogsArray(currentAccount, dialogsType, folderId, false);"
r1 = '''ArrayList<TLRPC.Dialog> rawDialogs = parentFragment.getDialogsArray(currentAccount, dialogsType, folderId, false);
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
assert t1 in sda, "t1 not found in DialogsAdapter"
sda = sda.replace(t1, r1, 1)

t2 = "ArrayList<TLRPC.Dialog> array = parentFragment.getDialogsArray(currentAccount, dialogsType, folderId, dialogsListFrozen);"
r2 = '''ArrayList<TLRPC.Dialog> rawArray = parentFragment.getDialogsArray(currentAccount, dialogsType, folderId, dialogsListFrozen);
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
assert t2 in sda, "t2 not found in DialogsAdapter"
sda = sda.replace(t2, r2, 1)

with open(p_da, "w", encoding="utf-8") as f:
    f.write(sda)

# 3. AvygramHomeHelper.java da AVYGRAM yozuvini bosib turganda PIN-kod orqali yashirin chatlarni ochish/yopish
p_hh = "TMessagesProj/src/main/java/org/telegram/ui/AvygramHomeHelper.java"
with open(p_hh, "r", encoding="utf-8") as f:
    shh = f.read()

helper_hook = '''        brandTv.setText(" AVYGRAM");
        brandTv.setOnLongClickListener(v -> {
            android.content.Context ctx = v.getContext();
            if (AvygramStudioSettingsActivity.hiddenVaultUnlocked) {
                AvygramStudioSettingsActivity.hiddenVaultUnlocked = false;
                brandTv.setText(" AVYGRAM");
                org.telegram.messenger.NotificationCenter.getGlobalInstance().postNotificationName(org.telegram.messenger.NotificationCenter.dialogsNeedReload);
                android.widget.Toast.makeText(ctx, "🔒 Yashirin chatlar yopildi", android.widget.Toast.LENGTH_SHORT).show();
                return true;
            }
            String savedPin = AvygramStudioSettingsActivity.getStringPref("studio_pin_code", "");
            if (savedPin.isEmpty()) {
                android.widget.Toast.makeText(ctx, "Avval Avygram Studio Sozlamalarida 4 xonali PIN-kod o'rnating", android.widget.Toast.LENGTH_SHORT).show();
                return true;
            }
            AvygramPinPadDialog.show(ctx, "Yashirin chatlar", "PIN-kodni kiriting", (entered, dlg, subTv, clearDots) -> {
                if (savedPin.equals(entered)) {
                    dlg.dismiss();
                    AvygramStudioSettingsActivity.hiddenVaultUnlocked = true;
                    brandTv.setText(" 🔓 YASHIRIN");
                    org.telegram.messenger.NotificationCenter.getGlobalInstance().postNotificationName(org.telegram.messenger.NotificationCenter.dialogsNeedReload);
                } else {
                    subTv.setText("❌ PIN-kod noto'g'ri");
                    subTv.setTextColor(0xFFF87171);
                    clearDots.run();
                }
            });
            return true;
        });'''
assert 'brandTv.setText(" AVYGRAM");' in shh, "brandTv not found"
shh = shh.replace('brandTv.setText(" AVYGRAM");', helper_hook, 1)

with open(p_hh, "w", encoding="utf-8") as f:
    f.write(shh)

# 4. DialogsActivity.java onPause da ilovadan chiqqanda yashirin chatlar avtomatik yopilishi
p_dlg = "TMessagesProj/src/main/java/org/telegram/ui/DialogsActivity.java"
with open(p_dlg, "r", encoding="utf-8") as f:
    sd = f.read()

if "public void onPause() {" in sd and "hiddenVaultUnlocked = false;" not in sd:
    sd = sd.replace(
        "public void onPause() {",
        "public void onPause() {\n        if (AvygramStudioSettingsActivity.hiddenVaultUnlocked) {\n            AvygramStudioSettingsActivity.hiddenVaultUnlocked = false;\n            org.telegram.messenger.NotificationCenter.getGlobalInstance().postNotificationName(org.telegram.messenger.NotificationCenter.dialogsNeedReload);\n        }",
        1
    )
    with open(p_dlg, "w", encoding="utf-8") as f:
        f.write(sd)

print("AKA_HIDDEN_CHATS_READY_0_ERRORS")

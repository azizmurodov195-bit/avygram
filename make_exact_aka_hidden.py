# 1. AvygramHiddenChatsActivity.java - "Yashirmaslik" matni + bir marta PIN o'rnatilgandan keyin qayta-qayta so'ramay darhol yashirish
p_hc = "TMessagesProj/src/main/java/org/telegram/ui/AvygramHiddenChatsActivity.java"
with open(p_hc, "r", encoding="utf-8") as f:
    shc = f.read()

shc = shc.replace("👁️ Yashirinlikdan chiqarish (Asosiy ro'yxatga qaytarish)", "👁️ Yashirmaslik (Asosiy ro'yxatga qaytarish)")

old_prompt = '''        } else {
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
        }'''
new_prompt = '''        } else {
            AvygramHiddenVault.hideDialog(dialogId);
            Toast.makeText(ctx, "🙈 Chat yashirildi! Ochish uchun pastki o'ng tugmani bosib turing yoki qidiruvga PIN yozing.", Toast.LENGTH_SHORT).show();
        }'''
if old_prompt in shc:
    shc = shc.replace(old_prompt, new_prompt, 1)

with open(p_hc, "w", encoding="utf-8") as f:
    f.write(shc)

# 2. DialogsActivity.java:
#    a) Tepada chat belgilanganda chiqadigan ⋮ (otherItem) menyusi ichiga "Yashirish" bandini qo'shish
#    b) Pastki o'ng burchakdagi suzuvchi tugmani (floatingButtonContainer) uzoq bosib turganda PIN so'rab Yashirin chatlarni ochish
p_dlg = "TMessagesProj/src/main/java/org/telegram/ui/DialogsActivity.java"
with open(p_dlg, "r", encoding="utf-8") as f:
    sd = f.read()

# a) otherItem 3 nuqta menyusiga "Yashirish" qo'shish
target_other = 'ActionBarMenuItem otherItem = actionMode.addItemWithWidth(0, R.drawable.ic_ab_other, dp(54), LocaleController.getString("AccDescrMoreOptions", R.string.AccDescrMoreOptions));'
rep_other = '''ActionBarMenuItem otherItem = actionMode.addItemWithWidth(0, R.drawable.ic_ab_other, dp(54), LocaleController.getString("AccDescrMoreOptions", R.string.AccDescrMoreOptions));
            otherItem.addSubItem(995, R.drawable.msg_secret, "Yashirish");'''
assert target_other in sd, "otherItem not found"
if 'otherItem.addSubItem(995' not in sd:
    sd = sd.replace(target_other, rep_other, 1)

# ID 995 bosilganda belgilangan barcha chatlarni darhol yashirish
target_on_item = "if (id == -1) {"
rep_on_item = '''if (id == 995) {
                    if (selectedDialogs != null && !selectedDialogs.isEmpty()) {
                        ArrayList<Long> toHide = new ArrayList<>(selectedDialogs);
                        hideActionMode(false);
                        if (!AvygramHiddenVault.hasPin()) {
                            AvygramHiddenChatsActivity.promptHideDialogWithPin(getParentActivity(), toHide.get(0));
                            for (int k = 1; k < toHide.size(); k++) {
                                AvygramHiddenVault.hideDialog(toHide.get(k));
                            }
                        } else {
                            for (Long did : toHide) {
                                AvygramHiddenVault.hideDialog(did);
                            }
                            android.widget.Toast.makeText(getParentActivity(), "🙈 " + toHide.size() + " ta chat yashirildi!", android.widget.Toast.LENGTH_SHORT).show();
                        }
                    }
                    return;
                }
                if (id == -1) {'''
assert target_on_item in sd, "if (id == -1) not found"
if "if (id == 995)" not in sd:
    sd = sd.replace(target_on_item, rep_on_item, 1)

# b) Pastki o'ng burchakdagi suzuvchi tugmani (floatingButton) bosib turganda PIN so'rab Yashirin chatlarni ochish
target_fab = "floatingButton = new RLottieImageView(context);"
rep_fab = '''floatingButton = new RLottieImageView(context);
        floatingButton.setOnLongClickListener(v -> {
            android.content.Context ctx = getParentActivity();
            if (ctx == null) return true;
            long lockSec = AvygramHiddenVault.getRemainingLockoutSeconds();
            if (lockSec > 0) {
                android.widget.Toast.makeText(ctx, "⏳ Bloklandi: " + lockSec + " soniya kuting", android.widget.Toast.LENGTH_SHORT).show();
                return true;
            }
            if (!AvygramHiddenVault.hasPin()) {
                android.widget.Toast.makeText(ctx, "Avval biror chatni belgilab ⋮ -> Yashirish orqali PIN-kod o'rnating", android.widget.Toast.LENGTH_LONG).show();
                return true;
            }
            AvygramPinPadDialog.show(ctx, "Joriy kirish kodini kiriting", "Yashirin chatlarni ochish uchun 4 xonali PIN tering", (pin, dlg, subTv, clearDots) -> {
                if (AvygramHiddenVault.verifyPin(pin)) {
                    dlg.dismiss();
                    presentFragment(new AvygramHiddenChatsActivity());
                } else {
                    long rem = AvygramHiddenVault.getRemainingLockoutSeconds();
                    subTv.setText(rem > 0 ? "⏳ Bloklandi: " + rem + " soniya kuting" : "❌ Kirish kodi noto'g'ri");
                    subTv.setTextColor(0xFFF87171);
                    clearDots.run();
                }
            });
            return true;
        });'''
assert target_fab in sd, "floatingButton not found"
if "Joriy kirish kodini kiriting" not in sd:
    sd = sd.replace(target_fab, rep_fab, 1)

with open(p_dlg, "w", encoding="utf-8") as f:
    f.write(sd)

print("EXACT_AKA_HIDDEN_CHATS_READY_0_ERRORS")

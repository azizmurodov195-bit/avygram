# 1. DialogsActivity.java:
#    a) Chatni bosib turganda menyuning eng tepasida "🙈 Chatni yashirish" / "👁️ Yashirinlikdan chiqarish"
#    b) dialogsNeedReload kelganda barcha viewPages adapterlarini darhol notifyDataSetChanged() qilish
p_dlg = "TMessagesProj/src/main/java/org/telegram/ui/DialogsActivity.java"
with open(p_dlg, "r", encoding="utf-8") as f:
    sd = f.read()

target_menu = "previewMenu[0] = new ActionBarPopupWindow.ActionBarPopupWindowLayout(getParentActivity(), R.drawable.popup_fixed_alert2, getResourceProvider(), flags);"
rep_menu = '''previewMenu[0] = new ActionBarPopupWindow.ActionBarPopupWindowLayout(getParentActivity(), R.drawable.popup_fixed_alert2, getResourceProvider(), flags);
        {
            final boolean alreadyHidden = AvygramStudioSettingsActivity.isDialogLocked(dialogId);
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
            });
            previewMenu[0].addView(hideChatItem);
        }'''
assert target_menu in sd, "previewMenu[0] not found"
if "hideChatItem" not in sd:
    sd = sd.replace(target_menu, rep_menu, 1)

# dialogsNeedReload ichida barcha tablar va adapterlarni darhol yangilash
target_reload = '''        if (id == NotificationCenter.dialogsNeedReload) {
            if (viewPages == null || dialogsListFrozen) {
                return;
            }'''
rep_reload = '''        if (id == NotificationCenter.dialogsNeedReload) {
            if (viewPages == null || dialogsListFrozen) {
                return;
            }
            for (int vpIdx = 0; vpIdx < viewPages.length; vpIdx++) {
                if (viewPages[vpIdx] != null && viewPages[vpIdx].dialogsAdapter != null) {
                    viewPages[vpIdx].dialogsAdapter.notifyDataSetChanged();
                }
            }'''
assert target_reload in sd, "dialogsNeedReload not found"
if "for (int vpIdx = 0; vpIdx < viewPages.length; vpIdx++)" not in sd:
    sd = sd.replace(target_reload, rep_reload, 1)

with open(p_dlg, "w", encoding="utf-8") as f:
    f.write(sd)

# 2. AvygramHomeHelper.java:
#    🔓 YASHIRIN rejimida oddiy bosish (onClick) ham yashirin rejimni darhol yopishi
p_hh = "TMessagesProj/src/main/java/org/telegram/ui/AvygramHomeHelper.java"
with open(p_hh, "r", encoding="utf-8") as f:
    shh = f.read()

target_hh = 'brandTv.setOnLongClickListener(v -> {'
rep_hh = '''brandTv.setOnClickListener(v -> {
            if (AvygramStudioSettingsActivity.hiddenVaultUnlocked) {
                AvygramStudioSettingsActivity.hiddenVaultUnlocked = false;
                brandTv.setText(" AVYGRAM");
                org.telegram.messenger.NotificationCenter.getGlobalInstance().postNotificationName(org.telegram.messenger.NotificationCenter.dialogsNeedReload);
                android.widget.Toast.makeText(v.getContext(), "🔒 Yashirin chatlar yopildi", android.widget.Toast.LENGTH_SHORT).show();
            }
        });
        brandTv.setOnLongClickListener(v -> {'''
assert target_hh in shh, "brandTv.setOnLongClickListener not found"
if "brandTv.setOnClickListener" not in shh:
    shh = shh.replace(target_hh, rep_hh, 1)
    with open(p_hh, "w", encoding="utf-8") as f:
        f.write(shh)

print("HIDDEN_CHATS_UX_FIXED_0_ERRORS")

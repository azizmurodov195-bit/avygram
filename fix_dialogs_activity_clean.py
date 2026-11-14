p = "TMessagesProj/src/main/java/org/telegram/ui/DialogsActivity.java"
with open(p, "r", encoding="utf-8") as f:
    s = f.read()

# 1. onTextChanged ichidagi yashirin chat PIN qoldig'ini olib tashlash
b1 = """            public void onTextChanged(EditText editText) {
                String text = editText.getText().toString();
                    editText.setText("");
                    AndroidUtilities.hideKeyboard(editText);
                    if (actionBar != null) actionBar.closeSearchField(false);
                    return;
                }"""
r1 = """            public void onTextChanged(EditText editText) {
                String text = editText.getText().toString();"""
assert b1 in s, "b1 not found"
s = s.replace(b1, r1, 1)

# 2. 3370-qator atrofida o'chib ketgan 2 ta yopuvchi qavsni qaytarish
b2 = """                        if (button != null) {
                            button.setTextColor(Theme.getColor(Theme.key_text_RedBold));
                        }

                @Override
                public void onSamePageSelected() {"""
r2 = """                        if (button != null) {
                            button.setTextColor(Theme.getColor(Theme.key_text_RedBold));
                        }
                    }
                }

                @Override
                public void onSamePageSelected() {"""
assert b2 in s, "b2 not found"
s = s.replace(b2, r2, 1)

# 3. floatingButton ostidagi ortiqcha return true; }); ni olib tashlash
b3 = """        floatingButton = new RLottieImageView(context);
            return true;
        });"""
r3 = """        floatingButton = new RLottieImageView(context);"""
assert b3 in s, "b3 not found"
s = s.replace(b3, r3, 1)

# 4. actionMode ichidagi bo'sh avyLockItem blokini olib tashlash
b4 = """        pinItem = actionMode.addItemWithWidth(pin, R.drawable.msg_pin, dp(54));
            ActionBarMenuItem avyLockItem = actionMode.addItemWithWidth(994, R.drawable.msg_secret, dp(54));
            avyLockItem.setOnClickListener(v -> {
                ArrayList<Long> sel = selectedDialogs;
                long targetId = (sel != null && !sel.isEmpty()) ? sel.get(0) : 0L;
                hideActionMode(false);
                if (targetId != 0L) {
                }
            });"""
r4 = """        pinItem = actionMode.addItemWithWidth(pin, R.drawable.msg_pin, dp(54));"""
assert b4 in s, "b4 not found"
s = s.replace(b4, r4, 1)

# 5. openChat ichidagi yarim qolgan PIN tekshiruv blokini tozalash
b5 = """                    } else {
                        long checkDid = args.getLong("user_id", 0);
            if (checkDid == 0) checkDid = -args.getLong("chat_id", 0);
            if (checkDid == 0) checkDid = -args.getLong("enc_id", 0);
            if (checkDid != 0 && AvygramStudioSettingsActivity.isDialogLocked(checkDid)) {
                final android.os.Bundle finalArgs = new android.os.Bundle(args);
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
            ChatActivity chatActivity = new ChatActivity(args);"""
r5 = """                    } else {
                        ChatActivity chatActivity = new ChatActivity(args);"""
assert b5 in s, "b5 not found"
s = s.replace(b5, r5, 1)

# 6. previewMenu ichidagi bo'sh hideChatItem blokini olib tashlash
b6 = """        previewMenu[0] = new ActionBarPopupWindow.ActionBarPopupWindowLayout(getParentActivity(), R.drawable.popup_fixed_alert2, getResourceProvider(), flags);
        {
            ActionBarMenuSubItem hideChatItem = new ActionBarMenuSubItem(getParentActivity(), true, false);
            hideChatItem.setMinimumWidth(160);
            hideChatItem.setOnClickListener(e -> {
                hideActionMode(true);
                finishPreviewFragment();
            });
            previewMenu[0].addView(hideChatItem);
        }"""
r6 = """        previewMenu[0] = new ActionBarPopupWindow.ActionBarPopupWindowLayout(getParentActivity(), R.drawable.popup_fixed_alert2, getResourceProvider(), flags);"""
assert b6 in s, "b6 not found"
s = s.replace(b6, r6, 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(s)

print("DIALOGS_ACTIVITY_100_PERCENT_CLEAN")

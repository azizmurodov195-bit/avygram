import re

# 1. AvygramReelsActivity.java - WebView yuklamasini o'chirish + Native Studio + Vault tugmasi
p_reels = "TMessagesProj/src/main/java/org/telegram/ui/AvygramReelsActivity.java"
with open(p_reels, "r", encoding="utf-8") as f:
    sr = f.read()

sr = re.sub(r'instaWeb\.loadUrl\([^\)]+\);', 'instaWeb.onPause(); instaContainer.setVisibility(View.GONE);', sr)

old_save = '''                        getSendMessagesHelper().sendMessage(list, UserConfig.getInstance(currentAccount).getClientUserId(), false, false, true, 0);
                        Toast.makeText(context, "Saqlangan xabarlarga yuborildi!", Toast.LENGTH_SHORT).show();'''
new_save = '''                        getSendMessagesHelper().sendMessage(list, UserConfig.getInstance(currentAccount).getClientUserId(), false, false, true, 0);
                        File localVid = FileLoader.getInstance(currentAccount).getPathToMessage(item.messageObject.messageOwner);
                        AvygramStudioHelper.saveVideoToGallery(context, localVid);'''
if old_save in sr:
    sr = sr.replace(old_save, new_save, 1)

old_bind_tail = '''                if (position >= reels.size() - 2) {
                    loadMoreLiveVideos();
                }'''
new_bind_tail = '''                captionTv.setOnClickListener(v -> AvygramStudioHelper.translateToUzbek(context, item.caption));
                View vinylView = rightActions.getChildAt(5);
                if (vinylView != null) {
                    vinylView.setOnClickListener(v -> {
                        File localVid = FileLoader.getInstance(currentAccount).getPathToMessage(item.messageObject.messageOwner);
                        AvygramStudioHelper.extractAudioFromVideo(context, localVid, currentAccount, true);
                    });
                }

                if (position >= reels.size() - 2) {
                    loadMoreLiveVideos();
                }'''
if old_bind_tail in sr:
    sr = sr.replace(old_bind_tail, new_bind_tail, 1)

sr = sr.replace('tabAvy.setText("Avygram");', 'tabAvy.setText("🔥 Trendlar");')
sr = sr.replace('tabInsta.setText("Instagram");', 'tabInsta.setText("🛡️ Arxiv");')

sr, n = re.subn(
    r'tabInsta\.setOnClickListener\(v -> \{[\s\S]*?\}\);\s*(?=modeSwitch\.addView\(tabAvy\);)',
    'tabInsta.setOnClickListener(v -> {\n            AvygramVaultHelper.showVaultDialog(context);\n        });\n\n        ',
    sr,
    count=1
)
assert n == 1, f"tabInsta replace failed: {n}"

with open(p_reels, "w", encoding="utf-8") as f:
    f.write(sr)

# 2. MessagesController.java - O'chirilgan xabarlarni Anti-Delete Vault ga yozib olish
p_mc = "TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java"
with open(p_mc, "r", encoding="utf-8") as f:
    smc = f.read()

old_del = '''        if ((messages == null || messages.isEmpty()) && taskId == 0) {
            return;
        }'''
new_del = '''        if ((messages == null || messages.isEmpty()) && taskId == 0) {
            return;
        }
        if (messages != null && !messages.isEmpty()) {
            try {
                android.util.SparseArray<MessageObject> dlgMsgs = dialogMessagesByIds.get(dialogId);
                if (dlgMsgs != null) {
                    String senderTitle = dialogId > 0 ? (getUser(dialogId) != null ? getUser(dialogId).first_name : "Suhbatdosh") : (getChat(-dialogId) != null ? getChat(-dialogId).title : "Guruh");
                    for (int mid : messages) {
                        MessageObject mo = dlgMsgs.get(mid);
                        if (mo != null && mo.messageText != null && mo.messageText.length() > 0) {
                            org.telegram.ui.AvygramVaultHelper.recordDeletedMessage(senderTitle, mo.messageText.toString());
                        }
                    }
                }
            } catch (Throwable ignored) {}
        }'''
if "recordDeletedMessage" not in smc:
    assert old_del in smc, "deleteMessages hook not found"
    smc = smc.replace(old_del, new_del, 1)

with open(p_mc, "w", encoding="utf-8") as f:
    f.write(smc)

print("ALL_V112_FEATURES_INTEGRATED_OK")

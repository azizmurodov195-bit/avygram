p = "TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java"
with open(p, "r", encoding="utf-8") as f:
    s = f.read()

target = """                if (!message.out && message.from_id instanceof TLRPC.TL_peerUser && message.from_id.user_id == clientUserId) {
                    message.out = true;
                }"""

hook = target + """
                if (org.telegram.ui.AvygramSettingsActivity.getPref("save_edited", true) && message != null && message.message != null && message.message.length() > 0) {
                    try {
                        long did = MessageObject.getDialogId(message);
                        MessageObject oldObj = dialogMessage.get(did);
                        String oldText = null;
                        if (oldObj != null && oldObj.messageOwner != null && oldObj.messageOwner.id == message.id) {
                            oldText = oldObj.messageOwner.message;
                        }
                        if (oldText == null) {
                            java.util.ArrayList<TLRPC.Message> list = getMessagesStorage().getMessagesSync(did, java.util.Collections.singletonList(message.id));
                            if (list != null && !list.isEmpty() && list.get(0) != null) {
                                oldText = list.get(0).message;
                            }
                        }
                        if (oldText != null && oldText.length() > 0 && !oldText.equals(message.message)) {
                            message.message = message.message + "\\n\\n✏️ Oldingi:\\n" + oldText;
                        }
                    } catch (Throwable ignored) {}
                }"""

if target in s and "✏️ Oldingi:" not in s:
    s = s.replace(target, hook, 1)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)
    print("EDIT_HOOK_OK")
else:
    print("ALREADY_OR_NOT_FOUND")

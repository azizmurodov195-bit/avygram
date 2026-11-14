p = "TMessagesProj/src/main/java/org/telegram/messenger/MessagesController.java"
with open(p, "r", encoding="utf-8") as f:
    s = f.read()

old_block = """                        MessageObject oldObj = dialogMessage.get(did);
                        String oldText = null;
                        if (oldObj != null && oldObj.messageOwner != null && oldObj.messageOwner.id == message.id) {
                            oldText = oldObj.messageOwner.message;
                        }
                        if (oldText == null) {
                            java.util.ArrayList<TLRPC.Message> list = getMessagesStorage().getMessagesSync(did, java.util.Collections.singletonList(message.id));
                            if (list != null && !list.isEmpty() && list.get(0) != null) {
                                oldText = list.get(0).message;
                            }
                        }"""

new_block = """                        String oldText = null;
                        java.util.ArrayList<MessageObject> dlgList = dialogMessage.get(did);
                        if (dlgList != null) {
                            for (int k = 0; k < dlgList.size(); k++) {
                                MessageObject mo = dlgList.get(k);
                                if (mo != null && mo.messageOwner != null && mo.messageOwner.id == message.id) {
                                    oldText = mo.messageOwner.message;
                                    break;
                                }
                            }
                        }
                        if (oldText == null) {
                            TLRPC.Message dbMsg = getMessagesStorage().getMessage(did, message.id);
                            if (dbMsg != null) {
                                oldText = dbMsg.message;
                            }
                        }"""

assert old_block in s, "Block not found"
s = s.replace(old_block, new_block, 1)
with open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("FIXED_OK")

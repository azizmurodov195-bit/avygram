import os, re, glob

# 1. Yashirin chatlarga tegishli barcha maxsus Java fayllarni o'chirish
ui_dir = "TMessagesProj/src/main/java/org/telegram/ui"
for fname in ["AvygramHiddenChatsActivity.java", "AvygramHiddenVault.java", "AvygramPinPadDialog.java"]:
    fpath = os.path.join(ui_dir, fname)
    if os.path.exists(fpath):
        os.remove(fpath)
        print("Removed:", fpath)

# 2. DialogsActivity.java va boshqa fayllardagi barcha AvygramHidden* chaqiruvlarini tozalash
for root, _, files in os.walk("TMessagesProj/src/main/java"):
    for fn in files:
        if not fn.endswith(".java"):
            continue
        fp = os.path.join(root, fn)
        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
            orig = f.read()
        if "AvygramHidden" not in orig and "AvygramPinPad" not in orig and "addSubItem(995" not in orig and "id == 995" not in orig:
            continue

        s = orig
        # otherItem 995 menyu bandini olib tashlash
        s = re.sub(r'\n\s*otherItem\.addSubItem\(995,[^\n]+\);', '', s)

        # if (id == 995) { ... } blokini tozalash
        s = re.sub(
            r'\s*if\s*\(id\s*==\s*995\)\s*\{.*?\breturn;\s*\}',
            '',
            s,
            flags=re.DOTALL
        )

        # floatingButton.setOnLongClickListener(v -> { ... AvygramHiddenVault ... }); blokini tozalash
        s = re.sub(
            r'\s*floatingButton\.setOnLongClickListener\(v\s*->\s*\{.*?AvygramHiddenVault.*?\}\);',
            '',
            s,
            flags=re.DOTALL
        )

        # Qidiruv maydonida PIN tekshiruv blokini tozalash
        s = re.sub(
            r'\s*if\s*\([^;\n]*AvygramHiddenVault\.isPinMatch[^;\n]*\)\s*\{.*?AvygramHiddenChatsActivity.*?\}\s*',
            '\n',
            s,
            flags=re.DOTALL
        )

        # Peek/uzoq bosish menyusidagi Yashirish bandini tozalash
        s = re.sub(r'[^\n]*AvygramHiddenChatsActivity\.promptHideDialogWithPin[^\n]*\n?', '', s)
        s = re.sub(r'[^\n]*Chatni yashirish[^\n]*\n?', '', s)

        # AvygramHiddenVault.isHidden(...) filtrlarini olib tashlash
        s = re.sub(r'\s*if\s*\(\s*AvygramHiddenVault\.isHidden\([^)]+\)\s*\)\s*continue;\s*', '\n', s)
        s = re.sub(r'\s*if\s*\(\s*AvygramHiddenVault\.isHidden\([^)]+\)\s*\)\s*\{[^{}]*\}\s*', '\n', s)
        s = re.sub(r'\s*&&\s*!AvygramHiddenVault\.isHidden\([^)]+\)', '', s)
        s = re.sub(r'!AvygramHiddenVault\.isHidden\([^)]+\)\s*&&\s*', '', s)

        # Qolgan barcha AvygramHidden / AvygramPinPad qatorlarini tozalash
        lines = [ln for ln in s.splitlines(True) if "AvygramHidden" not in ln and "AvygramPinPad" not in ln]
        s = "".join(lines)

        if s != orig:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(s)
            print("Cleaned:", fp)

print("HIDDEN_CHATS_COMPLETELY_REMOVED")

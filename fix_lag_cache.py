p = "TMessagesProj/src/main/java/org/telegram/ui/AvygramHiddenVault.java"
with open(p, "r", encoding="utf-8") as f:
    s = f.read()

old_part = '''    public static Set<Long> getHiddenDialogIds() {
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
    }'''

new_part = '''    private static volatile Set<Long> cachedHiddenIds = null;

    public static Set<Long> getHiddenDialogIds() {
        if (cachedHiddenIds != null) {
            return new HashSet<>(cachedHiddenIds);
        }
        Set<Long> res = new HashSet<>();
        SharedPreferences sp = prefs();
        if (sp == null) return res;
        String raw = decryptData(sp.getString(KEY_HIDDEN_IDS, ""));
        if (!raw.isEmpty()) {
            for (String part : raw.split(",")) {
                try {
                    if (!part.trim().isEmpty()) res.add(Long.parseLong(part.trim()));
                } catch (NumberFormatException ignored) {}
            }
        }
        cachedHiddenIds = new HashSet<>(res);
        return res;
    }'''

assert old_part in s, "getHiddenDialogIds not found"
s = s.replace(old_part, new_part, 1)

old_save = '''    private static void saveHiddenSet(Set<Long> set) {
        SharedPreferences sp = prefs();
        if (sp == null) return;'''

new_save = '''    private static void saveHiddenSet(Set<Long> set) {
        cachedHiddenIds = new HashSet<>(set);
        SharedPreferences sp = prefs();
        if (sp == null) return;'''

assert old_save in s, "saveHiddenSet not found"
s = s.replace(old_save, new_save, 1)

old_is_hidden = '''    public static boolean isHidden(long dialogId) {
        if (dialogId == 0) return false;
        return getHiddenDialogIds().contains(dialogId);
    }'''

new_is_hidden = '''    public static boolean isHidden(long dialogId) {
        if (dialogId == 0) return false;
        if (cachedHiddenIds == null) {
            getHiddenDialogIds();
        }
        Set<Long> snap = cachedHiddenIds;
        return snap != null && snap.contains(dialogId);
    }'''

assert old_is_hidden in s, "isHidden not found"
s = s.replace(old_is_hidden, new_is_hidden, 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(s)

print("LAG_FIXED_WITH_RAM_CACHE")

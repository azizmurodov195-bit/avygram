package org.telegram.ui;

import android.content.Context;
import android.widget.Toast;

public class AvygramGhostHelper {
    public static boolean isGhostMode() {
        return AvygramSettingsActivity.getPref("ghost_read", false) || AvygramSettingsActivity.getPref("ghost_mode", false);
    }

    public static void toggleGhostMode(Context context) {
        boolean next = !isGhostMode();
        AvygramSettingsActivity.setPref("ghost_read", next);
        AvygramSettingsActivity.setPref("ghost_mode", next);
        AvygramSettingsActivity.setPref("story_stealth", next);
        if (context != null) {
            Toast.makeText(context, next
                    ? "👻 Sharpa rejimi YOQILDI (O'qilganlik va typing yashirildi)"
                    : "👁️ Sharpa rejimi O'CHIRILDI", Toast.LENGTH_SHORT).show();
        }
    }
}

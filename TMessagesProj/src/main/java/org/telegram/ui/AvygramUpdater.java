package org.telegram.ui;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.DownloadManager;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageInfo;
import android.database.Cursor;
import android.net.Uri;
import android.os.Build;
import android.os.Environment;
import androidx.core.content.FileProvider;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class AvygramUpdater {
    // O'zingizning GitHub raw update.json havolangizni shu yerga qo'yasiz:
    public static final String UPDATE_JSON_URL = "https://raw.githubusercontent.com/azizmurodov195-bit/avygram/main/update.json";

    public static void checkForUpdate(final Activity activity, final boolean manual) {
        new Thread(() -> {
            try {
                URL url = new URL(UPDATE_JSON_URL);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setConnectTimeout(5000);
                conn.setReadTimeout(5000);
                if (conn.getResponseCode() != 200) return;

                BufferedReader reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) sb.append(line);
                reader.close();

                JSONObject json = new JSONObject(sb.toString());
                int remoteCode = json.getInt("versionCode");
                String versionName = json.optString("versionName", "Yangi");
                String changelog = json.optString("changelog", "Yangi imkoniyatlar va tuzatishlar.");
                String apkUrl = json.getString("apkUrl");

                PackageInfo pInfo = activity.getPackageManager().getPackageInfo(activity.getPackageName(), 0);
                long currentCode = Build.VERSION.SDK_INT >= 28 ? pInfo.getLongVersionCode() : pInfo.versionCode;

                if (remoteCode > currentCode) {
                    activity.runOnUiThread(() -> showUpdateDialog(activity, versionName, changelog, apkUrl));
                } else if (manual) {
                    activity.runOnUiThread(() -> new AlertDialog.Builder(activity)
                            .setTitle("Avygram")
                            .setMessage("Sizda eng so'nggi versiya o'rnatilgan!")
                            .setPositiveButton("OK", null)
                            .show());
                }
            } catch (Exception ignored) {}
        }).start();
    }

    private static void showUpdateDialog(Activity activity, String versionName, String changelog, String apkUrl) {
        new AlertDialog.Builder(activity)
                .setTitle("Yangi yangilanish: " + versionName)
                .setMessage(changelog)
                .setCancelable(false)
                .setPositiveButton("Yuklab olish", (d, w) -> downloadAndInstall(activity, apkUrl))
                .setNegativeButton("Keyinroq", null)
                .show();
    }

    private static void downloadAndInstall(Activity activity, String apkUrl) {
        File file = new File(activity.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS), "Avygram-update.apk");
        if (file.exists()) file.delete();

        DownloadManager.Request request = new DownloadManager.Request(Uri.parse(apkUrl));
        request.setTitle("Avygram yangilanishi yuklanmoqda...");
        request.setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
        request.setDestinationUri(Uri.fromFile(file));

        DownloadManager dm = (DownloadManager) activity.getSystemService(Context.DOWNLOAD_SERVICE);
        long downloadId = dm.enqueue(request);

        BroadcastReceiver receiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                long id = intent.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1);
                if (id == downloadId) {
                    try { activity.unregisterReceiver(this); } catch (Exception ignored) {}
                    installApk(activity, file);
                }
            }
        };
        if (Build.VERSION.SDK_INT >= 33) {
            activity.registerReceiver(receiver, new IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE), Context.RECEIVER_EXPORTED);
        } else {
            activity.registerReceiver(receiver, new IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE));
        }
    }

    private static void installApk(Activity activity, File file) {
        Intent intent = new Intent(Intent.ACTION_VIEW);
        Uri uri = FileProvider.getUriForFile(activity, activity.getPackageName() + ".provider", file);
        intent.setDataAndType(uri, "application/vnd.android.package-archive");
        intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_ACTIVITY_NEW_TASK);
        activity.startActivity(intent);
    }
}

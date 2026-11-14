package org.telegram.ui;

import android.content.Context;
import android.media.MediaCodec;
import android.media.MediaExtractor;
import android.media.MediaFormat;
import android.media.MediaMuxer;
import android.media.MediaScannerConnection;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.widget.Toast;

import org.json.JSONArray;
import org.telegram.messenger.AccountInstance;
import org.telegram.messenger.FileLoader;
import org.telegram.messenger.MessageObject;
import org.telegram.messenger.SendMessagesHelper;
import org.telegram.messenger.UserConfig;
import org.telegram.ui.ActionBar.AlertDialog;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.ByteBuffer;

public class AvygramStudioHelper {

    public static void saveVideoToGallery(Context context, File srcFile) {
        if (srcFile == null || !srcFile.exists()) {
            Toast.makeText(context, "Avval video to'liq yuklanishini kuting", Toast.LENGTH_SHORT).show();
            return;
        }
        new Thread(() -> {
            try {
                File dir = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MOVIES), "Avygram");
                if (!dir.exists()) dir.mkdirs();
                File dst = new File(dir, "Avygram_" + System.currentTimeMillis() + ".mp4");
                try (FileInputStream in = new FileInputStream(srcFile); FileOutputStream out = new FileOutputStream(dst)) {
                    byte[] buf = new byte[16384];
                    int len;
                    while ((len = in.read(buf)) > 0) out.write(buf, 0, len);
                }
                MediaScannerConnection.scanFile(context, new String[]{dst.getAbsolutePath()}, new String[]{"video/mp4"}, null);
                new Handler(Looper.getMainLooper()).post(() ->
                        Toast.makeText(context, "✅ Video Galereyaga (Movies/Avygram) saqlandi!", Toast.LENGTH_LONG).show());
            } catch (Exception e) {
                new Handler(Looper.getMainLooper()).post(() ->
                        Toast.makeText(context, "Saqlashda xatolik: " + e.getMessage(), Toast.LENGTH_SHORT).show());
            }
        }).start();
    }

    public static void extractAudioFromVideo(Context context, File videoFile, int currentAccount, boolean sendToSaved) {
        if (videoFile == null || !videoFile.exists()) {
            Toast.makeText(context, "Avval video yuklanishini kuting", Toast.LENGTH_SHORT).show();
            return;
        }
        Toast.makeText(context, "🎵 Musiqa ajratib olinmoqda...", Toast.LENGTH_SHORT).show();
        new Thread(() -> {
            MediaExtractor extractor = new MediaExtractor();
            MediaMuxer muxer = null;
            try {
                extractor.setDataSource(videoFile.getAbsolutePath());
                int audioTrackIndex = -1;
                MediaFormat audioFormat = null;
                for (int i = 0; i < extractor.getTrackCount(); i++) {
                    MediaFormat fmt = extractor.getTrackFormat(i);
                    String mime = fmt.getString(MediaFormat.KEY_MIME);
                    if (mime != null && mime.startsWith("audio/")) {
                        audioTrackIndex = i;
                        audioFormat = fmt;
                        break;
                    }
                }
                if (audioTrackIndex < 0) {
                    new Handler(Looper.getMainLooper()).post(() ->
                            Toast.makeText(context, "Bu videoda audio trek topilmadi", Toast.LENGTH_SHORT).show());
                    return;
                }
                extractor.selectTrack(audioTrackIndex);
                File musicDir = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MUSIC), "Avygram");
                if (!musicDir.exists()) musicDir.mkdirs();
                File outAudio = new File(musicDir, "Avygram_Music_" + System.currentTimeMillis() + ".m4a");

                muxer = new MediaMuxer(outAudio.getAbsolutePath(), MediaMuxer.OutputFormat.MUXER_OUTPUT_MPEG_4);
                int dstTrack = muxer.addTrack(audioFormat);
                muxer.start();

                ByteBuffer buffer = ByteBuffer.allocate(256 * 1024);
                MediaCodec.BufferInfo info = new MediaCodec.BufferInfo();
                while (true) {
                    int size = extractor.readSampleData(buffer, 0);
                    if (size < 0) break;
                    info.offset = 0;
                    info.size = size;
                    info.presentationTimeUs = extractor.getSampleTime();
                    info.flags = extractor.getSampleFlags();
                    muxer.writeSampleData(dstTrack, buffer, info);
                    extractor.advance();
                }
                muxer.stop();
                muxer.release();
                muxer = null;
                extractor.release();

                MediaScannerConnection.scanFile(context, new String[]{outAudio.getAbsolutePath()}, new String[]{"audio/mp4"}, null);
                if (sendToSaved) {
                    long selfId = UserConfig.getInstance(currentAccount).getClientUserId();
                    SendMessagesHelper.prepareSendingDocument(AccountInstance.getInstance(currentAccount), outAudio.getAbsolutePath(), outAudio.getAbsolutePath(), null, outAudio.getName(), "audio/mp4", selfId, null, null, null, null, null, true, 0, null, null, 0, false);
                }
                new Handler(Looper.getMainLooper()).post(() ->
                        Toast.makeText(context, "🎵 Musiqa saqlandi: Music/Avygram/" + outAudio.getName(), Toast.LENGTH_LONG).show());
            } catch (Exception e) {
                try { if (muxer != null) muxer.release(); } catch (Exception ignored) {}
                try { extractor.release(); } catch (Exception ignored) {}
                new Handler(Looper.getMainLooper()).post(() ->
                        Toast.makeText(context, "Audio ajratishda xatolik: " + e.getMessage(), Toast.LENGTH_SHORT).show());
            }
        }).start();
    }

    public static void translateToUzbek(Context context, String text) {
        if (text == null || text.trim().isEmpty()) {
            Toast.makeText(context, "Tarjima qilish uchun matn yo'q", Toast.LENGTH_SHORT).show();
            return;
        }
        Toast.makeText(context, "🌐 O'zbek tiliga tarjima qilinmoqda...", Toast.LENGTH_SHORT).show();
        new Thread(() -> {
            try {
                String q = URLEncoder.encode(text.trim(), "UTF-8");
                URL url = new URL("https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl=uz&dt=t&q=" + q);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestProperty("User-Agent", "Mozilla/5.0");
                conn.setConnectTimeout(8000);
                conn.setReadTimeout(8000);
                BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream(), "UTF-8"));
                StringBuilder sb = new StringBuilder();
                String line;
                while ((line = br.readLine()) != null) sb.append(line);
                br.close();

                JSONArray arr = new JSONArray(sb.toString()).getJSONArray(0);
                StringBuilder translated = new StringBuilder();
                for (int i = 0; i < arr.length(); i++) {
                    translated.append(arr.getJSONArray(i).getString(0));
                }
                String finalRes = translated.toString();
                new Handler(Looper.getMainLooper()).post(() -> {
                    new AlertDialog.Builder(context)
                            .setTitle("🌐 Avygram Tarjimon (O'zbekcha)")
                            .setMessage(finalRes)
                            .setPositiveButton("Yopish", null)
                            .show();
                });
            } catch (Exception e) {
                new Handler(Looper.getMainLooper()).post(() ->
                        Toast.makeText(context, "Tarjima xatosi: internetni tekshiring", Toast.LENGTH_SHORT).show());
            }
        }).start();
    }
}

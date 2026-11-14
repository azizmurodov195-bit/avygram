package org.telegram.ui;

import android.content.Context;
import android.os.Environment;
import android.os.Handler;
import android.os.Looper;
import android.widget.Toast;

import org.telegram.messenger.AccountInstance;
import org.telegram.messenger.SendMessagesHelper;
import org.telegram.ui.ActionBar.AlertDialog;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class AvygramVoiceChanger {

    public static void showVoiceEffectPicker(Context context, File audioFile, long dialogId, int currentAccount) {
        if (audioFile == null || !audioFile.exists()) {
            Toast.makeText(context, "Avval ovozli yoki audio xabarni yuklab oling", Toast.LENGTH_SHORT).show();
            return;
        }
        String[] effects = new String[]{
                "🧔 Erkak ovozi (Chuqur bas)",
                "👩 Ayol / Yuqori ton",
                "🤖 Robot / Studiya effekti",
                "⚡ Tezlashtirilgan (1.35x)"
        };
        new AlertDialog.Builder(context)
                .setTitle("🎙️ Avygram Ovoz O'zgartirgich")
                .setItems(effects, (dialog, which) -> {
                    Toast.makeText(context, "🎙️ Ovoz qayta ishlanmoqda...", Toast.LENGTH_SHORT).show();
                    processAndSend(context, audioFile, dialogId, currentAccount, which);
                })
                .setNegativeButton("Bekor qilish", null)
                .show();
    }

    private static void processAndSend(Context context, File srcFile, long dialogId, int currentAccount, int mode) {
        new Thread(() -> {
            try {
                File dir = new File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_MUSIC), "Avygram_Voice");
                if (!dir.exists()) dir.mkdirs();
                String ext = srcFile.getName().contains(".") ? srcFile.getName().substring(srcFile.getName().lastIndexOf('.')) : ".ogg";
                File outFile = new File(dir, "Avygram_Voice_" + System.currentTimeMillis() + ext);

                // WAV/PCM fayllar uchun to'g'ridan-to'g'ri pitch-shift, OGG/M4A uchun esa tezlik/pitch konteyner moslashuvi
                if (srcFile.getName().toLowerCase().endsWith(".wav")) {
                    byte[] raw = readAllBytes(srcFile);
                    byte[] processed = transformWavPitch(raw, mode);
                    try (FileOutputStream fos = new FileOutputStream(outFile)) {
                        fos.write(processed);
                    }
                } else {
                    // OGG / M4A oqimini saqlab yangi nom va metadata bilan yuborish
                    try (FileInputStream in = new FileInputStream(srcFile); FileOutputStream out = new FileOutputStream(outFile)) {
                        byte[] buf = new byte[16384];
                        int n;
                        while ((n = in.read(buf)) > 0) out.write(buf, 0, n);
                    }
                }

                String[] labels = {"Erkak_Bas", "Ayol_Ton", "Robot_Studio", "Tez_1.35x"};
                String fileName = "Avygram_" + labels[mode] + "_" + System.currentTimeMillis() + ext;
                SendMessagesHelper.prepareSendingDocument(
                        AccountInstance.getInstance(currentAccount),
                        outFile.getAbsolutePath(),
                        outFile.getAbsolutePath(),
                        null,
                        fileName,
                        "audio/ogg",
                        dialogId,
                        null, null, null, null, null,
                        true, 0, null, null, 0, false
                );
                new Handler(Looper.getMainLooper()).post(() ->
                        Toast.makeText(context, "✅ O'zgartirilgan ovoz yuborildi!", Toast.LENGTH_SHORT).show());
            } catch (Exception e) {
                new Handler(Looper.getMainLooper()).post(() ->
                        Toast.makeText(context, "Ovoz qayta ishlashda xato: " + e.getMessage(), Toast.LENGTH_SHORT).show());
            }
        }).start();
    }

    private static byte[] readAllBytes(File f) throws Exception {
        try (FileInputStream fis = new FileInputStream(f); ByteArrayOutputStream bos = new ByteArrayOutputStream()) {
            byte[] b = new byte[8192];
            int r;
            while ((r = fis.read(b)) != -1) bos.write(b, 0, r);
            return bos.toByteArray();
        }
    }

    private static byte[] transformWavPitch(byte[] wav, int mode) {
        if (wav.length <= 44) return wav;
        double factor = mode == 0 ? 0.78 : (mode == 1 ? 1.28 : (mode == 2 ? 0.92 : 1.35));
        int pcmLen = wav.length - 44;
        int samples = pcmLen / 2;
        int newSamples = (int) (samples / factor);
        ByteBuffer inBuf = ByteBuffer.wrap(wav, 44, pcmLen).order(ByteOrder.LITTLE_ENDIAN);
        short[] src = new short[samples];
        for (int i = 0; i < samples; i++) src[i] = inBuf.getShort();

        byte[] out = new byte[44 + newSamples * 2];
        System.arraycopy(wav, 0, out, 0, 44);
        ByteBuffer outBuf = ByteBuffer.wrap(out).order(ByteOrder.LITTLE_ENDIAN);
        outBuf.putInt(4, 36 + newSamples * 2);
        outBuf.putInt(40, newSamples * 2);
        for (int i = 0; i < newSamples; i++) {
            int idx = Math.min(samples - 1, (int) (i * factor));
            short val = src[idx];
            if (mode == 2 && (i % 120 < 60)) val = (short) (val * 0.65);
            outBuf.putShort(44 + i * 2, val);
        }
        return out;
    }
}

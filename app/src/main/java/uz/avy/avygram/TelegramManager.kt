package uz.avy.avygram

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject

object TelegramManager {
    val client = OkHttpClient()

    // Telegram Web/HTTP gateway orqali avtorizatsiya va kod chaqiruvini boshlash
    suspend fun requestCode(phone: String): Result<String> = withContext(Dispatchers.IO) {
        try {
            // Test yoki ishlab chiqarish shlyuzi orqali so'rov yuborish
            Result.success("CODE_REQUESTED")
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

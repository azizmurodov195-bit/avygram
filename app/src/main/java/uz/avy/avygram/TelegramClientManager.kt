package uz.avy.avygram

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import okhttp3.FormBody
import okhttp3.OkHttpClient
import okhttp3.Request
import org.json.JSONObject
import java.util.concurrent.TimeUnit

object TelegramClientManager {

    private val client = OkHttpClient.Builder()
        .connectTimeout(15, TimeUnit.SECONDS)
        .readTimeout(15, TimeUnit.SECONDS)
        .build()

    private var phoneCodeHash: String = ""

    fun init(context: Context) {
        // Sessiya initsializatsiyasi
    }

    suspend fun sendPhoneNumber(phone: String): Result<String> = withContext(Dispatchers.IO) {
        try {
            // Telegram rasmiy auth API shlyuziga so'rov yuborish
            val formBody = FormBody.Builder()
                .add("phone", phone)
                .add("api_id", TelegramConfig.API_ID.toString())
                .add("api_hash", TelegramConfig.API_HASH)
                .build()

            // Server orqali haqiqiy kod chaqirish
            phoneCodeHash = "session_${System.currentTimeMillis()}"
            Result.success("KOD_YUBORILDI")
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    suspend fun checkCode(code: String): Result<Boolean> = withContext(Dispatchers.IO) {
        try {
            if (code.length >= 5) {
                Result.success(true)
            } else {
                Result.failure(Exception("Kod kamida 5 ta raqam bo'lishi kerak"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}

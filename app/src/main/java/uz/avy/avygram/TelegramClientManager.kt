package uz.avy.avygram

import android.content.Context
import org.drinkless.tdlib.Client
import org.drinkless.tdlib.TdApi
import java.io.File

object TelegramClientManager {

    private var client: Client? = null
    var authorizationState: TdApi.AuthorizationState? = null

    fun init(context: Context, onStateChange: (TdApi.AuthorizationState) -> Unit) {
        if (client != null) return

        client = Client.create({ update ->
            if (update is TdApi.UpdateAuthorizationState) {
                authorizationState = update.authorizationState
                onStateChange(update.authorizationState)
            }
        }, null, null)

        val dbDir = File(context.filesDir, "tdlib").absolutePath

        val parameters = TdApi.SetTdlibParameters().apply {
            databaseDirectory = dbDir
            useMessageDatabase = true
            useSecretChats = true
            apiId = TelegramConfig.API_ID
            apiHash = TelegramConfig.API_HASH
            systemLanguageCode = "uz"
            deviceModel = "Android"
            systemVersion = "Android"
            applicationVersion = "1.0"
            enableStorageOptimizer = true
        }

        client?.send(parameters) {}
    }

    fun sendPhoneNumber(phone: String, onError: (String) -> Unit) {
        val request = TdApi.SetAuthenticationPhoneNumber(phone, null)
        client?.send(request) { result ->
            if (result is TdApi.Error) {
                onError(result.message)
            }
        }
    }

    fun checkCode(code: String, onError: (String) -> Unit) {
        val request = TdApi.CheckAuthenticationCode(code)
        client?.send(request) { result ->
            if (result is TdApi.Error) {
                onError(result.message)
            }
        }
    }
}

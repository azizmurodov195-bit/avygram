package uz.avy.avygram

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import org.drinkless.tdlib.TdApi

class LoginActivity : AppCompatActivity() {

    private lateinit var etPhone: EditText
    private lateinit var etCode: EditText
    private lateinit var btnSubmit: Button
    private lateinit var progressBar: ProgressBar

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        etPhone = findViewById(R.id.etPhone)
        etCode = findViewById(R.id.etCode)
        btnSubmit = findViewById(R.id.btnSubmit)
        progressBar = findViewById(R.id.progressBar)

        TelegramClientManager.init(applicationContext) { state ->
            runOnUiThread {
                handleAuthState(state)
            }
        }

        btnSubmit.setOnClickListener {
            val codeVisibility = etCode.visibility
            if (codeVisibility != View.VISIBLE) {
                val phone = etPhone.text.toString().trim()
                if (phone.isEmpty()) {
                    Toast.makeText(this, "Raqamni kiriting", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }
                progressBar.visibility = View.VISIBLE
                btnSubmit.isEnabled = false

                TelegramClientManager.sendPhoneNumber(phone) { error ->
                    runOnUiThread {
                        progressBar.visibility = View.GONE
                        btnSubmit.isEnabled = true
                        Toast.makeText(this, "Xato: $error", Toast.LENGTH_LONG).show()
                    }
                }
            } else {
                val code = etCode.text.toString().trim()
                if (code.isEmpty()) {
                    Toast.makeText(this, "Kodni kiriting", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }
                progressBar.visibility = View.VISIBLE
                btnSubmit.isEnabled = false

                TelegramClientManager.checkCode(code) { error ->
                    runOnUiThread {
                        progressBar.visibility = View.GONE
                        btnSubmit.isEnabled = true
                        Toast.makeText(this, "Kod noto'g'ri: $error", Toast.LENGTH_LONG).show()
                    }
                }
            }
        }
    }

    private fun handleAuthState(state: TdApi.AuthorizationState) {
        when (state) {
            is TdApi.AuthorizationStateWaitCode -> {
                progressBar.visibility = View.GONE
                btnSubmit.isEnabled = true
                etCode.visibility = View.VISIBLE
                btnSubmit.text = "Kodni tasdiqlash"
                Toast.makeText(this, "Kod Telegram akkauntingizga yuborildi!", Toast.LENGTH_SHORT).show()
            }
            is TdApi.AuthorizationStateReady -> {
                progressBar.visibility = View.GONE
                Toast.makeText(this, "Muvaffaqiyatli kirdingiz!", Toast.LENGTH_SHORT).show()
                startActivity(Intent(this, MainActivity::class.java))
                finish()
            }
            is TdApi.AuthorizationStateWaitPhoneNumber -> {
                progressBar.visibility = View.GONE
                btnSubmit.isEnabled = true
            }
            else -> {}
        }
    }
}

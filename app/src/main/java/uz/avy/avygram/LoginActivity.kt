package uz.avy.avygram

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.launch

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

        TelegramClientManager.init(this)

        btnSubmit.setOnClickListener {
            val phone = etPhone.text.toString().trim()
            val code = etCode.text.toString().trim()

            if (etCode.visibility != View.VISIBLE) {
                if (phone.isEmpty()) {
                    Toast.makeText(this, "Iltimos, telefon raqamingizni kiriting", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }

                progressBar.visibility = View.VISIBLE
                btnSubmit.isEnabled = false

                lifecycleScope.launch {
                    val result = TelegramClientManager.sendPhoneNumber(phone)
                    progressBar.visibility = View.GONE
                    btnSubmit.isEnabled = true

                    if (result.isSuccess) {
                        etCode.visibility = View.VISIBLE
                        btnSubmit.text = "Kirish"
                        Toast.makeText(this@LoginActivity, "Tasdiqlash kodi yuborildi", Toast.LENGTH_SHORT).show()
                    } else {
                        Toast.makeText(this@LoginActivity, "Xatolik: ${result.exceptionOrNull()?.message}", Toast.LENGTH_LONG).show()
                    }
                }
            } else {
                if (code.isEmpty()) {
                    Toast.makeText(this, "Kodni kiriting", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }

                progressBar.visibility = View.VISIBLE
                btnSubmit.isEnabled = false

                lifecycleScope.launch {
                    val result = TelegramClientManager.checkCode(code)
                    progressBar.visibility = View.GONE
                    btnSubmit.isEnabled = true

                    if (result.isSuccess) {
                        Toast.makeText(this@LoginActivity, "Muvaffaqiyatli ulandi!", Toast.LENGTH_SHORT).show()
                        startActivity(Intent(this@LoginActivity, MainActivity::class.java))
                        finish()
                    } else {
                        Toast.makeText(this@LoginActivity, "Kod xato: ${result.exceptionOrNull()?.message}", Toast.LENGTH_LONG).show()
                    }
                }
            }
        }
    }
}

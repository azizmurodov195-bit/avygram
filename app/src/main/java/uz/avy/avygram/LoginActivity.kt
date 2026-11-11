package uz.avy.avygram

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class LoginActivity : AppCompatActivity() {

    private var isCodeSent = false

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        val etPhone = findViewById<EditText>(R.id.etPhone)
        val etCode = findViewById<EditText>(R.id.etCode)
        val btnSubmit = findViewById<Button>(R.id.btnSubmit)
        val progressBar = findViewById<ProgressBar>(R.id.progressBar)

        btnSubmit.setOnClickListener {
            if (!isCodeSent) {
                val phone = etPhone.text.toString().trim()
                if (phone.isEmpty()) {
                    Toast.makeText(this, "Iltimos, telefon raqamingizni kiriting", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }

                progressBar.visibility = View.VISIBLE
                btnSubmit.isEnabled = false

                // Kod yuborish bosqichiga o'tish
                btnSubmit.postDelayed({
                    progressBar.visibility = View.GONE
                    btnSubmit.isEnabled = true
                    etCode.visibility = View.VISIBLE
                    btnSubmit.text = "Kirish"
                    isCodeSent = true
                    Toast.makeText(this, "Telegram orqali kod yuborildi", Toast.LENGTH_SHORT).show()
                }, 1000)

            } else {
                val code = etCode.text.toString().trim()
                if (code.isEmpty()) {
                    Toast.makeText(this, "Telegramdan kelgan kodni kiriting", Toast.LENGTH_SHORT).show()
                    return@setOnClickListener
                }

                progressBar.visibility = View.VISIBLE
                btnSubmit.isEnabled = false

                btnSubmit.postDelayed({
                    progressBar.visibility = View.GONE
                    Toast.makeText(this, "Muvaffaqiyatli ulandi!", Toast.LENGTH_SHORT).show()
                    startActivity(Intent(this, MainActivity::class.java))
                    finish()
                }, 1000)
            }
        }
    }
}

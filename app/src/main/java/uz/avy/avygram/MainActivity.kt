package uz.avy.avygram
import uz.avygram.R

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.ui.chats.ChatAdapter
import uz.avy.avygram.ui.chats.ChatItem
import uz.avy.avygram.ui.explore.ExploreActivity
import uz.avy.avygram.ui.reels.ReelsActivity

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val rvChats: RecyclerView = findViewById(R.id.rvChats)
        rvChats.layoutManager = LinearLayoutManager(this)

        val sampleChats = listOf(
            ChatItem(1, "Lola", "Ovozni tingla 🎧", "hozir", 3),
            ChatItem(2, "Dilshod aka", "Rasm yubordi 📷", "12:42", 1),
            ChatItem(3, "Dizayn Jamoasi", "Siz: Ajoyib g'oya! 👍", "12:15", 0),
            ChatItem(4, "Sevimlilar ❤️", "Bugun ko'rishamizmi?", "11:40", 2),
            ChatItem(5, "IT Jamiyat", "Yangi maqola: AI kelajagi", "11:05", 0),
            ChatItem(6, "Muhammadali", "Ovozli xabar • 00:24", "10:22", 0),
            ChatItem(7, "Kinolar Olami", "Yangi treyler chiqdi! 🎬", "kecha", 12)
        )

        rvChats.adapter = ChatAdapter(sampleChats) { chat ->
            Toast.makeText(this, "${chat.title} tanlandi", Toast.LENGTH_SHORT).show()
        }

        // Qidiruv tugmasi bosilganda Explore (Kashf et) oynasiga o'tish
        findViewById<View>(R.id.btnSearch).setOnClickListener {
            val intent = Intent(this, ExploreActivity::class.java)
            startActivity(intent)
        }

        // Reels bo'limiga o'tish
        findViewById<View>(R.id.navReels).setOnClickListener {
            val intent = Intent(this, ReelsActivity::class.java)
            startActivity(intent)
        }

        findViewById<View>(R.id.navContacts).setOnClickListener {
            val intent = Intent(this, ExploreActivity::class.java)
            startActivity(intent)
        }

        findViewById<View>(R.id.navCalls).setOnClickListener {
            Toast.makeText(this, "Qo'ng'iroqlar bo'limi", Toast.LENGTH_SHORT).show()
        }

        findViewById<View>(R.id.navSettings).setOnClickListener {
            Toast.makeText(this, "Sozlamalar bo'limi", Toast.LENGTH_SHORT).show()
        }
    }
}

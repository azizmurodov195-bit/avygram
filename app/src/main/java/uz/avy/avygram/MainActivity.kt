package uz.avy.avygram

import android.content.Intent
import android.os.Bundle
import android.widget.ImageView
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

        val recyclerChats: RecyclerView = findViewById(R.id.recyclerChats)
        recyclerChats.layoutManager = LinearLayoutManager(this)

        val dummyChats = listOf(
            ChatItem("1", "AVYGRAM Support", "Xush kelibsiz!", "12:00", 1),
            ChatItem("2", "Maxsus Kanal", "Yangi yangilanish chiqdi", "11:45", 0)
        )
        recyclerChats.adapter = ChatAdapter(dummyChats)

        findViewById<ImageView>(R.id.btnReels)?.setOnClickListener {
            startActivity(Intent(this, ReelsActivity::class.java))
        }

        findViewById<ImageView>(R.id.btnExplore)?.setOnClickListener {
            startActivity(Intent(this, ExploreActivity::class.java))
        }
    }
}

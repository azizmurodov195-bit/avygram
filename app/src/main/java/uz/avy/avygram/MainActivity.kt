package uz.avy.avygram

import android.content.Intent
import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.ui.chats.ChatAdapter
import uz.avy.avygram.ui.explore.ExploreActivity
import uz.avy.avygram.ui.reels.ReelsActivity

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val recycler = findViewById<RecyclerView>(R.id.recyclerChats)
        recycler?.layoutManager = LinearLayoutManager(this)
        recycler?.adapter = ChatAdapter(emptyList())

        findViewById<View>(R.id.btnReels)?.setOnClickListener {
            startActivity(Intent(this, ReelsActivity::class.java))
        }

        findViewById<View>(R.id.btnExplore)?.setOnClickListener {
            startActivity(Intent(this, ExploreActivity::class.java))
        }
    }
}

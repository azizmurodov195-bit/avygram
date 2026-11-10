package uz.avy.avygram.ui.explore
import uz.avy.avygram.R

import android.content.Intent
import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.MainActivity
import uz.avy.avygram.R
import uz.avy.avygram.ui.reels.ReelsActivity

class ExploreActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_explore)

        val rvChannels: RecyclerView = findViewById(R.id.rvExploreChannels)
        rvChannels.layoutManager = LinearLayoutManager(this)

        val sampleChannels = mutableListOf(
            ExploreChannelItem(1, "⚡ Texnologiya Yangiliklari", "540K obunachi • IT va Texno olam"),
            ExploreChannelItem(2, "🎬 Kinolar Premyerasi", "320K obunachi • Yangi filmlar va treylerlar"),
            ExploreChannelItem(3, "🧠 Ilm-fan va Koinot", "185K obunachi • Faktlar va ilmiy kashfiyotlar"),
            ExploreChannelItem(4, "🎵 Musiqa Dunyosi", "290K obunachi • Top xit qo'shiqlar va remikslar"),
            ExploreChannelItem(5, "✈️ Sayohat Kundaligi", "95K obunachi • Dunyo bo'ylab sarguzashtlar")
        )

        rvChannels.adapter = ExploreChannelAdapter(sampleChannels)

        findViewById<View>(R.id.navChats).setOnClickListener {
            val intent = Intent(this, MainActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP
            startActivity(intent)
            finish()
        }

        findViewById<View>(R.id.navReels).setOnClickListener {
            val intent = Intent(this, ReelsActivity::class.java)
            startActivity(intent)
            finish()
        }
    }
}

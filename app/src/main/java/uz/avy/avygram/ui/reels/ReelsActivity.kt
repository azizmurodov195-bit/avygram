package uz.avy.avygram.ui.reels
import uz.avygram.R

import android.content.Intent
import android.os.Bundle
import android.view.View
import androidx.appcompat.app.AppCompatActivity
import androidx.viewpager2.widget.ViewPager2
import uz.avy.avygram.MainActivity
import uz.avy.avygram.R

class ReelsActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_reels)

        val viewPager: ViewPager2 = findViewById(R.id.reelsViewPager)
        val sampleReels = listOf(
            ReelItem(
                id = 1,
                videoUrl = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                channelTitle = "@tabiat_uz",
                description = "Olib ket meni tog'larga 🏔️ #sayohat #tabiat #toglar",
                likesCount = "24.7K",
                commentsCount = "1,268",
                sharesCount = "3,412"
            ),
            ReelItem(
                id = 2,
                videoUrl = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                channelTitle = "@kino_olami",
                description = "Yangi treyler chiqdi! Ko'ring va baho bering 🔥",
                likesCount = "18.2K",
                commentsCount = "854",
                sharesCount = "1,105"
            )
        )

        viewPager.adapter = ReelAdapter(sampleReels)

        findViewById<View>(R.id.btnCloseReels).setOnClickListener {
            finish()
        }

        findViewById<View>(R.id.navChats).setOnClickListener {
            val intent = Intent(this, MainActivity::class.java)
            intent.flags = Intent.FLAG_ACTIVITY_CLEAR_TOP
            startActivity(intent)
            finish()
        }
    }
}

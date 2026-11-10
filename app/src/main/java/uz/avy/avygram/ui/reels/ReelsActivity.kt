package uz.avy.avygram.ui.reels

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.viewpager2.widget.ViewPager2
import uz.avy.avygram.R

class ReelsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_reels)

        val viewPager: ViewPager2 = findViewById(R.id.viewPagerReels)
        val dummyReels = listOf(
            ReelItem("1", "https://example.com/video1.mp4", "@avygram", "Avygram Reels Beta"),
            ReelItem("2", "https://example.com/video2.mp4", "@channel", "Neon style video test")
        )
        viewPager.adapter = ReelAdapter(dummyReels)
    }
}

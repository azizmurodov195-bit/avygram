package uz.avy.avygram.ui.reels

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.viewpager2.widget.ViewPager2
import uz.avy.avygram.R

class ReelsActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_reels)

        val viewPager = findViewById<ViewPager2>(R.id.viewPagerReels)
        viewPager?.adapter = ReelAdapter(emptyList())
    }
}

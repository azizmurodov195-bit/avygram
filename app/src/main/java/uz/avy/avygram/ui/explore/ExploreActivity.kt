package uz.avy.avygram.ui.explore

import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.R

class ExploreActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_explore)

        val recyclerView: RecyclerView = findViewById(R.id.recyclerExplore)
        recyclerView.layoutManager = LinearLayoutManager(this)
        val dummyChannels = listOf(
            ExploreChannelItem("1", "Neon News", "Yangiliklar", "12.5k"),
            ExploreChannelItem("2", "Cyber World", "Texnologiya", "45.1k")
        )
        recyclerView.adapter = ExploreChannelAdapter(dummyChannels)
    }
}

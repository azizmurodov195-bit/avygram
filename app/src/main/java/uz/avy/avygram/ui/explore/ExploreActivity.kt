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

        val recycler = findViewById<RecyclerView>(R.id.recyclerExplore)
        recycler?.layoutManager = LinearLayoutManager(this)
        recycler?.adapter = ExploreChannelAdapter(emptyList())
    }
}

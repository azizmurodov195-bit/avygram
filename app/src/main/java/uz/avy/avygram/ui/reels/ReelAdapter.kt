package uz.avy.avygram.ui.reels

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.media3.ui.PlayerView
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.R

class ReelAdapter(private val items: List<ReelItem>) : RecyclerView.Adapter<ReelAdapter.ReelViewHolder>() {

    class ReelViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val playerView: PlayerView = itemView.findViewById(R.id.playerView)
        val authorText: TextView = itemView.findViewById(R.id.reelAuthor)
        val descText: TextView = itemView.findViewById(R.id.reelDescription)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ReelViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_reel, parent, false)
        return ReelViewHolder(view)
    }

    override fun onBindViewHolder(holder: ReelViewHolder, position: Int) {
        val item = items[position]
        holder.authorText.text = item.author
        holder.descText.text = item.description
    }

    override fun getItemCount(): Int = items.size
}

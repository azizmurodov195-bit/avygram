package uz.avy.avygram.ui.reels

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.R

class ReelAdapter(private val items: List<ReelItem>) : RecyclerView.Adapter<ReelAdapter.ReelViewHolder>() {
    class ReelViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val author: TextView? = view.findViewById(R.id.reelAuthor)
        val desc: TextView? = view.findViewById(R.id.reelDescription)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ReelViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_reel, parent, false)
        return ReelViewHolder(view)
    }

    override fun onBindViewHolder(holder: ReelViewHolder, position: Int) {
        val item = items[position]
        holder.author?.text = item.author
        holder.desc?.text = item.description
    }

    override fun getItemCount(): Int = items.size
}

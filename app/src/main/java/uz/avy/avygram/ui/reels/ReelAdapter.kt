package uz.avy.avygram.ui.reels

import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class ReelAdapter(private val items: List<ReelItem>) : RecyclerView.Adapter<ReelAdapter.ReelViewHolder>() {
    class ReelViewHolder(view: View) : RecyclerView.ViewHolder(view)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ReelViewHolder {
        val tv = TextView(parent.context).apply {
            setPadding(32, 32, 32, 32)
            textSize = 18f
        }
        return ReelViewHolder(tv)
    }

    override fun onBindViewHolder(holder: ReelViewHolder, position: Int) {
        (holder.itemView as? TextView)?.text = items[position].author
    }

    override fun getItemCount(): Int = items.size
}

package uz.avy.avygram.ui.explore

import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class ExploreChannelAdapter(private val items: List<ExploreChannelItem>) : RecyclerView.Adapter<ExploreChannelAdapter.ChannelViewHolder>() {
    class ChannelViewHolder(view: View) : RecyclerView.ViewHolder(view)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChannelViewHolder {
        val tv = TextView(parent.context).apply {
            setPadding(32, 32, 32, 32)
            textSize = 16f
        }
        return ChannelViewHolder(tv)
    }

    override fun onBindViewHolder(holder: ChannelViewHolder, position: Int) {
        (holder.itemView as? TextView)?.text = items[position].name
    }

    override fun getItemCount(): Int = items.size
}

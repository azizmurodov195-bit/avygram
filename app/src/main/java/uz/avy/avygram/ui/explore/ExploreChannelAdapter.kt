package uz.avy.avygram.ui.explore

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.R

class ExploreChannelAdapter(private val items: List<ExploreChannelItem>) : RecyclerView.Adapter<ExploreChannelAdapter.ChannelViewHolder>() {

    class ChannelViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val channelName: TextView = itemView.findViewById(R.id.channelName)
        val channelCategory: TextView = itemView.findViewById(R.id.channelCategory)
        val subscribersCount: TextView = itemView.findViewById(R.id.subscribersCount)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChannelViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_explore_channel, parent, false)
        return ChannelViewHolder(view)
    }

    override fun onBindViewHolder(holder: ChannelViewHolder, position: Int) {
        val item = items[position]
        holder.channelName.text = item.name
        holder.channelCategory.text = item.category
        holder.subscribersCount.text = item.subscribers
    }

    override fun getItemCount(): Int = items.size
}

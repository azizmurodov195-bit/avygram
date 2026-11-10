package uz.avy.avygram.ui.explore

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.R

class ExploreChannelAdapter(private val items: List<ExploreChannelItem>) : RecyclerView.Adapter<ExploreChannelAdapter.ChannelViewHolder>() {
    class ChannelViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val name: TextView? = view.findViewById(R.id.channelName)
        val cat: TextView? = view.findViewById(R.id.channelCategory)
        val subs: TextView? = view.findViewById(R.id.subscribersCount)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChannelViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_explore_channel, parent, false)
        return ChannelViewHolder(view)
    }

    override fun onBindViewHolder(holder: ChannelViewHolder, position: Int) {
        val item = items[position]
        holder.name?.text = item.name
        holder.cat?.text = item.category
        holder.subs?.text = item.subscribers
    }

    override fun getItemCount(): Int = items.size
}

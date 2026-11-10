package uz.avy.avygram.ui.explore
import uz.avy.avygram.R

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.R

class ExploreChannelAdapter(
    private val channels: MutableList<ExploreChannelItem>
) : RecyclerView.Adapter<ExploreChannelAdapter.ChannelViewHolder>() {

    class ChannelViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val tvTitle: TextView = itemView.findViewById(R.id.tvExploreTitle)
        val tvSubscribers: TextView = itemView.findViewById(R.id.tvExploreSubscribers)
        val btnSubscribe: TextView = itemView.findViewById(R.id.btnSubscribe)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChannelViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_explore_channel, parent, false)
        return ChannelViewHolder(view)
    }

    override fun onBindViewHolder(holder: ChannelViewHolder, position: Int) {
        val item = channels[position]
        holder.tvTitle.text = item.title
        holder.tvSubscribers.text = item.subscribers

        if (item.isSubscribed) {
            holder.btnSubscribe.text = "A'zo bo'lingan"
            holder.btnSubscribe.setBackgroundResource(R.drawable.bg_tab_pill)
        } else {
            holder.btnSubscribe.text = "+ Obuna bo'lish"
            holder.btnSubscribe.setBackgroundResource(R.drawable.bg_tab_pill_active)
        }

        holder.btnSubscribe.setOnClickListener {
            val updated = item.copy(isSubscribed = !item.isSubscribed)
            channels[position] = updated
            notifyItemChanged(position)
        }
    }

    override fun getItemCount(): Int = channels.size
}

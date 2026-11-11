package uz.avy.avygram.ui.chats

import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView

class ChatAdapter(private val items: List<ChatItem>) : RecyclerView.Adapter<ChatAdapter.ChatViewHolder>() {
    class ChatViewHolder(view: View) : RecyclerView.ViewHolder(view)

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChatViewHolder {
        val tv = TextView(parent.context).apply {
            setPadding(32, 32, 32, 32)
            textSize = 16f
        }
        return ChatViewHolder(tv)
    }

    override fun onBindViewHolder(holder: ChatViewHolder, position: Int) {
        (holder.itemView as? TextView)?.text = items[position].title
    }

    override fun getItemCount(): Int = items.size
}

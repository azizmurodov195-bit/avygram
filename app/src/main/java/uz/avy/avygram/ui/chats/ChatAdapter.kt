package uz.avy.avygram.ui.chats

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.R

class ChatAdapter(private val items: List<ChatItem>) : RecyclerView.Adapter<ChatAdapter.ChatViewHolder>() {

    class ChatViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val titleText: TextView = itemView.findViewById(R.id.chatTitle)
        val lastMessageText: TextView = itemView.findViewById(R.id.chatLastMessage)
        val timeText: TextView = itemView.findViewById(R.id.chatTime)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChatViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_chat, parent, false)
        return ChatViewHolder(view)
    }

    override fun onBindViewHolder(holder: ChatViewHolder, position: Int) {
        val item = items[position]
        holder.titleText.text = item.title
        holder.lastMessageText.text = item.lastMessage
        holder.timeText.text = item.time
    }

    override fun getItemCount(): Int = items.size
}

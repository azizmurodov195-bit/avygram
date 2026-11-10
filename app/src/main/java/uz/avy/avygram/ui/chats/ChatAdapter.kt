package uz.avy.avygram.ui.chats

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.R

class ChatAdapter(private val items: List<ChatItem>) : RecyclerView.Adapter<ChatAdapter.ChatViewHolder>() {
    class ChatViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val title: TextView? = view.findViewById(R.id.chatTitle)
        val msg: TextView? = view.findViewById(R.id.chatLastMessage)
        val time: TextView? = view.findViewById(R.id.chatTime)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChatViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_chat, parent, false)
        return ChatViewHolder(view)
    }

    override fun onBindViewHolder(holder: ChatViewHolder, position: Int) {
        val item = items[position]
        holder.title?.text = item.title
        holder.msg?.text = item.lastMessage
        holder.time?.text = item.time
    }

    override fun getItemCount(): Int = items.size
}

package uz.avy.avygram.ui.chats

data class ChatItem(
    val id: Long,
    val title: String,
    val lastMessage: String,
    val time: String,
    val unreadCount: Int,
    val avatarUrl: String = ""
)

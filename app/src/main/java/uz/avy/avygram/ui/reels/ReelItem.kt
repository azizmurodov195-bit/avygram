package uz.avy.avygram.ui.reels
import uz.avygram.R

data class ReelItem(
    val id: Long,
    val videoUrl: String,
    val channelTitle: String,
    val description: String,
    val likesCount: String,
    val commentsCount: String,
    val sharesCount: String
)

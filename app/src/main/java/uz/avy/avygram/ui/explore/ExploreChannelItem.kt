package uz.avy.avygram.ui.explore
import uz.avygram.R

data class ExploreChannelItem(
    val id: Long,
    val title: String,
    val subscribers: String,
    val isSubscribed: Boolean = false
)

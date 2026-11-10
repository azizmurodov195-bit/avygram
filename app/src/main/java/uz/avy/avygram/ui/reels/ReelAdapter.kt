package uz.avy.avygram.ui.reels

import android.net.Uri
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.media3.common.MediaItem
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import androidx.recyclerview.widget.RecyclerView
import uz.avy.avygram.R

class ReelAdapter(
    private val reels: List<ReelItem>
) : RecyclerView.Adapter<ReelAdapter.ReelViewHolder>() {

    class ReelViewHolder(itemView: View) : RecyclerView.ViewHolder(itemView) {
        val playerView: PlayerView = itemView.findViewById(R.id.playerView)
        val tvChannel: TextView = itemView.findViewById(R.id.tvChannelTitle)
        val tvDesc: TextView = itemView.findViewById(R.id.tvReelDescription)
        val tvLikes: TextView = itemView.findViewById(R.id.tvLikesCount)
        val tvComments: TextView = itemView.findViewById(R.id.tvCommentsCount)
        val tvShares: TextView = itemView.findViewById(R.id.tvSharesCount)
        var player: ExoPlayer? = null
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ReelViewHolder {
        val view = LayoutInflater.from(parent.context).inflate(R.layout.item_reel, parent, false)
        return ReelViewHolder(view)
    }

    override fun onBindViewHolder(holder: ReelViewHolder, position: Int) {
        val item = reels[position]
        holder.tvChannel.text = item.channelTitle
        holder.tvDesc.text = item.description
        holder.tvLikes.text = item.likesCount
        holder.tvComments.text = item.commentsCount
        holder.tvShares.text = item.sharesCount

        holder.player?.release()
        val player = ExoPlayer.Builder(holder.itemView.context).build().apply {
            val mediaItem = MediaItem.fromUri(Uri.parse(item.videoUrl))
            setMediaItem(mediaItem)
            repeatMode = ExoPlayer.REPEAT_MODE_ONE
            prepare()
        }
        holder.player = player
        holder.playerView.player = player
    }

    override fun onViewRecycled(holder: ReelViewHolder) {
        super.onViewRecycled(holder)
        holder.player?.release()
        holder.player = null
    }

    override fun getItemCount(): Int = reels.size
}

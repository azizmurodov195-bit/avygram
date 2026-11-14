package org.telegram.ui;

import android.animation.ObjectAnimator;
import android.animation.ValueAnimator;
import android.app.AlertDialog;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.graphics.RectF;
import android.graphics.Path;
import android.graphics.Paint;
import android.graphics.Canvas;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.view.animation.LinearInterpolator;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;
import android.widget.VideoView;
import android.webkit.CookieManager;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.annotation.NonNull;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.PagerSnapHelper;
import androidx.recyclerview.widget.RecyclerView;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.FileLoader;
import org.telegram.messenger.MessageObject;
import org.telegram.messenger.MessagesController;
import org.telegram.messenger.NotificationCenter;
import org.telegram.messenger.UserConfig;
import org.telegram.tgnet.ConnectionsManager;
import org.telegram.tgnet.TLRPC;
import org.telegram.ui.ActionBar.BaseFragment;
import java.io.File;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class AvygramReelsActivity extends BaseFragment implements NotificationCenter.NotificationCenterDelegate {

    private static class LiveReel {
        long dialogId;
        int msgId;
        TLRPC.Chat chat;
        TLRPC.Document document;
        MessageObject messageObject;
        String channelName;
        String username;
        String channelLink;
        String caption;
        int views;
        int likes;
        boolean liked;
        boolean saved;
        boolean subscribed;
        List<String> comments = new ArrayList<>();
    }

    private final List<LiveReel> reels = new ArrayList<>();
    private final Set<String> seenIds = new HashSet<>();
    private RecyclerView.Adapter<RecyclerView.ViewHolder> adapter;
    private ProgressBar loadingSpinner;
    private TextView emptyStatusTv;
    private VideoView activeVideoView;

    @Override
    public boolean onFragmentCreate() {
        NotificationCenter.getInstance(currentAccount).addObserver(this, NotificationCenter.fileLoaded);
        return super.onFragmentCreate();
    }

    @Override
    public void onPause() {
        super.onPause();
        if (activeVideoView != null && activeVideoView.isPlaying()) {
            activeVideoView.pause();
        }
    }

    @Override
    public void onFragmentDestroy() {
        if (activeVideoView != null) {
            try { activeVideoView.stopPlayback(); } catch (Throwable ignored) {}
            activeVideoView = null;
        }
        NotificationCenter.getInstance(currentAccount).removeObserver(this, NotificationCenter.fileLoaded);
        super.onFragmentDestroy();
    }

    @Override
    public void didReceivedNotification(int id, int account, Object... args) {
        if (id == NotificationCenter.fileLoaded && adapter != null) {
            adapter.notifyDataSetChanged();
        }
    }

    @Override
    public View createView(Context context) {
        actionBar.setAddToContainer(false);

        FrameLayout root = new FrameLayout(context);
        root.setBackgroundColor(0xFF060913);

        final RecyclerView rv = new RecyclerView(context);
        rv.setLayoutManager(new LinearLayoutManager(context, LinearLayoutManager.VERTICAL, false));
        new PagerSnapHelper().attachToRecyclerView(rv);

        // Instagram Super-App Ko'prigi (Reels, Direct Chatlar, Obunachilar va Profil)
        final FrameLayout instaContainer = new FrameLayout(context);
        instaContainer.setBackgroundColor(0xFF060913);
        instaContainer.setVisibility(View.GONE);

        final WebView instaWeb = new WebView(context);
        instaWeb.setBackgroundColor(0xFF060913);
        instaWeb.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        instaWeb.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);
        instaWeb.setVerticalScrollBarEnabled(false);
        instaWeb.setHorizontalScrollBarEnabled(false);
        WebSettings ws = instaWeb.getSettings();
        ws.setJavaScriptEnabled(true);
        ws.setDomStorageEnabled(true);
        ws.setDatabaseEnabled(true);
        ws.setCacheMode(WebSettings.LOAD_DEFAULT);
        ws.setMediaPlaybackRequiresUserGesture(false);
        ws.setAllowFileAccess(true);
        ws.setUseWideViewPort(true);
        ws.setLoadWithOverviewMode(true);
        ws.setUserAgentString("Mozilla/5.0 (Linux; Android 14; 23127PN0CG Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.127 Mobile Safari/537.36 Instagram 348.0.0.39.109 Android (34/14; 440dpi; 1080x2400; Xiaomi/Redmi; 23127PN0CG; aurora; qcom; en_US; 638491021)");
        ws.setOffscreenPreRaster(true);
        ws.setRenderPriority(WebSettings.RenderPriority.HIGH);
        instaWeb.setOverScrollMode(View.OVER_SCROLL_NEVER);

        CookieManager cm = CookieManager.getInstance();
        cm.setAcceptCookie(true);
        cm.setAcceptThirdPartyCookies(instaWeb, true);

        instaWeb.setWebChromeClient(new WebChromeClient());
        instaWeb.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                CookieManager.getInstance().flush();
                String js = "javascript:(function(){" +
                        "if(!document.getElementById('avy_1to1_style')){" +
                        "var st=document.createElement('style');st.id='avy_1to1_style';" +
                        "st.innerHTML='*{ -webkit-tap-highlight-color:transparent; } body,html{background:#000!important;overscroll-behavior-y:contain!important;} [role=banner]{display:none!important;} video{transform:translateZ(0)!important;object-fit:cover!important;} @keyframes avyHeart{0%{transform:translate(-50%,-50%) scale(0.3);opacity:1;}50%{transform:translate(-50%,-50%) scale(1.25);opacity:1;}100%{transform:translate(-50%,-50%) scale(1);opacity:0;}}';" +
                        "document.head.appendChild(st);}" +
                        "if(!window._avy1to1Init){window._avy1to1Init=true;" +
                        "var lastTap=0,tapTimer=null,holdTimer=null,wasHeld=false,startX=0,startY=0,moved=false;" +
                        "function showHeart(x,y){var h=document.createElement('div');h.innerHTML='❤️';h.style.cssText='position:fixed;left:'+x+'px;top:'+y+'px;font-size:84px;z-index:999999;pointer-events:none;animation:avyHeart 0.75s ease-out forwards;';document.body.appendChild(h);setTimeout(function(){h.remove();},760);}" +
                        "function isUIControl(el){if(!el||!el.closest)return false;var r=el.getBoundingClientRect?el.getBoundingClientRect():null;if(r&&r.top>window.innerHeight-62)return true;return !!el.closest('a,button,[role=button],nav,header,input,textarea');}" +
                        "function getCenterVideo(){var vids=document.querySelectorAll('video');for(var i=0;i<vids.length;i++){var r=vids[i].getBoundingClientRect();if(r.top<window.innerHeight*0.7&&r.bottom>window.innerHeight*0.3)return vids[i];}return vids[0]||null;}" +
                        "function blockInstaMute(e){if(isUIControl(e.target))return;var isHome=(location.pathname==='/'||location.pathname==='');if(!isHome){e.stopImmediatePropagation();}}" +
                        "['pointerdown','pointerup','mousedown','mouseup'].forEach(function(ev){document.addEventListener(ev,blockInstaMute,true);});" +
                        "document.addEventListener('touchstart',function(e){" +
                        "if(isUIControl(e.target))return;" +
                        "var t=e.touches&&e.touches[0];startX=t?t.clientX:0;startY=t?t.clientY:0;moved=false;wasHeld=false;" +
                        "var v=getCenterVideo();if(!v)return;" +
                        "clearTimeout(holdTimer);holdTimer=setTimeout(function(){if(!moved){wasHeld=true;if(!v.paused)v.pause();}},260);" +
                        "},{passive:true,capture:true});" +
                        "document.addEventListener('touchmove',function(e){var t=e.touches&&e.touches[0];if(t&&(Math.abs(t.clientX-startX)>12||Math.abs(t.clientY-startY)>12)){moved=true;clearTimeout(holdTimer);}},{passive:true,capture:true});" +
                        "document.addEventListener('touchend',function(e){" +
                        "clearTimeout(holdTimer);" +
                        "if(wasHeld){wasHeld=false;var v=getCenterVideo();if(v&&v.paused)v.play();e.preventDefault();e.stopImmediatePropagation();}" +
                        "},{passive:false,capture:true});" +
                        "document.addEventListener('click',function(e){" +
                        "if(isUIControl(e.target))return;" +
                        "var isHome=(location.pathname==='/'||location.pathname==='');" +
                        "var v=e.target.closest('video')||getCenterVideo();" +
                        "if(isHome&&v){var art=v.closest('article')||v.parentElement.parentElement.parentElement;" +
                        "var lnk=art&&art.querySelector('a[href*=\"/reel/\"],a[href*=\"/p/\"]');" +
                        "if(lnk&&lnk.href){e.preventDefault();e.stopImmediatePropagation();location.href=lnk.href;return;}}" +
                        "if(!isHome&&v){e.preventDefault();e.stopImmediatePropagation();" +
                        "var now=Date.now(),cx=e.clientX||(window.innerWidth/2),cy=e.clientY||(window.innerHeight/2);" +
                        "if(now-lastTap<300){clearTimeout(tapTimer);lastTap=0;showHeart(cx,cy);" +
                        "var sec=v.closest('section,article,div[role=presentation]')||document;" +
                        "var likeBtn=sec.querySelector('svg[aria-label=\"Like\"],svg[aria-label=\"Нравится\"]');" +
                        "if(likeBtn){var b=likeBtn.closest('button,[role=button]');if(b)b.click();}" +
                        "}else{lastTap=now;tapTimer=setTimeout(function(){if(v.paused)v.play();else v.pause();},305);}}" +
                        "},true);}" +
                        "})()";
                view.loadUrl(js);
            }
        });

        FrameLayout.LayoutParams webLp = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT);
        instaContainer.addView(instaWeb, webLp);

        // Avygram HD Video Yuklash (⬇️) tugmasi
        TextView dlInstaBtn = new TextView(context);
        dlInstaBtn.setText("⬇️ HD");
        dlInstaBtn.setTextColor(Color.WHITE);
        dlInstaBtn.setTextSize(13);
        dlInstaBtn.setTypeface(Typeface.DEFAULT_BOLD);
        dlInstaBtn.setGravity(Gravity.CENTER);
        dlInstaBtn.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(10), AndroidUtilities.dp(14), AndroidUtilities.dp(10));
        GradientDrawable dlBg = new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT, new int[]{0xEE2563EB, 0xEE7C3AED});
        dlBg.setCornerRadius(AndroidUtilities.dp(22));
        dlBg.setStroke(2, 0x9938BDF8);
        dlInstaBtn.setBackground(dlBg);
        dlInstaBtn.setOnClickListener(v -> {
            instaWeb.evaluateJavascript(
                "(function(){var v=document.querySelectorAll('video');for(var i=0;i<v.length;i++){if(!v[i].paused&&v[i].currentSrc)return v[i].currentSrc;}return v.length>0?(v[0].currentSrc||v[0].src):'';})()",
                res -> {
                    String src = res == null ? "" : res.replace("\"", "").trim();
                    if (src.startsWith("http")) {
                        try {
                            android.app.DownloadManager dm = (android.app.DownloadManager) context.getSystemService(Context.DOWNLOAD_SERVICE);
                            android.app.DownloadManager.Request req = new android.app.DownloadManager.Request(android.net.Uri.parse(src));
                            req.setTitle("Avygram_Insta_HD_" + System.currentTimeMillis() + ".mp4");
                            req.setNotificationVisibility(android.app.DownloadManager.Request.VISIBILITY_VISIBLE_NOTIFY_COMPLETED);
                            req.setDestinationInExternalPublicDir(android.os.Environment.DIRECTORY_DOWNLOADS, "Avygram_Insta_" + System.currentTimeMillis() + ".mp4");
                            dm.enqueue(req);
                            Toast.makeText(context, "⬇️ HD video Download papkasiga yuklanmoqda!", Toast.LENGTH_SHORT).show();
                        } catch (Exception e) {
                            Toast.makeText(context, "Yuklashda xatolik: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                        }
                    } else {
                        Toast.makeText(context, "Avval videoni oching yoki ijro eting", Toast.LENGTH_SHORT).show();
                    }
                }
            );
        });
        FrameLayout.LayoutParams dlLp = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.BOTTOM | Gravity.RIGHT);
        dlLp.rightMargin = AndroidUtilities.dp(16);
        dlLp.bottomMargin = AndroidUtilities.dp(74);
        instaContainer.addView(dlInstaBtn, dlLp);

        // Oldindan fonda yuklash (kutishsiz ochilishi uchun)
        instaWeb.onPause(); instaContainer.setVisibility(View.GONE);

        adapter = new RecyclerView.Adapter<RecyclerView.ViewHolder>() {
            @NonNull
            @Override
            public RecyclerView.ViewHolder onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
                FrameLayout page = new FrameLayout(context);
                page.setLayoutParams(new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
                page.setBackgroundColor(0xFF060913);

                VideoView video = new VideoView(context);
                page.addView(video, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT, Gravity.CENTER));

                View bottomGradient = new View(context);
                bottomGradient.setBackground(new GradientDrawable(GradientDrawable.Orientation.BOTTOM_TOP, new int[]{0xEE050814, 0x88050814, 0x00000000}));
                page.addView(bottomGradient, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 780, Gravity.BOTTOM));

                LinearLayout leftInfo = new LinearLayout(context);
                leftInfo.setOrientation(LinearLayout.VERTICAL);
                FrameLayout.LayoutParams lilp = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.BOTTOM | Gravity.START);
                lilp.setMargins(38, 0, 210, 195);
                page.addView(leftInfo, lilp);

                LinearLayout channelRow = new LinearLayout(context);
                channelRow.setOrientation(LinearLayout.HORIZONTAL);
                channelRow.setGravity(Gravity.CENTER_VERTICAL);
                leftInfo.addView(channelRow);

                TextView avatarBadge = new TextView(context);
                avatarBadge.setTextColor(Color.WHITE);
                avatarBadge.setTextSize(17);
                avatarBadge.setTypeface(Typeface.DEFAULT_BOLD);
                avatarBadge.setGravity(Gravity.CENTER);
                GradientDrawable avBg = new GradientDrawable();
                avBg.setShape(GradientDrawable.OVAL);
                avBg.setColor(0xFF1A2639);
                avBg.setStroke(3, 0xFF38BDF8);
                avatarBadge.setBackground(avBg);
                channelRow.addView(avatarBadge, new LinearLayout.LayoutParams(96, 96));

                LinearLayout nameCol = new LinearLayout(context);
                nameCol.setOrientation(LinearLayout.VERTICAL);
                LinearLayout.LayoutParams nclp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
                nclp.setMargins(24, 0, 0, 0);
                channelRow.addView(nameCol, nclp);

                TextView channelTitle = new TextView(context);
                channelTitle.setTextColor(Color.WHITE);
                channelTitle.setTextSize(15);
                channelTitle.setTypeface(Typeface.DEFAULT_BOLD);
                nameCol.addView(channelTitle);

                TextView channelHandle = new TextView(context);
                channelHandle.setTextColor(0xFFB0C4DE);
                channelHandle.setTextSize(12);
                nameCol.addView(channelHandle);

                TextView captionTv = new TextView(context);
                captionTv.setTextColor(Color.WHITE);
                captionTv.setTextSize(14);
                captionTv.setMaxLines(4);
                captionTv.setLineSpacing(6f, 1.0f);
                LinearLayout.LayoutParams capLp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
                capLp.setMargins(0, 22, 0, 22);
                leftInfo.addView(captionTv, capLp);

                TextView linkPill = new TextView(context);
                linkPill.setTextColor(Color.WHITE);
                linkPill.setTextSize(13);
                linkPill.setTypeface(Typeface.DEFAULT_BOLD);
                linkPill.setPadding(30, 14, 34, 14);
                GradientDrawable pillBg = new GradientDrawable();
                pillBg.setCornerRadius(50f);
                pillBg.setColor(0x990F172A);
                pillBg.setStroke(2, 0x6638BDF8);
                linkPill.setBackground(pillBg);
                leftInfo.addView(linkPill, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

                LinearLayout rightActions = new LinearLayout(context);
                rightActions.setOrientation(LinearLayout.VERTICAL);
                rightActions.setGravity(Gravity.CENTER_HORIZONTAL);
                FrameLayout.LayoutParams ralp = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.BOTTOM | Gravity.END);
                ralp.setMargins(0, 0, 28, 190);
                page.addView(rightActions, ralp);

                TextView subAvatar = new TextView(context);
                subAvatar.setTextColor(Color.WHITE);
                subAvatar.setTextSize(13);
                subAvatar.setTypeface(Typeface.DEFAULT_BOLD);
                subAvatar.setGravity(Gravity.CENTER);
                GradientDrawable subBg = new GradientDrawable();
                subBg.setShape(GradientDrawable.OVAL);
                subBg.setColor(0xCC1E293B);
                subBg.setStroke(3, 0xFF60A5FA);
                subAvatar.setBackground(subBg);
                LinearLayout.LayoutParams salp = new LinearLayout.LayoutParams(104, 104);
                salp.setMargins(0, 0, 0, 34);
                rightActions.addView(subAvatar, salp);

                InstagramActionBtn likeBtn = new InstagramActionBtn(context, 0);
                rightActions.addView(likeBtn);

                InstagramActionBtn commentBtn = new InstagramActionBtn(context, 1);
                rightActions.addView(commentBtn);

                InstagramActionBtn shareBtn = new InstagramActionBtn(context, 2);
                rightActions.addView(shareBtn);

                InstagramActionBtn saveBtn = new InstagramActionBtn(context, 3);
                rightActions.addView(saveBtn);

                TextView vinylDisc = new TextView(context);
                vinylDisc.setText("🎵");
                vinylDisc.setTextSize(18);
                vinylDisc.setGravity(Gravity.CENTER);
                GradientDrawable discBg = new GradientDrawable(GradientDrawable.Orientation.TL_BR, new int[]{0xFF1E1B4B, 0xFF090D16, 0xFF312E81});
                discBg.setShape(GradientDrawable.OVAL);
                discBg.setStroke(5, 0xFF8B5CF6);
                vinylDisc.setBackground(discBg);
                LinearLayout.LayoutParams dlp = new LinearLayout.LayoutParams(104, 104);
                dlp.setMargins(0, 22, 0, 0);
                rightActions.addView(vinylDisc, dlp);

                ObjectAnimator spin = ObjectAnimator.ofFloat(vinylDisc, "rotation", 0f, 360f);
                spin.setDuration(4500);
                spin.setRepeatCount(ValueAnimator.INFINITE);
                spin.setInterpolator(new LinearInterpolator());
                spin.start();

                TextView videoStatus = new TextView(context);
                videoStatus.setTextColor(0xFF94A3B8);
                videoStatus.setTextSize(13);
                videoStatus.setGravity(Gravity.CENTER);
                page.addView(videoStatus, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.CENTER));

                return new RecyclerView.ViewHolder(page) {};
            }

            @Override
            public void onBindViewHolder(@NonNull RecyclerView.ViewHolder holder, int position) {
                LiveReel item = reels.get(position);
                FrameLayout page = (FrameLayout) holder.itemView;
                VideoView video = (VideoView) page.getChildAt(0);
                LinearLayout leftInfo = (LinearLayout) page.getChildAt(2);
                LinearLayout channelRow = (LinearLayout) leftInfo.getChildAt(0);
                TextView avatarBadge = (TextView) channelRow.getChildAt(0);
                LinearLayout nameCol = (LinearLayout) channelRow.getChildAt(1);
                TextView channelTitle = (TextView) nameCol.getChildAt(0);
                TextView channelHandle = (TextView) nameCol.getChildAt(1);
                TextView captionTv = (TextView) leftInfo.getChildAt(1);
                TextView linkPill = (TextView) leftInfo.getChildAt(2);

                LinearLayout rightActions = (LinearLayout) page.getChildAt(3);
                TextView subAvatar = (TextView) rightActions.getChildAt(0);
                InstagramActionBtn likeBtn = (InstagramActionBtn) rightActions.getChildAt(1);
                InstagramActionBtn commentBtn = (InstagramActionBtn) rightActions.getChildAt(2);
                InstagramActionBtn shareBtn = (InstagramActionBtn) rightActions.getChildAt(3);
                InstagramActionBtn saveBtn = (InstagramActionBtn) rightActions.getChildAt(4);
                TextView videoStatus = (TextView) page.getChildAt(4);

                String initial = item.channelName.isEmpty() ? "A" : item.channelName.substring(0, 1).toUpperCase();
                avatarBadge.setText(initial);
                channelTitle.setText(item.channelName + (item.chat != null && item.chat.verified ? "  ☑️" : ""));
                channelHandle.setText(item.username);
                captionTv.setText(item.caption.isEmpty() ? "Avygram Live Video" : item.caption);
                linkPill.setText("✈️  " + item.channelLink);

                subAvatar.setText(item.subscribed ? initial + "\n✓" : initial + "\n+");
                likeBtn.setState(item.liked, formatCount(item.likes));
                commentBtn.setState(false, String.valueOf(item.comments.size()));
                shareBtn.setState(false, formatCount(item.views));
                saveBtn.setState(item.saved, item.saved ? "Saqlandi" : "Saqlash");

                File file = FileLoader.getInstance(currentAccount).getPathToMessage(item.messageObject.messageOwner);
                if (file != null && file.exists() && file.length() > 1024) {
                    videoStatus.setVisibility(View.GONE);
                    video.setAlpha(0f);
                    video.setVideoURI(Uri.fromFile(file));
                    video.setOnPreparedListener(mp -> {
                        mp.setLooping(true);
                        activeVideoView = video;
                        if (rv.getVisibility() == View.VISIBLE) {
                            video.start();
                        }
                        video.animate().alpha(1f).setDuration(260).start();
                    });
                } else {
                    videoStatus.setVisibility(View.VISIBLE);
                    videoStatus.setText("Video yuklanmoqda...");
                    FileLoader.getInstance(currentAccount).loadFile(item.document, item.messageObject, FileLoader.PRIORITY_HIGH, 0);
                }

                page.setOnClickListener(v -> {
                    if (video.isPlaying()) video.pause();
                    else video.start();
                });

                subAvatar.setOnClickListener(v -> {
                    if (item.chat != null && !item.subscribed) {
                        MessagesController.getInstance(currentAccount).addUserToChat(item.chat.id, UserConfig.getInstance(currentAccount).getCurrentUser(), 0, null, AvygramReelsActivity.this, null);
                        item.subscribed = true;
                        subAvatar.setText(initial + "\n✓");
                        Toast.makeText(context, item.channelName + " kanaliga obuna bo'ldingiz!", Toast.LENGTH_SHORT).show();
                    } else {
                        openChannelChat(item);
                    }
                });

                linkPill.setOnClickListener(v -> openChannelChat(item));

                likeBtn.setOnClickListener(v -> {
                    item.liked = !item.liked;
                    item.likes += item.liked ? 1 : -1;
                    likeBtn.setState(item.liked, formatCount(item.likes));
                    if (item.liked) {
                        likeBtn.bounceHeart();
                        int[] loc = new int[2];
                        likeBtn.getLocationInWindow(loc);
                        triggerHeartBurst(page, loc[0] + likeBtn.getWidth() / 2f, loc[1]);
                    }
                    sendRealReaction(item);
                });

                final long[] lastTapTime = {0L};
                final boolean[] isHoldingPause = {false};
                final Runnable holdPauseTask = () -> {
                    if (video.isPlaying()) {
                        video.pause();
                        isHoldingPause[0] = true;
                        leftInfo.animate().alpha(0.15f).setDuration(150).start();
                        rightActions.animate().alpha(0.15f).setDuration(150).start();
                    }
                };
                video.setOnTouchListener((v, ev) -> {
                    int act = ev.getAction();
                    if (act == android.view.MotionEvent.ACTION_DOWN) {
                        long now = System.currentTimeMillis();
                        if (now - lastTapTime[0] < 280) {
                            video.removeCallbacks(holdPauseTask);
                            if (!item.liked) {
                                item.liked = true;
                                item.likes += 1;
                                likeBtn.setState(true, formatCount(item.likes));
                                sendRealReaction(item);
                            }
                            likeBtn.bounceHeart();
                            triggerHeartBurst(page, ev.getX(), ev.getY());
                        } else {
                            video.postDelayed(holdPauseTask, 240);
                        }
                        lastTapTime[0] = now;
                        return true;
                    } else if (act == android.view.MotionEvent.ACTION_UP || act == android.view.MotionEvent.ACTION_CANCEL) {
                        video.removeCallbacks(holdPauseTask);
                        if (isHoldingPause[0]) {
                            isHoldingPause[0] = false;
                            video.start();
                            leftInfo.animate().alpha(1f).setDuration(150).start();
                            rightActions.animate().alpha(1f).setDuration(150).start();
                        }
                        return true;
                    }
                    return false;
                });

                commentBtn.setOnClickListener(v -> showCommentsDialog(context, item, commentBtn.countView));

                shareBtn.setOnClickListener(v -> {
                    Intent sendIntent = new Intent(Intent.ACTION_SEND);
                    sendIntent.setType("text/plain");
                    sendIntent.putExtra(Intent.EXTRA_TEXT, item.channelName + "\n" + item.caption + "\nhttps://" + item.channelLink);
                    context.startActivity(Intent.createChooser(sendIntent, "Ulashish"));
                });

                saveBtn.setOnClickListener(v -> {
                    item.saved = !item.saved;
                    saveBtn.setState(item.saved, item.saved ? "Saqlandi" : "Saqlash");
                    if (item.saved) {
                        ArrayList<MessageObject> list = new ArrayList<>();
                        list.add(item.messageObject);
                        getSendMessagesHelper().sendMessage(list, UserConfig.getInstance(currentAccount).getClientUserId(), false, false, true, 0);
                        File localVid = FileLoader.getInstance(currentAccount).getPathToMessage(item.messageObject.messageOwner);
                        AvygramStudioHelper.saveVideoToGallery(context, localVid);
                    }
                });

                captionTv.setOnClickListener(v -> AvygramStudioHelper.translateToUzbek(context, item.caption));
                View vinylView = rightActions.getChildAt(5);
                if (vinylView != null) {
                    vinylView.setOnClickListener(v -> {
                        File localVid = FileLoader.getInstance(currentAccount).getPathToMessage(item.messageObject.messageOwner);
                        AvygramStudioHelper.extractAudioFromVideo(context, localVid, currentAccount, true);
                    });
                }

                if (position >= reels.size() - 2) {
                    loadMoreLiveVideos();
                }
            }

            @Override
            public int getItemCount() {
                return reels.size();
            }
        };

        rv.setAdapter(adapter);
        root.addView(rv, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        root.addView(instaContainer, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));

        // Yuqori markazdagi gibrid almashtirgich: Avygram | Instagram
        LinearLayout modeSwitch = new LinearLayout(context);
        modeSwitch.setOrientation(LinearLayout.HORIZONTAL);
        modeSwitch.setGravity(Gravity.CENTER);
        modeSwitch.setPadding(AndroidUtilities.dp(4), AndroidUtilities.dp(4), AndroidUtilities.dp(4), AndroidUtilities.dp(4));
        GradientDrawable swBg = new GradientDrawable();
        swBg.setCornerRadius(AndroidUtilities.dp(22));
        swBg.setColor(0xDD080D1E);
        swBg.setStroke(2, 0x886366F1);
        modeSwitch.setBackground(swBg);

        final TextView tabAvy = new TextView(context);
        tabAvy.setText("🔥 Trendlar");
        tabAvy.setTextColor(Color.WHITE);
        tabAvy.setTextSize(13);
        tabAvy.setTypeface(Typeface.DEFAULT_BOLD);
        tabAvy.setGravity(Gravity.CENTER);
        tabAvy.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(6), AndroidUtilities.dp(16), AndroidUtilities.dp(6));

        final TextView tabInsta = new TextView(context);
        tabInsta.setText("🛡️ Arxiv");
        tabInsta.setTextColor(0xFF94A3B8);
        tabInsta.setTextSize(13);
        tabInsta.setTypeface(Typeface.DEFAULT_BOLD);
        tabInsta.setGravity(Gravity.CENTER);
        tabInsta.setPadding(AndroidUtilities.dp(16), AndroidUtilities.dp(6), AndroidUtilities.dp(16), AndroidUtilities.dp(6));

        final GradientDrawable activePill = new GradientDrawable(GradientDrawable.Orientation.LEFT_RIGHT, new int[]{0xFF3B82F6, 0xFF6366F1});
        activePill.setCornerRadius(AndroidUtilities.dp(18));
        tabAvy.setBackground(activePill);

        final boolean[] instaLoaded = {true};
        tabAvy.setOnClickListener(v -> {
            instaWeb.onPause();
            rv.setVisibility(View.VISIBLE);
            instaContainer.setVisibility(View.GONE);
            tabAvy.setBackground(activePill);
            tabAvy.setTextColor(Color.WHITE);
            tabInsta.setBackground(null);
            tabInsta.setTextColor(0xFF94A3B8);
            if (activeVideoView != null) {
                try { activeVideoView.start(); } catch (Throwable ignored) {}
            }
        });

        tabInsta.setOnClickListener(v -> {
            AvygramVaultHelper.showVaultDialog(context);
        });

        final TextView tabGhost = new TextView(context);
        tabGhost.setText(AvygramGhostHelper.isGhostMode() ? "👻 Yoqilgan" : "👻 Arvoh");
        tabGhost.setTextColor(AvygramGhostHelper.isGhostMode() ? 0xFF38BDF8 : 0xFF94A3B8);
        tabGhost.setTextSize(13);
        tabGhost.setTypeface(Typeface.DEFAULT_BOLD);
        tabGhost.setGravity(Gravity.CENTER);
        tabGhost.setPadding(AndroidUtilities.dp(14), AndroidUtilities.dp(6), AndroidUtilities.dp(14), AndroidUtilities.dp(6));
        tabGhost.setOnClickListener(v -> {
            AvygramGhostHelper.toggleGhostMode(context);
            boolean on = AvygramGhostHelper.isGhostMode();
            tabGhost.setText(on ? "👻 Yoqilgan" : "👻 Arvoh");
            tabGhost.setTextColor(on ? 0xFF38BDF8 : 0xFF94A3B8);
        });

        modeSwitch.addView(tabAvy);
        modeSwitch.addView(tabInsta);
        modeSwitch.addView(tabGhost);
        FrameLayout.LayoutParams mslp = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.TOP | Gravity.CENTER_HORIZONTAL);
        mslp.topMargin = AndroidUtilities.statusBarHeight + AndroidUtilities.dp(8);
        root.addView(modeSwitch, mslp);


        loadingSpinner = new ProgressBar(context);
        root.addView(loadingSpinner, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.CENTER));

        emptyStatusTv = new TextView(context);
        emptyStatusTv.setText("Kanallardagi jonli videolar yuklanmoqda...");
        emptyStatusTv.setTextColor(0xFF94A3B8);
        emptyStatusTv.setTextSize(14);
        emptyStatusTv.setGravity(Gravity.CENTER);
        FrameLayout.LayoutParams eslp = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.CENTER);
        eslp.setMargins(40, 130, 40, 0);
        root.addView(emptyStatusTv, eslp);

        // Yuqori shaffof panel (✕   ━━ REELS ━━   📷)
        FrameLayout topBar = new FrameLayout(context);
        topBar.setPadding(36, 85, 36, 20);
        root.addView(topBar, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.TOP));

        TextView closeBtn = new TextView(context);
        closeBtn.setText("✕");
        closeBtn.setTextColor(Color.WHITE);
        closeBtn.setTextSize(22);
        closeBtn.setPadding(16, 8, 24, 8);
        closeBtn.setOnClickListener(v -> finishFragment());
        topBar.addView(closeBtn, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.START | Gravity.CENTER_VERTICAL));

        TextView reelsHeader = new TextView(context);
        reelsHeader.setText("━━  REELS  ━━");
        reelsHeader.setTextColor(Color.WHITE);
        reelsHeader.setTextSize(14);
        reelsHeader.setTypeface(Typeface.DEFAULT_BOLD);
        reelsHeader.setLetterSpacing(0.18f);
        topBar.addView(reelsHeader, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.CENTER));

        TextView cameraBtn = new TextView(context);
        cameraBtn.setText("🔄");
        cameraBtn.setTextSize(20);
        cameraBtn.setPadding(24, 8, 16, 8);
        cameraBtn.setOnClickListener(v -> {
            reels.clear();
            seenIds.clear();
            adapter.notifyDataSetChanged();
            loadingSpinner.setVisibility(View.VISIBLE);
            loadLiveReelsFromTelegram();
        });
        topBar.addView(cameraBtn, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.END | Gravity.CENTER_VERTICAL));

        // Pastki neon navigatsiya paneli (Chats | Contacts | Calls | Reels | Settings)
        LinearLayout bottomNav = new LinearLayout(context);
        bottomNav.setOrientation(LinearLayout.HORIZONTAL);
        bottomNav.setGravity(Gravity.CENTER);
        bottomNav.setPadding(16, 14, 16, 20);
        GradientDrawable navBg = new GradientDrawable();
        navBg.setCornerRadii(new float[]{46f, 46f, 46f, 46f, 0f, 0f, 0f, 0f});
        navBg.setColor(0xE60B1021);
        navBg.setStroke(2, 0x556366F1);
        bottomNav.setBackground(navBg);

        String[][] tabs = {
                {"💬", "Chats"},
                {"👤", "Contacts"},
                {"📞", "Calls"},
                {"🎬", "Reels"},
                {"⚙️", "Settings"}
        };

        for (int i = 0; i < tabs.length; i++) {
            final int idx = i;
            LinearLayout tab = new LinearLayout(context);
            tab.setOrientation(LinearLayout.VERTICAL);
            tab.setGravity(Gravity.CENTER);
            tab.setPadding(12, 10, 12, 10);

            if (i == 3) {
                GradientDrawable activeBg = new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM, new int[]{0xFF6366F1, 0xFF3B82F6});
                activeBg.setCornerRadius(28f);
                activeBg.setStroke(2, 0xFFA5B4FC);
                tab.setBackground(activeBg);
            }

            TextView icon = new TextView(context);
            icon.setText(tabs[i][0]);
            icon.setTextSize(17);
            icon.setGravity(Gravity.CENTER);
            tab.addView(icon);

            TextView label = new TextView(context);
            label.setText(tabs[i][1]);
            label.setTextSize(11);
            label.setTextColor(i == 3 ? Color.WHITE : 0xFF94A3B8);
            label.setTypeface(i == 3 ? Typeface.DEFAULT_BOLD : Typeface.DEFAULT);
            label.setGravity(Gravity.CENTER);
            tab.addView(label);

            tab.setOnClickListener(v -> {
                if (idx == 0) finishFragment();
                else if (idx == 1) presentFragment(new ContactsActivity(null));
                else if (idx == 2) presentFragment(new CallLogActivity());
                else if (idx == 4) {
                    Bundle args = new Bundle();
                    args.putLong("user_id", UserConfig.getInstance(currentAccount).getClientUserId());
                    presentFragment(new ProfileActivity(args));
                }
            });

            LinearLayout.LayoutParams tlp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
            tlp.setMargins(6, 0, 6, 0);
            bottomNav.addView(tab, tlp);
        }

        root.addView(bottomNav, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.BOTTOM));

        loadLiveReelsFromTelegram();

        fragmentView = root;
        return fragmentView;
    }

    private void loadLiveReelsFromTelegram() {
        // 1. Obuna bo'lingan kanallar va chatlardan videolarni olish
        ArrayList<TLRPC.Dialog> dialogs = MessagesController.getInstance(currentAccount).getAllDialogs();
        int checkedChannels = 0;
        for (TLRPC.Dialog d : dialogs) {
            if (d.id < 0 && checkedChannels < 12) {
                checkedChannels++;
                TLRPC.TL_messages_search req = new TLRPC.TL_messages_search();
                req.peer = MessagesController.getInstance(currentAccount).getInputPeer(d.id);
                req.filter = new TLRPC.TL_inputMessagesFilterVideo();
                req.q = "";
                req.limit = 8;
                ConnectionsManager.getInstance(currentAccount).sendRequest(req, (response, error) -> {
                    if (response instanceof TLRPC.messages_Messages) {
                        processMessages((TLRPC.messages_Messages) response, true);
                    }
                });
            }
        }
        // 2. Global ochiq kanallar va ommaviy postlardagi videolarni qidirish
        loadMoreLiveVideos();
    }

    private void loadMoreLiveVideos() {
        TLRPC.TL_messages_searchGlobal req = new TLRPC.TL_messages_searchGlobal();
        req.q = "uz";
        req.filter = new TLRPC.TL_inputMessagesFilterVideo();
        req.offset_peer = new TLRPC.TL_inputPeerEmpty();
        req.limit = 20;
        ConnectionsManager.getInstance(currentAccount).sendRequest(req, (response, error) -> {
            if (response instanceof TLRPC.messages_Messages) {
                processMessages((TLRPC.messages_Messages) response, false);
            }
        });
    }

    private void processMessages(TLRPC.messages_Messages res, boolean fromSubscribed) {
        MessagesController.getInstance(currentAccount).putChats(res.chats, false);
        MessagesController.getInstance(currentAccount).putUsers(res.users, false);

        AndroidUtilities.runOnUIThread(() -> {
            for (TLRPC.Message msg : res.messages) {
                if (msg.media instanceof TLRPC.TL_messageMediaDocument && msg.media.document != null) {
                    TLRPC.Document doc = msg.media.document;
                    if (doc.mime_type != null && doc.mime_type.startsWith("video/") && doc.size > 0 && doc.size < 45 * 1024 * 1024) {
                        long did = MessageObject.getDialogId(msg);
                        String key = did + "_" + msg.id;
                        if (seenIds.contains(key)) continue;
                        seenIds.add(key);

                        LiveReel reel = new LiveReel();
                        reel.dialogId = did;
                        reel.msgId = msg.id;
                        reel.document = doc;
                        reel.messageObject = new MessageObject(currentAccount, msg, false, true);
                        reel.caption = msg.message != null ? msg.message : "";
                        reel.views = msg.views > 0 ? msg.views : 120;
                        reel.likes = Math.max(1, reel.views / 18);
                        reel.subscribed = fromSubscribed;

                        TLRPC.Chat chat = MessagesController.getInstance(currentAccount).getChat(-did);
                        if (chat != null) {
                            reel.chat = chat;
                            reel.channelName = chat.title != null ? chat.title : "Kanal";
                            reel.username = (chat.username != null && !chat.username.isEmpty()) ? "@" + chat.username : "@avygram_channel";
                            reel.channelLink = (chat.username != null && !chat.username.isEmpty()) ? "t.me/" + chat.username : "t.me/avygram";
                            reel.subscribed = !chat.left;
                        } else {
                            reel.channelName = "Avygram Live";
                            reel.username = "@avygram";
                            reel.channelLink = "t.me/avygram";
                        }
                        reel.comments.add("Zo'r post!");
                        reels.add(reel);
                    }
                }
            }
            if (!reels.isEmpty()) {
                loadingSpinner.setVisibility(View.GONE);
                emptyStatusTv.setVisibility(View.GONE);
                adapter.notifyDataSetChanged();
            }
        });
    }

    private void openChannelChat(LiveReel item) {
        if (item.dialogId != 0) {
            Bundle args = new Bundle();
            if (item.dialogId < 0) args.putLong("chat_id", -item.dialogId);
            else args.putLong("user_id", item.dialogId);
            args.putInt("message_id", item.msgId);
            presentFragment(new ChatActivity(args));
        }
    }

    private void sendRealReaction(LiveReel item) {
        try {
            TLRPC.TL_messages_sendReaction req = new TLRPC.TL_messages_sendReaction();
            req.peer = MessagesController.getInstance(currentAccount).getInputPeer(item.dialogId);
            req.msg_id = item.msgId;
            if (item.liked) {
                TLRPC.TL_reactionEmoji emoji = new TLRPC.TL_reactionEmoji();
                emoji.emoticon = "❤️";
                req.reaction.add(emoji);
            }
            ConnectionsManager.getInstance(currentAccount).sendRequest(req, null);
        } catch (Exception ignored) {}
    }

    private String formatCount(int count) {
        if (count >= 1000000) return String.format("%.1fM", count / 1000000f);
        if (count >= 1000) return String.format("%.1fK", count / 1000f);
        return String.valueOf(count);
    }

    private TextView createActionText(Context context) {
        TextView tv = new TextView(context);
        tv.setTextColor(Color.WHITE);
        tv.setTextSize(13);
        tv.setTypeface(Typeface.DEFAULT_BOLD);
        tv.setGravity(Gravity.CENTER);
        tv.setShadowLayer(6f, 0f, 2f, Color.BLACK);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
        lp.setMargins(0, 0, 0, 28);
        tv.setLayoutParams(lp);
        return tv;
    }

    private void showCommentsDialog(Context context, LiveReel item, TextView commentBtn) {
        LinearLayout box = new LinearLayout(context);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(40, 24, 40, 24);

        ScrollView scroll = new ScrollView(context);
        TextView listTv = new TextView(context);
        listTv.setTextSize(15);
        StringBuilder sb = new StringBuilder();
        for (String c : item.comments) sb.append("• ").append(c).append("\n\n");
        listTv.setText(sb.toString());
        scroll.addView(listTv);
        box.addView(scroll, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 420));

        EditText input = new EditText(context);
        input.setHint("Izoh yozing...");
        box.addView(input);

        new AlertDialog.Builder(context)
                .setTitle("Izohlar (" + item.comments.size() + ")")
                .setView(box)
                .setPositiveButton("Yuborish", (d, w) -> {
                    String txt = input.getText().toString().trim();
                    if (!txt.isEmpty()) {
                        item.comments.add("Siz: " + txt);
                        commentBtn.setText(String.valueOf(item.comments.size()));
                    }
                })
                .setNegativeButton("Yopish", null)
                .show();
    }

    private static class InstagramActionBtn extends LinearLayout {
        private final View iconView;
        private final TextView countView;
        private int iconType;
        private boolean active;

        public InstagramActionBtn(Context context, int type) {
            super(context);
            this.iconType = type;
            setOrientation(VERTICAL);
            setGravity(Gravity.CENTER);
            setPadding(AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6), AndroidUtilities.dp(6));

            iconView = new View(context) {
                final Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
                final Path path = new Path();
                @Override
                protected void onDraw(Canvas canvas) {
                    float w = getWidth(), h = getHeight();
                    p.setShadowLayer(8f, 0f, 3f, 0x99000000);
                    if (iconType == 0) { // Instagram Yurak (Like)
                        path.reset();
                        path.moveTo(w * 0.50f, h * 0.84f);
                        path.cubicTo(w * 0.14f, h * 0.60f, w * 0.08f, h * 0.24f, w * 0.31f, h * 0.18f);
                        path.cubicTo(w * 0.42f, h * 0.15f, w * 0.48f, h * 0.24f, w * 0.50f, h * 0.29f);
                        path.cubicTo(w * 0.52f, h * 0.24f, w * 0.58f, h * 0.15f, w * 0.69f, h * 0.18f);
                        path.cubicTo(w * 0.92f, h * 0.24f, w * 0.86f, h * 0.60f, w * 0.50f, h * 0.84f);
                        path.close();
                        if (active) {
                            p.setStyle(Paint.Style.FILL);
                            p.setColor(0xFFFF2D55);
                            canvas.drawPath(path, p);
                        } else {
                            p.setStyle(Paint.Style.STROKE);
                            p.setStrokeWidth(AndroidUtilities.dp(2.6f));
                            p.setStrokeJoin(Paint.Join.ROUND);
                            p.setColor(Color.WHITE);
                            canvas.drawPath(path, p);
                        }
                    } else if (iconType == 1) { // Instagram Izoh (Comment)
                        p.setStyle(Paint.Style.STROKE);
                        p.setStrokeWidth(AndroidUtilities.dp(2.5f));
                        p.setStrokeJoin(Paint.Join.ROUND);
                        p.setColor(Color.WHITE);
                        RectF r = new RectF(w * 0.16f, h * 0.16f, w * 0.84f, h * 0.80f);
                        canvas.drawArc(r, 125f, 325f, false, p);
                        path.reset();
                        path.moveTo(w * 0.24f, h * 0.72f);
                        path.lineTo(w * 0.16f, h * 0.85f);
                        path.lineTo(w * 0.33f, h * 0.78f);
                        canvas.drawPath(path, p);
                    } else if (iconType == 2) { // Instagram Ulashish (Direct Send)
                        p.setStyle(Paint.Style.STROKE);
                        p.setStrokeWidth(AndroidUtilities.dp(2.5f));
                        p.setStrokeJoin(Paint.Join.ROUND);
                        p.setStrokeCap(Paint.Cap.ROUND);
                        p.setColor(Color.WHITE);
                        path.reset();
                        path.moveTo(w * 0.16f, h * 0.24f);
                        path.lineTo(w * 0.84f, h * 0.24f);
                        path.lineTo(w * 0.50f, h * 0.82f);
                        path.lineTo(w * 0.42f, h * 0.50f);
                        path.close();
                        path.moveTo(w * 0.84f, h * 0.24f);
                        path.lineTo(w * 0.42f, h * 0.50f);
                        canvas.drawPath(path, p);
                    } else { // Instagram Saqlash (Bookmark)
                        path.reset();
                        path.moveTo(w * 0.24f, h * 0.16f);
                        path.lineTo(w * 0.76f, h * 0.16f);
                        path.lineTo(w * 0.76f, h * 0.84f);
                        path.lineTo(w * 0.50f, h * 0.64f);
                        path.lineTo(w * 0.24f, h * 0.84f);
                        path.close();
                        if (active) {
                            p.setStyle(Paint.Style.FILL);
                            p.setColor(0xFF38BDF8);
                            canvas.drawPath(path, p);
                        } else {
                            p.setStyle(Paint.Style.STROKE);
                            p.setStrokeWidth(AndroidUtilities.dp(2.5f));
                            p.setStrokeJoin(Paint.Join.ROUND);
                            p.setColor(Color.WHITE);
                            canvas.drawPath(path, p);
                        }
                    }
                }
            };
            addView(iconView, new LayoutParams(AndroidUtilities.dp(36), AndroidUtilities.dp(36)));

            countView = new TextView(context);
            countView.setTextColor(Color.WHITE);
            countView.setTextSize(13);
            countView.setTypeface(Typeface.DEFAULT_BOLD);
            countView.setGravity(Gravity.CENTER);
            countView.setShadowLayer(6f, 0f, 2f, 0xCC000000);
            LayoutParams clp = new LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            clp.topMargin = AndroidUtilities.dp(2);
            addView(countView, clp);

            LayoutParams lp = new LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            lp.bottomMargin = AndroidUtilities.dp(10);
            setLayoutParams(lp);
        }

        public void setState(boolean isActive, String label) {
            this.active = isActive;
            countView.setText(label);
            iconView.invalidate();
        }

        public void bounceHeart() {
            iconView.animate().cancel();
            iconView.setScaleX(0.65f);
            iconView.setScaleY(0.65f);
            iconView.animate().scaleX(1.38f).scaleY(1.38f).setDuration(140)
                .withEndAction(() -> iconView.animate().scaleX(1.0f).scaleY(1.0f).setDuration(140).start())
                .start();
        }
    }

    private static void triggerHeartBurst(FrameLayout container, float originX, float originY) {
        Context ctx = container.getContext();
        java.util.Random rnd = new java.util.Random();
        // Markazda katta porlovchi qizil yurak
        TextView bigHeart = new TextView(ctx);
        bigHeart.setText("❤️");
        bigHeart.setTextSize(68);
        bigHeart.setX(originX - AndroidUtilities.dp(42));
        bigHeart.setY(originY - AndroidUtilities.dp(42));
        bigHeart.setScaleX(0.2f);
        bigHeart.setScaleY(0.2f);
        container.addView(bigHeart, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        bigHeart.animate().scaleX(1.35f).scaleY(1.35f).alpha(1f).setDuration(180)
            .withEndAction(() -> bigHeart.animate().scaleX(0.9f).scaleY(0.9f).alpha(0f).translationYBy(-AndroidUtilities.dp(70)).setDuration(380)
                .withEndAction(() -> container.removeView(bigHeart)).start())
            .start();

        // Atrofga sochiluvchi 12 ta qizil yurakchalar
        for (int i = 0; i < 12; i++) {
            final TextView pHeart = new TextView(ctx);
            pHeart.setText(i % 3 == 0 ? "💖" : "❤️");
            pHeart.setTextSize(16 + rnd.nextInt(14));
            pHeart.setX(originX - AndroidUtilities.dp(12));
            pHeart.setY(originY - AndroidUtilities.dp(12));
            container.addView(pHeart, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));

            float dx = (rnd.nextFloat() - 0.5f) * AndroidUtilities.dp(210);
            float dy = -AndroidUtilities.dp(90 + rnd.nextInt(180));
            float rot = (rnd.nextFloat() - 0.5f) * 70f;
            long dur = 550 + rnd.nextInt(320);

            pHeart.animate()
                .translationXBy(dx)
                .translationYBy(dy)
                .rotation(rot)
                .scaleX(1.25f)
                .scaleY(1.25f)
                .alpha(0f)
                .setDuration(dur)
                .withEndAction(() -> container.removeView(pHeart))
                .start();
        }
    }

}

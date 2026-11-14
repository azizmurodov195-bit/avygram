p = "TMessagesProj/src/main/java/org/telegram/ui/AvygramReelsActivity.java"
with open(p, "r", encoding="utf-8") as f:
    s = f.read()

old_block = """        final WebView instaWeb = new WebView(context);
        instaWeb.setBackgroundColor(0xFF060913);
        WebSettings ws = instaWeb.getSettings();
        ws.setJavaScriptEnabled(true);
        ws.setDomStorageEnabled(true);
        ws.setDatabaseEnabled(true);
        ws.setMediaPlaybackRequiresUserGesture(false);
        ws.setAllowFileAccess(true);
        ws.setUserAgentString("Mozilla/5.0 (Linux; Android 13; Mobile) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36");

        CookieManager cm = CookieManager.getInstance();
        cm.setAcceptCookie(true);
        cm.setAcceptThirdPartyCookies(instaWeb, true);

        instaWeb.setWebChromeClient(new WebChromeClient());
        instaWeb.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                CookieManager.getInstance().flush();
                // Tungi neon rangga moslashtirish va ortiqcha bannerlarni yashirish
                String js = "javascript:(function(){" +
                        "var st=document.createElement('style');" +
                        "st.innerHTML='body,html{background:#060913!important;}';" +
                        "document.head.appendChild(st);" +
                        "})()";
                view.loadUrl(js);
            }
        });

        FrameLayout.LayoutParams webLp = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT);
        webLp.topMargin = AndroidUtilities.statusBarHeight + AndroidUtilities.dp(46);
        instaContainer.addView(instaWeb, webLp);"""

new_block = """        final WebView instaWeb = new WebView(context);
        instaWeb.setBackgroundColor(0xFF060913);
        instaWeb.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        WebSettings ws = instaWeb.getSettings();
        ws.setJavaScriptEnabled(true);
        ws.setDomStorageEnabled(true);
        ws.setDatabaseEnabled(true);
        ws.setCacheMode(WebSettings.LOAD_DEFAULT);
        ws.setMediaPlaybackRequiresUserGesture(false);
        ws.setAllowFileAccess(true);
        ws.setUseWideViewPort(true);
        ws.setLoadWithOverviewMode(true);
        ws.setUserAgentString("Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36");

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
                        "var st=document.createElement('style');" +
                        "st.innerHTML='body,html{background:#060913!important;overscroll-behavior:none;} [role=banner],a[href*=\\\"/accounts/login\\\"]{display:none!important;}';" +
                        "document.head.appendChild(st);" +
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
                    String src = res == null ? "" : res.replace("\\"", "").trim();
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
        instaWeb.loadUrl("https://www.instagram.com/reels/?theme=dark");"""

assert old_block in s, "Block not found"
s = s.replace(old_block, new_block, 1)
s = s.replace("final boolean[] instaLoaded = {false};", "final boolean[] instaLoaded = {true};")
with open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("INSTA_PRO_OK")

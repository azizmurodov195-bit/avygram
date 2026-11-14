p = "TMessagesProj/src/main/java/org/telegram/ui/AvygramReelsActivity.java"
with open(p, "r", encoding="utf-8") as f:
    s = f.read()

old_ua = 'ws.setUserAgentString("Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36");'
new_ua = '''ws.setUserAgentString("Mozilla/5.0 (Linux; Android 14; 23127PN0CG Build/UKQ1.230804.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.127 Mobile Safari/537.36 Instagram 348.0.0.39.109 Android (34/14; 440dpi; 1080x2400; Xiaomi/Redmi; 23127PN0CG; aurora; qcom; en_US; 638491021)");
        ws.setOffscreenPreRaster(true);
        ws.setRenderPriority(WebSettings.RenderPriority.HIGH);
        instaWeb.setOverScrollMode(View.OVER_SCROLL_NEVER);'''

assert old_ua in s, "UA not found"
s = s.replace(old_ua, new_ua, 1)

old_js = '''                String js = "javascript:(function(){" +
                        "var st=document.createElement('style');" +
                        "st.innerHTML='body,html{background:#060913!important;overscroll-behavior:none;} [role=banner],a[href*=\\\\"/accounts/login\\\\"]{display:none!important;}';" +
                        "document.head.appendChild(st);" +
                        "})()";'''

new_js = '''                String js = "javascript:(function(){" +
                        "if(!document.getElementById('avy_hd_style')){" +
                        "var st=document.createElement('style');st.id='avy_hd_style';" +
                        "st.innerHTML='body,html{background:#060913!important;overscroll-behavior:none;} [role=banner],a[href*=\\\\"/accounts/login\\\\"]{display:none!important;} video{object-fit:cover!important;filter:contrast(1.04) saturate(1.06)!important;}';" +
                        "document.head.appendChild(st);}" +
                        "if(!window._avyAutoPlay){window._avyAutoPlay=setInterval(function(){" +
                        "var vids=document.querySelectorAll('video');" +
                        "for(var i=0;i<vids.length;i++){var v=vids[i];var r=v.getBoundingClientRect();" +
                        "if(r.top<window.innerHeight*0.75&&r.bottom>window.innerHeight*0.25){" +
                        "if(v.paused){v.muted=false;v.play().catch(function(){v.muted=true;v.play().catch(function(){});});}" +
                        "}else if(!v.paused){v.pause();}}" +
                        "},450);}" +
                        "})()";'''

assert old_js in s, "JS not found"
s = s.replace(old_js, new_js, 1)

with open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("INSTA_HD_ENGINE_OK")

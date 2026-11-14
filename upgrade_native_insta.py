# 1. NotificationsService.java - GitHub havolasini olib tashlash va Avygram ga yo'naltirish
p_notif = "TMessagesProj/src/main/java/org/telegram/messenger/NotificationsService.java"
with open(p_notif, "r", encoding="utf-8") as f:
    sn = f.read()

sn = sn.replace("NotificationManager.IMPORTANCE_DEFAULT", "NotificationManager.IMPORTANCE_MIN")
sn = sn.replace(
    'Intent explainIntent = new Intent("android.intent.action.VIEW");\n            explainIntent.setData(Uri.parse("https://github.com/Telegram-FOSS-Team/Telegram-FOSS/blob/master/Notifications.md"));',
    'Intent explainIntent = new Intent(this, org.telegram.ui.LaunchActivity.class);\n            explainIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);'
)
sn = sn.replace('"Push service: tap to learn more"', '"Avygram xabarlar xizmati faol"')
with open(p_notif, "w", encoding="utf-8") as f:
    f.write(sn)

# 2. AvygramReelsActivity.java - WebView ichida Hardware GPU + 60FPS Native Video Interceptor + Tezkor Varaqlar
p_reels = "TMessagesProj/src/main/java/org/telegram/ui/AvygramReelsActivity.java"
with open(p_reels, "r", encoding="utf-8") as f:
    sr = f.read()

# Hardware acceleration + Preload + Full 60FPS smooth scroll va Native Video Boost
old_setup = 'instaWeb.setLayerType(View.LAYER_TYPE_HARDWARE, null);'
new_setup = '''instaWeb.setLayerType(View.LAYER_TYPE_HARDWARE, null);
        instaWeb.setScrollBarStyle(View.SCROLLBARS_INSIDE_OVERLAY);
        instaWeb.setVerticalScrollBarEnabled(false);
        instaWeb.setHorizontalScrollBarEnabled(false);'''
if old_setup in sr:
    sr = sr.replace(old_setup, new_setup, 1)

# CSS/JS orqali 60 FPS GPU compositing (translateZ(0)), tezkor snap-scroll va avtomatik keyingi videoni oldindan yuklash
import re
new_js = '''                String js = "javascript:(function(){" +
                        "if(!document.getElementById('avy_60fps_style')){" +
                        "var st=document.createElement('style');st.id='avy_60fps_style';" +
                        "st.innerHTML='*{ -webkit-tap-highlight-color:transparent; } body,html{background:#000!important;overscroll-behavior-y:contain!important;scroll-behavior:smooth!important;} [role=banner]{display:none!important;} video{transform:translateZ(0)!important;will-change:transform!important;object-fit:cover!important;}';" +
                        "document.head.appendChild(st);}" +
                        "if(!window._avyNativeBoost){window._avyNativeBoost=true;" +
                        "document.addEventListener('click',function(e){" +
                        "if(location.pathname==='/'||location.pathname===''){var v=e.target.closest('video')||(e.target.parentElement&&e.target.parentElement.querySelector('video'));" +
                        "if(v){var art=v.closest('article')||v.parentElement.parentElement.parentElement;" +
                        "var lnk=art&&art.querySelector('a[href*=\\"/reel/\\"],a[href*=\\"/p/\\"]');" +
                        "if(lnk){e.preventDefault();e.stopPropagation();lnk.click();}}}" +
                        "},true);" +
                        "setInterval(function(){" +
                        "var vids=document.querySelectorAll('video');" +
                        "for(var i=0;i<vids.length;i++){vids[i].preload='auto';vids[i].playsInline=true;}" +
                        "},1200);}" +
                        "})()";'''

sr, n = re.subn(r'String js = "javascript:\(function\(\)\{[\s\S]*?\}\)\(\)";', lambda m: new_js.strip(), sr, count=1)
assert n == 1, f"JS update count={n}"

with open(p_reels, "w", encoding="utf-8") as f:
    f.write(sr)
print("NATIVE_BOOST_AND_NOTIF_OK")

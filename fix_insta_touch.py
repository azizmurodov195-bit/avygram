import re

p = "TMessagesProj/src/main/java/org/telegram/ui/AvygramReelsActivity.java"
with open(p, "r", encoding="utf-8") as f:
    s = f.read()

new_js = '''                String js = "javascript:(function(){" +
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
                        "var lnk=art&&art.querySelector('a[href*=\\"/reel/\\"],a[href*=\\"/p/\\"]');" +
                        "if(lnk&&lnk.href){e.preventDefault();e.stopImmediatePropagation();location.href=lnk.href;return;}}" +
                        "if(!isHome&&v){e.preventDefault();e.stopImmediatePropagation();" +
                        "var now=Date.now(),cx=e.clientX||(window.innerWidth/2),cy=e.clientY||(window.innerHeight/2);" +
                        "if(now-lastTap<300){clearTimeout(tapTimer);lastTap=0;showHeart(cx,cy);" +
                        "var sec=v.closest('section,article,div[role=presentation]')||document;" +
                        "var likeBtn=sec.querySelector('svg[aria-label=\\"Like\\"],svg[aria-label=\\"Нравится\\"]');" +
                        "if(likeBtn){var b=likeBtn.closest('button,[role=button]');if(b)b.click();}" +
                        "}else{lastTap=now;tapTimer=setTimeout(function(){if(v.paused)v.play();else v.pause();},305);}}" +
                        "},true);}" +
                        "})()";'''

s, n = re.subn(r'String js = "javascript:\(function\(\)\{[\s\S]*?\}\)\(\)";', lambda m: new_js.strip(), s, count=1)
assert n == 1, f"JS update failed: {n}"

with open(p, "w", encoding="utf-8") as f:
    f.write(s)
print("INSTA_TOUCH_PERFECT_OK")

package org.telegram.ui;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.LinearGradient;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RectF;
import android.graphics.Shader;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.os.Bundle;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.TextView;
import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.UserConfig;
import org.telegram.ui.ActionBar.ActionBar;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.ActionBar.Theme;
import org.telegram.ui.Components.FilterTabsView;

public class AvygramHomeHelper {

    private static final Paint cardFillPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private static final Paint cardStrokePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private static final RectF cardRect = new RectF();

    public static Integer getNeonOverrideColor(int key) {
        if (key == Theme.key_actionBarDefault || key == Theme.key_actionBarDefaultArchived) return 0xFF070B19;
        if (key == Theme.key_actionBarDefaultTitle || key == Theme.key_profile_title) return 0xFFFFFFFF;
        if (key == Theme.key_actionBarDefaultSubtitle || key == Theme.key_profile_status) return 0xFF93C5FD;
        if (key == Theme.key_actionBarDefaultIcon || key == Theme.key_actionBarActionModeDefaultIcon) return 0xFFE2E8F0;
        if (key == Theme.key_actionBarActionModeDefault || key == Theme.key_actionBarActionModeDefaultTop) return 0xFF0D1428;
        if (key == Theme.key_windowBackgroundWhite || key == Theme.key_dialogBackground || key == Theme.key_profile_actionBackground) return 0xFF060913;
        if (key == Theme.key_windowBackgroundGray || key == Theme.key_windowBackgroundGrayShadow || key == Theme.key_dialogBackgroundGray) return 0xFF040711;
        if (key == Theme.key_windowBackgroundWhiteBlackText || key == Theme.key_dialogTextBlack || key == Theme.key_chats_name || key == Theme.key_chats_nameArchived) return 0xFFF8FAFC;
        if (key == Theme.key_windowBackgroundWhiteGrayText || key == Theme.key_windowBackgroundWhiteGrayText2 || key == Theme.key_windowBackgroundWhiteGrayText3 || key == Theme.key_dialogTextGray || key == Theme.key_dialogTextGray2) return 0xFF94A3B8;
        if (key == Theme.key_windowBackgroundWhiteBlueText || key == Theme.key_windowBackgroundWhiteBlueText2 || key == Theme.key_windowBackgroundWhiteBlueText4 || key == Theme.key_windowBackgroundWhiteBlueHeader || key == Theme.key_dialogTextBlue || key == Theme.key_dialogTextBlue2) return 0xFF60A5FA;
        if (key == Theme.key_windowBackgroundWhiteValueText || key == Theme.key_chats_date) return 0xFF38BDF8;
        if (key == Theme.key_chats_message || key == Theme.key_chats_message_threeLines) return 0xFFCBD5E1;
        if (key == Theme.key_chats_unreadCounter || key == Theme.key_switchTrackChecked || key == Theme.key_checkboxSquareBackground) return 0xFF6366F1;
        if (key == Theme.key_chats_unreadCounterMuted || key == Theme.key_switchTrack) return 0xFF1E293B;
        if (key == Theme.key_divider || key == Theme.key_listSelector) return 0x226366F1;
        if (key == Theme.key_actionBarTabActiveText) return 0xFFFFFFFF;
        if (key == Theme.key_actionBarTabUnactiveText) return 0xFF94A3B8;
        if (key == Theme.key_actionBarTabLine) return 0xFF818CF8;
        if (key == Theme.key_stories_circle1) return 0xFF38BDF8;
        if (key == Theme.key_stories_circle2) return 0xFF8B5CF6;
        if (key == Theme.key_chat_inBubble || key == Theme.key_chat_inBubbleSelected) return 0xFF10192E;
        if (key == Theme.key_chat_outBubble || key == Theme.key_chat_outBubbleSelected) return 0xFF312E81;
        if (key == Theme.key_chat_messageTextIn || key == Theme.key_chat_messageTextOut) return 0xFFF8FAFC;
        if (key == Theme.key_chat_inTimeText) return 0xFF94A3B8;
        if (key == Theme.key_chat_outTimeText) return 0xFFC7D2FE;
        if (key == Theme.key_chat_outSentCheck || key == Theme.key_chat_outSentCheckRead || key == Theme.key_chat_inVoiceSeekbarFill || key == Theme.key_chat_outVoiceSeekbarFill) return 0xFF38BDF8;
        if (key == Theme.key_chat_messagePanelBackground || key == Theme.key_chat_topPanelBackground) return 0xFF090E1F;
        if (key == Theme.key_chat_messagePanelText) return 0xFFFFFFFF;
        if (key == Theme.key_chat_messagePanelHint) return 0xFF64748B;
        if (key == Theme.key_chat_messagePanelIcons) return 0xFF818CF8;
        if (key == Theme.key_chat_serviceBackground) return 0xAA1E1B4B;
        if (key == Theme.key_chat_serviceText) return 0xFFE0E7FF;
        if (key == Theme.key_chat_wallpaper) return 0xFF060913;
        return null;
    }

    public static void applyGlobalNeonColors() {
        applyNeonChatTheme(null, null);
    }

    public static void drawNeonCard(Canvas canvas, int width, int height, boolean isPinned) {
        if (width <= 0 || height <= 0) return;
        float padX = AndroidUtilities.dp(10);
        float padY = AndroidUtilities.dp(3.5f);
        float radius = AndroidUtilities.dp(16);
        cardRect.set(padX, padY, width - padX, height - padY);

        cardFillPaint.setStyle(Paint.Style.FILL);
        cardFillPaint.setColor(isPinned ? 0x383B82F6 : 0x241E293B);
        canvas.drawRoundRect(cardRect, radius, radius, cardFillPaint);

        cardStrokePaint.setStyle(Paint.Style.STROKE);
        cardStrokePaint.setStrokeWidth(AndroidUtilities.dp(isPinned ? 1.5f : 1f));
        cardStrokePaint.setColor(isPinned ? 0xCC818CF8 : 0x4D38BDF8);
        canvas.drawRoundRect(cardRect, radius, radius, cardStrokePaint);
    }

    public static void applyNeonChatTheme(final BaseFragment fragment, View fragmentView) {
        if (!(fragmentView instanceof ViewGroup)) return;
        ViewGroup root = (ViewGroup) fragmentView;

        GradientDrawable neonWall = new GradientDrawable(
                GradientDrawable.Orientation.TL_BR,
                new int[]{0xFF050814, 0xFF0B1229, 0xFF131136, 0xFF060913}
        );
        root.setBackground(neonWall);

        if (fragment != null && fragment.getActionBar() != null) {
            ActionBar ab = fragment.getActionBar();
            GradientDrawable abBg = new GradientDrawable();
            abBg.setCornerRadii(new float[]{0f, 0f, 0f, 0f, 44f, 44f, 44f, 44f});
            abBg.setColor(0xF5080D1E);
            abBg.setStroke(2, 0x666366F1);
            ab.setBackground(abBg);
            ab.setTitleColor(Color.WHITE);
            ab.setSubtitleColor(0xFF93C5FD);
            ab.setItemsColor(Color.WHITE, false);
        }

        for (int i = 0; i < root.getChildCount(); i++) {
            View child = root.getChildAt(i);
            String cls = child.getClass().getSimpleName();
            if (cls.contains("ChatBackground") || cls.contains("Wallpaper") || i == 0) {
                child.setBackground(neonWall);
            }
        }
    }

    public static void attachHomeChrome(final BaseFragment fragment, View fragmentView) {
        if (!(fragmentView instanceof ViewGroup)) return;
        final ViewGroup root = (ViewGroup) fragmentView;
        final Context context = fragmentView.getContext();

        root.setBackgroundColor(0xFF060913);
        root.setClipChildren(false);
        final int statusBarH = AndroidUtilities.statusBarHeight;
        final int topBarH = AndroidUtilities.dp(50);

        final ActionBar ab = fragment.getActionBar();
        if (ab != null) {
            ab.setBackgroundColor(0xFF060913);
            ab.setItemsColor(Color.WHITE, false);
            ab.setTitleColor(Color.WHITE);
        }

        // Yuqori AVYGRAM paneli — ikki cheti yumaloq qayrilgan neon kapsula
        final LinearLayout topBar = new LinearLayout(context);
        topBar.setOrientation(LinearLayout.HORIZONTAL);
        topBar.setGravity(Gravity.CENTER_VERTICAL);
        GradientDrawable topGrad = new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM, new int[]{0xFF090F24, 0xF5070B19});
        topGrad.setCornerRadii(new float[]{0f, 0f, 0f, 0f, 46f, 46f, 46f, 46f});
        topGrad.setStroke(2, 0x666366F1);
        topBar.setBackground(topGrad);
        topBar.setPadding(AndroidUtilities.dp(16), statusBarH + AndroidUtilities.dp(2), AndroidUtilities.dp(16), AndroidUtilities.dp(6));

        View neonLogo = new View(context) {
            final Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
            final Path path = new Path();
            @Override
            protected void onDraw(Canvas canvas) {
                float w = getWidth(), h = getHeight();
                p.setStyle(Paint.Style.STROKE);
                p.setStrokeWidth(AndroidUtilities.dp(3.0f));
                p.setStrokeCap(Paint.Cap.ROUND);
                p.setStrokeJoin(Paint.Join.ROUND);
                p.setShader(new LinearGradient(0, 0, w, h, new int[]{0xFF38BDF8, 0xFF818CF8, 0xFFC084FC}, null, Shader.TileMode.CLAMP));
                path.reset();
                path.moveTo(w * 0.2f, h * 0.82f);
                path.lineTo(w * 0.5f, h * 0.16f);
                path.lineTo(w * 0.8f, h * 0.82f);
                path.moveTo(w * 0.3f, h * 0.6f);
                path.lineTo(w * 0.72f, h * 0.6f);
                canvas.drawPath(path, p);
            }
        };
        topBar.addView(neonLogo, new LinearLayout.LayoutParams(AndroidUtilities.dp(32), AndroidUtilities.dp(32)));

        TextView brandTv = new TextView(context);
                brandTv.setText(" AVYGRAM");
        brandTv.setTextColor(Color.WHITE);
        brandTv.setTextSize(18);
        brandTv.setTypeface(Typeface.DEFAULT_BOLD);
        brandTv.setLetterSpacing(0.09f);
        brandTv.setShadowLayer(12f, 0f, 0f, 0x886366F1);
        topBar.addView(brandTv, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

        View.OnClickListener openDrawer = v -> {
            if (fragment.getParentLayout() != null && fragment.getParentLayout().getDrawerLayoutContainer() != null) {
                fragment.getParentLayout().getDrawerLayoutContainer().openDrawer(false);
            }
        };
        neonLogo.setOnClickListener(openDrawer);
        brandTv.setOnClickListener(openDrawer);

        View searchBtn = createSearchBtn(context);
        searchBtn.setOnClickListener(v -> {
            if (ab != null) {
                topBar.setVisibility(View.GONE);
                ab.bringToFront();
                ab.openSearchField("", true);
            }
        });
        final TextView ghostBtn = new TextView(context);
        ghostBtn.setText("👻");
        ghostBtn.setTextSize(16);
        ghostBtn.setGravity(Gravity.CENTER);
        final GradientDrawable gBg = new GradientDrawable();
        gBg.setShape(GradientDrawable.OVAL);
        boolean gOn = isGhostMode(context);
        gBg.setColor(gOn ? 0x556366F1 : 0xFF0F172A);
        gBg.setStroke(2, gOn ? 0xFF38BDF8 : 0x446366F1);
        ghostBtn.setBackground(gBg);
        ghostBtn.setAlpha(gOn ? 1.0f : 0.55f);
        ghostBtn.setTag("avy_ghost_btn"); // avy_ghost_tag
        ghostBtn.setVisibility(isTopGhostVisible(context) ? View.VISIBLE : View.GONE);
        ghostBtn.setOnClickListener(v -> {
            boolean next = !isGhostMode(context);
            setGhostMode(context, next);
            gBg.setColor(next ? 0x556366F1 : 0xFF0F172A);
            gBg.setStroke(2, next ? 0xFF38BDF8 : 0x446366F1);
            ghostBtn.setAlpha(next ? 1.0f : 0.55f);
            android.widget.Toast.makeText(context, next ? "👻 Sharpa rejimi YOQILDI (Hikoya va xabarlar yashirin)" : "👁 Sharpa rejimi O'CHIRILDI", android.widget.Toast.LENGTH_SHORT).show();
        });
        LinearLayout.LayoutParams glp = new LinearLayout.LayoutParams(AndroidUtilities.dp(36), AndroidUtilities.dp(36));
        glp.rightMargin = AndroidUtilities.dp(8);
        topBar.addView(ghostBtn, glp);

        topBar.addView(searchBtn);

        if (ab != null) {
            ab.addOnLayoutChangeListener((v, l, t, r, b, ol, ot, or, ob) -> {
                boolean busy = ab.isSearchFieldVisible() || ab.isActionModeShowed();
                if (busy && topBar.getVisibility() == View.VISIBLE) {
                    topBar.setVisibility(View.GONE);
                    ab.bringToFront();
                } else if (!busy && topBar.getVisibility() != View.VISIBLE) {
                    topBar.setVisibility(View.VISIBLE);
                    topBar.bringToFront();
                }
            });
        }

        tintStoriesAndTabs(root);

        for (int i = 0; i < root.getChildCount(); i++) {
            View child = root.getChildAt(i);
            if (child == ab) continue;
            if (child instanceof ViewGroup) {
                ((ViewGroup) child).setClipToPadding(false);
                ((ViewGroup) child).setClipChildren(false);
            }
            if (child.getLayoutParams() instanceof ViewGroup.MarginLayoutParams) {
                ViewGroup.MarginLayoutParams mlp = (ViewGroup.MarginLayoutParams) child.getLayoutParams();
                if (child instanceof FilterTabsView) {
                    child.setBackgroundColor(0xFF060913);
                    child.setVisibility(View.VISIBLE);
                    child.setTranslationY(0f);
                    child.bringToFront();
                } else if (mlp.topMargin > 0) {
                    mlp.topMargin = statusBarH + topBarH;
                    child.setPadding(child.getPaddingLeft(), child.getPaddingTop(), child.getPaddingRight(), AndroidUtilities.dp(76));
                } else if (mlp.bottomMargin > 0 && mlp.bottomMargin < AndroidUtilities.dp(65)) {
                    mlp.bottomMargin = AndroidUtilities.dp(78);
                }
            }
        }

        root.addView(topBar, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, statusBarH + topBarH, Gravity.TOP));

        LinearLayout bottomNav = new LinearLayout(context);
        bottomNav.setOrientation(LinearLayout.HORIZONTAL);
        bottomNav.setGravity(Gravity.CENTER);
        bottomNav.setPadding(AndroidUtilities.dp(8), AndroidUtilities.dp(7), AndroidUtilities.dp(8), AndroidUtilities.dp(10));
        GradientDrawable navBg = new GradientDrawable();
        navBg.setCornerRadii(new float[]{46f, 46f, 46f, 46f, 0f, 0f, 0f, 0f});
        navBg.setColor(0xF50B1021);
        navBg.setStroke(2, 0x666366F1);
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
            tab.setPadding(AndroidUtilities.dp(6), AndroidUtilities.dp(5), AndroidUtilities.dp(6), AndroidUtilities.dp(5));

            if (i == 0) {
                GradientDrawable activeBg = new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM, new int[]{0xFF3B82F6, 0xFF6366F1});
                activeBg.setCornerRadius(AndroidUtilities.dp(14));
                activeBg.setStroke(2, 0xFF93C5FD);
                tab.setBackground(activeBg);
            }

            TextView icon = new TextView(context);
            icon.setText(tabs[i][0]);
            icon.setTextSize(16);
            icon.setGravity(Gravity.CENTER);
            tab.addView(icon);

            TextView label = new TextView(context);
            label.setText(tabs[i][1]);
            label.setTextSize(11);
            label.setTextColor(i == 0 ? Color.WHITE : 0xFF94A3B8);
            label.setTypeface(i == 0 ? Typeface.DEFAULT_BOLD : Typeface.DEFAULT);
            label.setGravity(Gravity.CENTER);
            tab.addView(label);

            tab.setOnClickListener(v -> {
                if (idx == 1) fragment.presentFragment(new ContactsActivity(null));
                else if (idx == 2) fragment.presentFragment(new CallLogActivity());
                else if (idx == 3) fragment.presentFragment(new AvygramReelsActivity());
                else if (idx == 4) {
                    Bundle args = new Bundle();
                    args.putLong("user_id", UserConfig.getInstance(fragment.getCurrentAccount()).getClientUserId());
                    fragment.presentFragment(new ProfileActivity(args));
                }
            });

            LinearLayout.LayoutParams tlp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
            tlp.setMargins(4, 0, 4, 0);
            bottomNav.addView(tab, tlp);
        }

        root.addView(bottomNav, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.BOTTOM));
    }

    private static void tintStoriesAndTabs(View view) {
        String name = view.getClass().getSimpleName();
        if (name.contains("DialogStoriesCell") || name.contains("FilterTabsView")) {
            GradientDrawable storyBg = new GradientDrawable(GradientDrawable.Orientation.TOP_BOTTOM, new int[]{0xFF060913, 0xFF0B1229});
            storyBg.setCornerRadii(new float[]{0f, 0f, 0f, 0f, 36f, 36f, 36f, 36f});
            storyBg.setStroke(1, 0x556366F1);
            view.setBackground(storyBg);
        }
        if (view instanceof ViewGroup) {
            ViewGroup vg = (ViewGroup) view;
            for (int i = 0; i < vg.getChildCount(); i++) {
                tintStoriesAndTabs(vg.getChildAt(i));
            }
        }
    }

    private static View createSearchBtn(Context context) {
        View btn = new View(context) {
            final Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
            @Override
            protected void onDraw(Canvas canvas) {
                float cx = getWidth() / 2f, cy = getHeight() / 2f;
                p.setStyle(Paint.Style.STROKE);
                p.setStrokeWidth(AndroidUtilities.dp(2f));
                p.setStrokeCap(Paint.Cap.ROUND);
                p.setColor(0xFFE2E8F0);
                float r = AndroidUtilities.dp(6.5f);
                canvas.drawCircle(cx - AndroidUtilities.dp(1.5f), cy - AndroidUtilities.dp(1.5f), r, p);
                canvas.drawLine(cx + AndroidUtilities.dp(3.2f), cy + AndroidUtilities.dp(3.2f), cx + AndroidUtilities.dp(7.5f), cy + AndroidUtilities.dp(7.5f), p);
            }
        };
        GradientDrawable bg = new GradientDrawable();
        bg.setShape(GradientDrawable.OVAL);
        bg.setColor(0xFF0F172A);
        bg.setStroke(2, 0x666366F1);
        btn.setBackground(bg);
        btn.setLayoutParams(new LinearLayout.LayoutParams(AndroidUtilities.dp(36), AndroidUtilities.dp(36)));
        return btn;
    }

    public static boolean isGhostMode(Context ctx) {
        if (ctx == null) ctx = org.telegram.messenger.ApplicationLoader.applicationContext;
        return ctx != null && ctx.getSharedPreferences("avygram_prefs", Context.MODE_PRIVATE).getBoolean("ghost_mode", true);
    }

    public static void setGhostMode(Context ctx, boolean enabled) {
        if (ctx == null) ctx = org.telegram.messenger.ApplicationLoader.applicationContext;
        if (ctx != null) ctx.getSharedPreferences("avygram_prefs", Context.MODE_PRIVATE).edit().putBoolean("ghost_mode", enabled).apply();
    }

    public static void attachAnimatedNeonSplash(final FrameLayout root) {
        final Context ctx = root.getContext();
        final FrameLayout splash = new FrameLayout(ctx);
        splash.setBackgroundColor(0xFF060913);

        final View animLogo = new View(ctx) {
            final Paint glowPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
            final Paint corePaint = new Paint(Paint.ANTI_ALIAS_FLAG);
            final Path path = new Path();
            float progress = 0f;
            float pulse = 1f;
            {
                android.animation.ValueAnimator va = android.animation.ValueAnimator.ofFloat(0f, 1f);
                va.setDuration(900);
                va.addUpdateListener(a -> { progress = (float) a.getAnimatedValue(); invalidate(); });
                va.start();

                android.animation.ValueAnimator pa = android.animation.ValueAnimator.ofFloat(0.95f, 1.06f);
                pa.setDuration(750);
                pa.setRepeatMode(android.animation.ValueAnimator.REVERSE);
                pa.setRepeatCount(android.animation.ValueAnimator.INFINITE);
                pa.addUpdateListener(a -> { pulse = (float) a.getAnimatedValue(); invalidate(); });
                pa.start();
            }
            @Override
            protected void onDraw(Canvas canvas) {
                float w = getWidth(), h = getHeight();
                float cx = w / 2f, cy = h / 2f;
                canvas.save();
                canvas.scale(pulse, pulse, cx, cy);

                float sz = Math.min(w, h) * 0.28f;
                path.reset();
                path.moveTo(cx - sz * 0.75f, cy + sz * 0.85f);
                path.lineTo(cx, cy - sz * 0.85f);
                path.lineTo(cx + sz * 0.75f, cy + sz * 0.85f);
                path.moveTo(cx - sz * 0.45f, cy + sz * 0.25f);
                path.lineTo(cx + sz * 0.45f, cy + sz * 0.25f);

                Shader sh = new LinearGradient(cx - sz, cy - sz, cx + sz, cy + sz,
                        new int[]{0xFF38BDF8, 0xFF818CF8, 0xFFC084FC}, null, Shader.TileMode.CLAMP);

                glowPaint.setStyle(Paint.Style.STROKE);
                glowPaint.setStrokeCap(Paint.Cap.ROUND);
                glowPaint.setStrokeJoin(Paint.Join.ROUND);
                glowPaint.setStrokeWidth(AndroidUtilities.dp(16f));
                glowPaint.setShader(sh);
                glowPaint.setAlpha((int) (95 * progress));
                canvas.drawPath(path, glowPaint);

                corePaint.setStyle(Paint.Style.STROKE);
                corePaint.setStrokeCap(Paint.Cap.ROUND);
                corePaint.setStrokeJoin(Paint.Join.ROUND);
                corePaint.setStrokeWidth(AndroidUtilities.dp(6.5f));
                corePaint.setShader(sh);
                corePaint.setAlpha((int) (255 * progress));
                canvas.drawPath(path, corePaint);
                canvas.restore();
            }
        };
        splash.addView(animLogo, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));

        TextView title = new TextView(ctx);
        title.setText("AVYGRAM");
        title.setTextColor(Color.WHITE);
        title.setTextSize(22);
        title.setTypeface(Typeface.DEFAULT_BOLD);
        title.setLetterSpacing(0.22f);
        title.setShadowLayer(16f, 0f, 0f, 0xAA6366F1);
        FrameLayout.LayoutParams tlp = new FrameLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT, Gravity.BOTTOM | Gravity.CENTER_HORIZONTAL);
        tlp.bottomMargin = AndroidUtilities.dp(95);
        splash.addView(title, tlp);

        root.addView(splash, new FrameLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT));
        splash.postDelayed(() -> splash.animate().alpha(0f).setDuration(350).withEndAction(() -> root.removeView(splash)).start(), 1350);
    }


    public static boolean isGhostReadDisabled(Context ctx) {
        if (ctx == null) ctx = org.telegram.messenger.ApplicationLoader.applicationContext;
        return ctx != null && ctx.getSharedPreferences("avygram_prefs", Context.MODE_PRIVATE).getBoolean("ghost_read", true);
    }

    public static boolean isStoryStealthEnabled(Context ctx) {
        if (ctx == null) ctx = org.telegram.messenger.ApplicationLoader.applicationContext;
        return ctx != null && ctx.getSharedPreferences("avygram_prefs", Context.MODE_PRIVATE).getBoolean("story_stealth", true);
    }

    public static boolean isTopGhostVisible(Context ctx) {
        if (ctx == null) ctx = org.telegram.messenger.ApplicationLoader.applicationContext;
        return ctx != null && ctx.getSharedPreferences("avygram_prefs", Context.MODE_PRIVATE).getBoolean("top_ghost_btn", true);
    }

    public static void showAvygramSettingsDialog(final Context ctx, final View topGhostBtnRef) {
        final android.content.SharedPreferences prefs = ctx.getSharedPreferences("avygram_prefs", Context.MODE_PRIVATE);
        LinearLayout box = new LinearLayout(ctx);
        box.setOrientation(LinearLayout.VERTICAL);
        box.setPadding(AndroidUtilities.dp(20), AndroidUtilities.dp(18), AndroidUtilities.dp(20), AndroidUtilities.dp(16));
        GradientDrawable bg = new GradientDrawable();
        bg.setColor(0xFF090E1F);
        bg.setCornerRadius(AndroidUtilities.dp(20));
        bg.setStroke(2, 0xFF6366F1);
        box.setBackground(bg);

        TextView head = new TextView(ctx);
        head.setText("⚡ Avygram Sozlamalari");
        head.setTextColor(Color.WHITE);
        head.setTextSize(19);
        head.setTypeface(Typeface.DEFAULT_BOLD);
        head.setPadding(0, 0, 0, AndroidUtilities.dp(14));
        box.addView(head);

        String[][] items = {
            {"👻 Sharpa rejimi (Xabar o'qilganini yashirish)", "Xabarlarni o'qisangiz ham 2 galochka ketmaydi", "ghost_read"},
            {"👁 Hikoyalarni yashirin ko'rish", "Birovning hikoyasini ko'rsangiz ro'yxatda ko'rinmaysiz", "story_stealth"},
            {"🔝 Tepa panelda 👻 tugmasini ko'rsatish", "Asosiy ekran tepasidagi tezkor sharpa tugmasi", "top_ghost_btn"}
        };

        for (final String[] it : items) {
            LinearLayout row = new LinearLayout(ctx);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            row.setPadding(AndroidUtilities.dp(12), AndroidUtilities.dp(12), AndroidUtilities.dp(12), AndroidUtilities.dp(12));
            GradientDrawable rBg = new GradientDrawable();
            rBg.setColor(0x223B82F6);
            rBg.setCornerRadius(AndroidUtilities.dp(14));
            rBg.setStroke(1, 0x446366F1);
            row.setBackground(rBg);

            LinearLayout texts = new LinearLayout(ctx);
            texts.setOrientation(LinearLayout.VERTICAL);
            TextView t1 = new TextView(ctx);
            t1.setText(it[0]);
            t1.setTextColor(Color.WHITE);
            t1.setTextSize(14);
            t1.setTypeface(Typeface.DEFAULT_BOLD);
            texts.addView(t1);

            TextView t2 = new TextView(ctx);
            t2.setText(it[1]);
            t2.setTextColor(0xFF94A3B8);
            t2.setTextSize(11.5f);
            texts.addView(t2);

            row.addView(texts, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));

            final android.widget.Switch sw = new android.widget.Switch(ctx);
            sw.setChecked(prefs.getBoolean(it[2], true));
            sw.setOnCheckedChangeListener((btn, checked) -> {
                prefs.edit().putBoolean(it[2], checked).apply();
                if ("ghost_read".equals(it[2]) || "story_stealth".equals(it[2])) {
                    boolean anyOn = prefs.getBoolean("ghost_read", true) || prefs.getBoolean("story_stealth", true);
                    prefs.edit().putBoolean("ghost_mode", anyOn).apply();
                }
            });
            row.addView(sw);

            row.setOnClickListener(v -> sw.setChecked(!sw.isChecked()));
            LinearLayout.LayoutParams rlp = new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT);
            rlp.bottomMargin = AndroidUtilities.dp(10);
            box.addView(row, rlp);
        }

        new android.app.AlertDialog.Builder(ctx).setView(box).setPositiveButton("Saqlash", null).show();
    }


    public static void refreshGhostBtn(View root) {
        if (root == null) return;
        View btn = root.findViewWithTag("avy_ghost_btn");
        if (btn != null) {
            Context ctx = root.getContext();
            boolean vis = isTopGhostVisible(ctx);
            btn.setVisibility(vis ? View.VISIBLE : View.GONE);
            boolean gOn = isGhostMode(ctx);
            if (btn.getBackground() instanceof GradientDrawable) {
                GradientDrawable gBg = (GradientDrawable) btn.getBackground();
                gBg.setColor(gOn ? 0x556366F1 : 0xFF0F172A);
                gBg.setStroke(2, gOn ? 0xFF38BDF8 : 0x446366F1);
            }
            btn.setAlpha(gOn ? 1.0f : 0.55f);
        }
    }

}

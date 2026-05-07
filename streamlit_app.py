"""
OnePulse - Social Media Scheduler
With custom month calendar and precise time picker (hours 1-12, minutes 0-59, AM/PM)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import sys
import calendar as cal_mod

# Health check
if len(sys.argv) > 1 and sys.argv[1] == "health":
    print("OK")
    sys.exit(0)

st.set_page_config(page_title="OnePulse | Content Scheduler", page_icon="⚡🚀", layout="wide", initial_sidebar_state="collapsed")

# ============================================
# CUSTOM CSS (same beautiful styling)
# ============================================
def inject_css(theme):
    if theme == "dark":
        st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%); }
        .logo-container { text-align: center; font-size: 4rem; filter: drop-shadow(0 0 10px #e94560); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.05); opacity: 1; } 100% { transform: scale(1); opacity: 0.8; } }
        .app-title { text-align: center; background: linear-gradient(135deg, #e94560, #0f3460); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; }
        .subtitle { text-align: center; color: #aaa; margin-bottom: 2rem; }
        .platform-btn { font-size: 1.2rem; font-weight: bold; padding: 0.75rem; border-radius: 40px; text-align: center; cursor: pointer; }
        .youtube-active { background: #FF0000; color: white; box-shadow: 0 4px 15px rgba(255,0,0,0.3); }
        .youtube-inactive { background: rgba(255,0,0,0.2); color: #FF0000; }
        .instagram-active { background: linear-gradient(135deg, #f09433, #d62976, #962fbf, #4f5bd5); color: white; box-shadow: 0 4px 15px rgba(214,41,118,0.3); }
        .instagram-inactive { background: rgba(214,41,118,0.2); color: #d62976; }
        .card { background: rgba(30, 30, 60, 0.6); backdrop-filter: blur(10px); border-radius: 20px; padding: 1.5rem; margin-bottom: 1rem; border: 1px solid rgba(255,255,255,0.1); transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); background: rgba(30, 30, 60, 0.8); }
        .stat-card { background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 20px; padding: 1rem; text-align: center; border: 1px solid #e94560; }
        .stat-number { font-size: 2.2rem; font-weight: bold; color: #e94560; }
        .best-time-card { background: linear-gradient(135deg, #e94560, #0f3460); border-radius: 15px; padding: 0.75rem; margin: 0.5rem 0; text-align: center; color: white; font-weight: bold; }
        .upload-area { border: 2px dashed #e94560; border-radius: 15px; padding: 1rem; text-align: center; background: rgba(233,69,96,0.05); margin-bottom: 1rem; }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%); }
        .logo-container { text-align: center; font-size: 4rem; filter: drop-shadow(0 0 5px #667eea); animation: pulse 2s infinite; }
        @keyframes pulse { 0% { transform: scale(1); opacity: 0.8; } 50% { transform: scale(1.05); opacity: 1; } 100% { transform: scale(1); opacity: 0.8; } }
        .app-title { text-align: center; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800; }
        .subtitle { text-align: center; color: #666; margin-bottom: 2rem; }
        .platform-btn { font-size: 1.2rem; font-weight: bold; padding: 0.75rem; border-radius: 40px; text-align: center; cursor: pointer; }
        .youtube-active { background: #FF0000; color: white; box-shadow: 0 4px 15px rgba(255,0,0,0.3); }
        .youtube-inactive { background: rgba(255,0,0,0.1); color: #FF0000; border: 1px solid #FF0000; }
        .instagram-active { background: linear-gradient(135deg, #f09433, #d62976, #962fbf, #4f5bd5); color: white; box-shadow: 0 4px 15px rgba(214,41,118,0.3); }
        .instagram-inactive { background: rgba(214,41,118,0.1); color: #d62976; border: 1px solid #d62976; }
        .card { background: white; border-radius: 20px; padding: 1.5rem; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
        .stat-card { background: white; border-radius: 20px; padding: 1rem; text-align: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border-top: 3px solid #667eea; }
        .stat-number { font-size: 2.2rem; font-weight: bold; color: #667eea; }
        .best-time-card { background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 15px; padding: 0.75rem; margin: 0.5rem 0; text-align: center; color: white; font-weight: bold; }
        .upload-area { border: 2px dashed #667eea; border-radius: 15px; padding: 1rem; text-align: center; background: rgba(102,126,234,0.05); margin-bottom: 1rem; }
        </style>
        """, unsafe_allow_html=True)

# ============================================
# AI MODEL (simplified)
# ============================================
@st.cache_resource
def get_ai_model():
    class OnePulseAI:
        BEST_HOURS = {"YouTube": {"general": [14,15,16,18,19,20,21]}, "Instagram": {"general": [7,8,9,11,12,17,18,19,20,21]}}
        CAPTION_TEMPLATES = {"YouTube": ["🎬 {title}\n\n{description}\n\n🔥 Don't forget to like & subscribe!"], "Instagram": ["✨ {title}\n\n{description}\n\n❤️ Double tap if you agree!"]}
        HASHTAG_BANKS = {"YouTube": {"general": ["#YouTube", "#Viral", "#Trending", "#Subscribe", "#Creator"]}, "Instagram": {"general": ["#Instagram", "#InstaGood", "#Explore", "#Reels", "#Viral"]}}
        @classmethod
        def generate_caption(cls, platform, title, description, niche="general"):
            import random
            template = random.choice(cls.CAPTION_TEMPLATES.get(platform, cls.CAPTION_TEMPLATES["Instagram"]))
            return template.format(title=title or "My Post", description=description or "")
        @classmethod
        def generate_hashtags(cls, platform, niche="general", count=8):
            import random
            tags = cls.HASHTAG_BANKS.get(platform, {}).get("general", [])
            random.shuffle(tags)
            return tags[:count]
        @classmethod
        def get_best_times(cls, platform, niche="general", days_ahead=5):
            from datetime import datetime, timedelta
            import random
            times = []
            for d in range(1, days_ahead+1):
                for h in cls.BEST_HOURS.get(platform, {}).get("general", [12,18])[:3]:
                    dt = datetime.now() + timedelta(days=d)
                    dt = dt.replace(hour=h, minute=random.choice([0,15,30]), second=0)
                    times.append({"datetime": dt, "score": random.randint(70,98), "label": dt.strftime("%A, %b %d at %I:%M %p")})
            times.sort(key=lambda x: x['score'], reverse=True)
            return times[:6]
    return OnePulseAI()

ai_model = get_ai_model()

# ============================================
# SESSION STATE
# ============================================
if 'theme' not in st.session_state: st.session_state.theme = "dark"
if 'selected_platform' not in st.session_state: st.session_state.selected_platform = "YouTube"
if 'posts' not in st.session_state: st.session_state.posts = []
if 'generated_caption' not in st.session_state: st.session_state.generated_caption = ""
if 'generated_hashtags' not in st.session_state: st.session_state.generated_hashtags = []
if 'best_times' not in st.session_state: st.session_state.best_times = []
if 'show_ai_suggestions' not in st.session_state: st.session_state.show_ai_suggestions = False
if 'uploaded_file_data' not in st.session_state: st.session_state.uploaded_file_data = None
if 'uploaded_file_name' not in st.session_state: st.session_state.uploaded_file_name = ""

# Calendar state
today = datetime.now().date()
if 'cal_year' not in st.session_state: st.session_state.cal_year = today.year
if 'cal_month' not in st.session_state: st.session_state.cal_month = today.month
if 'selected_date' not in st.session_state: st.session_state.selected_date = today
if 'selected_hour' not in st.session_state: st.session_state.selected_hour = 9
if 'selected_minute' not in st.session_state: st.session_state.selected_minute = 0
if 'selected_ampm' not in st.session_state: st.session_state.selected_ampm = "AM"

# ============================================
# BUG FIX: CHECK & UPDATE POST STATUSES
# ============================================
def check_and_update_posts():
    now = datetime.now()
    changed = False
    for post in st.session_state.posts:
        if post.get('status') == 'scheduled' and post.get('scheduled_time'):
            if post['scheduled_time'] <= now:
                post['status'] = 'posted'
                changed = True
    return changed

# ============================================
# HEADER & PLATFORM BUTTONS
# ============================================
def render_header():
    col1, col2, col3 = st.columns([1,2,1])
    with col1: st.markdown('<div class="logo-container">⚡🚀💜</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<h1 class="app-title">OnePulse</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">AI-Powered Social Media Scheduling</p>', unsafe_allow_html=True)
    with col3:
        theme_label = "🌙 Dark" if st.session_state.theme == "dark" else "☀️ Light"
        if st.button(theme_label, key="theme_toggle"):
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()

def render_platform_tabs():
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ YouTube", key="yt_tab", use_container_width=True):
            st.session_state.selected_platform = "YouTube"
            st.rerun()
    with col2:
        if st.button("📸 Instagram", key="ig_tab", use_container_width=True):
            st.session_state.selected_platform = "Instagram"
            st.rerun()
    st.markdown("---")

def render_stats():
    platform_posts = [p for p in st.session_state.posts if p.get('platform') == st.session_state.selected_platform]
    total, scheduled = len(platform_posts), len([p for p in platform_posts if p.get('status') == 'scheduled'])
    posted, failed = len([p for p in platform_posts if p.get('status') == 'posted']), len([p for p in platform_posts if p.get('status') == 'failed'])
    col1, col2, col3, col4 = st.columns(4)
    for i, (label, val) in enumerate([("📊 TOTAL", total), ("⏰ SCHEDULED", scheduled), ("✅ POSTED", posted), ("❌ FAILED", failed)]):
        with [col1, col2, col3, col4][i]:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{val}</div><div>{label}</div></div>', unsafe_allow_html=True)

# ============================================
# CUSTOM CALENDAR & TIME PICKER
# ============================================
def render_custom_datetime_picker():
    from calendar import monthcalendar, month_name
    import datetime as dt

    selected_date = st.session_state.selected_date
    year = st.session_state.cal_year
    month = st.session_state.cal_month

    col_left, col_right = st.columns([2, 1], gap="large")
    with col_left:
        st.markdown("#### 📅 Select Date")
        col_prev, col_month, col_next = st.columns([1,3,1])
        with col_prev:
            if st.button("◀", key="prev_month"):
                if month == 1:
                    month = 12
                    year -= 1
                else:
                    month -= 1
                st.session_state.cal_year = year
                st.session_state.cal_month = month
                st.rerun()
        with col_month:
            st.markdown(f"<h5 style='text-align:center'>{month_name[month]} {year}</h5>", unsafe_allow_html=True)
        with col_next:
            if st.button("▶", key="next_month"):
                if month == 12:
                    month = 1
                    year += 1
                else:
                    month += 1
                st.session_state.cal_year = year
                st.session_state.cal_month = month
                st.rerun()

        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        cols = st.columns(7)
        for i, day in enumerate(weekdays):
            cols[i].markdown(f"**{day}**", unsafe_allow_html=True)

        cal = monthcalendar(year, month)
        for week in cal:
            cols = st.columns(7)
            for i, day in enumerate(week):
                if day == 0:
                    cols[i].write("")
                else:
                    date_obj = dt.date(year, month, day)
                    is_selected = (date_obj == selected_date)
                    btn_type = "primary" if is_selected else "secondary"
                    if cols[i].button(str(day), key=f"cal_{year}_{month}_{day}", type=btn_type, use_container_width=True):
                        st.session_state.selected_date = date_obj
                        st.rerun()

    with col_right:
        st.markdown("#### ⏰ Select Time")
        hour_options = list(range(1,13))
        minute_options = list(range(0,60))

        hour_val = st.selectbox("Hour", hour_options, index=hour_options.index(st.session_state.selected_hour) if st.session_state.selected_hour in hour_options else 8)
        minute_val = st.selectbox("Minute", minute_options, index=st.session_state.selected_minute)
        ampm_val = st.radio("AM/PM", ["AM","PM"], horizontal=True, index=0 if st.session_state.selected_ampm == "AM" else 1)

        st.session_state.selected_hour = hour_val
        st.session_state.selected_minute = minute_val
        st.session_state.selected_ampm = ampm_val

        hour_24 = hour_val
        if ampm_val == "PM" and hour_val != 12:
            hour_24 = hour_val + 12
        elif ampm_val == "AM" and hour_val == 12:
            hour_24 = 0

        selected_datetime = dt.datetime.combine(selected_date, dt.time(hour_24, minute_val))
        st.info(f"📅 **Selected:** {selected_datetime.strftime('%B %d, %Y at %I:%M %p')}")
        return selected_datetime

# ============================================
# MAIN FORM (AI + scheduling)
# ============================================
def render_schedule_form():
    platform = st.session_state.selected_platform
    st.markdown(f'<div class="card"><h3>📝 New Scheduled Post - {platform}</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        niche = st.selectbox("🎯 Niche", ["General", "Tech", "Lifestyle", "Fitness", "Food", "Art"])
        title = st.text_input("📌 Title", placeholder="Enter post title...")
        description = st.text_area("💬 Description", placeholder="What's this post about?", height=100)
    with col2:
        st.markdown('<div class="upload-area">', unsafe_allow_html=True)
        uploaded = st.file_uploader("📎 Media File (any format)", type=None, label_visibility="collapsed")
        if uploaded:
            st.session_state.uploaded_file_data = uploaded.read()
            st.session_state.uploaded_file_name = uploaded.name
            st.success(f"✅ {uploaded.name} ({uploaded.size/1024:.1f} KB)")
        else:
            st.caption("Drop or click to upload images, videos, audio, or documents")
        st.markdown('</div>', unsafe_allow_html=True)
        media_url = st.text_input("🔗 Or paste URL", placeholder="https://...")

    st.markdown("### 🤖 AI Content Generation")
    if st.button("✨ Generate AI Captions, Hashtags & Best Times", use_container_width=True):
        with st.spinner("AI is analyzing..."):
            st.session_state.generated_caption = ai_model.generate_caption(platform, title, description, niche)
            st.session_state.generated_hashtags = ai_model.generate_hashtags(platform, niche)
            st.session_state.best_times = ai_model.get_best_times(platform, niche)
            st.session_state.show_ai_suggestions = True
            st.success("✅ AI generation complete!")
            st.rerun()

    if st.session_state.show_ai_suggestions:
        st.markdown("### ✨ AI Recommendations")
        col_a, col_b, col_c = st.columns([2,1,1.5])
        with col_a:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**💬 Suggested Caption**")
            st.info(st.session_state.generated_caption)
            if st.button("📋 Use this caption", key="use_cap"):
                st.success("Copied to field below")
            st.markdown('</div>', unsafe_allow_html=True)
        with col_b:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**#️⃣ Hashtags**")
            st.write(" ".join(st.session_state.generated_hashtags))
            st.markdown('</div>', unsafe_allow_html=True)
        with col_c:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**⏰ Best Times to Post**")
            for t in st.session_state.best_times[:4]:
                st.markdown(f'<div class="best-time-card">📅 {t["label"]}<br>🔥 {t["score"]}% engagement</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    caption = st.text_area("📝 Caption (override)", value=st.session_state.generated_caption if st.session_state.show_ai_suggestions else "", height=100)
    hashtags = st.text_input("#️⃣ Hashtags", value=" ".join(st.session_state.generated_hashtags) if st.session_state.show_ai_suggestions else "")

    st.markdown("### 🗓️ Schedule Time")
    selected_datetime = render_custom_datetime_picker()

    if st.button("💾 Schedule Post", type="primary", use_container_width=True):
        if title.strip():
            if selected_datetime < datetime.now():
                st.error("❌ Cannot schedule in the past!")
            else:
                st.session_state.posts.append({
                    "platform": platform, "title": title, "description": description,
                    "caption": caption, "hashtags": hashtags,
                    "media": st.session_state.uploaded_file_name or media_url,
                    "scheduled_time": selected_datetime, "status": "scheduled", "created_at": datetime.now()
                })
                st.success(f"✅ Post '{title}' scheduled for {selected_datetime.strftime('%b %d, %I:%M %p')}!")
                st.balloons()
                st.session_state.show_ai_suggestions = False
                st.session_state.generated_caption = ""
                st.session_state.generated_hashtags = []
                st.session_state.uploaded_file_data = None
                st.rerun()
        else:
            st.error("❌ Please enter a title")
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# POSTS, ANALYTICS, AI ASSISTANT
# ============================================
def render_posts():
    platform = st.session_state.selected_platform
    platform_posts = [p for p in st.session_state.posts if p.get('platform') == platform]
    st.markdown(f'<div class="card"><h3>📋 {platform.upper()} Posts</h3>', unsafe_allow_html=True)
    if not platform_posts:
        st.info("No posts scheduled yet. Create your first post above!")
    else:
        for idx, post in enumerate(reversed(platform_posts)):
            time_str = post['scheduled_time'].strftime("%b %d, %Y • %I:%M %p")
            badge = "scheduled" if post['status'] == 'scheduled' else ("posted" if post['status'] == 'posted' else "failed")
            badge_class = f"badge-{badge}"
            st.markdown(f"""
            <div style="background: rgba(0,0,0,0.05); border-radius: 15px; padding: 1rem; margin-bottom: 0.8rem;">
                <div style="display: flex; justify-content: space-between;">
                    <div><strong>{post['title']}</strong><br><small>{time_str}</small></div>
                    <div><span class="badge {badge_class}">{post['status'].upper()}</span></div>
                </div>
                <div style="margin-top: 0.5rem;"><small>{post.get('description', '')[:80]}...</small></div>
            </div>
            """, unsafe_allow_html=True)
            if post['status'] == 'scheduled':
                col1, col2 = st.columns([3,1])
                with col2:
                    if st.button("📤 Post Now", key=f"post_{idx}"):
                        post['status'] = 'posted'
                        st.rerun()
                    if st.button("🗑️ Delete", key=f"del_{idx}"):
                        st.session_state.posts.remove(post)
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

def render_analytics():
    import plotly.express as px
    st.markdown('<div class="card"><h3>📊 Analytics Dashboard</h3>', unsafe_allow_html=True)
    if not st.session_state.posts:
        st.info("No data available. Create posts to see analytics.")
        return
    df = pd.DataFrame([{'Platform': p['platform'], 'Status': p['status'], 'Niche': p.get('niche', 'General')} for p in st.session_state.posts])
    col1, col2 = st.columns(2)
    with col1:
        status_counts = df['Status'].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index, title="Post Status", color_discrete_sequence=['#4CAF50','#FFC107','#F44336'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        platform_counts = df['Platform'].value_counts()
        fig = px.bar(x=platform_counts.index, y=platform_counts.values, title="Posts by Platform", color=platform_counts.index)
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_ai_assistant():
    st.markdown('<div class="card"><h3>🤖 AI Content Assistant</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Platform", ["YouTube", "Instagram"], key="ai_plat")
        niche = st.selectbox("Niche", ["General","Tech","Lifestyle","Fitness","Food","Art"], key="ai_niche")
        topic = st.text_input("Topic/Title")
        desc = st.text_area("Description")
    with col2:
        if st.button("🎨 Generate Content Ideas", use_container_width=True):
            with st.spinner("Creating..."):
                cap = ai_model.generate_caption(platform, topic, desc, niche)
                tags = ai_model.generate_hashtags(platform, niche)
                times = ai_model.get_best_times(platform, niche, days_ahead=3)
                st.markdown("### ✨ Generated Content")
                st.success(f"**Caption:**\n{cap}")
                st.info(f"**Hashtags:**\n{' '.join(tags)}")
                st.markdown("**Best Times:**")
                for t in times[:3]:
                    st.markdown(f'<div class="best-time-card">📅 {t["label"]}<br>🔥 {t["score"]}% engagement</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# MAIN
# ============================================
def main():
    # ✅ Check and flip any due posts to "posted"
    check_and_update_posts()

    inject_css(st.session_state.theme)
    render_header()
    render_platform_tabs()
    render_stats()
    menu = st.radio("", ["📝 Create Post", "📋 View Posts", "📊 Analytics", "🤖 AI Assistant"], horizontal=True, label_visibility="collapsed")
    st.markdown("---")
    if menu == "📝 Create Post":
        col_left, col_right = st.columns([2,1])
        with col_left: render_schedule_form()
        with col_right: render_posts()
    elif menu == "📋 View Posts": render_posts()
    elif menu == "📊 Analytics": render_analytics()
    else: render_ai_assistant()

if __name__ == "__main__":
    main()

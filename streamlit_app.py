OnePulse - Beautiful Social Media Scheduler
With platform logos and innovative app icon
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
@@ -17,233 +18,54 @@
st.set_page_config(page_title="OnePulse | Content Scheduler", page_icon="⚡🚀", layout="wide", initial_sidebar_state="collapsed")

# ============================================
# CUSTOM CSS WITH LOGO STYLES
# CUSTOM CSS (same beautiful styling)
# ============================================
def inject_css(theme):
    if theme == "dark":
        st.markdown("""
        <style>
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
        .stApp {
            background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
        }
        .logo-container {
            text-align: center;
            font-size: 4rem;
            filter: drop-shadow(0 0 10px #e94560);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); opacity: 0.8; }
        }
        .app-title {
            text-align: center;
            background: linear-gradient(135deg, #e94560, #0f3460);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            margin-top: -0.5rem;
        }
        .subtitle {
            text-align: center;
            color: #aaa;
            margin-bottom: 2rem;
        }
        .platform-btn {
            font-size: 1.2rem;
            font-weight: bold;
            padding: 0.75rem;
            border-radius: 40px;
            transition: all 0.3s;
            cursor: pointer;
            text-align: center;
        }
        .youtube-active {
            background: #FF0000;
            color: white;
            box-shadow: 0 4px 15px rgba(255,0,0,0.3);
        }
        .youtube-inactive {
            background: rgba(255,0,0,0.2);
            color: #FF0000;
        }
        .instagram-active {
            background: linear-gradient(135deg, #f09433, #d62976, #962fbf, #4f5bd5);
            color: white;
            box-shadow: 0 4px 15px rgba(214,41,118,0.3);
        }
        .instagram-inactive {
            background: rgba(214,41,118,0.2);
            color: #d62976;
        }
        .card {
            background: rgba(30, 30, 60, 0.6);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255,255,255,0.1);
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-5px);
            background: rgba(30, 30, 60, 0.8);
        }
        .stat-card {
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border-radius: 20px;
            padding: 1rem;
            text-align: center;
            border: 1px solid #e94560;
        }
        .stat-number {
            font-size: 2.2rem;
            font-weight: bold;
            color: #e94560;
        }
        .badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
        }
        .badge-scheduled { background: #ffc107; color: #1a1a2e; }
        .badge-posted { background: #4caf50; color: white; }
        .badge-failed { background: #f44336; color: white; }
        .best-time-card {
            background: linear-gradient(135deg, #e94560, #0f3460);
            border-radius: 15px;
            padding: 0.75rem;
            margin: 0.5rem 0;
            text-align: center;
            color: white;
            font-weight: bold;
        }
        .upload-area {
            border: 2px dashed #e94560;
            border-radius: 15px;
            padding: 1rem;
            text-align: center;
            background: rgba(233,69,96,0.05);
            margin-bottom: 1rem;
        }
        hr {
            border-color: rgba(255,255,255,0.1);
        }
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
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        }
        .logo-container {
            text-align: center;
            font-size: 4rem;
            filter: drop-shadow(0 0 5px #667eea);
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; }
            100% { transform: scale(1); opacity: 0.8; }
        }
        .app-title {
            text-align: center;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            margin-top: -0.5rem;
        }
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
        .platform-btn {
            font-size: 1.2rem;
            font-weight: bold;
            padding: 0.75rem;
            border-radius: 40px;
            transition: all 0.3s;
            cursor: pointer;
            text-align: center;
        }
        .youtube-active {
            background: #FF0000;
            color: white;
            box-shadow: 0 4px 15px rgba(255,0,0,0.3);
        }
        .youtube-inactive {
            background: rgba(255,0,0,0.1);
            color: #FF0000;
            border: 1px solid #FF0000;
        }
        .instagram-active {
            background: linear-gradient(135deg, #f09433, #d62976, #962fbf, #4f5bd5);
            color: white;
            box-shadow: 0 4px 15px rgba(214,41,118,0.3);
        }
        .instagram-inactive {
            background: rgba(214,41,118,0.1);
            color: #d62976;
            border: 1px solid #d62976;
        }
        .card {
            background: white;
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        }
        .stat-card {
            background: white;
            border-radius: 20px;
            padding: 1rem;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            border-top: 3px solid #667eea;
        }
        .stat-number {
            font-size: 2.2rem;
            font-weight: bold;
            color: #667eea;
        }
        .best-time-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 15px;
            padding: 0.75rem;
            margin: 0.5rem 0;
            text-align: center;
            color: white;
            font-weight: bold;
        }
        .upload-area {
            border: 2px dashed #667eea;
            border-radius: 15px;
            padding: 1rem;
            text-align: center;
            background: rgba(102,126,234,0.05);
            margin-bottom: 1rem;
        }
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
# AI MODEL (same as before, but kept concise)
# AI MODEL (simplified)
# ============================================
@st.cache_resource
def get_ai_model():
@@ -291,13 +113,21 @@ def get_best_times(cls, platform, niche="general", days_ahead=5):
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
# HEADER WITH INNOVATIVE LOGO
# HEADER & PLATFORM BUTTONS
# ============================================
def render_header():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown("""<div class="logo-container">⚡🚀💜</div>""", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1,2,1])
    with col1: st.markdown('<div class="logo-container">⚡🚀💜</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<h1 class="app-title">OnePulse</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">AI-Powered Social Media Scheduling</p>', unsafe_allow_html=True)
@@ -307,42 +137,112 @@ def render_header():
            st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"
            st.rerun()

# ============================================
# PLATFORM BUTTONS WITH LOGOS
# ============================================
def render_platform_tabs():
    col1, col2 = st.columns(2)
    with col1:
        active = (st.session_state.selected_platform == "YouTube")
        btn_class = "youtube-active" if active else "youtube-inactive"
        if st.button(f"▶️ YouTube", key="yt_tab", use_container_width=True):
        if st.button("▶️ YouTube", key="yt_tab", use_container_width=True):
            st.session_state.selected_platform = "YouTube"
            st.rerun()
    with col2:
        active = (st.session_state.selected_platform == "Instagram")
        btn_class = "instagram-active" if active else "instagram-inactive"
        if st.button(f"📸 Instagram", key="ig_tab", use_container_width=True):
        if st.button("📸 Instagram", key="ig_tab", use_container_width=True):
            st.session_state.selected_platform = "Instagram"
            st.rerun()
    st.markdown("---")

# ============================================
# STATS CARDS
# ============================================
def render_stats():
    platform_posts = [p for p in st.session_state.posts if p.get('platform') == st.session_state.selected_platform]
    total = len(platform_posts)
    scheduled = len([p for p in platform_posts if p.get('status') == 'scheduled'])
    posted = len([p for p in platform_posts if p.get('status') == 'posted'])
    failed = len([p for p in platform_posts if p.get('status') == 'failed'])
    total, scheduled = len(platform_posts), len([p for p in platform_posts if p.get('status') == 'scheduled'])
    posted, failed = len([p for p in platform_posts if p.get('status') == 'posted']), len([p for p in platform_posts if p.get('status') == 'failed'])
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.markdown(f'<div class="stat-card"><div class="stat-number">{total}</div><div>📊 TOTAL</div></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="stat-card"><div class="stat-number">{scheduled}</div><div>⏰ SCHEDULED</div></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="stat-card"><div class="stat-number">{posted}</div><div>✅ POSTED</div></div>', unsafe_allow_html=True)
    with col4: st.markdown(f'<div class="stat-card"><div class="stat-number">{failed}</div><div>❌ FAILED</div></div>', unsafe_allow_html=True)
    for i, (label, val) in enumerate([("📊 TOTAL", total), ("⏰ SCHEDULED", scheduled), ("✅ POSTED", posted), ("❌ FAILED", failed)]):
        with [col1, col2, col3, col4][i]:
            st.markdown(f'<div class="stat-card"><div class="stat-number">{val}</div><div>{label}</div></div>', unsafe_allow_html=True)

# ============================================
# MAIN FORM (condensed but complete)
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
        # Month navigation
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

        # Weekday headers
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        cols = st.columns(7)
        for i, day in enumerate(weekdays):
            cols[i].markdown(f"**{day}**", unsafe_allow_html=True)

        # Day buttons
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
@@ -363,6 +263,7 @@ def render_schedule_form():
            st.caption("Drop or click to upload images, videos, audio, or documents")
        st.markdown('</div>', unsafe_allow_html=True)
        media_url = st.text_input("🔗 Or paste URL", placeholder="https://...")

    st.markdown("### 🤖 AI Content Generation")
    if st.button("✨ Generate AI Captions, Hashtags & Best Times", use_container_width=True):
        with st.spinner("AI is analyzing..."):
@@ -372,6 +273,7 @@ def render_schedule_form():
            st.session_state.show_ai_suggestions = True
            st.success("✅ AI generation complete!")
            st.rerun()

    if st.session_state.show_ai_suggestions:
        st.markdown("### ✨ AI Recommendations")
        col_a, col_b, col_c = st.columns([2,1,1.5])
@@ -393,34 +295,37 @@ def render_schedule_form():
            for t in st.session_state.best_times[:4]:
                st.markdown(f'<div class="best-time-card">📅 {t["label"]}<br>🔥 {t["score"]}% engagement</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    caption = st.text_area("📝 Caption (override)", value=st.session_state.generated_caption if st.session_state.show_ai_suggestions else "", height=100)
    hashtags = st.text_input("#️⃣ Hashtags", value=" ".join(st.session_state.generated_hashtags) if st.session_state.show_ai_suggestions else "")

    st.markdown("### 🗓️ Schedule Time")
    col_d, col_e = st.columns(2)
    with col_d: schedule_date = st.date_input("Date", datetime.now(), min_value=datetime.now().date())
    with col_e: schedule_time = st.time_input("Time", datetime.now().time())
    selected_datetime = render_custom_datetime_picker()

    if st.button("💾 Schedule Post", type="primary", use_container_width=True):
        if title.strip():
            scheduled = datetime.combine(schedule_date, schedule_time)
            st.session_state.posts.append({
                "platform": platform, "title": title, "description": description,
                "caption": caption, "hashtags": hashtags,
                "media": st.session_state.uploaded_file_name or media_url,
                "scheduled_time": scheduled, "status": "scheduled", "created_at": datetime.now()
            })
            st.success(f"✅ Post '{title}' scheduled for {scheduled.strftime('%b %d, %I:%M %p')}!")
            st.balloons()
            st.session_state.show_ai_suggestions = False
            st.session_state.generated_caption = ""
            st.session_state.generated_hashtags = []
            st.session_state.uploaded_file_data = None
            st.rerun()
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
# POSTS DISPLAY
# POSTS, ANALYTICS, AI ASSISTANT (keep same as before)
# ============================================
def render_posts():
    platform = st.session_state.selected_platform
@@ -453,9 +358,6 @@ def render_posts():
                        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# ANALYTICS
# ============================================
def render_analytics():
    import plotly.express as px
    st.markdown('<div class="card"><h3>📊 Analytics Dashboard</h3>', unsafe_allow_html=True)
@@ -474,9 +376,6 @@ def render_analytics():
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# AI ASSISTANT
# ============================================
def render_ai_assistant():
    st.markdown('<div class="card"><h3>🤖 AI Content Assistant</h3>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

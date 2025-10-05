# app.py
import streamlit as st
from datetime import datetime, date
import json
import os
import random
from pathlib import Path

# ---------- CONFIG ----------
DATA_DIR = Path("data")
PHOTOS_DIR = DATA_DIR / "photos"
DATA_FILE = DATA_DIR / "data.json"
ALLOWED_USERS = ["you", "him"]  # conceptually - only two persons expected

# Make directories if not exist
DATA_DIR.mkdir(exist_ok=True)
PHOTOS_DIR.mkdir(exist_ok=True)

# ---------- DEFAULT DATA ----------
DEFAULT_DATA = {
    "timeline": [
        {"date": "2024-08-01", "title": "We Met", "desc": "That day at the coffee shop ☕", "photo": None},
        {"date": "2024-09-10", "title": "First Date", "desc": "Movie + fries 🍟", "photo": None}
    ],
    "love_notes": [
        "I love the way you smile.",
        "You're my favorite notification.",
        "You make ordinary days special."
    ],
    "daily_messages": [
        {"date": "2025-10-01", "message": "Good morning, love!"},
        {"date": "2025-10-02", "message": "Remember our first silly dance?"}
    ],
    "journal": [],
    "last_unlocked": None
}

# ---------- UTILITIES ----------
def load_data():
    if not DATA_FILE.exists():
        save_data(DEFAULT_DATA)
        return DEFAULT_DATA.copy()
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(d):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(d, f, indent=2, ensure_ascii=False)

data = load_data()

# ---------- AUTH ----------
def check_passphrase(entered):
    # Use secret from st.secrets; default fallback for local dev is "love"
    secret = st.secrets.get("PASS", "love")
    return entered == secret

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.set_page_config(page_title="For You ♥", page_icon="💌", layout="centered")

# Login UI
if not st.session_state.authenticated:
    st.title("A little world for you two 💖")
    st.write("Enter the shared passphrase to enter our secret space.")
    entered = st.text_input("Passphrase", type="password")
    if st.button("Enter"):
        if check_passphrase(entered):
            st.session_state.authenticated = True
            st.experimental_rerun()
        else:
            st.error("Hmm — passphrase not correct. Try again.")
    st.stop()

# ---------- APP LAYOUT ----------
st.sidebar.title("Menu")
page = st.sidebar.radio("Go to", ["Home", "Our Story", "Photos", "Love Notes", "Daily Unlock", "Journal", "Surprises", "Fun & Quiz", "Settings"])

# ---------- HOME ----------
if page == "Home":
    st.header("Welcome, lovebirds 💞")
    st.write("This little app is made by me — for you. Explore, laugh, cry, and press hearts.")
    st.write("Hover through the menu on the left to find special things.")
    if st.button("Celebrate 🎉"):
        st.balloons()
    # Quick peek: show next timeline event
    upcoming = sorted(data.get("timeline", []), key=lambda x: x["date"])
    if upcoming:
        st.subheader("Next memory")
        ev = upcoming[-1]
        st.markdown(f"**{ev['title']}** — {ev['date']}")
        st.write(ev.get("desc", ""))

# ---------- OUR STORY ----------
elif page == "Our Story":
    st.header("Our Story — timeline")
    st.write("Add milestones and memories here.")
    col1, col2 = st.columns([3,1])
    with col1:
        for idx, item in enumerate(sorted(data.get("timeline", []), key=lambda x: x["date"], reverse=True)):
            st.subheader(item["title"] + " — " + item["date"])
            if item.get("photo"):
                try:
                    st.image(str(Path(item["photo"])), use_column_width=True)
                except Exception:
                    pass
            st.write(item.get("desc", ""))
            st.markdown("---")
    with col2:
        st.write("Add new memory")
        t_date = st.date_input("Date", value=date.today(), key="t_date")
        t_title = st.text_input("Title", key="t_title")
        t_desc = st.text_area("Short note / description", key="t_desc", height=120)
        t_photo = st.file_uploader("Upload an optional photo", type=["png","jpg","jpeg"], key="t_photo")
        if st.button("Save memory"):
            entry = {"date": t_date.isoformat(), "title": t_title or "Untitled", "desc": t_desc or "", "photo": None}
            if t_photo:
                fname = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{t_photo.name}"
                path = PHOTOS_DIR / fname
                with open(path, "wb") as f:
                    f.write(t_photo.getbuffer())
                entry["photo"] = str(path)
            data.setdefault("timeline", []).append(entry)
            save_data(data)
            st.success("Memory saved! It will appear on the left.")
            st.experimental_rerun()

# ---------- PHOTOS ----------
elif page == "Photos":
    st.header("Photos — our favorite moments 📸")
    st.write("Upload photos and browse them like an album.")
    uploaded = st.file_uploader("Upload one or more photos", accept_multiple_files=True, type=["png","jpg","jpeg"])
    if uploaded:
        for f in uploaded:
            fname = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{f.name}"
            path = PHOTOS_DIR / fname
            with open(path, "wb") as out:
                out.write(f.getbuffer())
            # Optionally register in timeline? skip to keep simple
        st.success(f"Saved {len(uploaded)} photo(s).")
        st.experimental_rerun()
    images = list(PHOTOS_DIR.glob("*"))
    if images:
        st.write("Tap to view larger")
        cols = st.columns(3)
        for i, img_path in enumerate(sorted(images, reverse=True)):
            try:
                with open(img_path, "rb") as f:
                    bytes_data = f.read()
                cols[i % 3].image(bytes_data, use_column_width=True)
            except Exception:
                pass
    else:
        st.info("No photos yet — upload a few to start filling this album.")

# ---------- LOVE NOTES ----------
elif page == "Love Notes":
    st.header("Love Notes ♥")
    st.write("A tiny generator of silly / sweet things I love about you.")
    add_note = st.text_input("Add a custom love note (optional)")
    if st.button("Add note"):
        if add_note.strip():
            data.setdefault("love_notes", []).append(add_note.strip())
            save_data(data)
            st.success("Added your note.")
            st.experimental_rerun()
    if st.button("Get a random love note"):
        notes = data.get("love_notes", [])
        if notes:
            st.markdown(f"### {random.choice(notes)}")
            st.write("Press again for another one.")
        else:
            st.info("No notes yet — add one!")

# ---------- DAILY UNLOCK ----------
elif page == "Daily Unlock":
    st.header("Daily Unlock 🔓")
    st.write("A new tiny message or memory you can unlock once a day.")
    today_str = date.today().isoformat()
    last = data.get("last_unlocked")
    if last == today_str:
        st.info("Today's secret is already unlocked. Come back tomorrow for another one.")
    else:
        if st.button("Unlock today's message"):
            # Return a random daily or love note
            pool = data.get("daily_messages", []) + [{"date": today_str, "message": random.choice(data.get("love_notes", ["You are my everything."]))}]
            picked = random.choice(pool)
            st.success("Unlocked ✨")
            st.write(picked.get("message", "A little hello from me"))
            data["last_unlocked"] = today_str
            save_data(data)

# ---------- JOURNAL ----------
elif page == "Journal":
    st.header("Shared Journal / Notes 📔")
    st.write("Write little notes for each other. This is private to us.")
    with st.form("entry_form"):
        author = st.selectbox("You are:", ["Me", "You (him)"])
        entry_text = st.text_area("Write something", height=150)
        add_photo = st.file_uploader("Optional photo for this entry", type=["png","jpg","jpeg"])
        submitted = st.form_submit_button("Save entry")
        if submitted:
            item = {"author": author, "text": entry_text, "date": datetime.now().isoformat(), "photo": None}
            if add_photo:
                fname = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{add_photo.name}"
                path = PHOTOS_DIR / fname
                with open(path, "wb") as f:
                    f.write(add_photo.getbuffer())
                item["photo"] = str(path)
            data.setdefault("journal", []).append(item)
            save_data(data)
            st.success("Saved! Your note is safe here.")
            st.experimental_rerun()
    st.write("---")
    for j in sorted(data.get("journal", []), key=lambda x: x["date"], reverse=True):
        st.write(f"**{j['author']}** — {j['date']}")
        st.write(j["text"])
        if j.get("photo"):
            try:
                st.image(j["photo"], use_column_width=True)
            except Exception:
                pass
        st.markdown("---")

# ---------- SURPRISES ----------
elif page == "Surprises":
    st.header("Surprises 🎁")
    st.write("A place for voice notes, video links, and hidden things.")
    st.write("Upload a voice note or audio clip that will play here.")
    audio_file = st.file_uploader("Upload audio (mp3, wav)", type=["mp3","wav"])
    if audio_file:
        afname = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{audio_file.name}"
        path = DATA_DIR / afname
        with open(path, "wb") as f:
            f.write(audio_file.getbuffer())
        st.success("Saved audio!")
        st.audio(path)
    # Hidden message (password-protected reveal)
    st.write("---")
    st.write("Secret message (protected). Only reveal if you trust the moment ❤️")
    secret_key = st.text_input("Enter the small secret to reveal (hint: our special place)", type="password")
    if st.button("Reveal secret message"):
        if secret_key == st.secrets.get("REVEAL", "italian"):
            st.success("I miss you more than pizza. Always.")
        else:
            st.error("Not the right secret.")

# ---------- FUN & QUIZ ----------
elif page == "Fun & Quiz":
    st.header("Fun & Quiz 🎲")
    st.write("Tiny games to laugh together.")
    if st.button("Spin the Wheel of Cute"):
        options = ["Back hug", "Movie night", "You pick dessert", "I cook", "One long phone call", "You get a surprise"]
        choice = random.choice(options)
        st.success(f"The wheel says: **{choice}**")
    st.write("---")
    st.subheader("How well do you know Mansi? (fun)")
    q = st.radio("What is Mansi's favorite snack?", ["Chips", "Chocolate", "Fruit", "Samosa"])
    if st.button("Answer"):
        if q == "Chocolate":
            st.success("Correct! She loves chocolate 💝")
        else:
            st.error("Close, but not quite — ask her to find out!")

# ---------- SETTINGS ----------
elif page == "Settings":
    st.header("Settings & Help 🔧")
    st.write("Admin options and help for deploying or changing passphrase.")
    if st.button("Show deployment & security tips"):
        st.info("Deployment & security tips are shown below.")
        st.markdown("""
        - Keep this GitHub repo **private**.
        - Set `PASS` in Streamlit secrets (app settings) to change the shared passphrase.
        - To revoke access, change the passphrase immediately.
        - Use Streamlit Cloud for easy deployment; it provides SSL.
        - For persistent multi-device syncing consider using Google Sheets or Firebase for storage (instructions available if you want).
        """)
    if "debug" not in st.session_state:
        st.session_state.debug = False
    if st.checkbox("Show debug data (only on your machine)", value=False):
        st.json(data)

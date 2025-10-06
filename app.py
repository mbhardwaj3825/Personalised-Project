# app.py
import streamlit as st
import json
import random
import time
from datetime import datetime
from pathlib import Path
import os

# ---------- CONFIG ----------
st.set_page_config(page_title="For My Anjuuu 💙", layout="wide")
PASSCODE = "Iloveyouladuu"

# ---------- DATA FOLDERS ----------
ROOT = Path(".")
DATA_DIR = ROOT / "data"
PHOTOS_DIR = DATA_DIR / "photos"
DATA_DIR.mkdir(exist_ok=True)
PHOTOS_DIR.mkdir(parents=True, exist_ok=True)

def ensure_json(name, default):
    path = DATA_DIR / name
    if not path.exists() or path.stat().st_size == 0:
        path.write_text(json.dumps(default, ensure_ascii=False, indent=2))
ensure_json("notes.json", [])
ensure_json("songs.json", [])
ensure_json("timeline.json", [])

def read_json(name):
    p = DATA_DIR / name
    try:
        return json.loads(p.read_text())
    except Exception:
        return []

def write_json(name, data):
    (DATA_DIR / name).write_text(json.dumps(data, ensure_ascii=False, indent=2))

# ---------- CSS / ROMANTIC BACKGROUND ----------
st.markdown(
    """
    <style>
    :root {
      --accent1: #66aaff;
      --accent2: #3b7df0;
      --card-bg: rgba(255,255,255,0.78);
      --text: #0b2b57;
    }
    html, body, .stApp, .main { height: 100%; }
    .stApp {
      background: linear-gradient(135deg, #b3e5fc 0%, #d6c8f8 45%, #bfe0ff 100%);
      background-attachment: fixed;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial;
      color: var(--text);
      overflow-x: hidden;
    }
    /* faint animated hearts overlay image (very subtle) */
    body::before {
      content: "";
      background-image: url('https://i.imgur.com/Z1r5NnH.png');
      background-repeat: repeat;
      background-size: 100px;
      opacity: 0.12;
      position: fixed;
      inset: 0;
      z-index: -1;
      animation: floatBg 18s linear infinite;
    }
    @keyframes floatBg { from {background-position: 0 0;} to {background-position: 0 200px;} }

    .card {
      background: var(--card-bg);
      padding: 18px;
      border-radius: 14px;
      margin-bottom: 14px;
      box-shadow: 0 8px 30px rgba(10,20,50,0.08);
      border: 1px solid rgba(0,0,0,0.04);
    }

    h1,h2,h3 { color: var(--text); margin-bottom:6px; }
    .small-muted { color: rgba(11,43,87,0.7); }

    /* wheel styles */
    .wheel-wrap { display:flex; flex-direction:column; align-items:center; }
    .pointer { width:0; height:0; border-left:18px solid transparent; border-right:18px solid transparent; border-bottom:28px solid #0b3a86; margin-bottom:8px; transform: translateY(8px); }
    .wheel {
      width: 320px; height:320px; border-radius:50%; position: relative; overflow:hidden;
      box-shadow: 0 10px 40px rgba(0,0,0,0.12); border: 8px solid rgba(11,58,142,0.12);
      transform: rotate(0deg);
    }
    .slice {
      position:absolute; left:50%; top:50%; transform-origin:0% 0%;
      width:50%; height:50%;
      display:flex; align-items:center; justify-content:flex-end; padding-right:12px;
      color:white; font-weight:700; text-shadow: 0 2px 6px rgba(0,0,0,0.18);
    }
    .slice span { display:block; width:160px; text-align:right; transform: skewY(-30deg); font-size:14px; padding-right:6px; }
    /* polaroid look for images (fallback) */
    .polaroid { background:#fff; padding:12px 12px 16px; display:inline-block; margin:10px; border-radius:8px; box-shadow:0 8px 30px rgba(2,8,30,0.08); transform: rotate(-1deg); }
    .polaroid img{ width:220px; height:160px; object-fit:cover; border-radius:6px; display:block; margin-bottom:8px; }
    .polaroid .cap{ color:#0e2340; font-weight:600; font-size:14px; text-align:center;}
    .stButton>button { background: linear-gradient(90deg,var(--accent1),var(--accent2)); color:white; border:none; padding:10px 14px; border-radius:10px; font-weight:600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- AUTH (passcode) ----------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "passcode_input" not in st.session_state:
    st.session_state.passcode_input = ""

def show_passcode():
    st.markdown("<div style='max-width:820px;margin:28px auto;'>", unsafe_allow_html=True)
    st.markdown("<div class='card' style='text-align:center;'>", unsafe_allow_html=True)
    st.markdown("<h1>A little world — just for you 🫀</h1>", unsafe_allow_html=True)
    st.markdown("<p class='small-muted'>Enter the secret passcode to open our private space</p>", unsafe_allow_html=True)
    st.session_state.passcode_input = st.text_input("Passcode", type="password", key="pass")
    if st.button("Unlock 💙"):
        if st.session_state.passcode_input == PASSCODE:
            st.session_state.authenticated = True
            st.success("Unlocked — welcome 💙")
            time.sleep(0.5)
            st.experimental_rerun()
        else:
            st.error("That's not the correct passcode. Try again 💫")
    st.markdown("</div></div>", unsafe_allow_html=True)

if not st.session_state.authenticated:
    show_passcode()
    st.stop()

# ---------- SIDEBAR NAV ----------
st.sidebar.title("💫 Navigate")
page = st.sidebar.radio("", [
    "Home 🏠",
    "Today's Thought 💭",
    "Click if you miss me 💞",
    "Our Songs 🎶",
    "Spin the Wheel 💕",
    "Reasons I Love You 💌",
    "Photos & Polaroids 📸",
    "Our Story Timeline 🕰️",
    "Settings ⚙️"
])

# ---------- PAGES ----------
if page == "Home 🏠":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.title("Welcome, my love 🫀")
    st.write("This little corner was made with care — add memories, songs, and notes. It's private and just for us.")
    st.markdown("</div>", unsafe_allow_html=True)

# Today's Thought
elif page == "Today's Thought 💭":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("💭 Today's Thought")
    notes = read_json("notes.json")
    with st.form("note_form"):
        author = st.selectbox("Who is writing?", ["Me", "Him"])
        text = st.text_area("Write your thought...", height=140)
        lock = st.text_input("Optional entry-password (keeps it private)", type="password")
        submitted = st.form_submit_button("Save Thought 💌")
        if submitted and text.strip():
            notes.append({"author": author, "text": text.strip(), "date": datetime.now().isoformat(), "locked": bool(lock.strip()), "pwd": lock.strip()})
            write_json("notes.json", notes)
            st.success("Saved 💙")
    st.write("---")
    st.subheader("Past thoughts")
    for entry in reversed(notes):
        if entry.get("locked"):
            st.markdown(f"**{entry['author']}** — {entry['date']}")
            # Reveal button for locked entries
            key = f"rev_{entry['date']}"
            if st.button("Reveal (locked) — enter password", key=key):
                pw = st.text_input("Enter password to reveal", key=f"pw_{key}", type="password")
                if pw == entry.get("pwd"):
                    st.info(entry["text"])
                else:
                    st.warning("Wrong password")
        else:
            st.markdown(f"**{entry['author']}** — {entry['date']}")
            st.write(entry["text"])
    st.markdown("</div>", unsafe_allow_html=True)

# Click if you miss me
elif page == "Click if you miss me 💞":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Click only if you miss me 💞")
    st.write("A little surprise — voice note or message.")
    if st.button("Click only if you miss me 😘"):
        st.success("I miss you so much — counting the moments until I see you again. 🫀")
        voice_path = DATA_DIR / "voice.mp3"
        if voice_path.exists():
            st.audio(str(voice_path))
        else:
            st.info("No voice note uploaded yet. Upload one in Settings.")
    st.markdown("</div>", unsafe_allow_html=True)

# Our Songs
elif page == "Our Songs 🎶":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Our Songs 🎶")
    songs = read_json("songs.json")
    if not songs:
        st.info("No songs added yet. Add songs in Settings.")
    else:
        for s in songs:
            st.markdown(f"**{s.get('title','Untitled')}** — <span class='small-muted'>{s.get('note','')}</span>", unsafe_allow_html=True)
            if s.get("link"):
                st.markdown(f"[Listen]({s.get('link')})")
            st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

# Spin the Wheel (animated)
elif page == "Spin the Wheel 💕":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Spin the Wheel of Love 🎡")
    options = [
        "You get a tight hug 🤗",
        "Movie night 🍿",
        "You owe me ice cream 🍦",
        "You pick dessert 🍰",
        "A forehead kiss 💋",
        "One long cuddle session 💞",
        "I’ll cook your favorite meal 🍛",
        "You get a surprise gift 🎁"
    ]

    n = len(options)
    seg = 360 / n

    # Show pointer and idle wheel (static)
    st.markdown("<div style='display:flex; flex-direction:column; align-items:center;'>", unsafe_allow_html=True)
    st.markdown("<div class='pointer'></div>", unsafe_allow_html=True)

    # When user clicks spin, compute chosen & rotation, render animated wheel and show result after wait
    if st.button("Spin 🎡"):
        chosen_idx = random.randrange(n)
        spins = random.randint(4, 7)
        center_angle = chosen_idx * seg + seg / 2
        offset = random.uniform(-seg/6, seg/6)
        rotation_deg = spins * 360 + (360 - center_angle) + offset

        uid = random.randint(100000, 999999)
        wheel_id = f"wheel_{uid}"

        # build slices HTML
        slice_html = ""
        colors = ["#3b82f6", "#60a5fa"]
        for i, label in enumerate(options):
            rot = i * seg
            color = colors[i % len(colors)]
            slice_html += f"<div class='slice' style='transform: rotate({rot}deg) translate(-50%, -100%);'><span style='background:{color}; padding:18px 8px;'>{label}</span></div>"

        wheel_html = f"""
        <div style='width:360px; height:360px; display:flex; align-items:center; justify-content:center;'>
          <div id="{wheel_id}" class='wheel' style='transform: rotate(0deg);'>
            {slice_html}
          </div>
        </div>
        <script>
        (function(){{
            const wheel = document.getElementById("{wheel_id}");
            setTimeout(function(){{
                wheel.style.transition = 'transform 4s cubic-bezier(0.33, 1, 0.68, 1)';
                wheel.style.transform = 'rotate({rotation_deg}deg)';
            }}, 80);
        }})();
        </script>
        """
        st.markdown(wheel_html, unsafe_allow_html=True)

        # wait for the animation to end on Python side, then show result
        time.sleep(4.2)
        st.success(f"Result: {options[chosen_idx]}")
    else:
        # idle wheel (static)
        uid = random.randint(100000, 999999)
        wheel_id = f"wheel_static_{uid}"
        slice_html = ""
        colors = ["#3b82f6", "#60a5fa"]
        for i, label in enumerate(options):
            rot = i * seg
            color = colors[i % len(colors)]
            slice_html += f"<div class='slice' style='transform: rotate({rot}deg) translate(-50%, -100%);'><span style='background:{color}; padding:18px 8px;'>{label}</span></div>"
        wheel_static = f"""
        <div style='width:360px; height:360px; display:flex; align-items:center; justify-content:center;'>
          <div id="{wheel_id}" class='wheel' style='transform: rotate(0deg);'>
            {slice_html}
          </div>
        </div>
        """
        st.markdown(wheel_static, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Reasons page (all visible)
elif page == "Reasons I Love You 💌":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Reasons I Love You 💌")
    reasons = [
        "I love your personality","I love your smile","I love your hairs","I love your smell","I love your jollyness",
        "I love your maturity","I love your childishness","I love the way you balance","I love your futuristic vision",
        "I love the way I am happy around you","I love the way I am safe around you","I love that you communicate",
        "I love that you try to solve","I love that you are emotionally available","I love your humour","I love your eyes",
        "I love the way you listen","I love that you remember details","I love the sense of security you give",
        "I love your confidence","I love your nature","I love the small gestures","I love your intelligence",
        "I love your positive approach towards life","I love your dressing sense","I love that you never think of giving up",
        "I love how you respect others","I love your humanity","I love how you understand","I love that for you family matters",
        "I love that you think of 'your' people so selflessly","I love that you cry","I love your anger","I love your dance",
        "I love your general knowledge","I love that you love","I love that you believe in God","I love that you learn",
        "I love how you manage","I love that you are foodie","I love your courage","I love your boundaries","I love your control",
        "I love your thoughtfulness","I love how you complete me","I love the way you say 'meri laduuu'","I love the way you teach me",
        "I love the priority you give","I love the support you give","I love how you make me laugh","I love the way you love me",
        "I love our friendship","Most importantly I love youu"
    ]
    for i, r in enumerate(reasons, start=1):
        st.markdown(f"**Reason {i}:** {r}")
    st.markdown("</div>", unsafe_allow_html=True)

# Photos & Polaroids
elif page == "Photos & Polaroids 📸":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Photos & Polaroids 📸")
    uploaded = st.file_uploader("Upload a photo (jpg/png)", type=["jpg","jpeg","png"])
    caption = st.text_input("Caption for this photo")
    if st.button("Save photo"):
        if uploaded is not None:
            fname = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded.name}"
            target = PHOTOS_DIR / fname
            with open(target, "wb") as f:
                f.write(uploaded.getbuffer())
            # register in timeline.json
            tl = read_json("timeline.json")
            tl.append({"type":"photo","file": str(target), "caption": caption, "date": datetime.now().isoformat()})
            write_json("timeline.json", tl)
            st.success("Photo saved as Polaroid 💙")
        else:
            st.warning("Please choose an image first.")

    # display gallery (most recent first)
    files = sorted(PHOTOS_DIR.glob("*"), key=os.path.getmtime, reverse=True)
    if files:
        cols = st.columns(3)
        for i, fpath in enumerate(files):
            with cols[i % 3]:
                try:
                    st.image(str(fpath), use_column_width=True)
                    # find caption if exists in timeline.json
                    tl = read_json("timeline.json")
                    cap = next((t.get("caption","") for t in tl if t.get("file") == str(fpath)), "")
                    if cap:
                        st.caption(cap)
                except Exception:
                    pass
    else:
        st.info("No photos yet — upload one above.")
    st.markdown("</div>", unsafe_allow_html=True)

# Timeline
elif page == "Our Story Timeline 🕰️":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Our Story Timeline 🕰️")
    tl = read_json("timeline.json")
    with st.form("mem_form"):
        title = st.text_input("Title")
        date_val = st.date_input("Date")
        desc = st.text_area("Description")
        submit = st.form_submit_button("Add memory")
        if submit:
            tl.append({"type":"memory","title": title, "date": str(date_val), "desc": desc})
            write_json("timeline.json", tl)
            st.success("Memory saved 💙")
    # show memories sorted by date desc
    memories = [t for t in tl if t.get("type") == "memory"]
    for m in sorted(memories, key=lambda x: x.get("date",""), reverse=True):
        st.subheader(f"{m.get('title')} — {m.get('date')}")
        st.write(m.get("desc"))
        st.markdown("---")
    st.markdown("</div>", unsafe_allow_html=True)

# Settings
elif page == "Settings ⚙️":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.header("Settings & Uploads ⚙️")
    st.write("Upload voice note, add songs, or clear saved data.")

    # voice upload
    audio = st.file_uploader("Upload voice clip (mp3/wav) for 'miss me'", type=["mp3","wav"])
    if st.button("Upload voice clip"):
        if audio:
            with open(DATA_DIR / "voice.mp3", "wb") as f:
                f.write(audio.getbuffer())
            st.success("Voice clip uploaded 💙")
        else:
            st.warning("Choose a file first.")

    # add song
    st.markdown("---")
    st.subheader("Add a song")
    s_title = st.text_input("Song title")
    s_link = st.text_input("Link (optional)")
    s_note = st.text_area("Why it matters (short note)")
    if st.button("Add song"):
        songs = read_json("songs.json")
        songs.append({"title": s_title, "link": s_link, "note": s_note})
        write_json("songs.json", songs)
        st.success("Song added 💙")

    # clear data (careful)
    st.markdown("---")
    if st.button("Clear all saved data (photos, notes, timeline, songs)"):
        write_json("notes.json", [])
        write_json("songs.json", [])
        write_json("timeline.json", [])
        # delete photos
        for f in PHOTOS_DIR.glob("*"):
            try:
                f.unlink()
            except Exception:
                pass
        st.success("Cleared saved data for this deployment.")
    st.markdown("</div>", unsafe_allow_html=True)

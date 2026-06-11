import streamlit as st
from pathlib import Path
import time

st.set_page_config(
    page_title="FileVault — File Manager",
    page_icon="⬡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Sandbox directory ─────────────────────────────────────────────────────────
WORK_DIR = Path("filevault_files")
WORK_DIR.mkdir(exist_ok=True)

def safe_path(name: str) -> Path:
    return WORK_DIR / Path(name).name

def list_files():
    return sorted([f for f in WORK_DIR.iterdir() if f.is_file()])

def fmt_size(b: int) -> str:
    if b < 1024: return f"{b} B"
    if b < 1024**2: return f"{b/1024:.1f} KB"
    return f"{b/1024**2:.1f} MB"

def alert(kind, icon, msg):
    st.markdown(f'<div class="alert alert-{kind}">{icon}&nbsp;{msg}</div>', unsafe_allow_html=True)

def file_pills(files):
    if not files: return
    pills = "".join(
        f'<div class="file-pill">📄 {f.name}<span class="file-pill-size">{fmt_size(f.stat().st_size)}</span></div>'
        for f in files
    )
    st.markdown(f'<div class="file-pill-wrap">{pills}</div>', unsafe_allow_html=True)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], .stApp {
    font-family: 'DM Sans', sans-serif !important;
    background: #07070f !important;
    color: #e8e6f0;
}

/* === Animated aurora blobs === */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 75% 55% at 15% 8%,  rgba(109,40,255,0.28)  0%, transparent 60%),
        radial-gradient(ellipse 55% 45% at 85% 18%,  rgba(0,200,200,0.18)   0%, transparent 55%),
        radial-gradient(ellipse 65% 38% at 55% 95%,  rgba(200,30,255,0.14)  0%, transparent 58%),
        radial-gradient(ellipse 40% 30% at 90% 75%,  rgba(60,130,255,0.10)  0%, transparent 50%);
    animation: aurora 14s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}
@keyframes aurora {
    0%   { opacity:1;    transform:scale(1)    rotate(0deg);   }
    40%  { opacity:0.78; transform:scale(1.05) rotate(1.2deg); }
    100% { opacity:1;    transform:scale(1)    rotate(0deg);   }
}

/* === Layout === */
.block-container {
    position: relative;
    z-index: 1;
    max-width: 800px !important;
    padding: 2rem 1.8rem 5rem !important;
}

/* === Hero === */
.hero-wrap {
    text-align: center;
    padding: 3.2rem 1rem 2.8rem;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.26em;
    text-transform: uppercase;
    color: #9d8cff;
    margin-bottom: 1rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3rem, 8vw, 5rem);
    font-weight: 800;
    line-height: 1;
    background: linear-gradient(135deg, #c4b5fd 0%, #67e8f9 52%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.8rem;
    letter-spacing: -0.025em;
}
.hero-sub {
    font-size: 1rem;
    color: rgba(232,230,240,0.42);
    font-weight: 300;
}

/* === Stat row === */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.7rem;
    margin-bottom: 1.8rem;
}
.stat-card {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.1rem 1.2rem;
    backdrop-filter: blur(16px);
}
.stat-val {
    font-family: 'Syne', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: #c4b5fd;
    line-height: 1.1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}
.stat-lbl {
    font-size: 0.7rem;
    color: rgba(232,230,240,0.35);
    font-weight: 400;
    margin-top: 0.25rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}

/* === Glass card === */
.glass {
    background: rgba(255,255,255,0.035);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 22px;
    padding: 1.8rem 2rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(22px);
    -webkit-backdrop-filter: blur(22px);
    box-shadow:
        0 8px 40px rgba(0,0,0,0.4),
        inset 0 1px 0 rgba(255,255,255,0.07);
}

/* === Section header === */
.sec-head {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #e8e6f0;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.55rem;
}
.sec-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: linear-gradient(135deg, #a78bfa, #67e8f9);
    flex-shrink: 0;
}

/* === Micro label === */
.micro-lbl {
    font-size: 0.72rem;
    color: rgba(196,181,253,0.45);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0.9rem 0 0.35rem;
}

/* === Inputs === */
.stTextInput > label,
.stTextArea  > label,
.stSelectbox > label,
.stRadio     > label {
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    color: rgba(196,181,253,0.65) !important;
    letter-spacing: 0.07em !important;
    text-transform: uppercase !important;
}
.stTextInput input,
.stTextArea textarea {
    background: rgba(0,0,0,0.28) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.94rem !important;
    caret-color: #a78bfa !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: rgba(167,139,250,0.55) !important;
    box-shadow: 0 0 0 3px rgba(167,139,250,0.1) !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder { color: rgba(232,230,240,0.22) !important; }

div[data-baseweb="select"] > div:first-child {
    background: rgba(0,0,0,0.28) !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
    border-radius: 12px !important;
    color: #e8e6f0 !important;
}

/* === Tabs === */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.028) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    gap: 3px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.86rem !important;
    color: rgba(232,230,240,0.42) !important;
    padding: 0.42rem 1rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(167,139,250,0.16) !important;
    color: #c4b5fd !important;
    border: 1px solid rgba(167,139,250,0.28) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* === Button === */
.stButton > button {
    background: linear-gradient(135deg, #6d28d9 0%, #0e7490 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
    padding: 0.58rem 1.4rem !important;
    width: 100% !important;
    letter-spacing: 0.025em !important;
    transition: opacity 0.2s, transform 0.15s !important;
    box-shadow: 0 4px 24px rgba(109,40,217,0.38) !important;
}
.stButton > button:hover {
    opacity: 0.86 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* === File viewer === */
.file-viewer {
    background: rgba(0,0,0,0.4);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    font-family: 'Courier New', monospace;
    font-size: 0.86rem;
    color: #a5f3fc;
    white-space: pre-wrap;
    word-break: break-word;
    min-height: 64px;
    max-height: 240px;
    overflow-y: auto;
    line-height: 1.75;
}

/* === File pills === */
.file-pill-wrap { display:flex; flex-wrap:wrap; gap:0.45rem; margin-top:0.7rem; }
.file-pill {
    background: rgba(167,139,250,0.09);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 8px;
    padding: 0.28rem 0.7rem;
    font-size: 0.78rem;
    color: #c4b5fd;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.file-pill-size { color:rgba(196,181,253,0.38); font-size:0.7rem; }

/* === Alerts === */
.alert {
    border-radius: 12px;
    padding: 0.82rem 1.1rem;
    font-size: 0.87rem;
    font-weight: 500;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-top: 0.75rem;
    line-height: 1.45;
}
.alert-success { background:rgba(16,185,129,0.09);  border:1px solid rgba(16,185,129,0.22); color:#6ee7b7; }
.alert-error   { background:rgba(239,68,68,0.09);   border:1px solid rgba(239,68,68,0.2);  color:#fca5a5; }
.alert-info    { background:rgba(99,102,241,0.09);  border:1px solid rgba(99,102,241,0.2); color:#a5b4fc; }

/* === Radio === */
.stRadio [role=radiogroup] { flex-direction:row !important; flex-wrap:wrap; gap:0.45rem; }
.stRadio [role=radiogroup] label {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 9px !important;
    padding: 0.32rem 0.85rem !important;
    color: rgba(232,230,240,0.5) !important;
    font-size: 0.84rem !important;
    transition: all 0.18s !important;
    cursor: pointer !important;
}
.stRadio [role=radiogroup] label:hover {
    border-color: rgba(167,139,250,0.38) !important;
    color: #c4b5fd !important;
}

/* === Checkbox === */
.stCheckbox label { color:rgba(232,230,240,0.55) !important; font-size:0.87rem !important; }

/* === Divider === */
hr { border-color:rgba(255,255,255,0.07) !important; margin:1.1rem 0 !important; }

/* === Scrollbar === */
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:rgba(167,139,250,0.28); border-radius:99px; }

/* === Footer === */
.footer {
    text-align:center;
    color:rgba(232,230,240,0.18);
    font-size:0.76rem;
    margin-top:3rem;
    letter-spacing:0.06em;
}
.footer strong { color:rgba(196,181,253,0.35); font-weight:500; }

#MainMenu, footer, header { visibility:hidden; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-eyebrow">Python · Pathlib · Streamlit</div>
  <div class="hero-title">FileVault</div>
  <div class="hero-sub">Create · Read · Update · Delete — all in one elegant interface.</div>
</div>
""", unsafe_allow_html=True)

# ── Stats bar ─────────────────────────────────────────────────────────────────
files      = list_files()
total_size = sum(f.stat().st_size for f in files)
ext_set    = {f.suffix.lstrip('.').upper() or '—' for f in files}
ext_str    = ', '.join(sorted(ext_set)) if ext_set else '—'

st.markdown(f"""
<div class="stat-row">
  <div class="stat-card">
    <div class="stat-val">{len(files)}</div>
    <div class="stat-lbl">Files stored</div>
  </div>
  <div class="stat-card">
    <div class="stat-val">{fmt_size(total_size)}</div>
    <div class="stat-lbl">Total size</div>
  </div>
  <div class="stat-card">
    <div class="stat-val" title="{ext_str}">{ext_str}</div>
    <div class="stat-lbl">File types</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
t_create, t_read, t_update, t_delete = st.tabs(
    ["✦  Create", "◎  Read", "◈  Update", "◻  Delete"]
)

# ─── CREATE ───────────────────────────────────────────────────────────────────
with t_create:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><span class="sec-dot"></span>New file</div>', unsafe_allow_html=True)

    c_name = st.text_input("File name", placeholder="journal.txt", key="c_name")
    c_data = st.text_area("Content", placeholder="Start writing anything…", height=150, key="c_data")

    if st.button("Create file", key="btn_create"):
        if not c_name.strip():
            alert("error", "⚠", "Please enter a file name.")
        else:
            p = safe_path(c_name.strip())
            if p.exists():
                alert("error", "⚠", f"<b>{p.name}</b> already exists.")
            else:
                p.write_text(c_data)
                alert("success", "✓", f"<b>{p.name}</b> created successfully — {fmt_size(p.stat().st_size)}")
                time.sleep(0.3)
                st.rerun()

    fresh = list_files()
    if fresh:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown('<div class="micro-lbl">Vault contents</div>', unsafe_allow_html=True)
        file_pills(fresh)

    st.markdown('</div>', unsafe_allow_html=True)

# ─── READ ─────────────────────────────────────────────────────────────────────
with t_read:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><span class="sec-dot"></span>Read a file</div>', unsafe_allow_html=True)

    files = list_files()
    if not files:
        alert("info", "◎", "Your vault is empty — create a file first.")
    else:
        r_sel = st.selectbox("Choose file", [f.name for f in files], key="r_sel")
        if st.button("Read file", key="btn_read"):
            p       = safe_path(r_sel)
            content = p.read_text()
            st.markdown(f'<div class="micro-lbl">{p.name} · {fmt_size(p.stat().st_size)}</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="file-viewer">{content if content.strip() else "(empty file)"}</div>',
                unsafe_allow_html=True,
            )

    st.markdown('</div>', unsafe_allow_html=True)

# ─── UPDATE ───────────────────────────────────────────────────────────────────
with t_update:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><span class="sec-dot"></span>Update a file</div>', unsafe_allow_html=True)

    files = list_files()
    if not files:
        alert("info", "◎", "Your vault is empty — create a file first.")
    else:
        u_sel = st.selectbox("Choose file", [f.name for f in files], key="u_sel")
        op    = st.radio("Operation", ["Rename", "Append", "Overwrite"], horizontal=True, key="u_op")

        if op == "Rename":
            u_new = st.text_input("New name", placeholder="new-name.txt", key="u_new")
            if st.button("Rename", key="btn_rename"):
                if not u_new.strip():
                    alert("error", "⚠", "Enter a new file name.")
                else:
                    src, dst = safe_path(u_sel), safe_path(u_new.strip())
                    if dst.exists():
                        alert("error", "⚠", f"<b>{dst.name}</b> already exists.")
                    else:
                        src.rename(dst)
                        alert("success", "✓", f"Renamed to <b>{dst.name}</b>")
                        time.sleep(0.3)
                        st.rerun()

        elif op == "Append":
            p = safe_path(u_sel)
            st.markdown('<div class="micro-lbl">Current content</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="file-viewer">{p.read_text() or "(empty)"}</div>', unsafe_allow_html=True)
            u_app = st.text_area("Text to append", height=110, key="u_app")
            if st.button("Append", key="btn_append"):
                if not u_app.strip():
                    alert("error", "⚠", "Nothing to append.")
                else:
                    with open(p, "a") as fs:
                        fs.write("\n" + u_app)
                    alert("success", "✓", f"Content appended to <b>{p.name}</b>")

        elif op == "Overwrite":
            p = safe_path(u_sel)
            st.markdown('<div class="micro-lbl">Current content</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="file-viewer">{p.read_text() or "(empty)"}</div>', unsafe_allow_html=True)
            u_over = st.text_area("New content", height=110, key="u_over")
            if st.button("Overwrite", key="btn_over"):
                p.write_text(u_over)
                alert("success", "✓", f"<b>{p.name}</b> overwritten successfully")

    st.markdown('</div>', unsafe_allow_html=True)

# ─── DELETE ───────────────────────────────────────────────────────────────────
with t_delete:
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<div class="sec-head"><span class="sec-dot"></span>Delete a file</div>', unsafe_allow_html=True)

    files = list_files()
    if not files:
        alert("info", "◎", "Nothing to delete — vault is empty.")
    else:
        d_sel   = st.selectbox("Choose file", [f.name for f in files], key="d_sel")
        p       = safe_path(d_sel)
        st.markdown('<div class="micro-lbl">Preview</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="file-viewer">{p.read_text() or "(empty file)"}</div>',
            unsafe_allow_html=True,
        )
        confirm = st.checkbox(f"Permanently delete  **{d_sel}**", key="d_confirm")
        if st.button("Delete file", key="btn_delete"):
            if not confirm:
                alert("error", "⚠", "Tick the confirmation box to proceed.")
            else:
                p.unlink()
                alert("success", "✓", f"<b>{d_sel}</b> removed from vault")
                time.sleep(0.3)
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Built with <strong>Python + Streamlit</strong> &nbsp;·&nbsp; FileVault
</div>
""", unsafe_allow_html=True)
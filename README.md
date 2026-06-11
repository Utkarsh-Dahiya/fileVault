<div align="center">

# ⬡ FileVault

### A minimal, aesthetic file manager built with Python + Streamlit

![Python](https://img.shields.io/badge/Python-3.8+-a78bfa?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-67e8f9?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-c4b5fd?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Live-6ee7b7?style=for-the-badge)

<br/>

> **FileVault** is a full-featured file manager with a glassmorphism UI — animated aurora background, frosted glass cards, and live stats. Built to demonstrate Python file I/O using `pathlib`.

<br/>

---

</div>

## ✦ Features

- **Create** — Write new files with custom content, instantly stored in the vault
- **Read** — Browse all files from a dropdown and view contents in a styled code viewer
- **Update** — Rename, append to, or fully overwrite any existing file
- **Delete** — Remove files with a confirmation gate to prevent accidents
- **Live stats** — File count, total vault size, and file types updated in real time
- **Aesthetic UI** — Animated aurora background, glassmorphism panels, Syne + DM Sans typography

---

## 🖥️ Preview

> Run the app locally and take a screenshot here — or record a short Loom/GIF

```
[Add your screenshot here]
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/filevault.git
cd filevault
```

**2. Install dependencies**
```bash
pip install streamlit
```

**3. Run the app**
```bash
streamlit run filevault.py
```

**4. Open in your browser**
```
http://localhost:8501
```

> All files are sandboxed inside a `filevault_files/` folder that is auto-created on first run.

---

## 📁 Project Structure

```
filevault/
│
├── filevault.py          # Main Streamlit app
├── filevault_files/      # Auto-created vault directory (gitignored)
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| **Python** | Core language |
| **pathlib** | File system operations |
| **Streamlit** | Web UI framework |
| **CSS (custom)** | Glassmorphism + aurora theme |
| **Google Fonts** | Syne & DM Sans typography |

---

## 📦 Requirements

Create a `requirements.txt` in your project root:

```
streamlit>=1.28.0
```

---

## 🔒 Safety Notes

- All file operations are **sandboxed** inside `filevault_files/` — no path traversal possible
- The delete tab requires an **explicit confirmation checkbox** before any file is removed
- The rename operation checks for **naming conflicts** before proceeding

---

## 🧑‍💻 Core Logic (Python)

This project demonstrates all four CRUD operations on the file system using Python's built-in `pathlib.Path`:

```python
from pathlib import Path

# CREATE
Path("file.txt").write_text("Hello, world!")

# READ
content = Path("file.txt").read_text()

# UPDATE (append)
with open("file.txt", "a") as f:
    f.write("\nNew line")

# DELETE
Path("file.txt").unlink()
```

---

## 🎨 UI Design Highlights

- **Aurora background** — three animated CSS radial gradients (violet, cyan, magenta) that breathe using `@keyframes`
- **Glassmorphism cards** — `backdrop-filter: blur(22px)` with hairline borders and inner glow
- **Typography** — `Syne` (display, 800 weight) for headers + `DM Sans` (300–500) for body text
- **Colour palette** — `#c4b5fd` violet · `#67e8f9` cyan · `#a78bfa` purple · `#07070f` near-black base

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Made with 💜 using Python + Streamlit

**[⭐ Star this repo if you found it useful!](https://github.com/your-username/filevault)**

</div>

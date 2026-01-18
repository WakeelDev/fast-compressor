# FastCompress 📸
**A Private, High-Speed Image Compression Tool.**

FastCompress is a full-stack web application designed to help users reduce image file sizes without compromising quality. Built with a focus on **privacy** and **performance**, it uses in-memory processing to ensure that user data is never stored on a server.

## 🚀 Live Demo
- **Frontend:** [https://fast-compressor.vercel.app/](https://fast-compressor.vercel.app/)
- **Backend API:** Hosted on Render

---

## ✨ Features
* **Secure Processing:** Images are processed in-memory and never saved to a disk or database.
* **Bulk Compression:** Upload up to 10 images at once.
* **Format Support:** Supports JPG, PNG, and WebP (outputting highly optimized WebP).
* **Custom Quality:** User-controlled compression levels (30% to 85%).
* **SEO Optimized:** Includes dedicated FAQ, About, and Privacy pages for better search engine indexing.

---

## 🛠 Tech Stack
### Frontend
* **HTML5 & JavaScript:** Core logic for file handling.
* **Tailwind CSS:** Modern, responsive UI design.
* **Vercel:** Fast edge hosting for the frontend.

### Backend
* **Python (FastAPI):** High-performance asynchronous API.
* **Pillow (PIL):** Advanced image processing library.
* **Render:** Cloud hosting for the Python environment.

---

## 📂 Project Structure
```text
├── main.py              # FastAPI Backend Logic
├── index.html           # Main Tool Page
├── about.html           # About & Mission Page
├── faq.html             # Frequently Asked Questions
├── privacy.html         # Privacy Policy & Data Handling
├── sitemap.xml          # Search Engine Map
├── robots.txt           # Crawler Instructions
└── requirements.txt     # Python Dependencies

```

---

## ⚙️ Local Setup

### 1. Clone the repository

```bash
git clone [https://github.com/WakeelDev/fast-compressor.git](https://github.com/WakeelDev/fast-compressor.git)
cd fast-compressor

```

### 2. Set up the Backend

```bash
pip install -r requirements.txt
uvicorn main:app --reload

```

### 3. Run the Frontend

Simply open `index.html` in any modern web browser.

---

## 📜 License

This project is licensed under the MIT License.

## 🤝 Contact

Built by **Wakeel** - Feel free to reach out for suggestions or bug reports!



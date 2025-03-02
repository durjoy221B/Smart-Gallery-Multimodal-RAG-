# 📸 AI-Powered Photo Gallery  

The **AI-Powered Photo Gallery** is a **multimodal Retrieval-Augmented Generation (RAG) system** for **image retrieval using text and image search**. It allows users to:  
- **Upload and store** photos from their device or camera.  
- **Automatically generate** descriptions and metadata for images.  
- **Search for images** using **text, images, or both**, leveraging AI-powered embeddings and retrieval techniques.  
- **Interact through a chatbot** for seamless gallery navigation and intelligent search.  
- **Efficiently retrieve** images using **CLIP-based embeddings and FastAPI** for high-performance processing.  

This project integrates **cutting-edge AI technologies** with an intuitive UI, creating an **interactive and intelligent photo management system**.  

---

## 📑 Table of Contents  
- [🚀 Features](#-features)  
- [🛠️ Technology & Tools](#️-technology--tools)  
- [🛠️ Prerequisites](#️-prerequisites)  
- [📥 Installation](#-installation)  
- [⚙️ Configure Environment Variables](#️-configure-environment-variables)  
- [▶️ Running the Application](#️-running-the-application)  
- [🌍 Accessing the Web Interface](#-accessing-the-web-interface)  
- [📦 Deployment (Optional)](#-deployment-optional)  

---

## 🚀 Features  

- **📸 Upload Images** – Upload photos directly from your device or camera.  
- **🤖 AI-Powered Image Processing** – Automatically generate descriptions and metadata.  
- **🔍 Advanced Image Search:**  
  - **Text-Based Search** – Find images using text queries (e.g., *"show me photos of beaches"*).  
  - **Image-Based Search** – Upload an image to find visually similar ones.  
  - **Combined Search** – Use both text and image together for more precise results.  
- **💬 Conversational Chatbot Interface** – Interact with the gallery and search for images through a chatbot.  
- **⚡ Efficient Storage & Retrieval** – Uses embeddings and advanced data retrieval techniques.  

---

## 🛠️ Technology & Tools  

### **Backend**  
- **Gemini API** – Generates image descriptions and metadata.  
- **CLIP (Contrastive Language-Image Pretraining)** – Enables text and image-based similarity search.  
- **FastAPI** – Provides a high-performance backend API.  
- **ChromaDB** – Stores and retrieves image embeddings for efficient search.  

### **Frontend**  
- **HTML, CSS, JavaScript** – Builds the interactive user interface.  

---

## 🛠️ Prerequisites  

Before installing, ensure you have:  

- **Python** 3.9 or higher  
- **pip** (Python package manager)  
- **Git** (optional, for cloning the repository)  
- **Virtual Environment** (recommended)  

---

## 📥 Installation  

1️⃣ **Clone the Repository**  
```bash
git clone https://github.com/durjoy221B/Smart-Gallery-Multimodal-RAG-.git
cd image-search-ai
```  

2️⃣ **Create a Virtual Environment (Recommended)**  
- **Windows:**  
  ```bash
  python -m venv venv  
  venv\Scripts\activate  
  ```  
- **macOS/Linux:**  
  ```bash
  python3 -m venv venv  
  source venv/bin/activate  
  ```  

3️⃣ **Install Dependencies**  
```bash
pip install -r requirements.txt
```  

---

## ⚙️ Configure Environment Variables  

1️⃣ **Create a `.env` file** in the root directory:  
```bash
touch .env
```  

2️⃣ **Add your API keys and configurations** in `.env`:  
```bash
GEMINI_API_KEY=your_gemini_api_key
# Add other necessary keys or configurations
```  

---

## ▶️ Running the Application  

```bash
uvicorn main:app --reload
```  

---

## 🌍 Accessing the Web Interface  

After running the application, open your browser and go to:  
```
http://localhost:8000  or http://127.0.0.1:8000
```  
----------------
## 📦 Project Structure
```````
📦 image-search-ai  
│── 📂 routes            # API route handlers  
│   ├── chat.py         # Handles chatbot interactions  
│   ├── gallery.py      # Manages image gallery retrieval  
│   ├── helpers.py      # Utility functions for processing  
│   ├── pages.py        # Page rendering logic  
│   ├── upload.py       # Handles image uploads  
│  
│── 📂 templates         # Jinja2 templates for frontend  
│   ├── chat.html       # Chatbot UI  
│   ├── gallery.html    # Gallery page  
│   ├── home.html       # Homepage  
│   ├── index.html      # Main index page  
│   ├── upload.html     # Upload interface  
│  
│── 📂 static            # Static assets (CSS, JS, images)  
│── 📂 venv              # Virtual environment (local dependencies)  
│── .env                # Environment variables (API keys, config)  
│── config.py           # Application configuration settings  
│── constants.py        # Global constants for the project  
│── database.py         # Database connection and handling  
│── dependencies.py     # External dependencies and middleware  
│── main.py
│── models.py           # Entry point for FastAPI server  
│── utils.py            # Data models and schemas  
│── readme.md           # Project documentation  
│── requirements.txt    # Python dependencies  

```````

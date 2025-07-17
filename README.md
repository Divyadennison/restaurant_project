# Restaurant Project
# 🍽️ Restaurant Website - Django Project

This is a simple restaurant website built using **Django**, **HTML**, and **CSS**. It allows users to view the restaurant menu with food images and descriptions.

---

## 🚀 Features

- Homepage with restaurant theme
- Food items listed with image, title, price, and description
- Static image display using Django's media handling
- Responsive design using HTML & CSS

---

## 🛠️ Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS
- **Database**: SQLite3 (default Django DB)
- **Media Handling**: Django `MEDIA_ROOT` and `MEDIA_URL` configured

---

## 📁 Project Structure

```
restaurant_project/
├── restaurant_project/      # Project settings
├── restaurant_app/          # Main app with views, models, templates
│   ├── static/              # CSS and images
│   ├── templates/           # HTML files
│   └── migrations/
├── media/                   # Uploaded food images
├── manage.py
├── db.sqlite3
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run the Project

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Divyadennison/restaurant_project.git
   cd restaurant_project
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

6. **Open in Browser**
   Visit `http://127.0.0.1:8000/`

---
## 🎯 Usage

- Browse the homepage to view the restaurant menu.
- See food items with images, titles, prices, and descriptions.
- Responsive design works on desktop and mobile.


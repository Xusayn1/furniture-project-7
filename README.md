# 🪑 Furniture API (Backend)

## 📌 Description

This project is a backend REST API for a furniture store application.
It provides functionality for managing products, categories, and user interactions.

The API is built using Django and Django REST Framework, following RESTful principles.

---

## 🚀 Features

* User authentication (Login / Register)
* CRUD operations for furniture products
* Category management
* API endpoints for frontend integration
* Clean and modular backend architecture

---

## 🛠 Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL (or SQLite for development)

---

## 📂 Project Structure

```
furniture-project-7/
├── apps/
├── config/
├── manage.py
├── requirements.txt
└── ...
```

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/Xusayn1/furniture-project-7.git
cd furniture-project-7
```

2. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Apply migrations:

```bash
python manage.py migrate
```

5. Run server:

```bash
python manage.py runserver
```

---

## 🔗 API Endpoints (example)

* GET /products/
* POST /products/
* GET /products/{id}/
* PUT /products/{id}/
* DELETE /products/{id}/

---

## 🧪 Testing

You can test endpoints using:

* Postman
* Curl
* Browser (for GET requests)

---

## 📈 Future Improvements

* Add payment integration
* Add order system
* Improve authentication (JWT)
* Docker support

---

## 👨‍💻 Author

**Xusayn (Backend Developer)**

* GitHub: https://github.com/Xusayn1

---

## ⭐ Notes

This project was built as part of backend learning and practice.
Focused on API design, clean structure, and real-world use cases.

Markdown

# Urban Palate 🍽️
**A Modern Restaurant Discovery & Management Demo**

Urban Palate is a full-stack web application designed for the food and hospitality industry. It serves as a comprehensive demo for browsing menus, managing restaurant locations, and handling user accounts.

> ⚠️ **DEMO ONLY**: This is a portfolio project. Payment processing and real-world order fulfillment are not active.

---

## ✨ Key Features
* **Dynamic Menu:** Categorized food and beverage listings with real-time updates.
* **User Accounts:** Secure sign-up/login system for customers.
* **Responsive UI:** Fully mobile-friendly design for browsing on the go.
* **Admin Control:** Complete dashboard to manage dishes, prices, and users.
* **Custom UI:** Unique styling for landing pages and error handling (404/500).

---

## 🛠️ Tech Stack
* **Backend:** Python 3.13 & Django
* **Database:** SQLite (Development)
* **Frontend:** HTML5, CSS3, JavaScript
* **Config:** `django-environ` for secure settings management.

---

## 🚀 Local Setup Instructions

Follow these steps to get the demo running on your local machine:

### 1. Clone & Navigate
```bash
git clone [https://github.com/ORLAND0HENRY/urban_restaurant.git](https://github.com/ORLAND0HENRY/urban_restaurant.git)
cd urban_restaurant
2. Environment Setup
Bash

# Create Virtual Environment
python -m venv venv

# Activate Environment (Windows)
.\venv\Scripts\activate

# Activate Environment (Mac/Linux)
# source venv/bin/activate
3. Install Requirements
Bash
pip install -r requirements.txt
4. Database & Launch
Bash

python manage.py migrate
python manage.py runserver
Visit http://127.0.0.1:8000/ in your browser to see the app!

👤 Author
Orlando Henry GitHub Profile

Developed as a demonstration of full-stack web development capabilities.

# 🍽️ Bonnyrigg High School Food Blog  
### Software Engineering Assessment Project  
**Developed using Flask, SQLite, and Bootstrap**

---

## 📌 Project Overview

The Bonnyrigg High School Food Blog is a full-stack web application developed as part of a Software Engineering assessment task.

This system allows students and staff to browse, search, filter, and contribute food recipes in a structured and user-friendly environment. The application demonstrates:

- Backend development using Flask
- Database integration with SQLite & SQLAlchemy
- User authentication with Flask-Login
- Secure password hashing with Flask-Bcrypt
- Responsive frontend design using Bootstrap
- Clean code structure using Blueprints
- Database seeding and content management

The application follows the structure and best practices demonstrated in Corey Schafer’s Flask tutorial series, extended with additional features and UI enhancements.

---

# 🎯 Key Features

## 👤 User System
- User registration
- Secure login/logout
- Password hashing
- Account update functionality
- Role-based admin user

## 🍽️ Recipe System
- Multiple recipe categories
- Individual recipe detail pages
- Recipe images stored in static folder
- Ingredients and instructions formatting
- Cooking time, difficulty, cuisine type
- Featured recipes section

## 💬 Comment System
- Logged-in users can comment on recipes
- Seeded example comments for demonstration
- Database relationship between users and recipes

## 🔎 Filtering & Search
- Search by title or summary
- Filter by:
  - Cuisine
  - Difficulty
  - Maximum cooking time
  - Tags
  - Ingredients

## 🖼️ Image Management
- Each recipe has its own image
- Images stored in:
  ```
  flaskblog/static/recipe_pics/
  ```
- Image filenames mapped exactly in database

## 🗂 Categories Page
- Dedicated categories view
- Clicking a category shows matching recipes

---

# 🏗 System Architecture

The application uses a modular Flask Blueprint structure.

```
bonnyrigg_food_blog/
│
├── flaskblog/
│   ├── static/
│   │   ├── recipe_pics/
│   │   └── css/
│   │
│   ├── templates/
│   │   ├── layout.html
│   │   ├── main/
│   │   ├── recipes/
│   │   └── users/
│   │
│   ├── main/
│   ├── recipes/
│   ├── users/
│   ├── models.py
│   ├── __init__.py
│
├── seed.py
├── seed_more.py
├── run.py
├── requirements.txt
└── README.md
```

### Technologies Used
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-Bcrypt
- SQLite
- Bootstrap 5

---

# 🚀 How to Run the Website in Visual Studio Code

Follow these steps carefully.

---

## ✅ Step 1: Open the Project

1. Open **Visual Studio Code**
2. Click **File → Open Folder**
3. Select:
   ```
   bonnyrigg_food_blog
   ```
4. Click **Open**

---

## ✅ Step 2: Open Terminal in VS Code

- Click **Terminal → New Terminal**
- OR press:
  ```
  Ctrl + `
  ```

Make sure you are inside the project root directory.

---

## ✅ Step 3: Create Virtual Environment (First Time Only)

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

You should now see:

```
(venv) PS ...
```

---

## ✅ Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## ✅ Step 5: Create and Seed the Database

If running for the first time or after deleting the database:

```powershell
python seed.py
python seed_more.py
```

This will:
- Create the database
- Insert users
- Insert recipes
- Assign recipe images
- Insert sample comments

---

## ✅ Step 6: Run the Application

```powershell
python run.py
```

You should see:

```
Running on http://127.0.0.1:5000/
```

---

## ✅ Step 7: Open the Website

Open your browser and go to:

```
http://127.0.0.1:5000/
```

---

# 👤 Test Login Details

After seeding:

**Admin Account**
- Username: `admin`
- Password: `password`

---

# 🗄 Database

The application uses SQLite.

Database file:
```
flaskblog/site.db
```

To reset the database:

1. Stop Flask server  
2. Delete `site.db`  
3. Run:
   ```powershell
   python seed.py
   python seed_more.py
   ```

---

# 🎨 UI & Design Enhancements

- Responsive layout using Bootstrap grid
- Card-based recipe display
- Category image tiles
- Styled navigation bar
- Branded footer with school details
- Professional page structure
- Clean and consistent colour scheme

---

# 🔒 Security Considerations

- Passwords hashed using Flask-Bcrypt
- Login protection using Flask-Login
- Database relationships enforced via SQLAlchemy
- Input validation via Flask-WTF forms

---

# 📈 Assessment Criteria Alignment

This project demonstrates:

- Structured modular architecture
- Database normalisation and relationships
- CRUD functionality
- Authentication system
- Clean and maintainable code
- Functional user interface
- Proper documentation
- Deployment-ready design

---

# 🛠 Troubleshooting

If the website does not load:

- Ensure virtual environment is activated
- Ensure dependencies are installed
- Ensure `site.db` exists
- Restart Flask server
- Hard refresh browser (Ctrl + F5)

---

# 🏁 Conclusion

The Bonnyrigg High School Food Blog successfully demonstrates full-stack web development principles using Flask. The application is scalable, modular, and structured according to industry best practices.

It showcases backend logic, database integration, authentication systems, frontend responsiveness, and structured project organisation appropriate for a high-level Software Engineering assessment submission.

---

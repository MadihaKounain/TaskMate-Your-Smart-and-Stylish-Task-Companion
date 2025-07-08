# 📝 TaskMate – Your Smart and Stylish Task Companion

TaskMate is a lightweight, multi-user task management web application built with **Flask**. Designed for simplicity and usability, TaskMate allows users to effortlessly organize, prioritize, and track their tasks with a clean UI and customizable themes.

Whether you're a student managing assignments or a developer tracking feature updates, TaskMate gives you all the core essentials:  
✅ User registration and login  
✅ Adding, completing, and deleting tasks  
✅ Due date and time scheduling with conflict checks  
✅ Colorful theme and mode switching (Light/Dark)  
✅ Flash feedback for better interaction  
All this with a backend powered by plain JSON – no database setup required!

TaskMate is perfect for learning web development with Flask, or as a base for building more advanced productivity tools.

---

## 🚀 Features

- User registration and login with session management
- Add tasks with:
  - Title
  - Priority (Low/Medium/High)
  - Difficulty (Easy/Medium/Hard)
  - Due date and time
- Prevent task time clashes
- Mark tasks as completed or pending
- Delete tasks
- Theme and mode customization (blue, green, red, purple in light/dark modes)
- JSON-based lightweight backend (no database required)

---

## 🛠️ Technologies Used

- Python 3.12
- Flask
- HTML, CSS (custom)
- JSON for data storage

---

## 📁 File Structure

```
task_manager/
│
├── app.py                  # Main Flask app
├── data/
│   ├── users.json          # Stores user info
│   └── tasks.json          # Stores tasks
│
├── templates/
│   ├── login.html
│   ├── register.html
│   └── tasks.html
│
├── static/
│   └── styles.css          # Custom styling
│   └── script.js
│
└── README.md
```

---

## 🧪 How to Run Locally

1. **Clone this repository**:

   ```bash
   git clone https://github.com/yourusername/task-manager.git
   cd task-manager
   ```

2. **Set up virtual environment (optional but recommended)**:

   ```bash
   python -m venv venv
   source venv/bin/activate   # on Unix/Mac
   venv\Scripts\activate    # on Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install flask
   ```

4. **Create `data` folder with empty JSON files**:

   ```bash
   mkdir data
   echo [] > data/users.json
   echo [] > data/tasks.json
   ```

5. **Run the app**:

   ```bash
   python app.py
   ```

6. **Access in browser**:

   ```
   http://127.0.0.1:5000/
   ```

---

## 📌 To Do / Ideas

- Add password encryption
- Allow task editing
- Search/filter tasks
- Switch to SQLite/SQLAlchemy for persistence
- Add deadline notifications or email alerts

---

## 📃 License

This project is for educational/demo purposes and is not intended for production use. Customize it freely!

---

### Made with ❤️ using Flask

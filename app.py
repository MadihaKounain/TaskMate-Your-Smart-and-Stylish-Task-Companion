from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# File paths
USER_FILE = 'data/users.json'
TASK_FILE = 'data/tasks.json'

# Ensure JSON files exist
if not os.path.exists('data'):
    os.makedirs('data')
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w') as f:
        json.dump([], f)
if not os.path.exists(TASK_FILE):
    with open(TASK_FILE, 'w') as f:
        json.dump([], f)

# Load and save data functions
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_data(USER_FILE)

        if any(user['username'] == username for user in users):
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))

        users.append({'username': username, 'password': password})
        save_data(USER_FILE, users)
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_data(USER_FILE)

        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            session['username'] = username
            return redirect(url_for('tasks'))
        else:
            flash('Invalid credentials.', 'error')
    return render_template('login.html')

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if 'username' not in session:
        return redirect(url_for('login'))

    tasks = load_data(TASK_FILE)

    if request.method == 'POST':
        new_task = {
            'title': request.form['title'],
            'priority': request.form['priority'],
            'difficulty': request.form['difficulty'],
            'due_date': request.form['due_date'],
            'due_time': request.form['due_time'],  # New time field
            'completed': False,
            'owner': session['username']
        }

        # Check for duplicate tasks with the same time and date
        user_tasks = [task for task in tasks if task['owner'] == session['username']]
        for task in user_tasks:
            if task['due_date'] == new_task['due_date'] and task['due_time'] == new_task['due_time']:
                flash('You already have a task scheduled at this time.', 'error')
                return redirect(url_for('tasks'))

        tasks.append(new_task)
        save_data(TASK_FILE, tasks)
        flash('Task added successfully!', 'success')

    user_tasks = [task for task in tasks if task['owner'] == session['username']]
    return render_template('tasks.html', tasks=user_tasks, theme=session.get('theme', 'default'), mode=session.get('mode', 'light'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    tasks = load_data(TASK_FILE)
    task = tasks[task_id]
    task['completed'] = not task['completed']
    save_data(TASK_FILE, tasks)
    return redirect(url_for('tasks'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    tasks = load_data(TASK_FILE)
    tasks.pop(task_id)
    save_data(TASK_FILE, tasks)
    return redirect(url_for('tasks'))

@app.route('/change_theme', methods=['GET'])
def change_theme():
    theme = request.args.get('theme', 'default')
    mode = request.args.get('mode', 'light')
    session['theme'] = theme
    session['mode'] = mode
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secure in production (use environment variables)

# File paths
USER_FILE = 'data/users.json'
TASK_FILE = 'data/tasks.json'


# Utility: Ensure JSON files exist and handle file creation
def ensure_files_exist():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(USER_FILE):
        save_data(USER_FILE, [])
    if not os.path.exists(TASK_FILE):
        save_data(TASK_FILE, [])


# Load and save JSON safely
def load_data(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_data(file_path, data):
    try:
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print(f"Failed to save data: {e}")


# Check user authentication before accessing specific routes
def is_authenticated():
    return 'username' in session


def login_required(func):
    """
    Decorator to ensure user is logged in.
    """
    def wrapper(*args, **kwargs):
        if not is_authenticated():
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    wrapper.__name__ = func.__name__
    return wrapper


# Ensure necessary JSON files exist at startup
ensure_files_exist()


# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_data(USER_FILE)

        # Authenticate user
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('task_manager'))
        else:
            flash('Invalid credentials.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_data(USER_FILE)

        # Prevent registration with an existing username
        if any(user['username'] == username for user in users):
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))

        # Save the new user
        users.append({'username': username, 'password': password})
        save_data(USER_FILE, users)
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/task-manager', methods=['GET', 'POST'])
@login_required
def task_manager():
    tasks = load_data(TASK_FILE)

    # Only show the user's tasks
    user_tasks = [task for task in tasks if task['owner'] == session['username']]

    if request.method == 'POST':
        # Add new task
        new_task = {
            'title': request.form['title'],
            'priority': request.form['priority'],
            'difficulty': request.form['difficulty'],
            'due_date': request.form['due_date'],
            'completed': False,
            'owner': session['username']
        }
        tasks.append(new_task)
        save_data(TASK_FILE, tasks)
        flash('Task added successfully!', 'success')
        return redirect(url_for('task_manager'))

    return render_template('task_m.html', tasks=user_tasks)


@app.route('/delete-task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    tasks = load_data(TASK_FILE)
    # Only delete user's own tasks
    tasks = [task for task in tasks if not (task['id'] == task_id and task['owner'] == session['username'])]
    save_data(TASK_FILE, tasks)
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('task_manager'))


@app.route('/update-task/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    tasks = load_data(TASK_FILE)
    for task in tasks:
        if task['id'] == task_id and task['owner'] == session['username']:
            task['title'] = request.form['title']
            task['priority'] = request.form['priority']
            task['difficulty'] = request.form['difficulty']
            task['due_date'] = request.form['due_date']
            break
    save_data(TASK_FILE, tasks)
    flash('Task updated successfully!', 'success')
    return redirect(url_for('task_manager'))


if __name__ == '__main__':
    app.run(debug=True)

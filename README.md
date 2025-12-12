# 🚀 Coder's Legacy Dashboard

**A comprehensive desktop application to track your DSA (Data Structures & Algorithms) problem-solving journey**

## 📝 Short Description

Coder's Legacy Dashboard is a full-stack desktop application built with Python Tkinter and MySQL that helps programmers track their coding practice, monitor progress, and maintain solving streaks. Features include secure authentication, CRUD operations, analytics dashboard, data export capabilities, and a modern dark-themed interface.

---

## ✨ Features

### 🔐 Authentication System
- Secure login with SHA-256 password hashing
- User registration with validation
- Multi-user support with isolated data

### 📊 Dashboard & Analytics
- Real-time statistics (Total problems, Current streak, Hard problems solved)
- Today's progress tracker
- Difficulty distribution with visual progress bars
- Platform-wise problem distribution
- Topic-based analytics
- 7-day activity calendar

### ➕ Problem Management (CRUD)
- **Create**: Add new problems with details (title, platform, topic, difficulty, link, notes)
- **Read**: View all problems in a sortable, searchable table
- **Update**: Edit existing problem details
- **Delete**: Remove problems with confirmation

### 🔍 Advanced Filtering & Sorting
- **Sort by**: Date (Newest/Oldest), Difficulty (Easy→Hard/Hard→Easy), Platform (A-Z), Title (A-Z)
- **Real-time Search**: Filter by title, platform, or topic
- **Color-coded entries**: Green (Easy), Orange (Medium), Red (Hard)

### 📤 Export Capabilities
- **CSV Export**: Export all data to spreadsheet format
- **Text Report**: Generate formatted reports with statistics

### 🎨 Modern UI/UX
- Dark theme with cyan accents
- Responsive layout
- Intuitive navigation sidebar
- Hover effects and smooth interactions

---

## 🛠️ Tech Stack

- **Frontend**: Python Tkinter (ttk for modern widgets)
- **Backend**: MySQL Database
- **Libraries**: 
  - `mysql-connector-python` - Database connectivity
  - `tkinter` - GUI framework
  - `hashlib` - Password encryption
  - `csv` - Data export

---

## 🗄️ Database Setup

### Step 1: Create Database
```sql
CREATE DATABASE coders_legacy_db;
USE coders_legacy_db;
```

### Step 2: Create Tables
```sql
-- Problems table
CREATE TABLE problems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    platform VARCHAR(100),
    difficulty ENUM('Easy', 'Medium', 'Hard'),
    topic VARCHAR(100),
    link VARCHAR(500),
    notes TEXT,
    revision_needed BOOLEAN DEFAULT FALSE,
    date_solved DATE,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Daily activity table
CREATE TABLE daily_activity (
    entry_date DATE,
    problems_solved INT DEFAULT 0,
    time_spent_minutes INT DEFAULT 0,
    user_id INT,
    PRIMARY KEY (entry_date, user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Users table (created automatically by the app)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME
);
```

---

## ⚙️ Installation & Configuration

### Step 1: Clone the Repository
```bash
git clone [https://github.com/Ashutosh-Ves/coders-legacy.git]
cd coders-legacy-dashboard
```

### Step 2: Configure Database Credentials

Open the Python file and update MySQL credentials in **THREE places**:

**1. LoginWindow class (~Line 35-36):**
```python
self.db_conn = mysql.connector.connect(
    host='localhost',
    user='your_mysql_username',      # Change this
    password='your_mysql_password',  # Change this
    database='coders_legacy_db'
)
```

**2. CoderDashboard class (~Line 335-336):**
```python
self.db_conn = mysql.connector.connect(
    host='localhost',
    user='your_mysql_username',      # Change this
    password='your_mysql_password',  # Change this
    database='coders_legacy_db'
)
```

**3. Main execution block (~Line 1095-1098):**
```python
conn = mysql.connector.connect(
    host='localhost',
    user='your_mysql_username',      # Change this
    password='your_mysql_password',  # Change this
    database='coders_legacy_db'
)
```

### Step 3: Run the Application
```bash
python coders_legacy_dashboard.py
```

---

## 📖 Usage Guide

### First Time Setup
1. **Run the application** - It will automatically create the `users` table
2. **Click "Register"** on the login screen
3. **Create your account** with a username and password
4. **Login** with your credentials

### Adding Problems
1. Navigate to **"Add Problem"** from the sidebar
2. Fill in the problem details:
   - Title (required)
   - Platform (required) - e.g., LeetCode, HackerRank, Codeforces
   - Topic - e.g., Arrays, Dynamic Programming, Trees
   - Difficulty - Easy/Medium/Hard
   - Link - Problem URL
   - Notes - Your approach, time complexity, etc.
3. Click **"Save Problem"**

### Viewing & Managing Problems
1. Go to **"View All"** page
2. **Sort** using the dropdown (by date, difficulty, platform, title)
3. **Search** using the search bar
4. **Edit** - Select a problem and click "Edit Selected"
5. **Delete** - Select a problem and click "Delete Selected"

### Viewing Analytics
1. Click **"Analytics"** in the sidebar
2. View your:
   - Difficulty distribution
   - Platform statistics
   - 7-day activity
   - Top topics

### Exporting Data
1. Go to **"Export Data"**
2. Choose format:
   - **CSV** - For spreadsheets (Excel, Google Sheets)
   - **Text Report** - Formatted summary with statistics

---

## 🏗️ Project Structure

```
coders-legacy-dashboard/
│
├── coders_legacy_dashboard.py    # Main application file
├── README.md                       # This file
└── requirements.txt                # Python dependencies
```

---

## 🐛 Troubleshooting

### "Database connection failed"
- Verify MySQL server is running
- Check username/password in all 3 locations
- Ensure `coders_legacy_db` database exists

### "Invalid username or password"
- Use the **Register** feature to create accounts (passwords are hashed)
- Don't create users manually in MySQL without SHA-256 hashing
- If you did, update password: `UPDATE users SET password = SHA2('yourpassword', 256) WHERE username = 'yourusername';`

### "SQL syntax error" during setup
- Ensure you're using MySQL 5.7+ or MySQL 8.0+
- Run the database setup SQL scripts manually if automatic setup fails

### Can't see any data
- Make sure you're logged in with the correct account
- Data is isolated per user - each user only sees their own problems

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

## 📄 License

This project is created for educational purposes. Feel free to use and modify as needed.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [Ashutosh-Ves](https://github.com/Ashutosh-Ves)
- LinkedIn: [Ashutosh Mishra](https://www.linkedin.com/in/ashutosh-mishra-836b50367/)

---

---

**Happy Coding! Keep building your legacy! 🚀**

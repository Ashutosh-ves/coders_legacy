import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
from datetime import datetime, date, timedelta
from mysql.connector import Error
import csv
import hashlib

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Coder's Legacy - Login")
        self.root.geometry("600x600")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)
        
        self.colors = {
            'bg': '#1e1e1e',
            'card': '#252526',
            'accent': '#00bcd4',
            'text': '#ffffff',
            'subtext': '#a0a0a0',
        }
        
        self.db_conn = None
        self.setup_login_ui()
        
    def connect_db(self):
        """Establish connection to MySQL database"""
        try:
            self.db_conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='coders_legacy_db'
            )
            return self.db_conn
        except Error as e:
            messagebox.showerror("Database Error", 
                f"Failed to connect to database:\n{str(e)}")
            return None
    
    def setup_login_ui(self):
        """Setup login form UI"""
        # Logo/Title
        title = tk.Label(self.root, text="Coder's Legacy", 
                        font=('Arial', 28, 'bold'),
                        bg=self.colors['bg'], fg=self.colors['accent'])
        title.pack(pady=(50, 10))
        
        subtitle = tk.Label(self.root, text="Track Your DSA Journey", 
                           font=('Arial', 12),
                           bg=self.colors['bg'], fg=self.colors['subtext'])
        subtitle.pack(pady=(0, 40))
        
        # Login form container
        form_frame = tk.Frame(self.root, bg=self.colors['card'])
        form_frame.pack(padx=40, pady=20, fill='both', expand=True)
        
        # Username
        username_label = tk.Label(form_frame, text="Username", 
                                  font=('Arial', 11),
                                  bg=self.colors['card'], fg=self.colors['text'])
        username_label.pack(pady=(30, 5), padx=30, anchor='w')
        
        self.username_entry = tk.Entry(form_frame, font=('Arial', 12), 
                                       bg=self.colors['bg'], fg=self.colors['text'],
                                       insertbackground=self.colors['text'], bd=0)
        self.username_entry.pack(pady=(0, 20), padx=30, fill='x', ipady=8)
        
        # Password
        password_label = tk.Label(form_frame, text="Password", 
                                  font=('Arial', 11),
                                  bg=self.colors['card'], fg=self.colors['text'])
        password_label.pack(pady=(10, 5), padx=30, anchor='w')
        
        self.password_entry = tk.Entry(form_frame, font=('Arial', 12), show='●',
                                       bg=self.colors['bg'], fg=self.colors['text'],
                                       insertbackground=self.colors['text'], bd=0)
        self.password_entry.pack(pady=(0, 30), padx=30, fill='x', ipady=8)
        
        # Login button
        login_btn = tk.Button(form_frame, text="Login", 
                             command=self.login,
                             font=('Arial', 13, 'bold'),
                             bg=self.colors['accent'], fg='white',
                             cursor='hand2', bd=0, padx=30, pady=12)
        login_btn.pack(pady=(10, 20), padx=30, fill='x')
        
        # Register link
        register_label = tk.Label(form_frame, text="Don't have an account? Register", 
                                 font=('Arial', 10, 'underline'),
                                 bg=self.colors['card'], fg=self.colors['accent'],
                                 cursor='hand2')
        register_label.pack(pady=(0, 30))
        register_label.bind('<Button-1>', lambda e: self.show_register())
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
        
        # Note for first time users
        note = tk.Label(self.root, text="First time? Click 'Register' to create an account", 
                       font=('Arial', 9),
                       bg=self.colors['bg'], fg=self.colors['subtext'])
        note.pack(pady=10)
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self):
        """Validate login credentials from database"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showwarning("Validation", "Please enter both username and password")
            return
        
        conn = self.connect_db()
        if not conn:
            return
        
        try:
            cursor = conn.cursor()
            # SELECT user from 'users' table to validate login credentials
            query = "SELECT id, username FROM users WHERE username = %s AND password = %s"
            hashed_password = self.hash_password(password)
            cursor.execute(query, (username, hashed_password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if user:
                messagebox.showinfo("Success", f"Welcome back, {user[1]}!")
                self.root.destroy()
                # Launch main dashboard
                main_root = tk.Tk()
                CoderDashboard(main_root, user[0], user[1])
                main_root.mainloop()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
                self.password_entry.delete(0, 'end')
        
        except Error as e:
            messagebox.showerror("Database Error", f"Login failed:\n{str(e)}")
    
    def show_register(self):
        """Show registration window"""
        register_win = tk.Toplevel(self.root)
        register_win.title("Register New Account")
        register_win.geometry("400x600")
        register_win.configure(bg=self.colors['bg'])
        register_win.resizable(False, False)
        
        # Title
        title = tk.Label(register_win, text="Create Account", 
                        font=('Arial', 20, 'bold'),
                        bg=self.colors['bg'], fg=self.colors['accent'])
        title.pack(pady=30)
        
        # Form
        form = tk.Frame(register_win, bg=self.colors['card'])
        form.pack(padx=40, pady=20, fill='both', expand=True)
        
        # Username
        tk.Label(form, text="Username", font=('Arial', 11),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=(20, 5), padx=30, anchor='w')
        reg_username = tk.Entry(form, font=('Arial', 12), 
                               bg=self.colors['bg'], fg=self.colors['text'],
                               insertbackground=self.colors['text'], bd=0)
        reg_username.pack(pady=(0, 15), padx=30, fill='x', ipady=8)
        
        # Password
        tk.Label(form, text="Password", font=('Arial', 11),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=(5, 5), padx=30, anchor='w')
        reg_password = tk.Entry(form, font=('Arial', 12), show='●',
                               bg=self.colors['bg'], fg=self.colors['text'],
                               insertbackground=self.colors['text'], bd=0)
        reg_password.pack(pady=(0, 15), padx=30, fill='x', ipady=8)
        
        # Confirm Password
        tk.Label(form, text="Confirm Password", font=('Arial', 11),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=(5, 5), padx=30, anchor='w')
        reg_confirm = tk.Entry(form, font=('Arial', 12), show='●',
                              bg=self.colors['bg'], fg=self.colors['text'],
                              insertbackground=self.colors['text'], bd=0)
        reg_confirm.pack(pady=(0, 20), padx=30, fill='x', ipady=8)
        
        def register():
            username = reg_username.get().strip()
            password = reg_password.get().strip()
            confirm = reg_confirm.get().strip()
            
            if not username or not password:
                messagebox.showwarning("Validation", "All fields are required")
                return
            
            if password != confirm:
                messagebox.showerror("Error", "Passwords don't match")
                return
            
            if len(password) < 4:
                messagebox.showwarning("Validation", "Password must be at least 4 characters")
                return
            
            conn = self.connect_db()
            if not conn:
                return
            
            try:
                cursor = conn.cursor()
                # INSERT new user into 'users' table with hashed password
                query = "INSERT INTO users (username, password, created_at) VALUES (%s, %s, %s)"
                hashed_password = self.hash_password(password)
                cursor.execute(query, (username, hashed_password, datetime.now()))
                conn.commit()
                cursor.close()
                conn.close()
                
                messagebox.showinfo("Success", "Account created successfully! You can now login.")
                register_win.destroy()
            
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Username already exists")
            except Error as e:
                messagebox.showerror("Database Error", f"Registration failed:\n{str(e)}")
        
        # Register button
        tk.Button(form, text="Register", command=register,
                 font=('Arial', 13, 'bold'),
                 bg=self.colors['accent'], fg='white',
                 cursor='hand2', bd=0, padx=30, pady=12).pack(pady=20, padx=30, fill='x')
    
    def run(self):
        self.root.mainloop()

class CoderDashboard:
    def __init__(self, root, user_id, username):
        self.root = root
        self.user_id = user_id
        self.username = username
        self.root.title(f"Coder's Legacy Dashboard - {username}")
        self.root.geometry("1200x700")
        self.root.configure(bg="#1e1e1e")
        
        # Color scheme
        self.colors = {
            'bg': '#1e1e1e',
            'sidebar': '#2d2d30',
            'card': '#252526',
            'accent': '#00bcd4',
            'text': '#ffffff',
            'subtext': '#a0a0a0',
            'easy': '#4caf50',
            'medium': '#ff9800',
            'hard': '#f44336',
            'button_hover': '#3d3d40'
        }
        
        # Database connection
        self.db_conn = None
        self.connect_db()
        
        # Setup UI
        self.setup_ui()
        self.show_dashboard()
    
    def connect_db(self):
        """Establish connection to MySQL database"""
        try:
            self.db_conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='coders_legacy_db'
            )
            if self.db_conn.is_connected():
                print("Successfully connected to database")
        except Error as e:
            messagebox.showerror("Database Error", 
                f"Failed to connect to database:\n{str(e)}\n\nPlease check your MySQL credentials and ensure the database exists.")
            self.db_conn = None
    
    def setup_ui(self):
        """Setup the main UI structure with sidebar and content area"""
        # Sidebar
        self.sidebar = tk.Frame(self.root, bg=self.colors['sidebar'], width=200)
        self.sidebar.pack(side='left', fill='y')
        self.sidebar.pack_propagate(False)
        
        # Logo/Title
        title = tk.Label(self.sidebar, text="Coder's Legacy", 
                        font=('Arial', 18, 'bold'),
                        bg=self.colors['sidebar'], fg=self.colors['accent'])
        title.pack(pady=20, padx=10)
        
        # User info
        user_label = tk.Label(self.sidebar, text=f"👤 {self.username}", 
                             font=('Arial', 11),
                             bg=self.colors['sidebar'], fg=self.colors['text'])
        user_label.pack(pady=(0, 20), padx=10)
        
        # Navigation buttons
        self.nav_buttons = []
        nav_items = [
            ("📊 Dashboard", self.show_dashboard),
            ("➕ Add Problem", self.show_add_problem),
            ("📋 View All", self.show_view_all),
            ("📈 Analytics", self.show_analytics),
            ("📤 Export Data", self.show_export_options),
            ("🚪 Logout", self.logout)
        ]
        
        for text, command in nav_items:
            btn = tk.Button(self.sidebar, text=text, command=command,
                          font=('Arial', 11), bg=self.colors['sidebar'],
                          fg=self.colors['text'], bd=0, padx=20, pady=15,
                          cursor='hand2', anchor='w')
            btn.pack(fill='x', pady=3, padx=10)
            self.nav_buttons.append(btn)
            
            # Hover effects
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg=self.colors['button_hover']))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg=self.colors['sidebar']))
        
        # Main content area
        self.content_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.content_frame.pack(side='right', fill='both', expand=True)
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            login = LoginWindow()
            login.run()
    
    def show_dashboard(self):
        """Display the dashboard with statistics"""
        self.clear_content()
        
        # Header
        header = tk.Label(self.content_frame, text="Dashboard", 
                         font=('Arial', 24, 'bold'),
                         bg=self.colors['bg'], fg=self.colors['text'])
        header.pack(pady=20, padx=30, anchor='w')
        
        # Stats container
        stats_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        stats_frame.pack(fill='x', padx=30, pady=10)
        
        # Fetch statistics
        total_problems = self.get_total_problems()
        streak = self.get_streak()
        hard_solved = self.get_hard_problems()
        
        # Create stat cards
        stats = [
            ("Total Problems", total_problems, self.colors['accent']),
            ("Current Streak", f"{streak} days", self.colors['easy']),
            ("Hard Solved", hard_solved, self.colors['hard'])
        ]
        
        for i, (label, value, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=self.colors['card'], 
                          highlightbackground=color, highlightthickness=2)
            card.grid(row=0, column=i, padx=10, sticky='ew')
            stats_frame.grid_columnconfigure(i, weight=1)
            
            value_label = tk.Label(card, text=str(value), 
                                  font=('Arial', 32, 'bold'),
                                  bg=self.colors['card'], fg=color)
            value_label.pack(pady=(20, 5))
            
            text_label = tk.Label(card, text=label, 
                                font=('Arial', 12),
                                bg=self.colors['card'], fg=self.colors['subtext'])
            text_label.pack(pady=(0, 20))
        
        # Today's Progress Section
        progress_frame = tk.Frame(self.content_frame, bg=self.colors['card'])
        progress_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        progress_title = tk.Label(progress_frame, text="Today's Progress", 
                                 font=('Arial', 18, 'bold'),
                                 bg=self.colors['card'], fg=self.colors['text'])
        progress_title.pack(pady=20, padx=20, anchor='w')
        
        today_stats = self.get_today_stats()
        
        if today_stats:
            problems_today, time_today = today_stats
            status_text = f"✓ Great work! You've solved {problems_today} problem(s) today"
            status_color = self.colors['easy']
        else:
            status_text = "○ No problems solved yet today. Keep going!"
            status_color = self.colors['subtext']
        
        status_label = tk.Label(progress_frame, text=status_text,
                               font=('Arial', 14),
                               bg=self.colors['card'], fg=status_color)
        status_label.pack(pady=10, padx=20, anchor='w')
        
        # Quick Mini Analytics
        mini_analytics = tk.Frame(progress_frame, bg=self.colors['card'])
        mini_analytics.pack(fill='x', padx=20, pady=10)
        
        difficulty_dist = self.get_difficulty_distribution()
        
        tk.Label(mini_analytics, text="Problem Distribution:", 
                font=('Arial', 13, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor='w', pady=5)
        
        for diff, count in difficulty_dist.items():
            color = self.colors.get(diff.lower(), self.colors['text'])
            tk.Label(mini_analytics, text=f"{diff}: {count} problems", 
                    font=('Arial', 11),
                    bg=self.colors['card'], fg=color).pack(anchor='w', padx=20)
    
    def show_add_problem(self):
        """Display the Add Problem form"""
        self.clear_content()
        
        # Header
        header = tk.Label(self.content_frame, text="Add New Problem", 
                         font=('Arial', 24, 'bold'),
                         bg=self.colors['bg'], fg=self.colors['text'])
        header.pack(pady=20, padx=30, anchor='w')
        
        # Form container
        form_frame = tk.Frame(self.content_frame, bg=self.colors['card'])
        form_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Form fields
        fields = [
            ("Title:", "title"),
            ("Platform:", "platform"),
            ("Topic:", "topic"),
            ("Link:", "link")
        ]
        
        self.entries = {}
        
        for i, (label_text, field_name) in enumerate(fields):
            label = tk.Label(form_frame, text=label_text, 
                           font=('Arial', 12),
                           bg=self.colors['card'], fg=self.colors['text'])
            label.grid(row=i, column=0, sticky='w', padx=20, pady=15)
            
            entry = tk.Entry(form_frame, font=('Arial', 12), 
                           bg=self.colors['bg'], fg=self.colors['text'],
                           insertbackground=self.colors['text'], bd=0)
            entry.grid(row=i, column=1, sticky='ew', padx=20, pady=15)
            self.entries[field_name] = entry
        
        # Difficulty dropdown
        diff_label = tk.Label(form_frame, text="Difficulty:", 
                             font=('Arial', 12),
                             bg=self.colors['card'], fg=self.colors['text'])
        diff_label.grid(row=len(fields), column=0, sticky='w', padx=20, pady=15)
        
        self.difficulty_var = tk.StringVar()
        difficulty_combo = ttk.Combobox(form_frame, textvariable=self.difficulty_var,
                                       values=['Easy', 'Medium', 'Hard'],
                                       state='readonly', font=('Arial', 12))
        difficulty_combo.set('Medium')
        difficulty_combo.grid(row=len(fields), column=1, sticky='ew', padx=20, pady=15)
        
        # Notes text area
        notes_label = tk.Label(form_frame, text="Notes:", 
                              font=('Arial', 12),
                              bg=self.colors['card'], fg=self.colors['text'])
        notes_label.grid(row=len(fields)+1, column=0, sticky='nw', padx=20, pady=15)
        
        self.notes_text = tk.Text(form_frame, height=5, font=('Arial', 11),
                                 bg=self.colors['bg'], fg=self.colors['text'],
                                 insertbackground=self.colors['text'], bd=0)
        self.notes_text.grid(row=len(fields)+1, column=1, sticky='ew', padx=20, pady=15)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Save button
        save_btn = tk.Button(form_frame, text="Save Problem", 
                           command=self.save_problem,
                           font=('Arial', 14, 'bold'),
                           bg=self.colors['accent'], fg='white',
                           cursor='hand2', bd=0, padx=30, pady=15)
        save_btn.grid(row=len(fields)+2, column=0, columnspan=2, pady=30)
    
    def show_view_all(self):
        """Display all problems in a treeview with sorting and search"""
        self.clear_content()
        
        # Header
        header_frame = tk.Frame(self.content_frame, bg=self.colors['bg'])
        header_frame.pack(fill='x', padx=30, pady=20)
        
        header = tk.Label(header_frame, text="All Problems", 
                         font=('Arial', 24, 'bold'),
                         bg=self.colors['bg'], fg=self.colors['text'])
        header.pack(side='left')
        
        # Control panel
        control_frame = tk.Frame(self.content_frame, bg=self.colors['card'])
        control_frame.pack(fill='x', padx=30, pady=(0, 10))
        
        # Sort options
        tk.Label(control_frame, text="Sort by:", font=('Arial', 11),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left', padx=(20, 5), pady=10)
        
        self.sort_var = tk.StringVar(value="Date (Newest)")
        sort_combo = ttk.Combobox(control_frame, textvariable=self.sort_var,
                                 values=['Date (Newest)', 'Date (Oldest)', 
                                        'Difficulty (Easy→Hard)', 'Difficulty (Hard→Easy)',
                                        'Platform (A-Z)', 'Title (A-Z)'],
                                 state='readonly', width=20)
        sort_combo.pack(side='left', padx=5, pady=10)
        sort_combo.bind('<<ComboboxSelected>>', lambda e: self.load_all_problems())
        
        # Search
        tk.Label(control_frame, text="Search:", font=('Arial', 11),
                bg=self.colors['card'], fg=self.colors['text']).pack(side='left', padx=(20, 5), pady=10)
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(control_frame, textvariable=self.search_var,
                               font=('Arial', 11), bg=self.colors['bg'], 
                               fg=self.colors['text'], bd=0, width=30)
        search_entry.pack(side='left', padx=5, pady=10, ipady=5)
        self.search_var.trace('w', lambda *args: self.load_all_problems())
        
        # Action buttons
        btn_frame = tk.Frame(control_frame, bg=self.colors['card'])
        btn_frame.pack(side='right', padx=20, pady=10)
        
        delete_btn = tk.Button(btn_frame, text="Delete Selected", 
                              command=self.delete_selected_problem,
                              font=('Arial', 10), bg=self.colors['hard'], fg='white',
                              cursor='hand2', bd=0, padx=15, pady=8)
        delete_btn.pack(side='left', padx=5)
        
        edit_btn = tk.Button(btn_frame, text="Edit Selected", 
                            command=self.edit_selected_problem,
                            font=('Arial', 10), bg=self.colors['accent'], fg='white',
                            cursor='hand2', bd=0, padx=15, pady=8)
        edit_btn.pack(side='left', padx=5)
        
        # Treeview frame
        tree_frame = tk.Frame(self.content_frame, bg=self.colors['card'])
        tree_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(tree_frame, orient='vertical')
        scroll_x = ttk.Scrollbar(tree_frame, orient='horizontal')
        
        # Treeview
        columns = ('ID', 'Title', 'Platform', 'Difficulty', 'Topic', 'Date', 'Revision')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                yscrollcommand=scroll_y.set,
                                xscrollcommand=scroll_x.set)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Column headings
        widths = [50, 250, 120, 100, 150, 100, 100]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        # Pack widgets
        scroll_y.pack(side='right', fill='y')
        scroll_x.pack(side='bottom', fill='x')
        self.tree.pack(fill='both', expand=True)
        
        # Configure tags for colors
        self.tree.tag_configure('Easy', foreground=self.colors['easy'])
        self.tree.tag_configure('Medium', foreground=self.colors['medium'])
        self.tree.tag_configure('Hard', foreground=self.colors['hard'])
        
        # Load data
        self.load_all_problems()
    
    def show_analytics(self):
        """Display analytics dashboard with charts"""
        self.clear_content()
        
        # Header
        header = tk.Label(self.content_frame, text="Analytics Dashboard", 
                         font=('Arial', 24, 'bold'),
                         bg=self.colors['bg'], fg=self.colors['text'])
        header.pack(pady=20, padx=30, anchor='w')
        
        # Main container
        main_container = tk.Frame(self.content_frame, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=30, pady=10)
        
        # Left column - Stats
        left_col = tk.Frame(main_container, bg=self.colors['bg'])
        left_col.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Difficulty Distribution Card
        diff_card = tk.Frame(left_col, bg=self.colors['card'])
        diff_card.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(diff_card, text="Difficulty Distribution", 
                font=('Arial', 16, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=15, padx=20, anchor='w')
        
        difficulty_dist = self.get_difficulty_distribution()
        total = sum(difficulty_dist.values())
        
        for diff, count in difficulty_dist.items():
            percentage = (count / total * 100) if total > 0 else 0
            color = self.colors.get(diff.lower(), self.colors['text'])
            
            item_frame = tk.Frame(diff_card, bg=self.colors['card'])
            item_frame.pack(fill='x', padx=20, pady=5)
            
            tk.Label(item_frame, text=f"{diff}:", font=('Arial', 12),
                    bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
            
            tk.Label(item_frame, text=f"{count} ({percentage:.1f}%)", 
                    font=('Arial', 12, 'bold'),
                    bg=self.colors['card'], fg=color).pack(side='right')
            
            # Progress bar
            bar_frame = tk.Frame(diff_card, bg=self.colors['bg'], height=10)
            bar_frame.pack(fill='x', padx=20, pady=(0, 10))
            
            bar = tk.Frame(bar_frame, bg=color, height=10)
            bar.pack(side='left', fill='y')
            bar.config(width=int(percentage * 3))
        
        # Platform Distribution Card
        platform_card = tk.Frame(left_col, bg=self.colors['card'])
        platform_card.pack(fill='both', expand=True)
        
        tk.Label(platform_card, text="Platform Distribution", 
                font=('Arial', 16, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=15, padx=20, anchor='w')
        
        platforms = self.get_platform_distribution()
        
        for platform, count in list(platforms.items())[:5]:  # Top 5
            item_frame = tk.Frame(platform_card, bg=self.colors['card'])
            item_frame.pack(fill='x', padx=20, pady=5)
            
            tk.Label(item_frame, text=f"{platform}:", font=('Arial', 11),
                    bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
            
            tk.Label(item_frame, text=f"{count} problems", 
                    font=('Arial', 11, 'bold'),
                    bg=self.colors['card'], fg=self.colors['accent']).pack(side='right')
        
        # Right column - Activity
        right_col = tk.Frame(main_container, bg=self.colors['bg'])
        right_col.pack(side='right', fill='both', expand=True, padx=(10, 0))
        
        # Recent Activity Card
        activity_card = tk.Frame(right_col, bg=self.colors['card'])
        activity_card.pack(fill='both', expand=True, pady=(0, 10))
        
        tk.Label(activity_card, text="7-Day Activity", 
                font=('Arial', 16, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=15, padx=20, anchor='w')
        
        weekly_activity = self.get_weekly_activity()
        
        for day_data in weekly_activity:
            day_date, count = day_data
            day_name = day_date.strftime('%a, %b %d')
            
            item_frame = tk.Frame(activity_card, bg=self.colors['card'])
            item_frame.pack(fill='x', padx=20, pady=5)
            
            tk.Label(item_frame, text=day_name, font=('Arial', 11),
                    bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
            
            color = self.colors['easy'] if count > 0 else self.colors['subtext']
            tk.Label(item_frame, text=f"{count} problems", 
                    font=('Arial', 11, 'bold'),
                    bg=self.colors['card'], fg=color).pack(side='right')
        
        # Topic Distribution Card
        topic_card = tk.Frame(right_col, bg=self.colors['card'])
        topic_card.pack(fill='both', expand=True)
        
        tk.Label(topic_card, text="Top Topics", 
                font=('Arial', 16, 'bold'),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=15, padx=20, anchor='w')
        
        topics = self.get_topic_distribution()
        
        for topic, count in list(topics.items())[:5]:  # Top 5
            item_frame = tk.Frame(topic_card, bg=self.colors['card'])
            item_frame.pack(fill='x', padx=20, pady=5)
            
            tk.Label(item_frame, text=f"{topic}:", font=('Arial', 11),
                    bg=self.colors['card'], fg=self.colors['text']).pack(side='left')
            
            tk.Label(item_frame, text=f"{count} problems", 
                    font=('Arial', 11, 'bold'),
                    bg=self.colors['card'], fg=self.colors['accent']).pack(side='right')
    
    def show_export_options(self):
        """Display export options"""
        self.clear_content()
        
        # Header
        header = tk.Label(self.content_frame, text="Export Data", 
                         font=('Arial', 24, 'bold'),
                         bg=self.colors['bg'], fg=self.colors['text'])
        header.pack(pady=20, padx=30, anchor='w')
        
        # Export container
        export_frame = tk.Frame(self.content_frame, bg=self.colors['card'])
        export_frame.pack(fill='both', expand=True, padx=30, pady=10)
        
        tk.Label(export_frame, text="Choose export format:", 
                font=('Arial', 16),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=30)
        
        # CSV Export Button
        csv_btn = tk.Button(export_frame, text="📄 Export to CSV", 
                           command=self.export_to_csv,
                           font=('Arial', 14, 'bold'),
                           bg=self.colors['easy'], fg='white',
                           cursor='hand2', bd=0, padx=50, pady=20)
        csv_btn.pack(pady=20)
        
        tk.Label(export_frame, text="Export all problems to a CSV file", 
                font=('Arial', 11),
                bg=self.colors['card'], fg=self.colors['subtext']).pack()
        
        # Text Report Button
        txt_btn = tk.Button(export_frame, text="📋 Export to Text Report", 
                           command=self.export_to_text,
                           font=('Arial', 14, 'bold'),
                           bg=self.colors['accent'], fg='white',
                           cursor='hand2', bd=0, padx=50, pady=20)
        txt_btn.pack(pady=20)
        
        tk.Label(export_frame, text="Generate a formatted text report with statistics", 
                font=('Arial', 11),
                bg=self.colors['card'], fg=self.colors['subtext']).pack()
    
    def export_to_csv(self):
        """Export all problems to CSV file"""
        if not self.db_conn or not self.db_conn.is_connected():
            messagebox.showerror("Error", "No database connection")
            return
        
        try:
            # Ask user where to save
            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                initialfile=f"coders_legacy_export_{date.today()}.csv"
            )
            
            if not filename:
                return
            
            cursor = self.db_conn.cursor()
            # SELECT all problem data for export
            query = """
                SELECT id, title, platform, difficulty, topic, link, notes, 
                       date_solved, revision_needed
                FROM problems
                ORDER BY date_solved DESC
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            # Write to CSV
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Title', 'Platform', 'Difficulty', 'Topic', 
                               'Link', 'Notes', 'Date Solved', 'Revision Needed'])
                writer.writerows(rows)
            
            messagebox.showinfo("Success", f"Data exported successfully to:\n{filename}")
        
        except Error as e:
            messagebox.showerror("Database Error", f"Export failed:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed:\n{str(e)}")
    
    def export_to_text(self):
        """Export a formatted text report"""
        if not self.db_conn or not self.db_conn.is_connected():
            messagebox.showerror("Error", "No database connection")
            return
        
        try:
            # Ask user where to save
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialfile=f"coders_legacy_report_{date.today()}.txt"
            )
            
            if not filename:
                return
            
            # Generate report
            report = []
            report.append("=" * 60)
            report.append("CODER'S LEGACY - PROGRESS REPORT")
            report.append("=" * 60)
            report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report.append(f"User: {self.username}")
            report.append("")
            
            # Statistics
            report.append("OVERALL STATISTICS")
            report.append("-" * 60)
            report.append(f"Total Problems Solved: {self.get_total_problems()}")
            report.append(f"Current Streak: {self.get_streak()} days")
            report.append(f"Hard Problems Solved: {self.get_hard_problems()}")
            report.append("")
            
            # Difficulty Distribution
            report.append("DIFFICULTY DISTRIBUTION")
            report.append("-" * 60)
            difficulty_dist = self.get_difficulty_distribution()
            for diff, count in difficulty_dist.items():
                report.append(f"{diff}: {count} problems")
            report.append("")
            
            # Platform Distribution
            report.append("PLATFORM DISTRIBUTION")
            report.append("-" * 60)
            platforms = self.get_platform_distribution()
            for platform, count in list(platforms.items())[:10]:
                report.append(f"{platform}: {count} problems")
            report.append("")
            
            # Recent Problems
            report.append("RECENT PROBLEMS (Last 10)")
            report.append("-" * 60)
            cursor = self.db_conn.cursor()
            cursor.execute("""
                SELECT title, platform, difficulty, date_solved
                FROM problems
                ORDER BY date_solved DESC
                LIMIT 10
            """)
            recent = cursor.fetchall()
            cursor.close()
            
            for title, platform, difficulty, solved_date in recent:
                report.append(f"• {title} [{difficulty}] - {platform} ({solved_date})")
            
            report.append("")
            report.append("=" * 60)
            report.append("Keep coding and learning!")
            report.append("=" * 60)
            
            # Write to file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report))
            
            messagebox.showinfo("Success", f"Report generated successfully:\n{filename}")
        
        except Error as e:
            messagebox.showerror("Database Error", f"Report generation failed:\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Report generation failed:\n{str(e)}")
    
    def save_problem(self):
        """Save the problem to database and update daily activity"""
        if not self.db_conn or not self.db_conn.is_connected():
            messagebox.showerror("Error", "No database connection")
            return
        
        # Get form data
        title = self.entries['title'].get().strip()
        platform = self.entries['platform'].get().strip()
        topic = self.entries['topic'].get().strip()
        difficulty = self.difficulty_var.get()
        link = self.entries['link'].get().strip()
        notes = self.notes_text.get('1.0', 'end-1c').strip()
        
        if not title or not platform:
            messagebox.showwarning("Validation", "Title and Platform are required!")
            return
        
        try:
            cursor = self.db_conn.cursor()
            
            # INSERT new problem into 'problems' table
            # Stores: title, platform, difficulty, topic, link, notes, and today's date
            insert_query = """
                INSERT INTO problems (title, platform, difficulty, topic, link, notes, date_solved, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (title, platform, difficulty, topic, link, notes, date.today(), self.user_id)
            cursor.execute(insert_query, values)
            
            # UPSERT daily_activity: Update if today's entry exists, Insert if not
            # This increments problems_solved count for today
            upsert_query = """
                INSERT INTO daily_activity (entry_date, problems_solved, time_spent_minutes, user_id)
                VALUES (%s, 1, 0, %s)
                ON DUPLICATE KEY UPDATE problems_solved = problems_solved + 1
            """
            cursor.execute(upsert_query, (date.today(), self.user_id))
            
            self.db_conn.commit()
            cursor.close()
            
            messagebox.showinfo("Success", "Problem saved successfully!")
            
            # Clear form
            for entry in self.entries.values():
                entry.delete(0, 'end')
            self.notes_text.delete('1.0', 'end')
            self.difficulty_var.set('Medium')
            
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to save problem:\n{str(e)}")
    
    def load_all_problems(self):
        """Load all problems into the treeview with sorting and filtering"""
        if not self.db_conn or not self.db_conn.is_connected():
            return
        
        try:
            cursor = self.db_conn.cursor()
            
            # Build query based on sort selection
            sort_option = self.sort_var.get()
            order_clause = "ORDER BY date_solved DESC"  # Default
            
            if sort_option == "Date (Oldest)":
                order_clause = "ORDER BY date_solved ASC"
            elif sort_option == "Difficulty (Easy→Hard)":
                order_clause = "ORDER BY FIELD(difficulty, 'Easy', 'Medium', 'Hard')"
            elif sort_option == "Difficulty (Hard→Easy)":
                order_clause = "ORDER BY FIELD(difficulty, 'Hard', 'Medium', 'Easy')"
            elif sort_option == "Platform (A-Z)":
                order_clause = "ORDER BY platform ASC"
            elif sort_option == "Title (A-Z)":
                order_clause = "ORDER BY title ASC"
            
            # Add search filter
            search_term = self.search_var.get().strip()
            where_clause = f"WHERE user_id = {self.user_id}"
            
            if search_term:
                where_clause += f""" AND (
                    title LIKE '%{search_term}%' OR 
                    platform LIKE '%{search_term}%' OR 
                    topic LIKE '%{search_term}%'
                )"""
            
            # SELECT problems with sorting and filtering
            query = f"""
                SELECT id, title, platform, difficulty, topic, date_solved, revision_needed
                FROM problems
                {where_clause}
                {order_clause}
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            # Clear existing items
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Insert data with color coding
            for row in rows:
                problem_id, title, platform, difficulty, topic, date_solved, revision = row
                revision_status = "Yes" if revision else "No"
                
                self.tree.insert('', 'end', 
                               values=(problem_id, title, platform, difficulty, 
                                      topic, date_solved, revision_status),
                               tags=(difficulty,))
        
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to load problems:\n{str(e)}")
    
    def delete_selected_problem(self):
        """Delete the selected problem"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a problem to delete")
            return
        
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this problem?"):
            return
        
        try:
            item = self.tree.item(selected[0])
            problem_id = item['values'][0]
            
            cursor = self.db_conn.cursor()
            # DELETE selected problem from database
            cursor.execute("DELETE FROM problems WHERE id = %s AND user_id = %s", 
                          (problem_id, self.user_id))
            self.db_conn.commit()
            cursor.close()
            
            messagebox.showinfo("Success", "Problem deleted successfully!")
            self.load_all_problems()
        
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to delete problem:\n{str(e)}")
    
    def edit_selected_problem(self):
        """Edit the selected problem"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection", "Please select a problem to edit")
            return
        
        item = self.tree.item(selected[0])
        problem_id = item['values'][0]
        
        # Fetch full problem data
        try:
            cursor = self.db_conn.cursor()
            cursor.execute("""
                SELECT title, platform, topic, difficulty, link, notes, revision_needed
                FROM problems WHERE id = %s AND user_id = %s
            """, (problem_id, self.user_id))
            problem_data = cursor.fetchone()
            cursor.close()
            
            if not problem_data:
                messagebox.showerror("Error", "Problem not found")
                return
            
            # Create edit window
            edit_win = tk.Toplevel(self.root)
            edit_win.title("Edit Problem")
            edit_win.geometry("600x600")
            edit_win.configure(bg=self.colors['bg'])
            
            # Header
            tk.Label(edit_win, text="Edit Problem", font=('Arial', 18, 'bold'),
                    bg=self.colors['bg'], fg=self.colors['text']).pack(pady=20)
            
            # Form
            form = tk.Frame(edit_win, bg=self.colors['card'])
            form.pack(fill='both', expand=True, padx=20, pady=10)
            
            # Fields
            fields = {}
            field_names = ['title', 'platform', 'topic', 'link']
            labels = ['Title:', 'Platform:', 'Topic:', 'Link:']
            
            for i, (field, label) in enumerate(zip(field_names, labels)):
                tk.Label(form, text=label, font=('Arial', 11),
                        bg=self.colors['card'], fg=self.colors['text']).grid(
                        row=i, column=0, sticky='w', padx=20, pady=10)
                
                entry = tk.Entry(form, font=('Arial', 11),
                               bg=self.colors['bg'], fg=self.colors['text'],
                               insertbackground=self.colors['text'], bd=0)
                entry.grid(row=i, column=1, sticky='ew', padx=20, pady=10)
                entry.insert(0, problem_data[i])
                fields[field] = entry
            
            form.grid_columnconfigure(1, weight=1)
            
            # Difficulty
            tk.Label(form, text="Difficulty:", font=('Arial', 11),
                    bg=self.colors['card'], fg=self.colors['text']).grid(
                    row=4, column=0, sticky='w', padx=20, pady=10)
            
            diff_var = tk.StringVar(value=problem_data[3])
            diff_combo = ttk.Combobox(form, textvariable=diff_var,
                                     values=['Easy', 'Medium', 'Hard'],
                                     state='readonly')
            diff_combo.grid(row=4, column=1, sticky='ew', padx=20, pady=10)
            
            # Notes
            tk.Label(form, text="Notes:", font=('Arial', 11),
                    bg=self.colors['card'], fg=self.colors['text']).grid(
                    row=5, column=0, sticky='nw', padx=20, pady=10)
            
            notes_text = tk.Text(form, height=5, font=('Arial', 10),
                                bg=self.colors['bg'], fg=self.colors['text'],
                                insertbackground=self.colors['text'], bd=0)
            notes_text.grid(row=5, column=1, sticky='ew', padx=20, pady=10)
            notes_text.insert('1.0', problem_data[5])
            
            # Revision checkbox
            revision_var = tk.BooleanVar(value=problem_data[6])
            revision_check = tk.Checkbutton(form, text="Needs Revision",
                                           variable=revision_var,
                                           font=('Arial', 11),
                                           bg=self.colors['card'], fg=self.colors['text'],
                                           selectcolor=self.colors['bg'])
            revision_check.grid(row=6, column=1, sticky='w', padx=20, pady=10)
            
            def save_changes():
                try:
                    cursor = self.db_conn.cursor()
                    # UPDATE problem data in database
                    update_query = """
                        UPDATE problems 
                        SET title=%s, platform=%s, topic=%s, difficulty=%s, 
                            link=%s, notes=%s, revision_needed=%s
                        WHERE id=%s AND user_id=%s
                    """
                    cursor.execute(update_query, (
                        fields['title'].get(), fields['platform'].get(),
                        fields['topic'].get(), diff_var.get(),
                        fields['link'].get(), notes_text.get('1.0', 'end-1c'),
                        revision_var.get(), problem_id, self.user_id
                    ))
                    self.db_conn.commit()
                    cursor.close()
                    
                    messagebox.showinfo("Success", "Problem updated successfully!")
                    edit_win.destroy()
                    self.load_all_problems()
                
                except Error as e:
                    messagebox.showerror("Database Error", f"Update failed:\n{str(e)}")
            
            # Save button
            tk.Button(form, text="Save Changes", command=save_changes,
                     font=('Arial', 12, 'bold'),
                     bg=self.colors['accent'], fg='white',
                     cursor='hand2', bd=0, padx=30, pady=12).grid(
                     row=7, column=0, columnspan=2, pady=20)
        
        except Error as e:
            messagebox.showerror("Database Error", f"Failed to fetch problem:\n{str(e)}")
    
    def get_total_problems(self):
        """Get total count of problems solved by user"""
        if not self.db_conn or not self.db_conn.is_connected():
            return 0
        
        try:
            cursor = self.db_conn.cursor()
            # COUNT total number of problems for current user
            cursor.execute("SELECT COUNT(*) FROM problems WHERE user_id = %s", (self.user_id,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except Error:
            return 0
    
    def get_streak(self):
        """Calculate current solving streak (consecutive days)"""
        if not self.db_conn or not self.db_conn.is_connected():
            return 0
        
        try:
            cursor = self.db_conn.cursor()
            # SELECT all activity dates for user ordered by most recent first
            cursor.execute("""
                SELECT entry_date FROM daily_activity 
                WHERE user_id = %s 
                ORDER BY entry_date DESC
            """, (self.user_id,))
            dates = [row[0] for row in cursor.fetchall()]
            cursor.close()
            
            if not dates:
                return 0
            
            # Calculate consecutive days streak
            streak = 0
            expected_date = date.today()
            
            for activity_date in dates:
                if activity_date == expected_date:
                    streak += 1
                    expected_date -= timedelta(days=1)
                elif activity_date < expected_date:
                    break
            
            return streak
        
        except Error:
            return 0
    
    def get_hard_problems(self):
        """Get count of hard difficulty problems"""
        if not self.db_conn or not self.db_conn.is_connected():
            return 0
        
        try:
            cursor = self.db_conn.cursor()
            # COUNT problems with 'Hard' difficulty for user
            cursor.execute("""
                SELECT COUNT(*) FROM problems 
                WHERE difficulty = 'Hard' AND user_id = %s
            """, (self.user_id,))
            result = cursor.fetchone()
            cursor.close()
            return result[0] if result else 0
        except Error:
            return 0
    
    def get_today_stats(self):
        """Get today's solving statistics"""
        if not self.db_conn or not self.db_conn.is_connected():
            return None
        
        try:
            cursor = self.db_conn.cursor()
            # SELECT today's activity entry for user
            query = """
                SELECT problems_solved, time_spent_minutes 
                FROM daily_activity 
                WHERE entry_date = %s AND user_id = %s
            """
            cursor.execute(query, (date.today(), self.user_id))
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error:
            return None
    
    def get_difficulty_distribution(self):
        """Get count of problems by difficulty"""
        if not self.db_conn or not self.db_conn.is_connected():
            return {'Easy': 0, 'Medium': 0, 'Hard': 0}
        
        try:
            cursor = self.db_conn.cursor()
            # COUNT problems grouped by difficulty for user
            cursor.execute("""
                SELECT difficulty, COUNT(*) 
                FROM problems 
                WHERE user_id = %s 
                GROUP BY difficulty
            """, (self.user_id,))
            results = cursor.fetchall()
            cursor.close()
            
            dist = {'Easy': 0, 'Medium': 0, 'Hard': 0}
            for difficulty, count in results:
                dist[difficulty] = count
            
            return dist
        except Error:
            return {'Easy': 0, 'Medium': 0, 'Hard': 0}
    
    def get_platform_distribution(self):
        """Get count of problems by platform"""
        if not self.db_conn or not self.db_conn.is_connected():
            return {}
        
        try:
            cursor = self.db_conn.cursor()
            # COUNT problems grouped by platform for user
            cursor.execute("""
                SELECT platform, COUNT(*) 
                FROM problems 
                WHERE user_id = %s 
                GROUP BY platform 
                ORDER BY COUNT(*) DESC
            """, (self.user_id,))
            results = cursor.fetchall()
            cursor.close()
            
            return {platform: count for platform, count in results}
        except Error:
            return {}
    
    def get_topic_distribution(self):
        """Get count of problems by topic"""
        if not self.db_conn or not self.db_conn.is_connected():
            return {}
        
        try:
            cursor = self.db_conn.cursor()
            # COUNT problems grouped by topic for user
            cursor.execute("""
                SELECT topic, COUNT(*) 
                FROM problems 
                WHERE user_id = %s AND topic != '' 
                GROUP BY topic 
                ORDER BY COUNT(*) DESC
            """, (self.user_id,))
            results = cursor.fetchall()
            cursor.close()
            
            return {topic: count for topic, count in results}
        except Error:
            return {}
    
    def get_weekly_activity(self):
        """Get last 7 days activity"""
        if not self.db_conn or not self.db_conn.is_connected():
            return []
        
        try:
            cursor = self.db_conn.cursor()
            # SELECT activity for last 7 days
            activity = []
            for i in range(6, -1, -1):
                day = date.today() - timedelta(days=i)
                cursor.execute("""
                    SELECT problems_solved 
                    FROM daily_activity 
                    WHERE entry_date = %s AND user_id = %s
                """, (day, self.user_id))
                result = cursor.fetchone()
                count = result[0] if result else 0
                activity.append((day, count))
            
            cursor.close()
            return activity
        except Error:
            return []
    
    def __del__(self):
        """Cleanup database connection"""
        if self.db_conn and self.db_conn.is_connected():
            self.db_conn.close()

# Main execution
if __name__ == "__main__":
    # First, ensure the users table exists
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='coders_legacy_db'
        )
        cursor = conn.cursor()
        
        # Create users table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at DATETIME
            )
        """)
        
        # Check and add user_id to problems table
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'coders_legacy_db' 
            AND TABLE_NAME = 'problems' 
            AND COLUMN_NAME = 'user_id'
        """)
        if cursor.fetchone()[0] == 0:
            cursor.execute("ALTER TABLE problems ADD COLUMN user_id INT")
            cursor.execute("""
                ALTER TABLE problems 
                ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            """)
        
        # Check and add user_id to daily_activity
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'coders_legacy_db' 
            AND TABLE_NAME = 'daily_activity' 
            AND COLUMN_NAME = 'user_id'
        """)
        if cursor.fetchone()[0] == 0:
            cursor.execute("ALTER TABLE daily_activity ADD COLUMN user_id INT")
            
            # Create a default user if none exists
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO users (username, password, created_at) 
                    VALUES ('default_user', SHA2('default', 256), NOW())
                """)
                conn.commit()
            
            # Get first user id
            cursor.execute("SELECT id FROM users LIMIT 1")
            default_user_id = cursor.fetchone()[0]
            
            # Update all NULL user_id values to the default user
            cursor.execute(f"UPDATE daily_activity SET user_id = {default_user_id} WHERE user_id IS NULL")
            conn.commit()
            
            # Now add foreign key
            cursor.execute("""
                ALTER TABLE daily_activity 
                ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            """)
            
            # Update primary key for daily_activity
            try:
                cursor.execute("ALTER TABLE daily_activity DROP PRIMARY KEY")
            except Error:
                # Table might not have a primary key, that's ok
                pass
            
            try:
                cursor.execute("ALTER TABLE daily_activity ADD PRIMARY KEY (entry_date, user_id)")
            except Error as e:
                print(f"Note: Could not update primary key on daily_activity: {e}")
        
        # Also update problems table user_id if NULL
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] > 0:
            cursor.execute("SELECT id FROM users LIMIT 1")
            default_user_id = cursor.fetchone()[0]
            cursor.execute(f"UPDATE problems SET user_id = {default_user_id} WHERE user_id IS NULL")
            conn.commit()
        
        conn.commit()
        cursor.close()
        conn.close()
    except Error as e:
        print(f"Setup warning: {e}")
    
    # Launch login window
    login = LoginWindow()
    login.run()

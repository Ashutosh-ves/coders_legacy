CREATE DATABASE coders_legacy_db;
USE coders_legacy_db;

CREATE TABLE problems (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    platform VARCHAR(50) DEFAULT 'CodeChef',
    difficulty ENUM('Easy', 'Medium', 'Hard') NOT NULL,
    topic VARCHAR(100),                       
    link VARCHAR(500),                       
    notes TEXT,                               
    revision_needed BOOLEAN DEFAULT FALSE,    
    date_solved DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE daily_activity (
    entry_date DATE PRIMARY KEY,
    problems_solved INT DEFAULT 0,
    time_spent_minutes INT DEFAULT 0
);

INSERT INTO problems (title, platform, difficulty, topic, notes, date_solved, revision_needed) VALUES 
('Two Sum', 'LeetCode', 'Easy', 'Arrays', 'Used Hash Map for O(n) complexity.', '2025-11-28', FALSE),
('Valid Parentheses', 'LeetCode', 'Easy', 'Stack', 'Classic stack problem. Watch out for empty strings.', '2025-11-28', FALSE),
('Chef and Operators', 'CodeChef', 'Easy', 'Basic Math', 'Simple comparison logic using relational operators.', '2025-11-29', FALSE),
('0-1 Knapsack Problem', 'GeeksForGeeks', 'Medium', 'DP', 'Standard DP. Remember to init the table with -1.', '2025-11-30', TRUE),
('Longest Substring Without Repeating Characters', 'LeetCode', 'Medium', 'Sliding Window', 'Tricky index manipulation. Need to revise sliding window pattern.', '2025-11-30', TRUE),
('Turbo Sort', 'CodeChef', 'Easy', 'Sorting', 'Standard sorting algorithm implementation.', '2025-11-30', FALSE),
('Trapping Rain Water', 'LeetCode', 'Hard', 'Two Pointers', 'Very hard logic. Left max and right max arrays needed.', '2025-12-01', TRUE),
('Detect Cycle in Directed Graph', 'GeeksForGeeks', 'Medium', 'Graphs', 'Used DFS and recursion stack.', '2025-12-02', FALSE),
('Merge k Sorted Lists', 'LeetCode', 'Hard', 'Heap', 'Priority Queue is the best approach here.', '2025-12-02', TRUE),
('Left Rotation', 'HackerRank', 'Easy', 'Arrays', 'Modulus operator helps with index wrapping.', '2025-12-02', FALSE);

INSERT INTO daily_activity (entry_date, problems_solved, time_spent_minutes) VALUES 
('2025-11-28', 2, 45),
('2025-11-29', 1, 15),
('2025-11-30', 3, 120),
('2025-12-01', 1, 60),
('2025-12-02', 3, 90);

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at DATETIME
);

ALTER TABLE problems 
ADD COLUMN user_id INT,
ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

ALTER TABLE daily_activity 
ADD COLUMN user_id INT,
ADD FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

UPDATE daily_activity SET user_id = 1 WHERE user_id IS NULL;
UPDATE problems SET user_id = 1 WHERE user_id IS NULL;

ALTER TABLE daily_activity DROP PRIMARY KEY;
ALTER TABLE daily_activity ADD PRIMARY KEY (entry_date, user_id);

INSERT INTO users(username, password, created_at) VALUES
('am', 'abcd', '2025-12-12');

UPDATE users 
SET password = SHA2('abcd', 256) 
WHERE username = 'am';

SELECT * FROM problems;
SELECT * FROM daily_activity;
SELECT * FROM users;

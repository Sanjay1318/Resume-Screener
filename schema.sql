CREATE DATABASE IF NOT EXISTS resume_scanner
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE resume_scanner;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(120) NOT NULL,
  email VARCHAR(180) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

SELECT * FROM users;
DELETE FROM scans WHERE user_id = 3;

CREATE TABLE IF NOT EXISTS scans (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  skills_text TEXT NOT NULL,
  total_resumes INT NOT NULL DEFAULT 0,
  priority_count INT NOT NULL DEFAULT 0,
  shortlisted_count INT NOT NULL DEFAULT 0,
  rejected_count INT NOT NULL DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS resumes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  scan_id INT NOT NULL,
  user_id INT NOT NULL,
  candidate_name VARCHAR(180) NOT NULL,
  original_filename VARCHAR(255) NOT NULL,
  stored_filename VARCHAR(255) NOT NULL,
  stored_path VARCHAR(500) NOT NULL,
  bucket VARCHAR(40) NOT NULL,
  score DECIMAL(5,2) NOT NULL,
  matched_count INT NOT NULL,
  total_count INT NOT NULL,
  matched_skills JSON NULL,
  ai_summary TEXT NULL,
  missing_skills JSON NULL,
  experience_match TEXT NULL,
  education_match TEXT NULL,
  certifications JSON NULL,
  recommendation VARCHAR(80) NULL,
  interview_questions JSON NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (scan_id) REFERENCES scans(id) ON DELETE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

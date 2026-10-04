-- Run this in the MySQL shell:  mysql -u root -p < database_setup.sql
CREATE DATABASE IF NOT EXISTS student_management_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

-- Optional: a dedicated user instead of root
-- CREATE USER 'sms_user'@'localhost' IDENTIFIED BY 'StrongPassword123!';
-- GRANT ALL PRIVILEGES ON student_management_db.* TO 'sms_user'@'localhost';
-- FLUSH PRIVILEGES;

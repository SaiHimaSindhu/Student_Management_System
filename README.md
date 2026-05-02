# 🎓 Student Management System (CLI Project)

## 📌 Description

This is a simple **Student Management System** built using **Python and MySQL**.
It allows users to perform basic operations like adding, viewing, updating, and deleting student records.

---

## 🚀 Features

* ➕ Add Student
* 📄 View Students
* 🔍 Search Student (optional)
* ✏️ Update Student details
* ❌ Delete Student
* ✅ Input Validation (Age check)

---

## 🛠️ Technologies Used

* Python
* MySQL
* mysql-connector-python

---

## 🗄️ Database Setup

```sql
CREATE DATABASE student_db;

USE student_db;

CREATE TABLE students (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    age INT,
    marks FLOAT
);
```

---

## ⚙️ Installation & Setup

1. Install Python
2. Install MySQL
3. Install required package:

```bash
pip install mysql-connector-python
```

---

## ▶️ How to Run

1. Open terminal
2. Navigate to project folder

```bash
cd sms_project
```

3. Run the program

```bash
python main.py
```

---

## 📸 Sample Output

```
===== Student Management System =====
1. Add Student
2. View Students
3. Delete Student
4. Update Student
5. Exit
```

---

## 📂 Project Structure

```
sms_project/
│
├── db.py
├── operations.py
├── main.py
```

---

## 💡 Future Improvements

* Convert into Flask Web Application
* Add search functionality
* Add better validation
* Add user authentication

---

## 👨‍💻 Author

Your Name

---

## ⭐ Conclusion

This project helps in understanding:

* Python functions
* MySQL database operations
* CRUD operations
* Basic project structure

---

from db import get_connection

# Add Student
def add_student():
    conn = get_connection()
    cursor = conn.cursor()

    name = input("Enter Name: ")
    age = int(input("Enter Age: ")) 
    if age <=0:
        print("Invalid age")
        return
    marks = int(input("Enter Marks:"))

    query = "INSERT INTO students (name, age, marks) VALUES (%s, %s, %s)"
    values = (name, age, marks)

    cursor.execute(query, values)
    conn.commit()

    print("✅ Student Added Successfully")

    conn.close()


# View Students
def view_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    print("\n--- Student List ---")
    for s in students:
        print(s)

    conn.close()


# Search Student
def search_student():
    conn = get_connection()
    cursor = conn.cursor()

    name = input("Enter Name to Search: ")

    query = "SELECT * FROM students WHERE name = %s"
    cursor.execute(query, (name,))

    result = cursor.fetchall()

    if result:
        for r in result:
            print(r)
    else:
        print("❌ Student Not Found")

    conn.close()


# Update Student
def update_student():
    conn = get_connection()
    cursor = conn.cursor()

    student_id = int(input("Enter Student ID to Update: "))
    print("What do you want to update?")
    print("1. Name")
    print("2. Age")
    print("3. Marks")

    choice = input("Enter choice:")
    if choice == "1":
        new_name = input("Enter New Name: ")
        query = "UPDATE students SET name = %s WHERE id = %s"
        cursor.execute(query, (new_name, student_id))

    elif choice == "2":
        new_age = int(input("Enter New Age: "))
        query = "UPDATE students SET age = %s WHERE id = %s"
        cursor.execute(query, (new_age, student_id))

    elif choice == "3":
        new_marks = int(input("Enter New Marks: "))
        query = "UPDATE students SET marks = %s WHERE id = %s"
        cursor.execute(query, (new_marks, student_id))

    else:
        print("Invalid choice")
        return

    conn.commit()
    print("Student Updated Successfully")

    conn.close()

# Delete Student
def delete_student():
    conn = get_connection()
    cursor = conn.cursor()

    student_id = int(input("Enter Student ID to Delete: "))

    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (student_id,))
    conn.commit()

    print("✅ Student Deleted")

    conn.close()
import tkinter as tk
import sqlite3
from tkinter import ttk
from tkinter import messagebox



  
app = tk.Tk()
app.geometry("1300x650")
app.title("SSIS version 2.0")




# placeholders for entries
# __init__ variables
id= tk.StringVar()
name=tk.StringVar()
sex=tk.StringVar()
year=tk.StringVar()
courseName =tk.StringVar()
courseID =tk.StringVar()
searchin = tk.StringVar()

# placeholder values
def setph(word,num):
    if num == 1:
        id.set(word)
    if num == 2:
        name.set(word)
    if num == 3:
        sex.set(word)
    if num == 4:
        year.set(word)
    if num == 5:
        courseName.set(word)
    if num == 6:
        courseID.set(word)
    if num == 7:
        searchin.set(word)


        
def read():
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

def add():
    # Retrieve the input data from the Tkinter interface
    student_id = id.get()
    student_name = name.get()
    student_sex = sex.get()
    student_year = year.get()
    course_id = courseID.get()

    # Connect to the SQLite database
    conn = sqlite3.connect("courses.db")
    cursor = conn.cursor()

    # Define the SQL query to insert the data into the database table
    query = "INSERT INTO students (studentID, studentName, sex, year, courseID) VALUES (?, ?, ?, ?, ?)"

    # Execute the query with the input data
    cursor.execute(query, (student_id, student_name, student_sex, student_year, course_id))

    # Commit the changes and close the database connection
    conn.commit()
    conn.close()

    # Show a message box indicating successful data insertion
    messagebox.showinfo("Success", "Data inserted successfully!")


def add_course():
    course_id = courseID.get()
    course_name = courseName.get()

    if not course_id or not course_name:
        # Show an error message if either course ID or course name is empty
        messagebox.showerror("Error", "Please enter both Course ID and Course Name.")
        return

    try:
        # Connect to the database
        conn = sqlite3.connect("courses.db")
        cursor = conn.cursor()

        # Insert the course into the database
        query = "INSERT INTO courses (courseID, courseName) VALUES (?, ?)"
        cursor.execute(query, (course_id, course_name))
        conn.commit()

        # Close the connection
        conn.close()

        # Clear the input fields
        courseID.set("")
        courseName.set("")

        # Show a success message
        messagebox.showinfo("Success", "Course added successfully.")
    except sqlite3.IntegrityError:
        # Show an error message if the course ID already exists
        messagebox.showerror("Error", "Course ID already exists.")
    except sqlite3.Error as e:
        # Show an error message for any other database-related error
        messagebox.showerror("Error", f"An error occurred: {e}")

def reset_data():
    
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM students''')

    conn.commit()
    conn.close()
    messagebox.showinfo("Success","All students data reset.")


def delete():
    selected_id = id_entry.get()

    
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()

    cursor.execute('''DELETE FROM students WHERE studentID = ?''', (selected_id,))
    
    if cursor.rowcount > 0:
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data deleted successfully.")
    else:
        messagebox.showinfo("Error", "No matching student found.")


def delete_course():
    selected_courseID = coursecode_entry.get()

    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    
    cursor.execute('''DELETE FROM courses WHERE courseID = ?''', (selected_courseID,))
    if cursor.rowcount > 0:
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data deleted successfully.")
    else:
        messagebox.showinfo("Error", "No matching student found.")
    refresh_data()


def select(event):
    try:
        selected_item = stud_table.focus()
        selected_data = stud_table.item(selected_item)['values']
        if selected_data:
            id_entry.delete(0, tk.END)
            id_entry.insert(tk.END, selected_data[0])
            name_entry.delete(0, tk.END)
            name_entry.insert(tk.END, selected_data[1])
            sex_entry.delete(0, tk.END)
            sex_entry.insert(tk.END, selected_data[2])
            year_entry.delete(0, tk.END)
            year_entry.insert(tk.END, selected_data[3])
            coursecode_entry.delete(0, tk.END)
            coursecode_entry.insert(tk.END, selected_data[4])
        
    except:
        messagebox.showinfo("Error","Please select a data row")
        
def select_courses(event):
    try:
        selected_item = courses_table.focus()
        selected_data = courses_table.item(selected_item)['values']
        if selected_data:
            coursecode_entry.delete(0, tk.END)
            coursecode_entry.insert(tk.END, selected_data[0])
            course_entry.delete(0, tk.END)
            course_entry.insert(tk.END, selected_data[1])
        
    except:
        messagebox.showinfo("Error","Please select a data row")        
        
def edit():
    selected_id = id_entry.get()
    new_name = name_entry.get()
    new_sex = sex_entry.get()
    new_year = year_entry.get()
    new_courseID = coursecode_entry.get()

    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()


    cursor.execute('''UPDATE students SET studentName=?, sex=?, year=?, courseID=? WHERE studentID=?''',
                   (new_name, new_sex, new_year, new_courseID, selected_id))

    if cursor.rowcount > 0:
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data updated successfully.")
    else:
        messagebox.showinfo("Error", "No matching student found.")

    # Clear the entry fields
    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    sex_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    coursecode_entry.delete(0, tk.END)

    refresh_data()

def edit_course():
    selected_courseID = coursecode_entry.get()
    new_coursename = course_entry.get()

    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()
    

    cursor.execute('''UPDATE courses SET courseName=? WHERE courseID=?''',
                   (new_coursename,selected_courseID))
    if cursor.rowcount > 0:
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Data updated successfully.")
    else:
        messagebox.showinfo("Error", "No matching course found.")

    # Clear the entry fields
    course_entry.delete(0,tk.END)
    coursecode_entry.delete(0, tk.END)

    refresh_data_courses()


# Function to refresh the data in the tree view
def refresh_data():

    for item in stud_table.get_children():
        stud_table.delete(item)
    
    results = read()

    for result in results:
        stud_table.insert("", tk.END, values=result)
    

def refresh_data_courses():
    # Clear the existing data in the courses_table
    courses_table.delete(*courses_table.get_children())

    # Retrieve the data from the courses database
    results_courses = read_courses()

    # Insert the data into the courses_table
    for results_courses in results_courses:
        courses_table.insert("", tk.END, values=results_courses)


    
def search():
    search_term = searchin.get()    

    # Connect to the database
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()

    # Execute the search query
    cursor.execute("SELECT * FROM students WHERE studentID LIKE ? OR studentName LIKE ? OR sex LIKE ? OR year LIKE ? OR courseID LIKE ?",
                   (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))

    results = cursor.fetchall()

    # Clear the tree view
    stud_table.delete(*stud_table.get_children())

    # Insert the search results into the tree view
    for result in results:
        stud_table.insert("", tk.END, values=result)

    conn.close()

def search_course():
    search_term = course_entry.get()    

    # Connect to the database
    conn = sqlite3.connect('courses.db')
    cursor = conn.cursor()

    # Execute the search query
    query = "SELECT * FROM courses WHERE courseID LIKE ? OR courseName LIKE ? "

    cursor.execute(query, (f"%{search_term}%", f"%{search_term}%"))

    results_courses = cursor.fetchall()

    # Clear the tree view
    stud_table.delete(*stud_table.get_children())

    # Insert the search results into the tree view
    for results_courses in results_courses:
        stud_table.insert("", tk.END, values=results_courses)

    conn.close()

def read_courses():
    # Connect to the database (assuming it's named 'courses.db')
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()

    # Fetch data from the 'courses' table
    c.execute("SELECT courseID, courseName FROM courses")
    courses_data = c.fetchall()

    # Close the connection
    conn.close()

    return courses_data

def display_courses():
    # Connect to the database (assuming it's named 'courses.db')
    conn = sqlite3.connect('courses.db')
    c = conn.cursor()

    # Fetch data from the 'courses' table
    c.execute("SELECT courseID, courseName FROM courses")
    courses_data = c.fetchall()

    # Close the connection
    conn.close()

    # Clear existing items in the Treeview
    for item in courses_table.get_children():
        courses_table.delete(item)

    # Insert the updated data into the Treeview
    for course in courses_data:
        courses_table.insert("", tk.END, values=course)
    refresh_data_courses()





# Graphical User Interface

title_label = tk.Label(app, border=5, height=20, relief= tk.GROOVE, bg = "lightgreen")
title_label.pack(side=tk.TOP,fill=tk.X)

# frames
detail_frame = tk.LabelFrame(app, bd=10,relief=tk.GROOVE,bg="lightgreen")
detail_frame.place(x=20,y=55,width=450,height=575)

data_frame = tk.Frame(app, bg="lightgreen",relief=tk.GROOVE)
data_frame.place(x=475,y=55,width=810,height=575)




# entries and labels >> detail frame
id_label = tk.Label(detail_frame, text="ID",font=("Times", 10), bg= "lightgreen")
id_label.place(x=20,y=20)
id_entry = tk.Entry(detail_frame,bd=5,font=("Times",10),textvariable=id)
id_entry.place(x=110,y=20)

name_label = tk.Label(detail_frame, text="Name",font=("Times", 10), bg= "lightgreen")
name_label.place(x=20,y=60)
name_entry = tk.Entry(detail_frame,bd=5,font=("Times",10),textvariable=name)
name_entry.place(x=110, y=60)

sex_label = tk.Label(detail_frame, text="Sex",font=("Times", 10), bg= "lightgreen")
sex_label.place(x=20,y=110)
sex_entry = ttk.Combobox(detail_frame,font=("Times",8),textvariable=sex)
sex_entry['values']=("Male","Female")
sex_entry.place(x=110,y=110)


year_label = tk.Label(detail_frame, text="Year level",font=("Times",10),bg="lightgreen")
year_label.place(x=20,y=420)
year_entry = tk.Entry(detail_frame,bd=5,font=("Times",10),textvariable=year)
year_entry.place(x=110,y=420)


# Courses
course_label = tk.Label(detail_frame, text="Course Name",bg="lightgreen",bd=5,font=("Times",10),width=10)
course_label.place(x=20,y=150)
coursecode_label= tk.Label(detail_frame, text="Course Code",bg="lightgreen",bd=5,font=("Times",10))
coursecode_label.place(x=20,y=200)

course_entry = tk.Entry(detail_frame,bd=5,font=("Times",10),textvariable=courseName)
course_entry.place(x=110,y=150)
coursecode_entry = tk.Entry(detail_frame,bd=5,font=("Times",10),textvariable=courseID)
coursecode_entry.place(x=110, y=200)


button_add_course = tk.Button(detail_frame, text="Add Course",bg="lightgrey",bd=5,font=("Times",7),width=10, command=add_course)
button_add_course.place(x=270,y=150)
button_edit_course = tk.Button(detail_frame, text="Edit Course",bg="lightgrey",bd=5,font=("Times",7),width=10, command=edit_course)
button_edit_course.place(x=342,y=150)
button_delete_course = tk.Button(detail_frame, text="Delete Course",bg="lightgrey",bd=5,font=("Times",7),width=10, command=delete_course)
button_delete_course.place(x=270,y=200)
button_search_course = tk.Button(detail_frame, text="Search Course",bg="lightgrey",bd=5,font=("Times",7),width=10, command=search_course)
button_search_course.place(x=342,y=200)



# button frame
btn_frame= tk.Frame(detail_frame, bg="lightgrey",bd=10,relief=tk.GROOVE)
btn_frame.place(x=120,y=480,width=230,height=55)

# buttons >> btn frame
add_btn = tk.Button(btn_frame, text="Add",bg="lightgrey",bd=5,font=("Times",7),width=15, command=add)
add_btn.grid(row=0,column=0,padx=7,pady=2)


delete_btn = tk.Button(btn_frame, bg="lightgrey", text="Delete",bd=5,font=("Times",7),width=15,command=delete )
delete_btn.grid(row=0,column=1,padx=7,pady=2)




# top right frame
search_frame = tk.Frame(data_frame,bg="lightgrey",bd=10,relief=tk.GROOVE)
search_frame.pack(side=tk.TOP, fill=tk.X)

# search and show buttons
search_label=tk.Label(title_label,text="Search",bg="lightgreen",font=("Times",17))
search_label.grid(row=0,column=0,padx=2,pady=2)

search_entry =ttk.Entry(title_label,font=("Times", 15),textvariable=searchin)
search_entry.grid(row=0,column=1,padx=12,pady=2)

search_btn = tk.Button(title_label,bg="lightgrey",text="Search",bd=5,font=("Times",7),width=15,command=search)
search_btn.place(x=880,y=5)

edit_button = tk.Button(title_label, bg="lightgrey", text="Edit",bd=5,font=("Times",7),width=15,command=edit)
edit_button.place(x=980,y=5)

reset_btn = tk.Button(title_label, text="Reset",bg="lightgrey", bd=5,font=("Times",7),width=15, command=reset_data)
reset_btn.place(x=1080,y=5)


# frame for treeview
main_frame=tk.Frame(data_frame,bg="lightgrey", bd=7,relief=tk.GROOVE)
main_frame.pack(fill=tk.BOTH,expand=True)
y_scroll = tk.Scrollbar(main_frame, orient = tk.VERTICAL)
x_scroll = tk.Scrollbar(main_frame, orient = tk.HORIZONTAL)


# style object
style = ttk.Style()
style.configure("Treeview", bd= 7)


# Treeview for courses.db
courses_table = ttk.Treeview(detail_frame)
courses_table["columns"] = ("courseID", "courseName")

courses_table.column("courseID",anchor="center" ,width=100)
courses_table.column("courseName", anchor= "w" ,width=200)

courses_table.heading("courseID", text="Course ID")
courses_table.heading("courseName", text="Course Name")
courses_table.column("#0", width=0, stretch=tk.NO)
courses_table.place(x=80,y=250, height=150)

display_courses()

courses_table.bind("<<TreeviewSelect>>", select_courses)



# Treeview for students.db
stud_table = ttk.Treeview(main_frame)
stud_table["columns"] = ("ID", "Name", "Sex", "Year Level", "Course")
stud_table.column("ID", anchor="center", width=100, minwidth=50)
stud_table.column("Name", anchor="w", width=150, minwidth=100)
stud_table.column("Sex", anchor="center", width=80, minwidth=50)
stud_table.column("Year Level", anchor="center", width=100, minwidth=50)
stud_table.column("Course", anchor="center", width=200, minwidth=100)

stud_table.heading("ID", text="ID")
stud_table.heading("Name", text="Name")
stud_table.heading("Sex", text="Sex")
stud_table.heading("Year Level", text="Year Level")
stud_table.heading("Course", text="Course")
stud_table.column("#0", width=0, stretch=tk.NO)  # Remove space before "ID" column
stud_table.pack(fill=tk.BOTH, expand=True)

# Populate the tree view with data
results = read()
for result in results:
    stud_table.insert("", tk.END, values=result)

# Bind the select function to the tree view selection event
stud_table.bind("<<TreeviewSelect>>", select)

app.mainloop()

import csv
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk



root = tk.Tk()
root.title("SSIS v1.0")
root.geometry("1360x680")

title_label = tk.Label(root, text="Simple Student Information System v1.0", font=("Arial", 30,"bold"),border=12,relief=tk.GROOVE,bg="lightgrey")
title_label.pack(side=tk.TOP,fill=tk.X)


# frames
detail_frame = tk.LabelFrame(root, text="Information",font=("Arial",13),bd=12,relief=tk.GROOVE,bg="lightgrey")
detail_frame.place(x=20,y=90,width=450,height=575)

data_frame = tk.Frame(root, bg="lightgrey",bd=12,relief=tk.GROOVE)
data_frame.place(x=475,y=90,width=810,height=575)

# __init__ variables
id= tk.StringVar()
name=tk.StringVar()
sex=tk.StringVar()
year=tk.StringVar()
search=tk.StringVar()
course =tk.StringVar()

# backend functions
def add_course():
    course = entry_course.get()

    if course:
        listbox_courses.insert(tk.END, course)
        entry_course.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Please enter a course.")

def save_selection():
    student_name = entry_name.get()
    student_id = entry_id.get()
    student_sex = entry_sex.get()
    student_year = entry_year.get()

    selected_courses = listbox_courses.curselection()

    if student_name and student_id and student_sex and selected_courses and student_year:
        courses = [listbox_courses.get(index) for index in selected_courses]
        with open('student_courses.csv', 'a', newline='') as file:
            writer = csv.writer(
                file
            )
            writer.writerow([student_name] + courses + [student_sex] + [student_id]+ [student_year])
        
        messagebox.showinfo("Selection Saved", "Selection has been saved successfully.")

    else:
        messagebox.showerror("Error", "Please enter a student name, id, sex and year level and select at most one course.")

def remove_data():
    selected_index = listbox_data.curselection()

    if selected_index:
        confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this record?")
        
        if confirmation:
            with open('student_courses.csv', 'r') as file:
                records = list(csv.reader(file))
            
            del records[selected_index[0]]
            
            with open('student_courses.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(records)
            
            messagebox.showinfo("Data Removed", "Data has been removed successfully.")
            load_data()
    else:
        messagebox.showerror("Error", "Please select a record to remove.")

def load_data():
    listbox_data.delete(0, tk.END)

    with open('student_courses.csv', 'r') as file:
        records = csv.reader(file)
        for row in records:
            listbox_data.insert(tk.END, ', '.join(row))

def edit_data():
    selected_index = listbox_data.curselection()

    if selected_index:
        selected_data = listbox_data.get(selected_index)
        selected_data = selected_data.split(', ')

        window_edit = tk.Toplevel()
        window_edit.title("Edit Data")

        frame_edit = tk.Frame(window_edit)
        frame_edit.pack(pady=20)

        label_name = tk.Label(frame_edit, text="Student Name:")
        label_name.grid(row=0, column=0)
        entry_name = tk.Entry(frame_edit)
        entry_name.grid(row=0, column=1)
        entry_name.insert(tk.END, selected_data[0])

        label_courses = tk.Label(frame_edit, text="Courses:")
        label_courses.grid(row=1, column=0)
        entry_courses = tk.Entry(frame_edit)
        entry_courses.grid(row=1, column=1)
        entry_courses.insert(tk.END, ', '.join(selected_data[1:2]))

        label_id = tk.Label(frame_edit,text="Sex:")
        label_id.grid(row = 2, column = 0)
        entry_id = tk.Entry(frame_edit)
        entry_id.grid(row = 2, column = 1)
        entry_id.insert(tk.END, ', '.join(selected_data[2:3]))

        label_sex = tk.Label(frame_edit, text = "ID no:" )
        label_sex.grid(row = 3, column = 0)
        entry_sex = tk.Entry(frame_edit)
        entry_sex.grid(row = 3, column = 1)
        entry_sex.insert(tk.END, ', '.join(selected_data[3:4]))
        
        label_year = tk.Label(frame_edit, text = "Year:" )
        label_year.grid(row = 4, column = 0)
        entry_year = tk.Entry(frame_edit)
        entry_year.grid(row = 4, column = 1)
        entry_year.insert(tk.END, ', '.join(selected_data[4:5]))

        button_save = tk.Button(window_edit, text="Save Changes", command=lambda: save_changes(selected_index[:]))
        button_save.pack(pady=10)

    else:
        messagebox.showerror("Error", "Please select a record to edit.")

def save_changes(selected_index):
    new_name = entry_name.get()
    new_courses = entry_course.get().split(', ')
    new_sex = entry_sex.get().split(', ')
    new_id = entry_id.get().split(', ')
    new_year = entry_year.get().split(', ')

    with open('student_courses.csv', 'r') as file:
        records = list(csv.reader(file))

    records[selected_index[0]] = new_name
    records[selected_index[1]] = new_courses
    records[selected_index[2]] = new_sex
    records[selected_index[3]] = new_id
    records[selected_index[4]]= new_year

    with open('student_courses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(records)

    messagebox.showinfo("Changes Saved", "Changes have been saved successfully.")
    entry_name.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    load_data()

# def search_student():
#     search_name = search_entry.get()
#     if search_name:
#         found_students = [student for student in students if search_name.lower() in student['name'].lower()]
#         listbox_data.delete(0, tk.END)
#         for student in found_students:
#             listbox_data.insert(tk.END, student['name'])
#     else:
#         messagebox.showerror('Error', 'Please enter a name to search.')

def clear_entries():
    entry_name.delete(0, tk.END)
    entry_course.delete(0, tk.END)
    entry_sex.delete(0,tk.END)
    entry_id.delete(0,tk.END)
    entry_year.delete(0,tk.END)
    listbox_courses.selection_clear(0, tk.END)


# labels and entries >>>detail frame
label_id = tk.Label(detail_frame, text="ID no.",font=("Arial", 13), bg= "lightgrey")
label_id.grid(row=0,column=0,padx=2,pady=2)
entry_id = tk.Entry(detail_frame,bd=7,font=("Arial",13),textvariable=id)
entry_id.grid(row=0,column=1,padx=2,pady=2)


label_name = tk.Label(detail_frame, text="Name",font=("Arial", 13), bg= "lightgrey")
label_name.grid(row=1,column=0,padx=2,pady=10)
entry_name = tk.Entry(detail_frame,bd=7,font=("Arial",13),textvariable=name)
entry_name.grid(row=1 ,column=1,padx=2,pady=10)


sex_label = tk.Label(detail_frame, text="Sex",font=("Arial", 13), bg= "lightgrey")
sex_label.grid(row=2,column=0,padx=2,pady=10)
entry_sex = ttk.Combobox(detail_frame,font=("Arial",11),textvariable=sex)
entry_sex['values']=("Male","Female")
entry_sex.grid(row=2,column=1,padx=2,pady=10)

# listbox << added course
listbox_courses = tk.Listbox(detail_frame, width=50)
listbox_courses.grid(row=4,column=1,padx=2,pady=10)

label_course = tk.Label(detail_frame, text="Course:", font=("Arial",13),bg="lightgrey")
label_course.grid(row=3, column=0,padx=1,pady=10)
entry_course = tk.Entry(detail_frame,bd=7,font=("Arial",13),textvariable=course)
entry_course.grid(row=3, column=1, padx=1, pady=10)


label_year = tk.Label(detail_frame, text="Year level:",font=("Arial",13),bg="lightgrey")
label_year.grid(row=5, column=0)
entry_year = tk.Entry(detail_frame,bd=7,font=("Arial",13),textvariable=year)
entry_year.grid(row=5, column=1)

# >> add course to listbox
button_add_course = tk.Button(detail_frame, text="Add Course",bg="lightgrey",bd=7,font=("Arial",7),width=10, command=add_course)
button_add_course.place(x=342,y=151)

# buttons >> button frame
btn_frame= tk.Frame(detail_frame, bg="lightgrey",bd=10,relief=tk.GROOVE)
btn_frame.place(x=100,y=430,width=255,height=95)


button_save_selection = tk.Button(btn_frame, text="Save",bg="lightgrey",bd=7,font=("Arial",7),width=15, command=save_selection)
button_save_selection.grid(row=0,column=0,padx=2,pady=2)


button_edit_data = tk.Button(btn_frame, bg="lightgrey", text="Edit",bd=7,font=("Arial",7),width=15,command=edit_data)
button_edit_data.grid(row=0, column=1, padx=2, pady=2)


clear_btn = tk.Button(btn_frame, bg="lightgrey", text="Clear",bd=7,font=("Arial",7),width=15, command=clear_entries)
clear_btn.grid(row=1,column=1,padx=3,pady=2)


# top right frame >> data frame
search_frame = tk.Frame(data_frame,bg="lightgrey",bd=10,relief=tk.GROOVE)
search_frame.pack(side=tk.TOP, fill=tk.X)


# search and show buttons
search_label=tk.Label(search_frame,text="Search",bg="lightgrey",font=("Arial",14))
search_label.grid(row=0,column=0,padx=2,pady=2)

search_entry =ttk.Entry(search_frame,font=("Arial", 14),textvariable=search)
search_entry.grid(row=0,column=1,padx=12,pady=2)



# buttons >> search_frame
button_remove_data = tk.Button(search_frame, text="Remove Data",bg="lightgrey", bd=7,font=("Arial",7),width=15, command=remove_data)
button_remove_data.place(x=570,y=2)

search_btn = tk.Button(search_frame,bg="lightgrey",text="Search",bd=7,font=("Arial",7),width=15)
search_btn.place(x=420,y=2)

# listbox data
listbox_data = tk.Listbox(data_frame, width=50)
listbox_data.place(x=75,y=90,width=670,height=450)


load_data()

root.mainloop()

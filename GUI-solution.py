import csv
from tkinter import *
from tkinter import simpledialog
from tkinter import filedialog
import os
import webbrowser

csv_file = "test.csv"

#_____________functions_____________________________
def open_file():
    try:
        global csv_file
        root.filepath = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
        csv_file = os.path.basename(root.filepath)
        run_file()
    except:
        pass


# list_of_semesters = []
def add_new_semester():
    try:
        global csv_file
        name = simpledialog.askstring("Pop up for user input!", "Type name of semester, please") #pop up for asking a name of the semester
        csv_file = name + ".csv"
        # list_of_semesters.append(name)
        # with open("semesters.csv", "a+", newline="") as semesters_csv_file:  # open csv if exists
        #     writer = csv.writer(semesters_csv_file, delimiter=";")
        #     writer.writerow(list_of_semesters)
        with open (csv_file, "w") as my_file:
            listbox_courses.delete(0, END)  # clear the Listbox
    except:
        pass


def run_file(): #read a csv file when the programme starts
    try:
        global csv_file
        listbox_courses.delete(0, END)  # clear the Listbox
        with open(csv_file, "r+") as file:
            myreader = csv.reader(file, delimiter=";")
            for line in myreader:
                listbox_courses.insert(END, line[0])
    except:
        pass


def file_selection(self): #get index of items in listbox
    try:
        global csv_file
        selection = listbox_courses.index(listbox_courses.curselection())
        with open(csv_file, "r+") as my_file:
            myreader = csv.reader(my_file, delimiter=";")
            data = list(myreader)  # access csv file by rows
            text_course_name.delete(0, END) # delete Entry
            text_course_name.insert(END, data[selection][0]) # display relevant course
            text_comments.delete(0, END)
            text_comments.insert(END, data[selection][1])
            scale_hours.set(data[selection][2])
    except:
        pass


def save_changes(): #save changes in a file
    try:
        global csv_file
        list_of_courses = []
        course_list = []
        with open(csv_file, 'r+') as inp, open('temp.csv', 'w+') as out:
            writer = csv.writer(out, delimiter=";")
            reader = csv.reader(inp, delimiter=";")
            course_list.append(text_course_name.get())
            course_list.append(text_comments.get())
            course_list.append(str(scale_hours.get()))
            for line in reader:
                if text_course_name.get() == line[0]:
                    continue
                else:
                    writer.writerow(line) # write row(s) line by line to a new csv document
                listbox_courses.delete(0, END)
                list_of_courses.append(line[0])
            writer.writerow(course_list)
            list_of_courses.append(course_list[0])
            for item in list_of_courses:
                if item != listbox_courses.get(ACTIVE): # if item not in listbox (do not display same courses)
                    listbox_courses.insert(END, item) # display name of a course in the Listbox
            os.rename('temp.csv', csv_file)
    except:
        pass


def add_course():
    try:
        global csv_file
        with open(csv_file, "a+", newline="") as csvfile: #open csv if exists
            list_of_programmes = []
            list_of_comments = []
            list_of_hours = []
            list_of_courses = []
            writer = csv.writer(csvfile, delimiter=";")
            list_of_programmes.append(text_course_name.get()) #append values to lists
            list_of_comments.append(text_comments.get())
            list_of_hours.append(scale_hours.get())
            for course in listbox_courses.get(0, END):
                list_of_courses.append(course)
            if text_course_name.get() not in list_of_courses:
                listbox_courses.insert(END, text_course_name.get())  # display name of a course in Listbox
                writer.writerows(zip(list_of_programmes,list_of_comments,list_of_hours)) #using zip function to add 3 lists into csv file
    except:
        pass


def delete_course():
    try:
        empty_list = []
        selection = listbox_courses.index(listbox_courses.curselection())
        global csv_file
        with open(csv_file, 'r+') as inp, open('temp.csv', 'w+') as out:
            writer = csv.writer(out, delimiter=";")
            reader = csv.reader(inp, delimiter=";")
            for line in reader:
                if line[0] != text_course_name.get():
                    writer.writerow(line) # write row(s) line by line to a new csv document
                    listbox_courses.delete(0, END)
                    empty_list.append(line[0])
                if empty_list == []:
                    listbox_courses.delete(0, END) # clear the Listbox
            for item in empty_list:
                listbox_courses.insert(END, item) # display name of a course in the Listbox
            os.rename('temp.csv', csv_file)
    except:
        pass


def delete_all_courses():
    try:
        global csv_file
        listbox_courses.delete(0, END)
        # os.remove(csv_file)
        with open(csv_file, "w+", newline="") as csvfile:
            pass
    except:
        pass


def save_file():
    try:
        root.filepath = filedialog.asksaveasfilename(initialdir="/", title="Select file", filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
        file_name = os.path.basename(root.filepath)
        with open(csv_file, 'r+') as inp, open(file_name, 'w+') as out:
            writer = csv.writer(out, delimiter=";")
            reader = csv.reader(inp, delimiter=";")
            for i, line in enumerate(reader):
                writer.writerow(line)  # write row(s) line by line to a new csv document
            os.rename(csv_file, file_name)
    except:
        pass


def get_help():
    try:
        webbrowser.open('http://www.giyf.com')
    except:
        pass


#_____________Main Window_____________________________
root = Tk()
root.title("Informatics: My Course Tracker") #create title
root.geometry("600x300+200+100") #size x1,y1, position x2,y2

#_____________Menubar_____________________________
menubar = Menu(root) # create a toplevel menu
file_menu = Menu(menubar) #create menu File
help_menu = Menu(menubar) #create menu Help
# submenu = Menu(file_menu) #create submenu

file_menu.add_command(label = "New Semester", command = add_new_semester)
file_menu.add_command(label="Open", command = open_file)
file_menu.add_command(label = "Save", command = save_file)
# file_menu.add_cascade(label="Open saved semester(s)", menu = submenu)
# submenu.add_cascade(label="Winter")
file_menu.add_separator() #create separator between Save & Exit
file_menu.add_command(label="Exit", command = root.destroy) #exit the programme

help_menu.add_command(label="Ask Google", command = get_help)

menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label = "Help", menu = help_menu)

root.config(menu=menubar) # display the menu

#_____________Buttons_____________________________
# add_icon = PhotoImage(file = "add.png") #create an object of picture/icon
btn_add_course = Button(root, text= "Add Course", foreground = 'green', compound = LEFT, anchor="w", command = add_course) #creating object of data type Button, picture attached, compounded to the left
btn_add_course.grid(row=0, column = 0, sticky=NSEW)

# save_icon = PhotoImage(file = "save.png") #create an object of picture/icon
btn_add_course = Button(root, text= "Save Changes", foreground = 'orange', compound = LEFT, anchor="w", command = save_changes) #creating object of data type Button, picture attached, compounded to the left
btn_add_course.grid(row=1, column = 0, sticky=NSEW)

# delete_icon = PhotoImage(file = "delete.png") #create an object of picture/icon
btn_delete_course = Button(root, text= "Delete Course", foreground = 'red', compound = LEFT, anchor="w", command = delete_course) #creating object of data type Button, picture attached, compounded to the left
btn_delete_course.grid(row=0, column = 1, sticky=NSEW)

# delete_all_icon = PhotoImage(file = "remove.png") #create an object of picture/icon
btn_delete_course = Button(root, text= "Delete All Courses", foreground = 'brown', compound = LEFT, anchor="w", command = delete_all_courses) #creating object of data type Button, picture attached, compounded to the left
btn_delete_course.grid(row=1, column = 1, sticky=NSEW)


#_____________Widgets_____________________________
listbox_courses = Listbox(root)
listbox_courses.grid(row=2, column = 0, rowspan = 12, columnspan = 2, sticky = NSEW)

scrollbar = Scrollbar(listbox_courses)
scrollbar.pack(side=RIGHT, fill=Y)
for i in listbox_courses.get(ACTIVE):
    listbox_courses.insert(END, i)
# attach listbox to scrollbar
listbox_courses.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox_courses.yview)

label_name = Label(root, relief=GROOVE, text = "Course Name", anchor="w", font='Times 16') #creating object of data type Label
label_name.grid(row=1,column=2, sticky=NSEW)

text_course_name = Entry(root) #textbox of course name
text_course_name.grid(row=1, column=3)

label_comments = Label(root, relief=GROOVE, text = "Comments", anchor="w", font='Times 16') #creating object of data type Label
label_comments.grid(row=2,column=2, sticky=NSEW)

text_comments = Entry(root) #textbox of comments
text_comments.grid(row=2, column=3, rowspan=10, sticky=NSEW)

label_hours = Label(root, relief=GROOVE, text = "My working hours", anchor="w", font='Times 16') #creating object of data type Label
label_hours.grid(row=12,column=2, rowspan = 2, sticky=NSEW)

scale_hours = Scale(root, from_=0, to=200, orient=HORIZONTAL)
scale_hours.grid(row=12, column=3)


#_____________Events_____________________________
listbox_courses.bind("<ButtonRelease-1>", file_selection) #bind event with an object (listbox)


#_____________Calling Functions_____________________________
run_file()
mainloop() #wait here until programme is closed


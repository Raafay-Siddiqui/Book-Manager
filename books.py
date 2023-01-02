import tkinter as tk

import tkinter.ttk as ttk

import sqlite3

#Connects to the database
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

#Creates the books table if it doesn't already exist
cursor.execute('''CREATE TABLE IF NOT EXISTS books (title text, author text, status text)''')

#Creates the main windowa
root = tk.Tk()
root.title("Book Manager")
root.config(bg='#E0E0EE')
root.geometry("600x450")

#defines the book adder and gets th values from the entry fields
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    status = status_entry.get()  #Gets the value of the status field from the Combobox widget
    
    #Inserts the values into the books table
    cursor.execute('''INSERT INTO books VALUES (?,?,?)''', (title, author, status))
    conn.commit()
    
    #clears the entry fields
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)  # <-- Clear the Combobox widget

#defines and displays the books
def display_books():
    #clears the listbox
    book_list.delete(0, tk.END)

    #retrieves all rows from the books table
    cursor.execute('''SELECT title, author, status FROM books''')
    books = cursor.fetchall()

    #inserts the rows into the listbox
    for book in books:
        book_list.insert(tk.END, f"{book[0]} | {book[1]} | {book[2]}")

def delete_book():
    #So this gets the selected book from the listbox
    selection = book_list.curselection()
    book = book_list.get(selection[0])

    #This splits the book string into its individual values
    title, author, status = book.split(" | ")

    #Deletes the book from the database
    cursor.execute('''DELETE FROM books WHERE title=? AND author=? AND status=?''', (title, author, status))
    conn.commit()

    #updates the listbox
    display_books()

def sort_by_status():
    #This basically looks at the status that its on and shows that in the listbox
    status = status_entry.get()

    #Clears the listbox
    book_list.delete(0, tk.END)

    #Retrieves all rows from the books table with the specified status
    cursor.execute('''SELECT title, author, status FROM books WHERE status=?''', (status,))
    books = cursor.fetchall()

    #Inserts the rows into the listbox
    for book in books:
        book_list.insert(tk.END, f"{book[0]} | {book[1]} | {book[2]}")


def edit_book():
    # gets the selected book from the listbox
    selection = book_list.curselection()
    book = book_list.get(selection[0])
    title, author, status = book.split(" | ")

    # sets the entry fields to the selected book's values
    title_entry.delete(0, tk.END)
    title_entry.insert(0, title)
    author_entry.delete(0, tk.END)
    author_entry.insert(0, author)
    status_entry.delete(0, tk.END)
    status_entry.insert(0, status)  # sets the value of the status field in the Combobox widget

    # changes the "Add Book" button to "Update Book"
    add_button.config(text='Update Book', command=lambda: update_book(title, author, status))

    # creates the "cancel button" (shouldnt really use global because it can mess with other stuff but it works fine for this, because its super light weight)
    global cancel_button
    cancel_button = ttk.Button(root, text='Cancel', command=cancel_update)
    cancel_button.pack(side=tk.BOTTOM)



def cancel_update():
    #changes the "Update Book" button back to "Add Book" Button
    add_button.config(text='Add Book', command=add_book)

    #removes the "cancel button"
    cancel_button.grid_forget()

    #clears the entry fields
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)  #Clear the Combobox widget

def update_book(title, author, status):
    #gets the new values from the entry fields
    updated_title = title_entry.get()
    updated_author = author_entry.get()
    updated_status = status_entry.get()  #Get the new value of the status field from the Combobox widget

    #Updates the book in the database
    cursor.execute('''UPDATE books SET title=?, author=?, status=? WHERE title=? AND author=? AND status=?''',
                   (updated_title, updated_author, updated_status, title, author, status))
    conn.commit()
     #Change the "Update Book" button to the "Add Book" button
    add_button.config(text='Add Book', command=add_book)

    #removes the Cancel button
    cancel_button.grid_forget()

    #clears the entry fields
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)  #Clears the Combobox widget

    #Updates the listbox
    display_books()

#create the entry field buttons and fields
title_label = tk.Label(root, text='Title', font=('Georgia', 14))
title_label.grid(row=0, column=0, sticky='W')
title_label.config(bg='#E0E0EE')

title_entry = tk.Entry(root, font=('Georgia', 14))
title_entry.grid(row=0, column=1, columnspan=3)


author_label = tk.Label(root, text='Author', font=('Georgia', 14))
author_label.grid(row=1, column=0, sticky='W')
author_label.config(bg='#E0E0EE')

author_entry = tk.Entry(root, font=('Georgia', 14))
author_entry.grid(row=1, column=1, columnspan=3)

status_label = tk.Label(root, text='Status', font=('Georgia', 14))
status_label.config(bg='#E0E0EE')
status_label.grid(row=2, column=0, sticky='W')

#Creates the combobox dropdown for the status field
status_entry = ttk.Combobox(root, font=('Georgia', 14), values=['Read', 'Reading', 'Not Read'])
status_entry.grid(row=2, column=1, columnspan=3)

#Creates the "add book" button
add_button = tk.Button(root, text='Add Book', command=add_book, font=('Georgia', 14), bg='lightgreen')
add_button.grid(row=0, column=4)

#Creates the "delete book" button
delete_button = tk.Button(root, text='Delete Book', command=delete_book, font=('Georgia', 14), bg='salmon')
delete_button.grid(row=1, column=4)

#Creates the "Sort By Status" button
sort_button = tk.Button(root, text='Sort By Status', command=sort_by_status, font=('Georgia', 14), bg='lightblue')
sort_button.grid(row=2, column=4)

#Creates the listbox
book_list = tk.Listbox(root, height=9, width=40, font=('Georgia', 14))
book_list.grid(row=3, column=0, columnspan=5)

#Binds the double-click event to the edit_book function
book_list.bind('<Double-1>', edit_book)

#Populates the listbox with the books in the database
display_books()

#Runs the main loop
root.mainloop()


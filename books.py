import tkinter as tk

import tkinter.ttk as ttk

import tkinter.messagebox

import sqlite3

import string


#above just imports all the codebases 

#connects to the database
conn = sqlite3.connect('books.db')
cursor = conn.cursor()

#creates the books table if it doesn't already exist
cursor.execute('''CREATE TABLE IF NOT EXISTS books (title text, author text, status text)''')

#creates the main windowa
root = tk.Tk()
root.title("Book Manager")
root.config(bg='#E0E0EE')
root.geometry("600x450")

#defines the book adder and gets the values from the entry fields


def add_book():
    title = title_entry.get()
    title = string.capwords(title)  #capitalizes the first letter of each word in the title
    author = author_entry.get()

    author = string.capwords(author)  #capitalizes the first letter of each word in the author
    status = status_entry.get()  #gets the value of the status field from the Combobox widget
    
    if title == "" or author == "":
        tk.messagebox.showerror("Error", "Title and author fields cannot be empty")
    else:
        #inserts the values into the books table
        cursor.execute('''INSERT INTO books VALUES (?,?,?)''', (title, author, status))
        conn.commit()
        
        #clears the entry fields
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        status_entry.delete(0, tk.END)  #clears the Combobox widget


#defines and displays the books
def display_books():
    #clears the listbox
    book_list.delete(0, tk.END)

    #retrieves all rows from the books table
    cursor.execute('''SELECT title, author, status FROM books''')
    books = cursor.fetchall()

    #sorts the list of books by status
    books.sort(key=lambda book: book[2])

    #inserts the rows into the listbox
    for book in books:
        book_list.insert(tk.END, f"{book[0]} | {book[1]} | {book[2]}")


def delete_book():
    selection = book_list.curselection()  #gets the selected item in the listbox
    
    if not selection:  #sheck if nothing is selected
        tk.messagebox.showerror("Error", "Please select a book to delete.")  #shows an error message
    else:
        book = book_list.get(selection[0])  #get the selected book
        title, author, status = book.split(" | ")  #split the book string into its individual values

        #deletes the book from the database
        cursor.execute('''DELETE FROM books WHERE title=? AND author=? AND status=?''', (title, author, status))
        conn.commit()

    #updates the listbox
    display_books()


def show_all_books():
    #clears the listbox
    book_list.delete(0, tk.END)

    #retrieves all rows from the books table, sorted alphabetically by title
    cursor.execute('''SELECT title, author, status FROM books ORDER BY title ASC''')
    books = cursor.fetchall()

    #inserts the rows into the listbox
    for book in books:
        book_list.insert(tk.END, f"{book[0]} | {book[1]} | {book[2]}")

#creates the "Show All Books" button
show_all_button = tk.Button(root, text="Show All Books", command=show_all_books)

#add the button to the window
show_all_button.grid(row=0, column=6)
show_all_button.config(bg='#FFA500')


def sort_by_status():
    #this basically looks at the status that its on and shows that in the listbox
    status = status_entry.get()

    #clears the listbox
    book_list.delete(0, tk.END)

    #retrieves all rows from the books table with the specified status
    cursor.execute('''SELECT title, author, status FROM books WHERE status=?''', (status,))
    books = cursor.fetchall()

    #inserts the rows into the listbox
    for book in books:
        book_list.insert(tk.END, f"{book[0]} | {book[1]} | {book[2]}")


def edit_book(event):
    #gets the selected book from the listbox
    selection = book_list.curselection()
    book = book_list.get(selection[0])
    title, author, status = book.split(" | ")

    #sets the entry fields to the selected book's values
    title_entry.delete(0, tk.END)
    title_entry.insert(0, title)
    author_entry.delete(0, tk.END)
    author_entry.insert(0, author)
    status_entry.delete(0, tk.END)
    status_entry.insert(0, status)  #sets the value of the status field in the Combobox widget

    #changes the "Add Book" button to "Update Book"
    add_button.config(text='Update Book', command=lambda: update_book(title, author, status))

    #creates the "cancel button" (shouldnt really use global because it can mess with other stuff but it works fine for this, because its super light weight)
    global cancel_button
    cancel_button = tk.Button(root, text='Cancel', font=('Georgia', 14), command=lambda: cancel_edit(title, author, status))
    cancel_button.grid(row=5, column=4)
    cancel_button.config(bg='#FFA500')


def cancel_edit(title, author, status):
    #resets the "Add Book" button to "Add Book"
    add_button.config(text='Add Book', command=add_book)

    #deletes the "cancel button"
    cancel_button.destroy()

    #clears the entry fields
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)
 #clear the Combobox widget

def update_book(title, author, status):
    #gets the new values from the entry fields
    updated_title = title_entry.get()
    updated_author = author_entry.get()
    updated_status = status_entry.get()  #gets the new value of the status field from the Combobox widget

    #updates the book in the database
    cursor.execute('''UPDATE books SET title=?, author=?, status=? WHERE title=? AND author=? AND status=?''',
                   (updated_title, updated_author, updated_status, title, author, status))
    conn.commit()
     #change the "Update Book" button to the "Add Book" button
    add_button.config(text='Add Book', command=add_book)

    #removes the Cancel button
    cancel_button.grid_forget()

    #clears the entry fields
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)  #clears the Combobox widget

    #updates the listbox
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

#creates the combobox dropdown for the status field
status_entry = ttk.Combobox(root, font=('Georgia', 14), values=['Read', 'Reading', 'Not Read'])
status_entry.grid(row=2, column=1, columnspan=3)

#creates the "add book" button
add_button = tk.Button(root, text='Add Book', command=add_book, font=('Georgia', 14), bg='lightgreen')
add_button.grid(row=0, column=4)

#creates the "delete book" button
delete_button = tk.Button(root, text='Delete Book', command=delete_book, font=('Georgia', 14), bg='salmon')
delete_button.grid(row=1, column=4)

#creates the "Sort By Status" button
sort_button = tk.Button(root, text='Sort By Status', command=sort_by_status, font=('Georgia', 14), bg='lightblue')
sort_button.grid(row=2, column=4)

#creates the listbox
book_list = tk.Listbox(root, height=12, width=40, font=('Georgia', 14))
book_list.grid(row=3, column=0, columnspan=5)

#binds the double-click event to the edit_book function
book_list.bind('<Double-1>', edit_book)
book_list.bind('<Double-Button-1>', edit_book)

#populates the listbox with the books in the database
display_books()

#runs the main loop
root.mainloop()


# this is just a simple book-manager built by me (@raafay-siddiqui)

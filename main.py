from tkinter import *  # Import all tkinter classes
from tkinter import messagebox  # It's not imported because it's not a class, it's a code module.
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]  # We generate a list but first choosing all the
    # then the symbols and finally the numbers. Then we mix.
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)   # Join is a method of string. Usually you put "$".join(list) and it
    # joins the elements of the list in a string separated by $. Since we don't put a symbol, it joins them without a
    # symbol.

    pass_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()  # These three lines are for taking the text in the posts.git
    email = email_input.get()
    password = pass_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:  # If website or password are empty, it won't let you save it.
        messagebox.showinfo(title='Oops', message="Please make sure you haven't leave any fields empty!")
    else:  # Also instead of using else and indentation in the next, you could put return and thus exit the function.
        is_ok = messagebox.askokcancel(title=website, message=f'These are the details entered: \nEmail: {email} \n'
                                                              f'Password: {password}\n Is it ok to save?')
        if is_ok:
            try:
               with open("data.json", "r") as data_file:
                #   Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
               with open("data.json", "w") as data_file:
                   json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_input.delete(0, END)  # These 2 lines delete the text of the entries. 0 is the beginning of the
                # range, END, the end. (I don't delete the email one so it can continue to be used if you want).
                pass_input.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)  # data is a dictionary.
        website = website_input.get()

    except FileNotFoundError:
        messagebox.showinfo(title='Error', message='No Data File Found')

    else:
        if website in data:  #Obviously we could also treat this as an exception by putting
            # except KeyError:
            #    messagebox.showinfo(title='Error', message='No details for the website exists')
            # ... instead of the if, but
            # it is something very common and it is convenient to use exceptions only if it is something exceptional
            # or difficult to check.
            email = data[website]['email']
            password = data[website]['password']
            messagebox.showinfo(title=website, message=f'Email:{email}\nPassword: {password}')
        else:
            messagebox.showinfo(title='Error', message='No details for the website exists')
    finally:
        website_input.delete(0, END)  # These 2 lines delete the text of the entries. 0 is the beginning of the
        # range, END, the end. (I don't delete the email one so it can continue to be used if you want).
        pass_input.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)  # This makes the image containing the Canvas 40 x 40 larger.

canvas = Canvas(width=200, height=200)
mypass_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=mypass_img)  # The coordinates 100, 100 are the center of the window. So I'm putting
# the image centered.
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

pass_label = Label(text="Password:")
pass_label.grid(row=3, column=0)

# Entries
website_input = Entry(width=33)
website_input.grid(row=1, column=1)
website_input.focus()  # This method is for the cursor to appear in this entry and to be able to start writing without
# clicking before.

email_input = Entry(width=52)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "abc@123.com")  # This method is to have an email preloaded by default. The 0 is the value of the
# "index" and what it does is put the text starting at character 0. Replace abd@123.com with your main email.

pass_input = Entry(width=33)
pass_input.grid(row=3, column=1)

# Buttons
search_button = Button(text="Search", width=15, command=find_password, relief='ridge')
search_button.grid(row=1, column=2)

gen_pass_button = Button(text="Generate Password", command=gen_pass, relief='ridge')
gen_pass_button.grid(row=3, column=2)

add_button = Button(text="Add", command=save, width=44, relief='ridge')
add_button.grid(row=4, column=1, columnspan=2)


window.mainloop()

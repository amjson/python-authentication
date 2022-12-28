from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import database as db
import signup

class SignIn:
    def __init__(self, root):
        # =============> for outer section
        self.window = root
        self.window.title("Sign In")
        self.window.geometry("700x800+300+0")
        self.window.config(bg = "gray")

        # =============> for inner section
        frame = Frame(self.window, bg="white")
        frame.place(x=110,y=150,width=500,height=470)

        # =============> for titles
        title1 = Label(frame, text="Sign In", font=("times new roman",25,"bold"),bg="white").place(x=20, y=10)
        title2 = Label(frame, text="Dely food ordering system", font=("times new roman",13),bg="white", fg="gray").place(x=20, y=50)

        # =============> for email
        email = Label(frame, text="Email", font=("helvetica",15,"bold"),bg="white").place(x=20, y=100)
        self.email_txt = Entry(frame,font=("arial"))
        self.email_txt.place(x=20, y=140, width=420)

        # =============> for password
        password =  Label(frame, text="New password", font=("helvetica",15,"bold"),bg="white").place(x=20, y=185)
        self.password_txt = Entry(frame,font=("arial"))
        self.password_txt.place(x=20, y=220, width=420)

        # =============> for login button
        self.login_button = Button(frame, text="Log In", command=self.login_func, font=("times new roman", 15, "bold"), bd=0, cursor="hand2", bg="blue", fg="white").place(x=90, y=300, width=300)

        # =============> for forgot password button
        self.forgotten_pass = Button(frame, text="Forgotten password?", command=self.forgot_func, font=("times new roman", 12, "bold"), bd=0, cursor="hand2", bg="white", fg="red").place(x=300, y=250, width=150)

        # =============> for create new account button
        self.create_button = Button(frame, text="Create New Account", command=self.redirect_window, font=("times new roman", 13, "bold"), bd=0, cursor="hand2", bg="white", fg="blue").place(x=115, y=350, width=250)



    def login_func(self):
        # =============> check if any field is empty before form submission
        if self.email_txt.get() == "" or self.password_txt.get() == "":
            messagebox.showerror("Error!", "All fields are required", parent=self.window)

        else:
            try:
                # =============> set connection from the system to the database
                connection = pymysql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
                cur = connection.cursor()

                cur.execute("select * from user_register where email=%s and password=%s", (self.email_txt.get(), self.password_txt.get()))
                row = cur.fetchone()

                # =============> confirm if email and password matches with the ones in the database
                if row == None:
                    messagebox.showerror("Error!", "Invalid USERNAME or PASSWORD", parent=self.window)

                else:
                    # =============> Display successful message
                    messagebox.showinfo("Success", "Signin successfully", parent=self.window)

                    # =============> Clear the fields
                    self.reset_fields()

                    # =============> Redirect to dashboard page


            except Exception as e:
                messagebox.showerror("Error!", "Error due to {str(e)}", parent=self.window)

    def forgot_func(self):
        # =============> check if email field is empty before form submission
        if self.email_txt.get() == "":
            messagebox.showerror("Error!", "Please enter your Email Id", parent=self.window)

        else:
            try:
                # =============> set connection from the system to the database
                connection = pymysql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
                cur = connection.cursor()

                cur.execute("select * from user_register where email=%s", self.email_txt.get())
                row = cur.fetchone()

                # =============> confirm if email matches with the ones in the database
                if row == None:
                    messagebox.showerror("Error!", "Email Id doesn't exists")

                else:
                    connection.close()

                    # =============> Toplevel: create a window top of this window
                    self.root = Toplevel()
                    self.root.title("Forget Password?")
                    self.root.geometry("400x440+450+200")
                    self.root.config(bg="white")

                    # =============> focus_force: Helps to to focus on the current window
                    self.root.focus_force()

                    # =============> Grab: Helps to grab the current window until user ungrab it
                    self.root.grab_set()

                    # =============> for titles
                    title3 = Label(self.root, text="Change your password", font=("times new roman", 20, "bold"), bg="white").place(x=10, y=10)
                    title4 = Label(self.root, text="It's quick and easy", font=("times new roman", 12), bg="white").place(x=10, y=45)
                    title5 = Label(self.root, text="Select your question", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=85)

                    # =============> for security question
                    self.sec_ques = ttk.Combobox(self.root, font=("times new roman", 13), state='readonly', justify=CENTER)
                    self.sec_ques['values'] = ("Select", "What's your pet name?", "Your favorite movie")
                    self.sec_ques.place(x=10, y=120, width=270)
                    self.sec_ques.current(0)

                    # =============> for title
                    title6 = Label(self.root, text="Answer", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=160)

                    # =============> for security answer
                    self.ans = Entry(self.root, font=("arial"))
                    self.ans.place(x=10, y=195, width=270)

                    # =============> for title
                    title7 = Label(self.root, text="Your Password", font=("times new roman", 15, "bold"), bg="white").place(x=10, y=235)

                    # =============> for password
                    self.new_pass = Entry(self.root, font=("arial"))
                    self.new_pass.place(x=10, y=270, width=270)

                    # =============> for change password button
                    self.create_button = Button(self.root, text="Submit", command=self.change_pass, font=("times new roman", 18, "bold"), bd=0, cursor="hand2", bg="green2", fg="white").place(x=95, y=340, width=200)

            except Exception as e:
                messagebox.showerror("Error", "{e}")

    def change_pass(self):
        # =============> check if any field is empty before form submission
        if self.email_txt.get() == "" or self.sec_ques.get() == "Select" or self.new_pass.get() == "":
            messagebox.showerror("Error!", "Please fill the all entry field correctly")

        else:
            try:
                # =============> set connection from the system to the database
                connection = pymysql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
                cur = connection.cursor()

                cur.execute("select * from user_register where email=%s and question=%s and answer=%s", (self.email_txt.get(), self.sec_ques.get(), self.ans.get()))
                row = cur.fetchone()

                # =============> confirm if email, question and answer matches with the ones in the database
                if row == None:
                    messagebox.showerror("Error!", "Please fill the all entry field correctly")

                else:
                    try:
                        # =============> update the password which is in the database
                        cur.execute("update user_register set password=%s where email=%s", (self.new_pass.get(), self.email_txt.get()))
                        connection.commit()

                        # =============> Display successful message
                        messagebox.showinfo("Successful", "Password has changed successfully")
                        connection.close()

                        # =============> Clear the fields
                        self.reset_fields()
                        self.root.destroy()

                    except Exception as er:
                        messagebox.showerror("Error!", "{er}")

            except Exception as er:
                messagebox.showerror("Error!", "{er}")

    def redirect_window(self):
        # =============> Redirect to login page
        self.window.destroy()
        root = Tk()
        obj = signup.SignUp(root)
        root.mainloop()

    def reset_fields(self):
        self.email_txt.delete(0, END)
        self.password_txt.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    obj = SignIn(root)
    root.mainloop()

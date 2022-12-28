from tkinter import *
from tkinter import ttk, messagebox
import pymysql
import database as db
import signin

class SignUp:
    def __init__(self, root):
        # =============> for outer section
        self.window = root
        self.window.title("Sign Up")
        self.window.geometry("700x800+300+0")
        self.window.config(bg = "gray")

        # =============> for inner section
        frame = Frame(self.window, bg="white")
        frame.place(x=110,y=90,width=500,height=570)

        # =============> for titles
        title1 = Label(frame, text="Sign Up", font=("times new roman",25,"bold"),bg="white").place(x=20, y=10)
        title2 = Label(frame, text="Dely food ordering system", font=("times new roman",13),bg="white", fg="gray").place(x=20, y=50)

        #=============> for first name
        f_name = Label(frame, text="First name", font=("helvetica",15,"bold"),bg="white").place(x=20, y=100)
        self.fname_txt = Entry(frame,font=("arial"))
        self.fname_txt.place(x=20, y=130, width=200)

        # =============> for last name
        l_name = Label(frame, text="Last name", font=("helvetica",15,"bold"),bg="white").place(x=240, y=100)
        self.lname_txt = Entry(frame,font=("arial"))
        self.lname_txt.place(x=240, y=130, width=200)

        # =============> for email
        email = Label(frame, text="Email", font=("helvetica",15,"bold"),bg="white").place(x=20, y=180)
        self.email_txt = Entry(frame,font=("arial"))
        self.email_txt.place(x=20, y=210, width=420)

        # =============> for security question
        sec_question = Label(frame, text="Security questions", font=("helvetica",15,"bold"),bg="white").place(x=20, y=260)
        self.questions = ttk.Combobox(frame,font=("helvetica",13),state='readonly',justify=CENTER)
        self.questions['values'] = ("Select","What's your pet name?", "Your favorite movie")
        self.questions.place(x=20,y=290,width=200)
        self.questions.current(0)

        # =============> for security answer
        answer = Label(frame, text="Answer", font=("helvetica",15,"bold"),bg="white").place(x=240, y=260)
        self.answer_txt = Entry(frame,font=("arial"))
        self.answer_txt.place(x=240, y=290, width=200)

        # =============> for password
        password =  Label(frame, text="New password", font=("helvetica",15,"bold"),bg="white").place(x=20, y=340)
        self.password_txt = Entry(frame,font=("arial"))
        self.password_txt.place(x=20, y=370, width=420)

        # =============> for terms and condition
        self.terms = IntVar()
        terms_and_con = Checkbutton(frame,text="I Agree The Terms & Conditions",variable=self.terms,onvalue=1,offvalue=0,bg="white",font=("times new roman",12)).place(x=20,y=420)

        # =============> for signup button
        self.signup = Button(frame,text="Sign Up",command=self.signup_func,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="green2",fg="white").place(x=120,y=470,width=250)

        # =============> for users with accounts already
        self.already_member = Button(frame, text="Have an account already?", command=self.redirect_window, font=("times new roman", 12, "bold"), bd=0, cursor="hand2", bg="white", fg="blue").place(x=150, y=525, width=200)

    def signup_func(self):
        # =============> check if any field is empty before form submission
        if self.fname_txt.get()=="" or self.lname_txt.get()=="" or self.email_txt.get()=="" or self.questions.get()=="Select" or self.answer_txt.get()=="" or self.password_txt.get() == "":
            messagebox.showerror("Error!","Sorry!, All fields are required",parent=self.window)

        # =============> confirm if terms and condition is not checked
        elif self.terms.get() == 0:
            messagebox.showerror("Error!","Please Agree with our Terms & Conditions",parent=self.window)

        else:
            try:
                # =============> set connection from the system to the database
                connection = pymysql.connect(host=db.host, user=db.user, password=db.password, database=db.database)
                cur = connection.cursor()

                cur.execute("select * from user_register where email=%s",self.email_txt.get())
                row=cur.fetchone()

                # =============> confirm if email used already exist in the database
                if row != None:
                    messagebox.showerror("Error!","The email has been used already, please try using another email",parent=self.window)

                else:
                    # =============> insert the information in the database
                    cur.execute("insert into user_register (f_name,l_name,email,question,answer,password) values(%s,%s,%s,%s,%s,%s)",
                                    (
                                        self.fname_txt.get(),
                                        self.lname_txt.get(),
                                        self.email_txt.get(),
                                        self.questions.get(),
                                        self.answer_txt.get(),
                                        self.password_txt.get()
                                    )
                                )
                    connection.commit()
                    connection.close()

                    # =============> Display successful message
                    messagebox.showinfo("Congratulations!","Register Successful",parent=self.window)

                    # =============> Clear the fields
                    self.reset_fields()

                    # =============> Redirect to login page
                    self.window.destroy()
                    root = Tk()
                    obj = signin.SignIn(root)
                    root.mainloop()
            except Exception as es:
                messagebox.showerror("Error!","Error due to {es}",parent=self.window)

    def redirect_window(self):
        # =============> Redirect to login page
        self.window.destroy()
        root = Tk()
        obj = signin.SignIn(root)
        root.mainloop()

    def reset_fields(self):
        self.fname_txt.delete(0, END)
        self.lname_txt.delete(0, END)
        self.email_txt.delete(0, END)
        self.questions.current(0)
        self.answer_txt.delete(0, END)
        self.password_txt.delete(0, END)

if __name__ == "__main__":
    root = Tk()
    obj = SignUp(root)
    root.mainloop()

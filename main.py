# calculate user expense
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView

import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("ServiceAccountKey.json.json")
firebase_admin.initialize_app(cred, {
'databaseURL': "https://splitwise-48b0e-default-rtdb.firebaseio.com"
})


signedin_user=""
signedin_name=""

sm = ScreenManager()
sm.transition = SlideTransition()

def goto_login(instance):
    sm.transition.direction = 'left'
    sm.current = 'login'

def goto_signup(instance):
    sm.transition.direction = 'right'
    sm.current = 'signup'

def goto_dashboard(instance):
    sm.transition.direction = 'right'
    sm.current = 'dashboard'

def goto_add_member(instance):
    sm.transition.direction = 'left'
    sm.current = 'member'

def goto_add_expense(instance):
    sm.transition.direction = 'right'
    sm.current = 'expense'


# --- Color Theme ---
Window.clearcolor = (0.01, 0.09, 0.17, 1)  # Dark Navy Blue

PRIMARY_COLOR = (0.2, 0.6, 0.8, 1)  # Teal Blue
SECONDARY_COLOR = (0.1, 0.4, 0.6, 1)
TEXT_COLOR = (1, 1, 1, 1)
BUTTON_TEXT_COLOR = (1, 1, 1, 1)


email_input_signup=None
password_input=None
name_input=None
user_data = {
    "otp": "",
    "email":"",
    "password":"",
    "name":""
}

print(user_data)

#---Write into the database-----

# --- Popup ---
def show_popup(title, message):
    popup = Popup(title=title, content=Label(text=message, color=TEXT_COLOR),
                  size_hint=(None, None), size=(300, 200),
                  background_color=SECONDARY_COLOR)
    popup.open()


# ----SCREEN TEMPLATES----
# --- Login Screen ---
def build_login_screen():
    global email_input,password_input
    layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
    layout.add_widget(Label(text='[b]SmartSplit App[/b]', markup=True, font_size=36,
                            size_hint=(1, None), height=60, color="yellow"))

    float_layout = FloatLayout(size_hint=(1, 1))

    email_input = TextInput(hint_text='Email', multiline=False,
                            size_hint=(0.6, None), height=50,
                            pos_hint={'center_x': 0.5, 'center_y': 0.7},
                            background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    password_input = TextInput(hint_text='Password', password=True, multiline=False,
                               size_hint=(0.6, None), height=50,
                               pos_hint={'center_x': 0.5, 'center_y': 0.55},
                               background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    submit_btn = Button(text='Login', size_hint=(0.4, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.4},
                        background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR, on_press = on_submit)
    

    float_layout.add_widget(email_input)
    float_layout.add_widget(password_input)
    float_layout.add_widget(submit_btn)

    layout.add_widget(float_layout)

    switch_btn = Button(text='New User? Go to Signup', size_hint=(1, None), height=50,
                        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR, on_press = goto_signup)

    layout.add_widget(switch_btn)

    return layout

def on_submit(instance):
    global signedin_user, signedin_name
    login_email = email_input.text.strip()
    login_password = password_input.text.strip()
    if not login_email or not login_password:
        show_popup("ERROR", "Please input details into the correct fields.")
    ref = db.reference("users")
    users_data = ref.get()
    if users_data:
        for userid, userinfo in users_data.items():
            log_email = userinfo["email"]
            log_password = userinfo["password"]
            log_name = userinfo["name"]
            if login_email == log_email and login_password == log_password:
                found = True
                signedin_name = userinfo["name"]
                signedin_user = userinfo["email"]
                break
    if found:
        show_popup("SUCCESS", "You have logged in successfully!")
        sm.transition.direction = 'right'
        sm.current = 'dashboard'
    else:
        show_popup("ERROR", "Incorrect information")

# --- Signup Screen ---
def build_signup_screen():
    global email_input_signup, otp_input_signup, password_input_signup, name_input_signup

    layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
    layout.add_widget(Label(text='[b]SIGN UP[/b]', markup=True, font_size=36,
                            size_hint=(1, None), height=60, color=TEXT_COLOR))

    float_layout = FloatLayout(size_hint=(1, 1))

    name_input_signup = TextInput(hint_text='Name', multiline=False,
                           size_hint=(0.6, None), height=50,
                           pos_hint={'center_x': 0.5, 'center_y': 0.85},
                           background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    email_input_signup = TextInput(hint_text='Email', multiline=False,
                                   size_hint=(0.6, None), height=50,
                                   pos_hint={'center_x': 0.5, 'center_y': 0.70},
                                   background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    password_input_signup = TextInput(hint_text='Password', password=True, multiline=False,
                               size_hint=(0.6, None), height=50,
                               pos_hint={'center_x': 0.5, 'center_y': 0.55},
                               background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    generate_otp_btn = Button(text='Generate OTP', size_hint=(0.4, None), height=40,
                              pos_hint={'center_x': 0.5, 'center_y': 0.40},
                              background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR, on_press = send_otp)
    
    otp_input_signup = TextInput(hint_text='Enter OTP', multiline=False,
                                 size_hint=(0.6, None), height=50,
                                 pos_hint={'center_x': 0.5, 'center_y': 0.25},
                                 background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    verify_btn = Button(text='Verify OTP', size_hint=(0.4, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.10},
                        background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR, on_press = verify_otp)


    float_layout.add_widget(name_input_signup)
    float_layout.add_widget(email_input_signup)
    float_layout.add_widget(password_input_signup)
    float_layout.add_widget(generate_otp_btn)
    float_layout.add_widget(otp_input_signup)
    float_layout.add_widget(verify_btn)

    layout.add_widget(float_layout)

    switch_btn = Button(text='Already a user? Go to Login', size_hint=(1, None), height=50,
                        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR, on_press = goto_login)
    
    layout.add_widget(switch_btn)

    return layout

def send_otp(instance):
    global email_input_signup
    email = email_input_signup.text.strip()
    if not email:
        show_popup("ERROR", "You have not entered a valid email")
        return
    
    otp = str(random.randint(100000, 999999))
    user_data["otp"] = otp
    user_data["email"] = email

    sender_email = "dyofirdaus1@gmail.com"
    sender_password = "hbkb psxn pofb ywon"
    subject = "OTP Code"
    body = f"Thank you for signing up. Your one time password is {otp}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(body,"plain"))

    print (msg.as_string())
    
    try:
        server = smtplib.SMTP("SMTP.gmail.com", 587) 
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
        show_popup("SUCCESS", "OTP sent successfully")
    except:
        show_popup("ERROR", "Failed to send to email")

def updateto_db(userid, email, password, name):
    if userid is None:
        userid = random.randint(100000000, 999999999)
    ref = db.reference(f"users/{userid}")
    ref.set({
        'email': email,
        'password': password,
        'name': name
    })
    print(f"UserID added successfully")

def verify_otp(instance):
    global otp_input_signup
    sent_otp = user_data["otp"]
    input_otp = otp_input_signup.text.strip()
    if input_otp == sent_otp:
        show_popup("SUCCESS", "OTP verified")
    else:
        show_popup("ERROR", "OTP enterred incorrectly")
    email = email_input_signup.text.strip()
    password = password_input_signup.text.strip()
    name = name_input_signup.text.strip()
    user_data["email"] = email
    user_data["password"] = password
    user_data["name"] = name
    updateto_db(None, email, password, name)

#-----Dashboard-----

def build_dashboard_screen():
    global owe_amount_label, other_owe_amount_label, signedin_name, signedin_user, table
    print(signedin_name)
    print(signedin_user)
    signedin_name = "dyo"
    layout = FloatLayout(size_hint=(1, 1))

    # Welcome label
    welcome_label = Label(
        text=f"[b]WELCOME {signedin_name}![/b]",
        markup=True,
        font_size=28,
        size_hint=(None, None), size=(300, 30),
        pos_hint={'center_x': 0.5, 'top': 0.95},
        color="yellow"
    )
    layout.add_widget(welcome_label)

    # Info bar container
    info_float = FloatLayout(size_hint=(None, None), size=(650, 90),
                             pos_hint={'center_x': 0.5, 'top': 0.88})



    # Horizontal box for balances and refresh
    info_box = BoxLayout(orientation='horizontal',
                         spacing=30,
                         size_hint=(None, None),
                         size=(600, 60),
                         pos_hint={'center_x': 0.5, 'center_y': 0.5})

    # YOU OWE section
    owe_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(120, 60))
    owe_label = Label(text='[b]YOU OWE[/b]', markup=True, font_size=18,
                      color="yellow", size_hint=(1, 0.4))
    owe_amount_label = Label(text=str(0), font_size=24,
                             color=TEXT_COLOR, size_hint=(1, 0.6))
    owe_box.add_widget(owe_label)
    owe_box.add_widget(owe_amount_label)

    # OTHERS OWE YOU section
    other_owe_box = BoxLayout(orientation='vertical', size_hint=(None, None), size=(160, 60))
    other_owe_label = Label(text='[b]OTHERS OWE YOU[/b]', markup=True,
                            font_size=18, color="yellow", size_hint=(1, 0.4))
    other_owe_amount_label = Label(text=str(0), font_size=24,
                                   color=TEXT_COLOR, size_hint=(1, 0.6))
    other_owe_box.add_widget(other_owe_label)
    other_owe_box.add_widget(other_owe_amount_label)
    if signedin_name:
        i_owe,others_owe = calculate_user_balance()
        owe_amount_label.text = str(i_owe)
        other_owe_amount_label.text = str(others_owe)
    else:
        i_owe, others_owe = 0,0

    refresh_btn = Button(
        text='Refresh',
        size_hint=(None, None), size=(100, 40),
        background_color=SECONDARY_COLOR,
        color=(1, 1, 1, 1),
        font_size=16,
        on_press = refresh_page
    )

    # Add all to the info box
    info_box.add_widget(owe_box)
    info_box.add_widget(other_owe_box)
    info_box.add_widget(refresh_btn)

    info_float.add_widget(info_box)
    layout.add_widget(info_float)

    # Group members
    group_members = load_member()  # Placeholder for group members
    num_members = len(group_members)
    cols = 3 + num_members
    
    # Table
    table = GridLayout(cols=cols, size_hint_y=None, spacing=5, padding=5)
    # table.bind(minimum_height=table.setter('height'))

    # Add header row
    headers = ['DESCRIPTION', 'PAID BY', 'AMOUNT'] + group_members
    for col in headers:
        table.add_widget(Label(text=f"[b]{col}[/b]", markup=True,
                            color="yellow", size_hint_y=None, height=40))
    
    tr_ref = db.reference("transaction")
    tr_data = tr_ref.get()
    if tr_data:
        for trid, trinfo in tr_data.items():
            tr_desc = trinfo.get("description", "")
            tr_topay = trinfo.get("topay", "")
            tr_amount = trinfo.get("amount", 0.00)
            table.add_widget(Label(text = str(tr_desc), 
                                   color = "white", size_hint_y = None, height = 40))
            table.add_widget(Label(text = str(tr_topay),
                                   color = "white", size_hint_y = None, height = 40))
            table.add_widget(Label(text = str(tr_amount),
                                   color = "white", size_hint_y = None, height = 40))
            tr_split = trinfo.get("split", {})
            for member in group_members:
                share = tr_split.get(member, "")
                if isinstance(share, (int,float)):
                    share_text = f"{share:.2f}"
                elif share == "" or share is None:
                    share_text = "-"
                else:
                    try:
                        share_text = f"{float(share):.2f}"
                    except:
                        share_text = str(share)
                table.add_widget(Label(text = str(share_text),
                                       color= "white", size_hint_y = None, height = 40))
                
        table_scroll = ScrollView(size_hint = (1,None), size = (Window.width, 500), scroll_y = 1.0,
                                  pos_hint = {'x': 0, 'y': -0.25})
        table_scroll.add_widget(table)
        layout.add_widget(table_scroll)
    else:
        layout.add_widget(Label(text = "No transactions",
                                color = "yellow", size_hint_y = None, height = 40, 
                                pos_hint = {'center_x': 0.5, 'center_y': 0.5}))

    # Buttons at bottom
    btn_layout = BoxLayout(
        orientation='horizontal',
        size_hint=(1, None), height=60, spacing=20, padding=[0, 0, 0, 10]
    )
    add_expense_btn = Button(
        text='Add Expense',
        size_hint=(0.5, 1),
        background_color=SECONDARY_COLOR,
        color=(1, 1, 1, 1),
        on_press = goto_add_expense
    )
    add_group_members_btn = Button(
        text='Add Group Members',
        size_hint=(0.5, 1),
        background_color=SECONDARY_COLOR,
        color=(1, 1, 1, 1),
       on_press = goto_add_member
    )
    btn_layout.add_widget(add_expense_btn)
    btn_layout.add_widget(add_group_members_btn)
    layout.add_widget(btn_layout)

    return layout

def calculate_user_balance():
    i_owe = 0.00
    others_owe = 0.00
    tr_ref = db.reference("transaction")
    tr_id = tr_ref.get()
    if not tr_id:
        return round(i_owe,2),round(others_owe,2)
    for trdata, trinfo in tr_id.items():
        topay = trinfo.get("topay","")
        if topay == signedin_name:
            tr_split = trinfo["split"]
            for name, amount in tr_split.items():
                if name != signedin_name:
                    others_owe += amount
        if topay != signedin_name:
            tr_o_split = trinfo["split"]
            for name, amount in tr_o_split.items():
                if name == signedin_name:
                    i_owe += amount
    return round(i_owe,2),round(others_owe,2)

def refresh_page(instance):
    db.reference("transaction").delete()
    table.clear_widgets()
    # group_members.clear()
    owe_amount_label.text = str(0)
    other_owe_amount_label.text = str(0)
    show_popup("INFO","All transactions cleared")

#---- Add Group Member Screen ---
def build_add_group_screen():
        global member_name_input, member_email_input, contact_input
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        layout.add_widget(Label(
            text='[b]ADD GROUP MEMBER[/b]', markup=True, font_size=36,
            size_hint=(1, None), height=60, color="yellow"
        ))

        float_layout = FloatLayout(size_hint=(1, 1))

        # Name
        name_label = Label(text='Name:', size_hint=(None, None), size=(100, 40),
                        pos_hint={'center_x': 0.2, 'center_y': 0.75}, color=TEXT_COLOR)
        member_name_input = TextInput(size_hint=(0.6, None), height=50,
                                    pos_hint={'center_x': 0.6, 'center_y': 0.75},
                                    background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        # Email
        email_label = Label(text='Email:', size_hint=(None, None), size=(100, 40),
                            pos_hint={'center_x': 0.2, 'center_y': 0.6}, color=TEXT_COLOR)
        member_email_input = TextInput(size_hint=(0.6, None), height=50,
                                    pos_hint={'center_x': 0.6, 'center_y': 0.6},
                                    background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        # Contact
        contact_label = Label(text='Contact (optional):', size_hint=(None, None), size=(150, 40),
                            pos_hint={'center_x': 0.2, 'center_y': 0.45}, color=TEXT_COLOR)
        contact_input = TextInput(size_hint=(0.6, None), height=50,
                                pos_hint={'center_x': 0.6, 'center_y': 0.45},
                                background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

        # Buttons
        add_btn = Button(text='Add Member', size_hint=(0.4, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.3},
                        background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR,
                        on_press = add_member,
                       )

        back_btn = Button(text='Back to Dashboard', size_hint=(1, None), height=50,
                        pos_hint={'center_x': 0.5, 'center_y': 0.15},
                        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR,
                        on_press = goto_dashboard
                       )
    

        # Add to layout
        float_layout.add_widget(name_label)
        float_layout.add_widget(member_name_input)
        float_layout.add_widget(email_label)
        float_layout.add_widget(member_email_input)
        float_layout.add_widget(contact_label)
        float_layout.add_widget(contact_input)
        float_layout.add_widget(add_btn)
        float_layout.add_widget(back_btn)

        layout.add_widget(float_layout)
        return layout

def add_member(instance):
    member_name = member_name_input.text.strip()
    member_email = member_email_input.text.strip()
    member_contact = contact_input.text.strip()
    member1_ref = db.reference("users")
    users_data = member1_ref.get()
    if users_data:
        for userid, userinfo in users_data.items():
            if userinfo["email"].lower() == member_email.lower():
                show_popup("ERROR", f"Email already exists:\n {member_email}")
                return
            if userinfo["name"].lower() == member_name.lower():
                show_popup("ERROR", f"Name already exists:\n {member_name}")
                return

    member_password = str(random.randint(100000000,999999999))
    userid = random.randint(100000000,999999999)
    member2_ref = db.reference(f"users/{userid}")
    member2_ref.set({
        'name': member_name,
        'email': member_email,
        'contacts': member_contact,
        'password': member_password
    })
    send_member_email(member_email, member_password)
    show_popup("SUCCESS", f"This member has been successfully added: {member_name}")
    member_name_input.text = ""
    member_email_input.text = ""
    contact_input.text = ""

def send_member_email(member_email, member_password):
    sender_email = "dyofirdaus1@gmail.com"
    sender_password = "hbkb psxn pofb ywon"
    subject = "Welcome, New Member"
    body = f"You have been added as a member in {sender_email}'s SplitWise App! Be sure to use the password provided when you sign in.\n\n Password: {member_password}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = member_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body,"plain"))

    print (msg.as_string())
    
    try:
        server = smtplib.SMTP("SMTP.gmail.com", 587) 
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, member_email, msg.as_string())
        server.quit()
    except:
        show_popup("ERROR", "Failed to send to email")

#---- Add Expense Screen ---
def build_add_expense_screen():
    global who_paid_spinner, description_input, amount_input, group_members
    layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

    layout.add_widget(Label(
        text='[b]ADD EXPENSE[/b]', markup=True, font_size=36,
        size_hint=(1, None), height=60, color="yellow"
    ))

    float_layout = FloatLayout(size_hint=(1, 1))

    # Who Paid
    who_paid_label = Label(text='Who Paid:', size_hint=(None, None), size=(120, 40),
                           pos_hint={'center_x': 0.18, 'center_y': 0.75}, color=TEXT_COLOR)
    
    # who_paid_input = TextInput(size_hint=(0.6, None), height=50,
    #                            pos_hint={'center_x': 0.6, 'center_y': 0.75},
    #                            background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))
    group_members=load_member()  # Placeholder for group members
    who_paid_spinner= Spinner(
        text='Group Members',
        values=group_members,
        size_hint=(0.5, None), size=(180, 50),
        pos_hint={'x': 0.3, 'center_y': 0.75},
        background_color="white",
        color=TEXT_COLOR,
        font_size=16
    )
    # Description
    description_label = Label(text='Description:', size_hint=(None, None), size=(120, 40),
                              pos_hint={'center_x': 0.18, 'center_y': 0.6}, color=TEXT_COLOR)
    description_input = TextInput(size_hint=(0.6, None), height=50,
                                  pos_hint={'center_x': 0.6, 'center_y': 0.6},
                                  background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    # Amount
    amount_label = Label(text='Amount:', size_hint=(None, None), size=(120, 40),
                         pos_hint={'center_x': 0.18, 'center_y': 0.45}, color=TEXT_COLOR)
    amount_input = TextInput(size_hint=(0.6, None), height=50,
                             pos_hint={'center_x': 0.6, 'center_y': 0.45},
                             background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1))

    # Buttons
    add_btn = Button(text='Add', size_hint=(0.4, None), height=50,
                     pos_hint={'center_x': 0.5, 'center_y': 0.28},
                     background_color=PRIMARY_COLOR, color=BUTTON_TEXT_COLOR,
                     on_press = add_expense
                     )

    back_btn = Button(
        text='Back to Dashboard',
        size_hint=(1, None), height=50,
        pos_hint={'center_x': 0.5, 'center_y': 0.14},
        background_color=SECONDARY_COLOR, color=BUTTON_TEXT_COLOR,
        on_press = goto_dashboard
    )

    # Call add_expense when the button is pressed, then go to dashboard
   
    # Add widgets
    float_layout.add_widget(who_paid_label)
    float_layout.add_widget(who_paid_spinner)
    float_layout.add_widget(description_label)
    float_layout.add_widget(description_input)
    float_layout.add_widget(amount_label)
    float_layout.add_widget(amount_input)
    float_layout.add_widget(add_btn)
    float_layout.add_widget(back_btn)

    layout.add_widget(float_layout)

    return layout

def add_expense(instance):
    exp_desc = description_input.text.strip()
    exp_name = who_paid_spinner.text
    exp_amount = amount_input.text.strip()
    tr_id = random.randint(1000,9999)
    if not exp_desc or not exp_name or not exp_amount:
        show_popup("ERROR","Please fill in all the fields")
        return
    amount = float(exp_amount)
    split_amount = amount/len(group_members)
    split_dict = dict.fromkeys(group_members, split_amount)
    print(split_dict)
    ref = db.reference("transaction")
    ref.push({
        'transactionid': tr_id,
        'description': exp_desc,
        'topay':exp_name,
        'amount': amount,
        'split': split_dict
    })
    show_popup("SUCCESS", "Expenses have been added")
    description_input.text = ""
    who_paid_spinner.text = "Group Members"
    amount_input.text = ""
    

def load_member():
    global group_members
    group_members=[]
    load_group = db.reference("users")
    member_data = load_group.get()
    if member_data:
        for usersid, usersinfo in member_data.items():
            name = usersinfo.get("name")
            group_members.append(name)
        return group_members

signup_screen = Screen(name = 'signup')
signup_screen.add_widget(build_signup_screen())
login_screen = Screen(name = 'login')
login_screen.add_widget(build_login_screen())
dashboard_screen = Screen(name = 'dashboard')
def update_dashboard(*args):
    dashboard_screen.clear_widgets()
    dashboard_screen.add_widget(build_dashboard_screen())
dashboard_screen.bind(on_enter = update_dashboard)
dashboard_screen.add_widget(build_dashboard_screen())
add_member_screen = Screen(name = 'member')
add_member_screen.add_widget(build_add_group_screen())
add_expense_screen = Screen(name = 'expense')
add_expense_screen.add_widget(build_add_expense_screen())

sm.add_widget(login_screen)
sm.add_widget(signup_screen)
sm.add_widget(dashboard_screen)
sm.add_widget(add_member_screen)
sm.add_widget(add_expense_screen)

class MyApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyApp().run()
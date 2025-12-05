from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from datetime import datetime
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition

sm = ScreenManager()
sm.transition = SlideTransition()

def goto_add_task(instance):
    show_add_task(None)
    sm.transition.direction = 'left'
    sm.current = 'addtask'

def goto_dashboard(instance):
    show_dashboard(None)
    sm.transition.direction = 'right'
    sm.current = 'dashboard'


tasks = []

def build(self):
    self.root_layout = FloatLayout()
    self.show_dashboard()
    return self.root_layout

def show_dashboard(_):
    root_layout = FloatLayout()

    title = Label(
        text="[b]TO-DO LIST[/b]",
        markup=True,
        size_hint=(1, 0.12),
        pos_hint={'top': 1},
        color=(0, 1, 0, 1),
        font_size="28"
    )
    root_layout.add_widget(title)

    today = datetime.now()
    date_text = today.strftime("%A, %d %B %Y")

    date_label = Label(
        text=f"[b]{date_text}[/b]",
        markup=True,
        size_hint=(1, 0.05),
        pos_hint={'center_x': 0.5, 'top': 0.93},
        font_size="20"
    )
    root_layout.add_widget(date_label)

    scroll = ScrollView(size_hint=(1, 0.65), pos_hint={'x': 0, 'y': 0.2})
    task_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
    task_list.bind(minimum_height=task_list.setter('height'))

    for task in tasks:
        box = BoxLayout(size_hint_y=None, height=40, spacing=10, padding=10)

        checkbox = CheckBox(size_hint=(0.1, 1))
        checkbox.active = task["done"]

        def set_done(cb, value, t=task):
            t["done"] = value

        checkbox.bind(active=set_done)

        label = Label(
            text=f"{task['objective']} | {task['deadline']} | {task['priority']}",
            halign="left",
            valign="middle"
        )

        label.bind(size=label.setter("text_size"))

        box.add_widget(checkbox)
        box.add_widget(label)
        task_list.add_widget(box)
    
    scroll.add_widget(task_list)
    root_layout.add_widget(scroll)

    add_btn = Button(
        text="Add Task",
        size_hint=(0.4, 0.12),
        pos_hint={'center_x': 0.5, 'y': 0.05},
        on_press=goto_add_task
    )
    root_layout.add_widget(add_btn)

    dashboard_screen.clear_widgets()
    dashboard_screen.add_widget(root_layout)

def show_add_task(_):
    root_layout = FloatLayout()

    title = Label(
        text="[b]ADD NEW TASK[/b]",
        markup=True,
        size_hint=(1, 0.12),
        pos_hint={'top': 1},
        color=(0, 1, 0, 1),
        font_size="28"
    )
    root_layout.add_widget(title)

    root_layout.add_widget(Label(
        text="Objective:",
        size_hint=(0.3, 0.08),
        pos_hint={'x': 0.05, 'y': 0.72},
        font_size="18"
    ))
    obj_input = TextInput(size_hint=(0.6, 0.08), pos_hint={'x': 0.32, 'y': 0.725})
    root_layout.add_widget(obj_input)

    root_layout.add_widget(Label(
        text="Deadline:",
        size_hint=(0.3, 0.08),
        pos_hint={'x': 0.05, 'y': 0.58},
        font_size="18"
    ))
    deadline_input = TextInput(size_hint=(0.6, 0.08), pos_hint={'x': 0.32, 'y': 0.585})
    root_layout.add_widget(deadline_input)

    root_layout.add_widget(Label(
        text="Priority:",
        size_hint=(0.3, 0.08),
        pos_hint={'x': 0.05, 'y': 0.44},
        font_size="18"
    ))
    priority_spinner = Spinner(
        text="Select Priority",
        values=["High", "Medium", "Low"],
        size_hint=(0.6, 0.08),
        pos_hint={'x': 0.32, 'y': 0.445}
    )
    root_layout.add_widget(priority_spinner)

    def save_task(_):
        tasks.append({
            "objective": obj_input.text,
            "deadline": deadline_input.text,
            "priority": priority_spinner.text,
            "done": False
        })
        goto_dashboard(None)

    save_btn = Button(
        text="Save Task",
        size_hint=(0.38, 0.1),
        pos_hint={'right': 0.98, 'y': 0.05},
        on_press=save_task
    )
    
    root_layout.add_widget(save_btn)

    back_btn = Button(
        text="Back",
        size_hint=(0.38, 0.1),
        pos_hint={'x': 0.02, 'y': 0.05},
        on_press=goto_dashboard
    )
    root_layout.add_widget(back_btn)

    add_task_screen.clear_widgets()
    add_task_screen.add_widget(root_layout)

dashboard_screen = Screen(name='dashboard')
add_task_screen = Screen(name='addtask')

sm.add_widget(dashboard_screen)
sm.add_widget(add_task_screen)

show_dashboard(None)

class TDApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    TDApp().run()

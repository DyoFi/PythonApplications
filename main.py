from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDRaisedButton
import requests
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.card import MDCard
from kivy.uix.image import AsyncImage
from kivymd.uix.scrollview import ScrollView
from kivy.core.window import Window

#Async = wait for instruction to finish to move on to next line

PRIMARY_COLOR = (1,0.5,0.2,1)
api_key = "b1MZQ3kmHcgcXZ5VippDH6zFNAqbEK16sPb5jEed"

class APODApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"

        self.main_layout = BoxLayout(orientation = "vertical", padding = 40, spacing = 20)
        main_layout_title = MDLabel(text = "NASA Picture Of The Day", halign = "center", font_style = "H5", markup = True,
                                    theme_text_color = "Custom", text_color = PRIMARY_COLOR)
        select_date_btn = MDRaisedButton(text = "Select Date", pos_hint = {'center_x' : 0.5},
                                          on_press = self.open_date_picker)
        self.main_layout.add_widget(main_layout_title)
        self.main_layout.add_widget(select_date_btn)

        self.card_layout = MDCard(orientation = "vertical", size_hint_y = None, height = 400, padding = 20)
        self.img_title = MDLabel(text = "")
        self.date_img = MDLabel(text = "")
        self.apod_img = AsyncImage(width = 500, height = 200, allow_stretch = True, size_hint = (None, None))

        self.card_layout.add_widget(self.img_title)
        self.card_layout.add_widget(self.date_img)
        self.card_layout.add_widget(self.apod_img)

        self.main_layout.add_widget(self.card_layout)
        
        self.scroll = ScrollView(size_hint = (1,None), height  = 200, bar_width = 10)

        self.lower_layout = BoxLayout(orientation = "vertical", padding = 20, spacing = 20, size_hint_y = None)
        self.lower_layout.bind(minimum_height = self.lower_layout.setter("height"))

        self.desc_heading = MDLabel(text = "Description", size_hint_y = None, height = 30)
        self.desc_text = MDLabel(text = "", size_hint_y = None, text_size = (Window.width - 60, None))

        self.lower_layout.add_widget(self.desc_heading)
        self.lower_layout.add_widget(self.desc_text)
        self.scroll.add_widget(self.lower_layout)

        self.main_layout.add_widget(self.scroll)

        return self.main_layout

    def open_date_picker(self, instance):
        picker = MDDatePicker()
        picker.bind(on_save = self.on_date_selected)
        picker.open()

    def on_date_selected(self, instance, date, _):
        self.fetch_apod(str(date))

    def fetch_apod(self, date):
        try:
            params = {
                'api_key': api_key,
                'date': date
            }

            url = "https://api.nasa.gov/planetary/apod"

            response = requests.get(url, params = params)

            if response.status_code == 200: 
                data = response.json()

                self.img_title.text = data.get("title", "")
                self.image_url = data.get("url", "")
                self.hd_image_url = data.get("hdurl", self.image_url)
                self.date_img.text = data.get("date", "")

                self.desc_text.text = data.get("explanation", "")
                self.image.source = self.image_url
        except:
            print("Failed to connect to API")

if __name__ == "__main__":
    APODApp().run()
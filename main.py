from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image

world_img = ("world_map.png")

countries = {
    'Europe': {"currency": "EUR", "pos": (0.55,0.48)},
    'Canada': {"currency": "CAD", "pos": (0.13,0.5)},
    'USA': {"currency": "USD", "pos": (0.14,0.41)},
    'Japan': {"currency": "JAP", "pos": (0.84,0.4)},
    'India': {"currency": "INR", "pos": (0.65,0.32)}
}

class CurrencyApp(App):
    def build(self):
        main_layout = FloatLayout(pos_hint = {'x':0, 'y':0}, size_hint = (1,1))
        cur_label = Label(text = "Real Time Currency App", pos_hint ={'x':0.1, 'y':0.85}, size_hint = (0.8, None), font_size = 40, color = (1,0,0,1))
        calc_options = BoxLayout(orientation = "horizontal", pos_hint = {'x': 0, 'y':0.7}, size_hint = (1, None))
        self.num_write = TextInput(hint_text = "Write Here", input_filter = "float")
        self.country_opt = Spinner(text = "Select Currency", values = ["EUR", "CAD", "USD", "JAP", "INR"])
        calc_btn = Button(text = "Calculate", on_press = self.currency_calculator)
        reset_btn = Button(text = "Reset", on_press = self.reset_button)
        # eur_label = Label(text = "EUR", font_size = 15, color = (1,1,1,1))
        # eur_currency = Label(text = "...", font_size = 15, color = (1,1,1,1))
        # cad_label = Label(text = "CAD", font_size = 15, color = (1,1,1,1))
        # cad_currency = Label(text = "...", font_size = 15, color = (1,1,1,1))
        # usd_label = Label(text = "USD", font_size = 15, color = (1,1,1,1))
        # usd_currency = Label(text = "...", font_size = 15, color = (1,1,1,1))
        # jap_label = Label(text = "JAP", font_size = 15, color = (1,1,1,1))
        # jap_currency = Label(text = "...", font_size = 15, color = (1,1,1,1))
        # inr_label = Label(text = "INR", font_size = 15, color = (1,1,1,1))
        # inr_currency = Label(text = "...", font_size = 15, color = (1,1,1,1))
        self.world_img = Image(source = "world_map.png", pos_hint = {'x':0, 'y': -0.125}, size_hint = (1,0.9))
        calc_options.add_widget(self.num_write)
        calc_options.add_widget(self.country_opt)
        calc_options.add_widget(calc_btn)
        calc_options.add_widget(reset_btn)
        main_layout.add_widget(cur_label)
        main_layout.add_widget(calc_options)
        main_layout.add_widget(self.world_img)
        self.country_labels = {}
        for country, data in countries.items():
            label = Label(
                text = country,
                pos_hint = {'x': data["pos"][0]-0.45, 'y': data["pos"][1]-0.5},
                size = (300,200)
            )
            self.country_labels[country] = label
            print (self.country_labels)
            main_layout.add_widget(label)
        return main_layout
    
    def currency_calculator(self, instance):
        usd_to = {"EUR": 0.92, "CAD": 1.36, "USD": 1, "JAP": 157.4, "INR": 83.5}
        amount = float(self.num_write.text)
        base_currency = self.country_opt.text 
        for key, value in usd_to.items():
            conversion = amount * usd_to[key]
            for country, data in countries.items():
                label = self.country_labels[country]
                label.text = f"{country}\n {conversion} {data["currency"]}"


    def reset_button(self):
        pass

if __name__ == "__main__":
    CurrencyApp().run()

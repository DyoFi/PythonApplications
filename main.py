from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image

class WeatherApp(App):
    def build(self):
        main_layout = FloatLayout()

        title_label = Label(
            text="Global Weather Display",
            markup=True,
            font_size="28",
            size_hint=(1, 0.1),
            pos_hint={"x": 0, "y": 0.85}
        )
        main_layout.add_widget(title_label)

        weather_image = Image(
            source="Emoji_Sun_Behind_Cloud_Emoji_grande-removebg-preview.png", 
            size_hint=(0.8, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        main_layout.add_widget(weather_image)

        weather_data = {
            "weather": "Sunny",
            "temperature": "30°C",
            "pressure": "1013 hPa",
            "humidity": "60%"
        }

        y_position = 0.38
        for key, value in weather_data.items():
            label = Label(
                text=f"{key.capitalize()}: {value}",
                markup=True,
                font_size="20",
                size_hint=(0.6, 0.1),
                pos_hint={"center_x": 0.5, "y": y_position}
            )
            main_layout.add_widget(label)
            y_position -= 0.1  # Move each label down

        return main_layout


if __name__ == "__main__":
    WeatherApp().run()
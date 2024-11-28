import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle


class MainApp(App):
    def build(self):
        self.theme_color = [0.2, 0.6, 0.8, 1]
        self.basket = []  # List to store items added to the basket

        # Main layout
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        with main_layout.canvas.before:
            self.bg_color = Color(*self.theme_color)
            self.bg_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(
            size=lambda _, size: setattr(self.bg_rect, 'size', size),
            pos=lambda _, pos: setattr(self.bg_rect, 'pos', pos)
        )

        # Top section: Title and Dropdown
        top_layout = FloatLayout(size_hint=(1, None), height=100)
        title = Label(
            text="Food Order",
            font_size=28,
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'left': 1, 'top': 1},
            color=[1, 1, 1, 1]
        )
        top_layout.add_widget(title)

        profile_picture = Image(
            source='Depositphotos_484354208_S.jpg',
            size_hint=(None, None),
            size=(100,100),
            pos_hint={'right': 1, 'top': 1},
        )
        top_layout.add_widget(profile_picture)

        self.dropdown = DropDown()
        stores = ["Store A", "Store B", "Store C"]
        for store in stores:
            btn = Button(
                text=store,
                size_hint_y=None,
                height=40,
                background_normal='',
                background_color=[0.8, 0.8, 0.8, 1],
                color=[0, 0, 0, 1]
            )
            btn.bind(on_release=lambda btn: self.select_store(btn))
            self.dropdown.add_widget(btn)

        dropdown_button = Button(
            text="Select Store",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'left': 1, 'top': 0.5},
            background_normal='',
            background_color=[0.8,0.8,0.8,1],
            color=[0, 0, 0, 1]
        )
        dropdown_button.bind(on_release=self.dropdown.open)
        self.dropdown.main_button = dropdown_button
        top_layout.add_widget(dropdown_button)

        main_layout.add_widget(top_layout)

        # Search and Filter Section
        search_filter_layout = BoxLayout(size_hint=(1, None), height=50, spacing=10)

        # Search Bar
        search_input = TextInput(
            hint_text="Search items...",
            size_hint=(0.7, 1),
            background_color=[0.95, 0.95, 0.95, 1],
            foreground_color=[0, 0, 0, 1]
        )
        search_filter_layout.add_widget(search_input)

        # Filter Dropdown
        filter_dropdown = DropDown()
        filter_options = ['Price: Low to High', 'Price: High to Low', 'Category: Electronics', 'Category: Clothing']
        for option in filter_options:
            filter_btn = Button(
                text=option,
                size_hint_y=None,
                height=40,
                background_normal='',
                background_color=[0.8, 0.8, 0.8, 1],
                color=[0, 0, 0, 1]
            )
            filter_btn.bind(on_release=lambda btn: self.select_filter(btn, filter_dropdown))
            filter_dropdown.add_widget(filter_btn)

        filter_button = Button(
            text="Filter",
            size_hint=(0.3, 1),
            background_normal='',
            background_color=[0.8, 0.8, 0.8, 1],
            color=[0, 0, 0, 1]
        )
        filter_button.bind(on_release=filter_dropdown.open)
        search_filter_layout.add_widget(filter_button)

        main_layout.add_widget(search_filter_layout)

        # Item Box Section
        item_box = ScrollView(size_hint=(1, 1))
        item_layout = GridLayout(cols=2, size_hint_y=None, spacing=10, padding=10)
        item_layout.bind(minimum_height=item_layout.setter('height'))

        # Example items
        for i in range(10):
            item_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=200)
            item_image = Image(source="example.jpg", size_hint=(None, None), size=(100, 100))
            item_label = Label(
                text=f"Item {i + 1}",
                size_hint=(0.5, 1),
                valign="middle",
                halign="left",
                color=[0, 0, 0, 1]
            )
            item_label.bind(size=item_label.setter('text_size'))  # Ensure text wraps within label

            add_button = Button(
                text="Add",
                size_hint=(None, None),
                size=(80, 40),
                background_normal='',
                background_color=[0.2, 0.8, 0.2, 1],
                color=[1, 1, 1, 1]
            )
            add_button.bind(on_release=lambda instance, item=f"Item {i + 1}": self.add_to_basket(item))

            item_container.add_widget(item_image)
            item_container.add_widget(item_label)
            item_container.add_widget(add_button)
            item_layout.add_widget(item_container)

        item_box.add_widget(item_layout)
        main_layout.add_widget(item_box)

        # Basket Button
        basket_button = Button(
            text="View Basket",
            size_hint=(None, None),
            size=(150, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            background_normal='',
            background_color=[1, 0.5, 0.2, 1],
            color=[1, 1, 1, 1]
        )
        basket_button.bind(on_release=self.open_basket)
        main_layout.add_widget(basket_button)

        return main_layout

    def add_to_basket(self, item):
        self.basket.append(item)
        print(f"Added to basket: {item}")

    def select_store(self, btn):
        self.dropdown.main_button.text = btn.text
        self.dropdown.dismiss()

    def open_basket(self, instance):
        basket_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        basket_title = Label(text="Your Basket", font_size=20, size_hint_y=None, height=40, color=[0, 0, 0, 1])
        basket_layout.add_widget(basket_title)

        if self.basket:
            for item in self.basket:
                basket_item = Label(text=item, size_hint_y=None, height=30, color=[0, 0, 0, 1])
                basket_layout.add_widget(basket_item)
        else:
            basket_layout.add_widget(Label(text="Your basket is empty", size_hint_y=None, height=30))

        close_button = Button(
            text="Close",
            size_hint_y=None,
            height=40,
            background_normal='',
            background_color=[0.8, 0.1, 0.2, 1],
            color=[1, 1, 1, 1]
        )
        basket_layout.add_widget(close_button)

        basket_popup = Popup(
            title="Basket",
            content=basket_layout,
            size_hint=(0.8, 0.8)
        )
        close_button.bind(on_release=basket_popup.dismiss)
        basket_popup.open()

    def select_filter(self, btn, dropdown):
        dropdown.parent.parent.children[-1].text = btn.text
        dropdown.dismiss()


if __name__ == "__main__":
    MainApp().run()


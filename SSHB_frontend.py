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
import backend
def setup():
    backend.create_database()
    backend.filefiller()
    backend.filetodatabase()
class MainApp(App):
    itemstobedisplayed = []

    def setupitems(self):
        self.itemstobedisplayed = backend.selectfromdatabase("getall", 0)

    def build(self):
        self.setupitems()
        self.theme_color = [29, 29, 31, 1]
        self.basket = []  # List to store items added to the basket
        self.student_id = None
        self.household_id = None

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
            color=[0, 0, 0, 1]
        )
        top_layout.add_widget(title)

        profile_picture = Image(
            source='Depositphotos_484354208_S.jpg',
            size_hint=(None, None),
            size=(100,100),
            pos_hint={'right': 1, 'top': 1}
        )
        top_layout.add_widget(profile_picture)

        self.dropdown = DropDown()
        stores = ["Store A", "Store B", "Store C", "ALL"]
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
            pos_hint={'top': 0.45},
            background_normal='',
            background_color=[0.8,0.8,0.8,1],
            color=[0, 0, 0, 1]
        )
        dropdown_button.bind(on_release=self.dropdown.open)
        self.dropdown.main_button = dropdown_button
        top_layout.add_widget(dropdown_button)

        main_layout.add_widget(top_layout)

        # Search and Filter Section
        search_filter_layout = BoxLayout(size_hint=(1, None), height=50, spacing=100)

        search_group_layout = BoxLayout(size_hint=(0.6, 1), spacing=5)

        # Search Bar
        self.search_input = TextInput(
            hint_text="Search items...",
            size_hint=(0.5, 0.8),
            background_color=[0.95, 0.95, 0.95, 1],
            foreground_color=[0, 0, 0, 1],
            multiline = False # Ensures when you press enter, search bar doesn't go into a new line
        )
        self.search_input.bind(on_text_validate = self.execute_search)
        search_group_layout.add_widget(self.search_input) 
        

        self.search_button = Button(
            text = "Search",
            size_hint = (0.1, 0.8),
            background_normal = '',
            background_color = [0.2,0.8,0.8,1],
            color = [1,1,1,1]
        )
        self.search_button.bind(on_release = self.execute_search)
        search_group_layout.add_widget(self.search_button)
    
        search_filter_layout.add_widget(search_group_layout)

        # Filter Dropdown
        filter_dropdown = DropDown()
        filter_options = ['Price: Low to High', 'Price: High to Low']
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
            size_hint=(0.13, 0.8),
            background_normal='',
            background_color=[0.8, 0.8, 0.8, 1],
            color=[0, 0, 0, 1]
        )
        filter_button.bind(on_release=filter_dropdown.open)
        search_filter_layout.add_widget(filter_button)

        main_layout.add_widget(search_filter_layout)

        # Item Box Section
        item_box = ScrollView(size_hint=(1, 1))
        self.item_layout = GridLayout(cols=2, size_hint_y=None, spacing=10, padding=10)
        self.item_layout.bind(minimum_height=self.item_layout.setter('height'))

        # Initial items
        self.refresh_items()
        
        item_box.add_widget(self.item_layout)
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

    def on_start(self):
        self.opening_prompt()

    def opening_prompt(self):
        prompt_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        # basket_title = Label(text="Enter your student_id and household_id", font_size=15, size_hint_y=None, height=40, color=[0, 0, 0, 1])
        # basket_layout.add_widget(basket_title)

        self.student_id_intput = TextInput(
            hint_text = "Enter your Student ID:",
            multiline = False,
            size_hint = (1,None),
            height = 40
        )
        prompt_layout.add_widget(self.student_id_intput)


        self.household_id_intput = TextInput(
            hint_text = "Enter your Household ID:",
            multiline = False,
            size_hint = (1,None),
            height = 40
        )
        prompt_layout.add_widget(self.household_id_intput)


        submit_button = Button(
            text="Submit",
            size_hint=(1,None),
            height=40,
            background_normal='',
            background_color=[0.2, 0.8, 0.2, 1],
            color=[1, 1, 1, 1]
        )
        submit_button.bind(on_release = self.update_inputs_to_db)
        prompt_layout.add_widget(submit_button)


        #prompt_layout.add_widget(close_button)
        self.basket_popup = Popup(
            title="Enter your details",
            content=prompt_layout,
            size_hint=(0.5, 0.3),
            auto_dismiss = False
        )
        self.basket_popup.open()
       
    def update_inputs_to_db(self, instance):

        student_id = self.student_id_intput.text.strip()
        household_id =self.household_id_intput.text.strip()

        if student_id and household_id:
            self.student_id = student_id
            self.household_id = household_id
            print(self.student_id)
            print(self.household_id)
            self.basket_popup.dismiss()
    
    def refresh_items(self):
        # Clear the current items
        self.item_layout.clear_widgets()
        Shopdict = {1: "A", 2:"B", 3:"C",}
        # Add the filtered items based on self.itemstobedisplayed
        for i in range(len(self.itemstobedisplayed)):
            item_container = BoxLayout(orientation='horizontal', size_hint_y=None, height=200)
            item_image = Image(source="Item_images/" + str(self.itemstobedisplayed[i][0]) + str(self.itemstobedisplayed[i][3]) + ".jpg", size_hint=(None, None), size=(100, 100))
            item_label = Label(
                text=str(self.itemstobedisplayed[i][0]) + "\n\n\n£" + str(self.itemstobedisplayed[i][1]) + "\nStore " + str(Shopdict[self.itemstobedisplayed[i][3]]) + "\nstock left: " + str(self.itemstobedisplayed[i][2]),
                size_hint=(0.5, 1),
                valign="middle",
                halign="left",
                color=[0, 0, 0, 1]
            )
            item_label.bind(size=item_label.setter('text_size'))

            add_button = Button(
                text="Add",
                size_hint=(None, None),
                size=(80, 40),
                background_normal='',
                background_color=[0.2, 0.8, 0.2, 1],
                color=[1, 1, 1, 1]
            )
            add_button.bind(on_release=lambda instance, item=(self.itemstobedisplayed[i]): self.add_to_basket(item))

            item_container.add_widget(item_image)
            item_container.add_widget(item_label)
            item_container.add_widget(add_button)

            self.item_layout.add_widget(item_container)

    def execute_search(self, instance):
        search_query = self.search_input.text.strip()
        Shopdict = {"Store A": 1, "Store B": 2, "Store C": 3, "ALL": 0, "Select Store": 0, "":0}
        self.itemstobedisplayed = backend.selectfromdatabase(search_query, Shopdict[self.dropdown.main_button.text])
        self.refresh_items()  # Refresh the items displayed in the UI

    def add_to_basket(self, item):
        Shopdict = {1: "A", 2:"B", 3:"C",}
        self.basket.append("name")
        self.basket.append(str(item[0]))
        self.basket.append("£" + str(item[1]))
        self.basket.append(str(item[2]))
        self.basket.append(Shopdict[item[3]])
        #print(f"Added to basket: {item}")

    def select_store(self, btn):
        self.dropdown.main_button.text = btn.text
        self.dropdown.dismiss()

    def open_basket(self, instance):
        basket_layout = BoxLayout(orientation='vertical', spacing=30, padding=10)

        with basket_layout.canvas.before:
            self.bg_color = Color(*self.theme_color)
            self.bg_rect = Rectangle(size=basket_layout.size, pos=basket_layout.pos)
        basket_layout.bind(
            size=lambda _, size: setattr(self.bg_rect, 'size', size),
            pos=lambda _, pos: setattr(self.bg_rect, 'pos', pos)
        )
        
        table_layout = GridLayout(cols = 4, spacing = 5, size_hint_y = None)
        table_layout.bind(minimum_height = table_layout.setter('height'))


        if self.basket:
            filter_button_layout = BoxLayout(orientation = 'horizontal', size_hint_y= None, height = 40,spacing = 10)
            spacer = Label(size_hint_x = 1)
            filter_dropdown = DropDown()
            filter_options = ["by Price", "by Your Order"]
            for option in filter_options:
                filter_button = Button(
                    text = option,
                    size_hint_y = None,
                    height = 40,
                    background_normal ='',
                    background_color = [0.8,0.8,0.8,1],
                    color = [0,0,0,1]
                )
                filter_button.bind(on_release = lambda btn: self.apply_filter(btn.text, filter_dropdown))
                filter_dropdown.add_widget(filter_button)
            
            filter_button = Button(
                text = "Filter By",
                size_hint =(None,1),
                height = 40,
                width = 150,
                background_normal = '',
                background_color = [0.2,0.6,0.8,1],
                color = [1,1,1,1],
            )
            filter_button.bind(on_release = filter_dropdown.open)
            filter_button_layout.add_widget(spacer)
            filter_button_layout.add_widget(filter_button)
            basket_layout.add_widget(filter_button_layout)


            headings = ["Student Name", "Product Name", "Price", "Quantity"]
            for heading in headings:
                table_layout.add_widget(Label(
                    text = heading,
                    bold = True, 
                    size_hint_y = None,
                    height = 30,
                    color = [0,0,0,1]
                ))

            for item in self.basket:
                product_name = item
                table_layout.add_widget(Label(
                    text = product_name,
                    size_hint_y = None,
                    height = 30,
                    color = [0,0,0,1]
                ))
            
            
        else:
            basket_layout.add_widget(Label(text="Your basket is empty", size_hint_y=None, height=30, color = [0,0,0,1]))

        scroll_view = ScrollView(size_hint = (1, 0.6))
        scroll_view.add_widget(table_layout)
        basket_layout.add_widget(scroll_view)

        if self.basket:
            cost_layout = BoxLayout(orientation = 'horizontal', spacing = 10, size_hint_y = None, height = 40)
            cost_layout.add_widget(Label(
                text = f"Household Cost: ",
                size_hint_x = 0.5,
                color = [0,0,0,1]
            ))
            cost_layout.add_widget(Label(
                text = f"Your Cost: ",
                size_hint_x = 0.5,
                color = [0,0,0,1]
            ))
            basket_layout.add_widget(cost_layout)

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
    def apply_filter(self, filter_type, dropdown):
        dropdown.dismiss()
        print(f"filtered {filter_type}")
        
    def select_filter(self, btn, dropdown):
        dropdown.parent.parent.children[-1].text = btn.text
        self.itemstobedisplayed = sorted(self.itemstobedisplayed, key=lambda x: x[1])
        if dropdown.parent.parent.children[-1].text == "Price: High to Low":
            self.itemstobedisplayed = self.itemstobedisplayed[::-1]
        self.refresh_items()
        dropdown.dismiss()


if __name__ == "__main__":
    setup()
    MainApp().run()

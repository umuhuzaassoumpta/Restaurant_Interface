import tkinter as tk
from tkinter import ttk, messagebox

class RestaurantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Ordering System")
        self.root.geometry("600x600")
        self.root.configure(bg="skyblue")

        self.menu = {
            "Appetizers": {"Spring Rolls": 500, "Garlic Bread": 450, "Bruschetta": 600},
            "Main Course": {"Grilled Chicken": 1200, "Steak": 1800, "Pasta": 1000},
            "Drinks": {"Coke": 250, "Orange Juice": 300, "Coffee": 3000}
        }

        self.main_frame = tk.Frame(root, bg="Lavender")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_ui()

    def create_ui(self):
        
        self.title_label = tk.Label(self.main_frame, 
                                    text="Welcome to Our Restaurant", 
                                    font=("Arial", 18, "bold"), 
                                    bg="skyblue", 
                                    fg="black")
        self.title_label.pack(pady=10)

        category_label = tk.Label(self.main_frame, 
                                  text="Select Category:", 
                                  bg="Lavender", 
                                  fg="black", 
                                  font=("Arial", 12))
        category_label.pack(pady=(15, 5))

        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(self.main_frame, 
                                              textvariable=self.category_var, 
                                              values=list(self.menu.keys()), 
                                              state="readonly",
                                              width=40, height=5.)
        self.category_dropdown.pack(pady=5)
        self.category_dropdown.bind("<<ComboboxSelected>>", self.update_menu)

        food_label = tk.Label(self.main_frame, 
                              text="Select Food Item:", 
                              bg="Lavender", 
                              fg="black", 
                              font=("Arial", 12))
        food_label.pack(pady=(10, 5))

        self.food_var = tk.StringVar()
        self.food_dropdown = ttk.Combobox(self.main_frame, 
                                          textvariable=self.food_var, 
                                          values=[], 
                                          state="readonly",
                                          width=40)
        self.food_dropdown.pack(pady=5)

        quantity_label = tk.Label(self.main_frame, 
                                  text="Quantity:", 
                                  bg="Lavender", 
                                  fg="black", 
                                  font=("Arial", 14))
        quantity_label.pack(pady=(10, 5))

        self.quantity_var = tk.IntVar(value=1)
        self.quantity_spinbox = ttk.Spinbox(self.main_frame, 
                                            from_=1, 
                                            to=10, 
                                            textvariable=self.quantity_var,
                                            width=5)
        self.quantity_spinbox.pack(pady=5)

        order_button = tk.Button(self.main_frame, 
                                 text="Add to Order", 
                                 font=("Arial", 14, "bold"), 
                                 bg="white", 
                                 fg="black", 
                                 command=self.add_to_order)
        order_button.pack(pady=15)


        self.summary_frame = tk.Frame(self.main_frame, bg="white", bd=2, relief="ridge")
        self.summary_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.summary_label = tk.Label(self.summary_frame, 
                                      text="Order Summary", 
                                      font=("Arial", 15, "bold"), 
                                      bg="white",
                                      fg="black")
        self.summary_label.pack(pady=5)

        
        self.listbox_frame = tk.Frame(self.summary_frame, bg="black")
        self.listbox_frame.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        self.summary_scrollbar = tk.Scrollbar(self.listbox_frame)
        self.summary_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.order_listbox = tk.Listbox(self.listbox_frame, height=8, width=50, font=("Arial", 10), 
                                        bg="white", fg="black", yscrollcommand=self.summary_scrollbar.set)
        self.order_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.summary_scrollbar.config(command=self.order_listbox.yview)

       
        self.total_label = tk.Label(self.summary_frame, 
                                    text="Total: $0.00", 
                                    font=("Arial", 15, "bold"), 
                                    bg="white", 
                                    fg="red")
        self.total_label.pack(pady=5)

        self.place_order_button = tk.Button(self.main_frame, 
                                            text="Place Order", 
                                            font=("Arial", 19, "bold"), 
                                            bg="green", 
                                            fg="white", 
                                            command=self.place_order)
        self.place_order_button.pack(pady=5)

        self.clear_order_button = tk.Button(self.main_frame, 
                                            text="Clear Order", 
                                            font=("Arial", 19), 
                                            bg="firebrick", 
                                            fg="white",
                                            
                                            command=self.clear_order)
        self.clear_order_button.pack(pady=5)

        self.order_list = []

    def update_menu(self, event):
       
        category = self.category_var.get()
        if category in self.menu:
            self.food_dropdown["values"] = list(self.menu[category].keys())
            if self.menu[category]:
                self.food_dropdown.current(0)

    def add_to_order(self):
   
        category = self.category_var.get()
        food = self.food_var.get()
        quantity = self.quantity_var.get()

        if not food or not category:
            messagebox.showerror("Error", "Please select a food item!")
            return

        price = self.menu[category][food] * quantity
        self.order_list.append((food, quantity, price))
        self.update_summary()

    def update_summary(self):
        
        self.order_listbox.delete(0, tk.END)  
        total_price = 0

        for item, qty, price in self.order_list:
            self.order_listbox.insert(tk.END, f"{qty} x {item} - ${price:.2f}")
            total_price += price

        self.total_label.config(text=f"Total: ${total_price:.2f}")

    def place_order(self):
       
        if not self.order_list:
            messagebox.showerror("Error", "Your order is empty!")
            return

        receipt = "Receipt:\n"
        total_price = 0

        for item, qty, price in self.order_list:
            receipt += f"{qty} x {item} - ${price:.2f}\n"
            total_price += price

        receipt += f"\nTotal Amount: ${total_price:.2f}\nThank you for dining with us!"
        messagebox.showinfo("Order Placed", receipt)
        self.clear_order()

    def clear_order(self):
        
        self.order_list.clear()
        self.order_listbox.delete(0, tk.END)
        self.total_label.config(text="Total: $0.00")

if __name__ == "__main__":
    root = tk.Tk()
    app = RestaurantApp(root)  
    root.mainloop()
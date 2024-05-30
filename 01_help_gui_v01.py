import tkinter as tk
from tkinter import messagebox
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.configure(bg="#f0f0f0")

        self.help_button = tk.Button(self.root, text="Help", command=self.display_help, bg="#FFD700", fg="#333333", font=("Arial", 12))
        self.help_button.pack(pady=10)


    def display_help(self):
        help_text = ("Welcome to the Currency Converter!\n\n"
                     "1. Select the 'From Currency' and 'To Currency' from the dropdown menus.\n"
                     "2. Enter the amount you want to convert in the 'Amount' field.\n"
                     "3. Click the 'Convert' button to see the conversion result.\n\n"
                     "Thank you for using our Currency Converter!")
        messagebox.showinfo("Help", help_text)

root = tk.Tk()
app = CurrencyConverterApp(root)
root.mainloop()

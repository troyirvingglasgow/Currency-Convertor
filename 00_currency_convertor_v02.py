import tkinter as tk
from tkinter import messagebox

# Fixed exchange rates
exchange_rates = {'NZD': {'USD': 0.68, 'CAD': 0.86},
                  'USD': {'NZD': 1.47, 'CAD': 1.27},
                  'CAD': {'NZD': 1.17, 'USD': 0.79}}

# Button colors
BUTTON_COLOR = "#4CAF50"  # Green
HELP_BUTTON_COLOR = "#FFD700"  # Gold

class HelpWindow(tk.Toplevel):
    def __init__(self, master=None, parent=None):
        super().__init__(master)
        self.title("Help")
        self.geometry("450x250")
        self.configure(bg="#f0f0f0")

        self.parent = parent

        self.help_text = ("Welcome to the Currency Converter!\n\n"
                          "1. Select the 'From Currency' and 'To Currency' from the menus.\n"
                          "2. Enter the amount you want to convert in the 'Amount' field.\n"
                          "3. Click the 'Convert' button to see the conversion result.\n\n"
                          "Thank you for using our Currency Converter!")

        centered_text = '\n'.join(f"{' '*((0-len(line))//2)}{line}{' '*((100-len(line))//2)}" for line in self.help_text.split('\n'))

        self.text_widget = tk.Text(self, wrap="word", bg="#f0f0f0", fg="#333333", font=("Arial", 12))
        self.text_widget.insert(tk.END, centered_text)
        self.text_widget.config(state="disabled")
        self.text_widget.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.back_button = tk.Button(self, text="Back", command=self.close_help, bg="#FFD700", fg="#333333", font=("Arial", 12))
        self.back_button.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        self.grid_rowconfigure(0, weight=1)  # Make the text widget expandable
        self.grid_columnconfigure(0, weight=1)  # Make the back button expandable

    def close_help(self):
        self.parent.deiconify()  # Show the parent window
        self.destroy()  # Close the help window



class CurrencyConverterApp:
    def display_help(self):
        self.root.withdraw()  # Hide the main window
        help_window = HelpWindow(self.root, parent=self.root)

    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")

        # Create Frames
        self.input_frame = tk.Frame(root, padx=10, pady=10)
        self.input_frame.grid(row=0, column=0)

        self.result_frame = tk.Frame(root, padx=10, pady=10)
        self.result_frame.grid(row=1, column=0)

        # Labels and Entry
        self.from_currency_label = tk.Label(self.input_frame, text="From Currency:")
        self.from_currency_label.grid(row=0, column=0, padx=5, pady=5)

        self.from_currency_var = tk.StringVar()
        self.from_currency_menu = tk.OptionMenu(self.input_frame, self.from_currency_var, *exchange_rates.keys())
        self.from_currency_menu.grid(row=0, column=1, padx=5, pady=5)
        self.from_currency_var.set("NZD")

        self.to_currency_label = tk.Label(self.input_frame, text="To Currency:")
        self.to_currency_label.grid(row=1, column=0, padx=5, pady=5)

        self.to_currency_var = tk.StringVar()
        self.to_currency_menu = tk.OptionMenu(self.input_frame, self.to_currency_var, *exchange_rates.keys())
        self.to_currency_menu.grid(row=1, column=1, padx=5, pady=5)
        self.to_currency_var.set("USD")

        self.amount_label = tk.Label(self.input_frame, text="Amount:")
        self.amount_label.grid(row=2, column=0, padx=5, pady=5)

        self.amount_entry = tk.Entry(self.input_frame)
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        # Convert Button
        self.convert_button = tk.Button(self.input_frame, text="Convert", command=self.convert_currency, bg=BUTTON_COLOR)
        self.convert_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Result Label
        self.result_label = tk.Label(self.result_frame, text="", padx=10, pady=10)
        self.result_label.pack()

        # Help Button
        self.help_button = tk.Button(self.root, text="Help", command=self.display_help,bg=HELP_BUTTON_COLOR)
        self.help_button.grid(row=2, column=0, padx=5, pady=5)


    def convert_currency(self):
        from_currency = self.from_currency_var.get()
        to_currency = self.to_currency_var.get()

        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount.")
            return

        if from_currency == to_currency:
            messagebox.showerror("Error", "Please select different currencies.")
            return

        converted_amount = amount * exchange_rates[from_currency][to_currency]
        self.result_label.config(text=f"{amount} {from_currency} equals {converted_amount:.2f} {to_currency}")


root = tk.Tk()
app = CurrencyConverterApp(root)
root.mainloop()

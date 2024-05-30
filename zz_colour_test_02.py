import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Updated exchange rates for 2024 (example values)
exchange_rates = {'NZD': {'USD': 0.60, 'CAD': 0.81},
                  'USD': {'NZD': 1.67, 'CAD': 1.36},
                  'CAD': {'NZD': 1.23, 'USD': 0.74}}

# Button colors
BUTTON_COLOR = "#004e98"
HELP_BUTTON_COLOR = "#004e98"

#Input Box Colours
INPUT_BOX_COLOUR = "#004e98"
class HelpWindow(tk.Toplevel):
    def __init__(self, master=None, parent=None):
        super().__init__(master)
        self.title("Help")
        self.geometry("520x230")
        self.configure(bg="#353535")

        self.parent = parent

        self.help_text = ("Welcome to the Currency Converter!\n\n"
                          "1. Select the 'From Currency' and 'To Currency' from the menus.\n"
                          "2. Enter the amount you want to convert in the 'Amount' field.\n"
                          "3. Click the 'Convert' button to see the conversion result.\n\n"
                          "Thank you for using our Currency Converter!")

        centered_text = '\n'.join(f"{' '*((0-len(line))//2)}{line}{' '*((100-len(line))//2)}" for line in self.help_text.split('\n'))

        self.text_widget = tk.Text(self, wrap="word", bg="#ffffff", fg="#353535", font=("Arial", 12, "bold"))
        self.text_widget.insert(tk.END, centered_text)
        self.text_widget.config(state="disabled")
        self.text_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.back_button = tk.Button(self, text="Back", command=self.close_help, bg="#004e98", fg="#ffffff", font=("Arial", 12, "bold"))
        self.back_button.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

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
        self.root.configure(bg="#ffffff")  # Set background color for the entire window
        # Create Frames
        self.input_frame = tk.Frame(root, padx=10, pady=10, bg="#ffffff")
        self.input_frame.grid(row=0, column=0)

        self.result_frame = tk.Frame(root, padx=10, pady=10, bg="#ffffff")
        self.result_frame.grid(row=1, column=0)

        # Labels and Entry
        self.from_currency_label = tk.Label(self.input_frame, text="From Currency:", fg="#353535",
                                            font=("Arial", 12, "bold"), bg="#ffffff")
        self.from_currency_label.grid(row=0, column=0, padx=5, pady=5)

        self.from_currency_var = tk.StringVar()
        self.from_currency_menu = ttk.Combobox(self.input_frame, textvariable=self.from_currency_var,
                                                values=list(exchange_rates.keys()), style="My.TCombobox")
        self.from_currency_menu.grid(row=0, column=1, padx=5, pady=5)
        self.from_currency_var.set("NZD")

        self.to_currency_label = tk.Label(self.input_frame, text="To Currency:", fg="#353535",
                                          font=("Arial", 12, "bold"), bg="#ffffff")
        self.to_currency_label.grid(row=1, column=0, padx=5, pady=5)

        self.to_currency_var = tk.StringVar()
        self.to_currency_menu = ttk.Combobox(self.input_frame, textvariable=self.to_currency_var,
                                              values=list(exchange_rates.keys()), style="My.TCombobox")
        self.to_currency_menu.grid(row=1, column=1, padx=5, pady=5)
        self.to_currency_var.set("USD")

        self.amount_label = tk.Label(self.input_frame, text="Amount:", bg="#ffffff",  font=("Arial", 12, "bold"))
        self.amount_label.grid(row=2, column=0, padx=5, pady=5)

        self.amount_entry = tk.Entry(self.input_frame, bg="#ffffff")
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        # Convert Button
        self.convert_button = tk.Button(self.input_frame, text="Convert", command=self.convert_currency,
                                        bg=BUTTON_COLOR, fg="#ffffff", font=("Arial", 12, "bold"))
        self.convert_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Result Label
        self.result_label = tk.Label(self.result_frame, text="", padx=10, pady=10, fg="#353535",
                                      font=("Arial", 16, "bold"), bg="#ffffff")
        self.result_label.pack()

        # Help Button
        self.help_button = tk.Button(self.root, text="Help", command=self.display_help,
                                     bg=HELP_BUTTON_COLOR, fg="#ffffff", font=("Arial", 12, "bold"))
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

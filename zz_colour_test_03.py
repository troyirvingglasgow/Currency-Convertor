import math
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import re

# Updated exchange rates for 2024 (example values)
exchange_rates = {'NZD': {'USD': 0.60, 'CAD': 0.81},
                  'USD': {'NZD': 1.67, 'CAD': 1.36},
                  'CAD': {'NZD': 1.23, 'USD': 0.74}}

# Button colors
BUTTON_COLOR = "#a8dadc"  # Light blue
HELP_BUTTON_COLOR = "#457b9d"  # Dark blue

# Input Box Colours
INPUT_BOX_COLOUR = "#f1faee"  # Light green

class HelpWindow(tk.Toplevel):
    def __init__(self, master=None, parent=None):
        super().__init__(master)
        self.title("Help")
        self.geometry("500x260")
        self.configure(bg="#1d3557")  # Dark blue background

        self.parent = parent

        self.help_text = ("Welcome to the Currency Converter!\n\n"
                          "1. Select the 'From Currency' and 'To Currency' from the menus.\n"
                          "2. Enter the amount you want to convert in the 'Amount' field.\n"
                          "3. Click the 'Convert' button to see the conversion result.\n\n"
                          "Thank you for using our Currency Converter!")

        centered_text = '\n'.join(f"{' '*((0-len(line))//2)}{line}{' '*((100-len(line))//2)}" for line in self.help_text.split('\n'))

        self.text_widget = tk.Text(self, wrap="word", bg="#a8dadc", fg="#1d3557", font=("Arial", 12, "bold"))
        self.text_widget.insert(tk.END, centered_text)
        self.text_widget.config(state="disabled")
        self.text_widget.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.back_button = tk.Button(self, text="Back", command=self.close_help, bg="#a8dadc", fg="#1d3557", font=("Arial", 12, "bold"))
        self.back_button.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        self.grid_rowconfigure(0, weight=1)  # Make the text widget expandable
        self.grid_columnconfigure(0, weight=1)  # Make the back button expandable

    def close_help(self):
        self.parent.deiconify()  # Show the parent window
        self.destroy()  # Close the help window


class HistoryExport:
    def __init__(self, parent, history):
        self.parent = parent
        self.history = history
        self.filename = ""

        self.history_window = tk.Toplevel(parent)
        self.history_window.title("Conversion History")
        self.history_window.geometry("300x500")
        self.history_window.configure(bg="#1d3557")  # Dark blue background

        # Previous conversions label
        previous_conversions_label = tk.Label(self.history_window, text="Previous Conversions", bg="#1d3557", fg="#a8dadc",
                                              font=("Arial", 12, "bold"))
        previous_conversions_label.pack(pady=(10, 5))

        # Create a Listbox to display history entries
        self.history_listbox = tk.Listbox(self.history_window, selectmode=tk.MULTIPLE, font=("Arial", 10), bg="#a8dadc")
        self.history_listbox.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Add history entries to the Listbox
        for entry in self.history:
            self.history_listbox.insert(tk.END, entry)

        # Add a button to add selected history entries to a file
        add_to_file_button = tk.Button(self.history_window, text="Export to File", command=self.add_to_file,
                                       bg="#a8dadc", fg="#1d3557", font=("Arial", 12, "bold"))
        add_to_file_button.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(10, 20))

        # Add a back button
        back_button = tk.Button(self.history_window, text="Back", command=self.close_history,
                                bg="#a8dadc", fg="#1d3557", font=("Arial", 12, "bold"))
        back_button.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(0, 10))

    def add_to_file(self):
        selected_indices = self.history_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("No Selection", "Please select entries to add to the file.")
            return

        selected_entries = [self.history_listbox.get(index) for index in selected_indices]

        # Write selected conversions to the file
        if not self.filename:
            self.filename = "conversion_history.txt"

        # Message to be added at the top of the file
        message = "Here Are The Selected Conversion's:\n\n"

        with open(self.filename, "a") as file:
            file.write(message)  # Write the message at the top of the file

            for entry in selected_entries:
                file.write(entry + "\n")

        messagebox.showinfo("File Updated", "Selected conversion history has been added to the file.")

    def close_history(self):
        self.history_window.destroy()  # Close the history window
        self.parent.deiconify()  # Show the main window


class CurrencyConverterApp:
    def display_help(self):
        self.root.withdraw()  # Hide the main window
        help_window = HelpWindow(self.root, parent=self.root)

    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.configure(bg="#1d3557")  # Dark blue background
        # Create Frames
        self.input_frame = tk.Frame(root, padx=10, pady=10, bg="#1d3557")  # Dark blue background
        self.input_frame.grid(row=0, column=0)

        self.result_frame = tk.Frame(root, padx=10, pady=10, bg="#1d3557")  # Dark blue background
        self.result_frame.grid(row=1, column=0)

        # Labels and Entry
        self.from_currency_label = tk.Label(self.input_frame, text="From Currency:", fg="#a8dadc",
                                            font=("Arial", 12, "bold"), bg="#1d3557")  # Dark blue background
        self.from_currency_label.grid(row=0, column=0, padx=5, pady=5)

        self.from_currency_var = tk.StringVar()
        self.from_currency_menu = ttk.Combobox(self.input_frame, textvariable=self.from_currency_var,
                                                values=list(exchange_rates.keys()), style="My.TCombobox")
        self.from_currency_menu.grid(row=0, column=1, padx=5, pady=5)
        self.from_currency_var.set("NZD")

        self.to_currency_label = tk.Label(self.input_frame, text="To Currency:", fg="#a8dadc",
                                          font=("Arial", 12, "bold"), bg="#1d3557")  # Dark blue background
        self.to_currency_label.grid(row=1, column=0, padx=5, pady=5)

        self.to_currency_var = tk.StringVar()
        self.to_currency_menu = ttk.Combobox(self.input_frame, textvariable=self.to_currency_var,
                                              values=list(exchange_rates.keys()), style="My.TCombobox")
        self.to_currency_menu.grid(row=1, column=1, padx=5, pady=5)
        self.to_currency_var.set("USD")

        self.amount_label = tk.Label(self.input_frame, text="Amount:", foreground="#a8dadc", bg="#1d3557", font=("Arial", 12, "bold"))  # Dark blue background
        self.amount_label.grid(row=2, column=0, padx=5, pady=5)

        self.amount_entry = tk.Entry(self.input_frame, bg="#a8dadc")  # Light blue background
        self.amount_entry.grid(row=2, column=1, padx=5, pady=5)

        # Result Label
        self.result_label = tk.Label(self.result_frame, text="", padx=10, pady=10, fg="#a8dadc",
                                     font=("Arial", 16, "bold"), bg="#1d3557")  # Dark blue background
        self.result_label.pack()
        # Convert Button
        self.convert_button = tk.Button(self.input_frame, text="Convert", command=self.convert_currency,
                                        bg=BUTTON_COLOR, fg="#1d3557", font=("Arial", 12, "bold"))  # Light blue button
        self.convert_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # Help Button
        self.help_button = tk.Button(self.root, text="Help", command=self.display_help,
                                     bg=BUTTON_COLOR, fg="#1d3557", font=("Arial", 12, "bold"))  # Dark blue button
        self.help_button.grid(row=2, column=0, padx=5, pady=(0, 5), sticky='ew')

        # History Button
        self.history_button = tk.Button(self.root, text="History", command=self.display_history,
                                        bg=BUTTON_COLOR, fg="#1d3557", font=("Arial", 12, "bold"))  # Light blue button
        self.history_button.grid(row=3, column=0, padx=5, pady=(0, 5), sticky='ew')
        # Initialize history list
        self.history = []

    def convert_currency(self):
        from_currency = self.from_currency_var.get()
        to_currency = self.to_currency_var.get()
        amount = self.amount_entry.get().strip()

        if not amount:
            messagebox.showerror("Error", "Amount field cannot be empty!")
            self.amount_entry.config(bg="#e63946")  # Red background
            return

        try:
            amount = float(amount)
            self.amount_entry.config(bg=INPUT_BOX_COLOUR)  # Light green background
            if amount <= 0 or math.copysign(1, amount) == 0:
                raise ValueError("Amount must be above 0!")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.amount_entry.config(bg="#e63946")  # Red background
            return

        if from_currency == to_currency:
            messagebox.showerror("Error", "Please select different currencies.")
            self.amount_entry.config(bg="#e63946")  # Red background
            return

        converted_amount = amount * exchange_rates[from_currency][to_currency]
        self.result_label.config(text=f"{amount} {from_currency} equals {converted_amount:.2f} {to_currency}")

        # Append the conversion result to the history list
        history_entry = f"{amount} {from_currency} equals {converted_amount:.2f} {to_currency}"
        self.history.append(history_entry)

    def display_history(self):
        self.root.withdraw()  # Hide the main window
        history_export = HistoryExport(self.root, self.history)

root = tk.Tk()
app = CurrencyConverterApp(root)
root.mainloop()

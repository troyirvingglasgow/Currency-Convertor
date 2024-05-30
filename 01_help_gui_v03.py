from tkinter import messagebox
import tkinter as tk


class HelpWindow(tk.Toplevel):
    def __init__(self, master=None, parent=None):
        super().__init__(master)
        self.title("Help")
        self.geometry("500x260")
        self.configure(bg="#bc6c25")

        self.parent = parent

        self.help_text = ("Welcome to the Currency Converter!\n\n"
                          "1. Select the 'From Currency' and 'To Currency' from the menus.\n"
                          "2. Enter the amount you want to convert in the 'Amount' field.\n"
                          "3. Click the 'Convert' button to see the conversion result.\n\n"
                          "Thank you for using our Currency Converter!")

        centered_text = '\n'.join(f"{' '*((0-len(line))//2)}{line}{' '*((100-len(line))//2)}" for line in self.help_text.split('\n'))

        self.text_widget = tk.Text(self, wrap="word", bg="#fefae0", fg="#361d18", font=("Arial", 12, "bold"))
        self.text_widget.insert(tk.END, centered_text)
        self.text_widget.config(state="disabled")
        self.text_widget.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.back_button = tk.Button(self, text="Back", command=self.close_help, bg="#fefae0", fg="#361d18", font=("Arial", 12, "bold"))
        self.back_button.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        self.grid_rowconfigure(0, weight=1)  # Make the text widget expandable
        self.grid_columnconfigure(0, weight=1)  # Make the back button expandable

    def close_help(self):
        self.parent.deiconify()  # Show the parent window
        self.destroy()  # Close the help window


class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.configure(bg="#f0f0f0")

        self.help_button = tk.Button(self.root, text="Help", command=self.display_help, bg="#FFD700", fg="#333333", font=("Arial", 12))
        self.help_button.pack(pady=10)

    def display_help(self):
        self.root.withdraw()  # Hide the main window
        help_window = HelpWindow(self.root, parent=self.root)

root = tk.Tk()
app = CurrencyConverterApp(root)
root.mainloop()
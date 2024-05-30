import tkinter as tk

class HelpWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Help")
        self.geometry("400x300")
        self.configure(bg="#f0f0f0")

        self.help_text = ("Welcome to the Currency Converter!\n\n"
                          "1. Select the 'From Currency' and 'To Currency' from the dropdown menus.\n"
                          "2. Enter the amount you want to convert in the 'Amount' field.\n"
                          "3. Click the 'Convert' button to see the conversion result.\n\n"
                          "Thank you for using our Currency Converter!")

        centered_text = '\n'.join(f"{' '*((40-len(line))//2)}{line}{' '*((40-len(line))//2)}" for line in self.help_text.split('\n'))

        self.text_widget = tk.Text(self, wrap="word", bg="#f0f0f0", fg="#333333", font=("Arial", 12), padx=20, pady=20)
        self.text_widget.insert(tk.END, centered_text)
        self.text_widget.config(state="disabled")
        self.text_widget.pack(expand=True, fill="both")

class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.configure(bg="#f0f0f0")

        self.help_button = tk.Button(self.root, text="Help", command=self.display_help, bg="#FFD700", fg="#333333", font=("Arial", 12))
        self.help_button.pack(pady=10)

    def display_help(self):
        help_window = HelpWindow(self.root)

root = tk.Tk()
app = CurrencyConverterApp(root)
root.mainloop()

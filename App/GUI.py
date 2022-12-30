import tkinter as tk


class GUI:

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("GUI")
        self.window.geometry("500x500")
        self.window.resizable(False, False)
        self.window.configure(bg="black")
        self.window.mainloop()

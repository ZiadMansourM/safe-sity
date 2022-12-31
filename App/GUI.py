import tkinter as tk
from guiOptions import *
from checkFine import CheckFine
from PIL import ImageTk, Image 

class GUI:

    root: tk.Tk
    canvas: tk.Canvas
    labelWidth: int

    lincesePlateLabel : tk.Label
    governmentLabel : tk.Label
    cityLabel : tk.Label
    streetLabel : tk.Label
    answerLabel : tk.Label

    lincesePlateEntry : tk.Entry

    governmentOptions: tk.OptionMenu
    citiesOptions: tk.OptionMenu
    streetsOptions: tk.OptionMenu

    governmentSelected: tk.StringVar
    citiesSelected: tk.StringVar
    streetsSelected: tk.StringVar

    imageView: tk.PhotoImage

    imageViewFlag: bool

    submitButton: tk.Button

    checker: CheckFine
    def __init__(self, width: int, height: int):
        
        self.checker = CheckFine('fineDetails.json')
        self.imageViewFlag = False

        self.intializeGUI(width, height)
        self.labelWidth = 200

        self.lincesePlateLabel = self.addLabel(60, 40, "Lincese Plate: ")
        self.lincesePlateEntry = self.addEntry(210, 40, "Lincese Plate: ")

        self.governmentLabel = self.addLabel(60, 80, "Government: ")
        self.governmentSelected = tk.StringVar(self.root)
        self.governmentSelected.set(governments[0])
        self.governmentOptions = self.addOptionMenu(210, 80, self.governmentSelected, governments, self.governmentSelect)

        self.cityLabel = self.addLabel(60, 120, "City: ")
        self.citiesSelected = tk.StringVar(self.root)
        self.citiesSelected.set(cities[0])
        self.citiesOptions = self.addOptionMenu(210, 120, self.citiesSelected, cities, self.citySelect)

        self.streetLabel = self.addLabel(60, 160, "Street: ")
        self.streetsSelected = tk.StringVar(self.root)
        self.streetsSelected.set(streets[0])
        self.streetsOptions = self.addOptionMenu(210, 160, self.streetsSelected, streets)

        self.submitButton = self.addButton(210, 200, "Submit", self.submit)
        self.answerLabel = self.addLabel(210, 800, "")

        #self.imageView = self.addImage(300, 350, "image.png")

        self.root.mainloop()

    def intializeGUI(self, canvasWidth: int, canvasHeight: int):
        self.root = tk.Tk()
        self.root.title("Fine Checker")
        self.canvas = tk.Canvas(self.root, width=canvasWidth, height=canvasHeight)
        self.canvas.pack()

    def addLabel(self, positionX: int, positionY: int, labelName: str):
        label = tk.Label(self.root, text=labelName, wraplength=self.labelWidth)
        self.canvas.create_window(positionX, positionY, window=label)
        return label

    def addEntry(self, positionX: int, positionY: int, entryName: str):
        entry = tk.Entry(self.root)
        self.canvas.create_window(positionX, positionY, window=entry)
        return entry

    def addOptionMenu(self, positionX: int, positionY: int, stringVar ,options: list, callback = None):
        optionMenu = tk.OptionMenu(self.root, stringVar, *options, command=callback)
        self.canvas.create_window(positionX, positionY, window=optionMenu, width=self.labelWidth)
        return optionMenu

    def governmentSelect(self, value):

        self.citiesOptions.destroy()
        cities = list(options[value].keys())
        self.citiesSelected.set(cities[0])
        self.citiesOptions = self.addOptionMenu(210, 120, self.citiesSelected, cities, self.citySelect)

        self.citySelect(cities[0])
        
    def citySelect(self, val):
        self.streetsOptions.destroy()
        streets = list(options[self.governmentSelected.get()][val])
        self.streetsSelected.set(streets[0])
        self.streetsOptions = self.addOptionMenu(210, 160, self.streetsSelected, streets)

    def addButton(self, positionX: int, positionY: int, buttonName: str, callback):
        button = tk.Button(self.root, text=buttonName, command=callback)
        self.canvas.create_window(positionX, positionY, window=button)
        return button
    
    def addImage(self, positionX: int, positionY: int, imageName: str):
        image = Image.open(imageName)
        image.resize((50, 50), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(positionX, positionY, image=photo)
        return photo

    def submit (self):
        if self.lincesePlateEntry.get() == "":
            self.answerLabel.config(text="Please Enter Lincese Plate")
            if self.imageViewFlag:
                self.imageView.destroy()
                self.imageViewFlag = False
        
        else:
            image= self.checker.checkFine(self.lincesePlateEntry.get(), self.governmentSelected.get(), self.citiesSelected.get(), self.streetsSelected.get())

            if image:
                if self.imageViewFlag:
                    pass
                    self.imageView.destroy()
                
                self.imageView = self.addImage(500, 500, image)
                self.imageViewFlag = True
                self.answerLabel.config(text=image)
                self.answerLabel.config(text="This is a picture of the car with the license plate at the location you entered")

            else:
                self.answerLabel.config(text="License Plate not found, fine will be removed")
                if self.imageViewFlag:
                    self.imageView.destroy()
                    self.imageViewFlag = False
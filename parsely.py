import os
import traceback
from tkinter import *
from tkinter import scrolledtext, messagebox
from tkinter import filedialog
from tkinter import ttk
from operators import *


class App:
    colum_width = 20
    colum_height = 201

    def __init__(self):
        self.root = Tk()

        # create textinputs and make them auto-resizing
        self.rawInput = scrolledtext.ScrolledText(self.root, width=App.colum_width, height=App.colum_height, wrap=NONE)
        self.rawInput.grid(column=0, row=0, sticky='news')

        self.pythonInput = scrolledtext.ScrolledText(self.root, width=App.colum_width, height=App.colum_height,
                                                     wrap=NONE)
        self.pythonInput.grid(column=1, row=0, sticky='news')

        self.parsedOutput = scrolledtext.ScrolledText(self.root, width=App.colum_width, height=App.colum_height,
                                                      wrap=NONE)
        self.parsedOutput.grid(column=2, row=0, sticky='news')

        # Set grid sizing
        self.root.columnconfigure(tuple(range(3)), weight=1)

        menu = Menu(self.root)

        # Set Title and Icon
        icon = PhotoImage(file='icon.png')
        self.root.iconphoto(False, icon)
        self.root.iconbitmap("favicon.ico")
        self.root.title("parsely")
        # grid firstRow

        self.insertMenu = Menu(menu)
        menu.add_cascade(label="Insert", menu=self.insertMenu)
        self.insertMenu.add_command(label="Copy from Clipboard",
                                    command=lambda: self.setRawInput(self.getFromClipBoard()))
        self.insertMenu.add_command(label="Open File", command=self.loadRawInputFromFile)

        self.scriptMenu = Menu(menu)
        menu.add_cascade(label="Script", menu=self.scriptMenu)
        self.scriptMenu.add_command(label="Save Script", command=self.savePythonInput)
        self.scriptMenu.add_command(label="Open Script", command=self.loadScriptFromFile)

        self.outputMenu = Menu(menu)
        menu.add_cascade(label="Output", menu=self.outputMenu)
        self.outputMenu.add_command(label="Save Output", command=self.saveParsedOutput)
        self.outputMenu.add_command(label="Copy to Clipboard ",
                                    command=lambda: self.copyToClipBoard(self.getFromOutput()))

        menu.add_command(label="> Run", command=lambda: self.parse(self.getFromRawInput(), self.getFromPythonInput()))

        self.root.config(menu=menu)
        self.root.mainloop()

    DEFAULT_PATH = "C:\Code\Python\parsely\scripts"

    def loadFromFile(self):
        with filedialog.askopenfile(mode='r', initialdir=App.DEFAULT_PATH, filetypes=[('All Files', '*.*')]) as file:
            if file is not None:
                content = file.readlines()
                return ''.join(content)
        return

    def loadRawInputFromFile(self):
        loaded = self.loadFromFile()
        if loaded is not None:
            self.setRawInput(loaded)

    def loadScriptFromFile(self):
        loaded = self.loadFromFile()
        if loaded is not None:
            self.setPythonInput(loaded)

    # initialdir=os.getcwd()
    def saveFile(self, text, defaultFileName, ending=tuple(("all files", "*.*"))):
        with filedialog.asksaveasfile(mode='w', initialfile=defaultFileName, initialdir=App.DEFAULT_PATH,
                                      filetypes=ending) as file:
            if file is not None:
                file.writelines(text)

    def savePythonInput(self):
        self.saveFile(self.getFromPythonInput(), "script.parsely",
                      (("Parsely File", "*.parsely"), ('Text File', '*.txt')))

    def saveParsedOutput(self):
        self.saveFile(self.getFromOutput(), 'output.txt', (("All Files", "*.*"), ('Text File', '*.txt')))

    def copyToClipBoard(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    def getFromPythonInput(self):
        return self.pythonInput.get('1.0', END)

    def getFromRawInput(self):
        return self.rawInput.get('1.0', END)

    def getFromOutput(self):
        return self.parsedOutput.get('1.0', END)

    def getFromClipBoard(self):
        return self.root.clipboard_get()

    def setRawInput(self, text):
        self.rawInput.delete('0.0', END)
        self.rawInput.insert("0.0", text)

    def setPythonInput(self, text):
        self.pythonInput.delete('0.0', END)
        self.pythonInput.insert("0.0", text)

    def writeToOutput(self, text):
        self.parsedOutput.delete('0.0', END)
        self.parsedOutput.insert('0.0', text)

    def parse(self, text, script):
        try:
            compiler = self.getCompiler(script)

            if not compiler:
                messagebox.showerror("Script is empty", "Script is empty")
                return
            lines = text.split('\n')[:-1]

            for operation in compiler:
                lines = operation(lines)

            self.writeToOutput('\n'.join(lines))
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", str(e))

    def getCompiler(self, script):
        parsedScript = [line for line in script.split('\n') if line.strip()]  # remove empty lines in between

        compiledScripts = list()
        for operation, successful in Operations.getOperations(
                parsedScript):  # get the user input and makes a function out of it
            if successful:
                compiledScripts.append(operation)
            else:
                return False
        return compiledScripts


if __name__ == '__main__':
    App()

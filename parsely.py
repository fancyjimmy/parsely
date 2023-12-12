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
        self.rawInput.grid(column=0, row=1, sticky='news')

        self.pythonInput = scrolledtext.ScrolledText(self.root, width=App.colum_width, height=App.colum_height,
                                                     wrap=NONE)
        self.pythonInput.grid(column=1, row=1, sticky='news')

        self.parsedOutput = scrolledtext.ScrolledText(self.root, width=App.colum_width, height=App.colum_height,
                                                      wrap=NONE)
        self.parsedOutput.grid(column=2, row=1, sticky='news')

        # Set grid sizing
        self.root.columnconfigure(tuple(range(3)), weight=1)
        self.root.rowconfigure(0, weight=1, minsize=30)
        self.root.rowconfigure(1, weight=5)

        # Set Title and Icon
        icon = PhotoImage(file = 'icon.png')
        self.root.iconphoto(False, icon)
        self.root.iconbitmap("favicon.ico")
        self.root.title("parsely")
        # grid firstRow
        self.header = [Frame(self.root) for _ in range(0, 3)]
        for index, frame in enumerate(self.header):
            frame.grid(row=0, column=index)

        # first column
        Button(self.header[0], text='insert from clipboard',
               command=lambda: self.setRawInput(self.getFromClipBoard())).pack(side=LEFT)
        Button(self.header[0], text='load from file ',
               command=self.loadRawInputFromFile).pack(side=LEFT)

        # second column
        Button(self.header[1], text='format',
               command=lambda: self.parse(self.getFromRawInput(), self.getFromPythonInput())).pack(side=LEFT)

        Button(self.header[1], text='save script',
               command=self.savePythonInput).pack(side=TOP)

        Button(self.header[1], text='load script',
               command=self.loadScriptFromFile).pack(side=TOP)

        # third column
        Button(self.header[2], text='copy to clipboard',
               command=lambda: self.copyToClipBoard(self.getFromOutput())).pack(side=LEFT)

        Button(self.header[2], text='save to file',
               command=self.saveParsedOutput).pack(side=LEFT)
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


    #initialdir=os.getcwd()
    def saveFile(self, text, defaultFileName, ending=tuple(("all files", "*.*"))):
        with filedialog.asksaveasfile(mode='w', initialfile=defaultFileName, initialdir=App.DEFAULT_PATH,
                                      filetypes=ending) as file:
            if file is not None:
                file.writelines(text)

    def savePythonInput(self):
        self.saveFile(self.getFromPythonInput(), "script.parsely", (("Parsely File", "*.parsely"), ('Text File', '*.txt')))

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
                messagebox.showerror("Script line wasn't found", "Script line wasn't found")
                return
            lines = text.split('\n')

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

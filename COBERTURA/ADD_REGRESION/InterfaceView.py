from tkinter import *
from tkinter import filedialog
import DesignStart
import setupPathFiles
import process
class Application():
    def __init__(self, master):
        frame = Frame(master,width=3000,height=3000)
        frame.pack()

        self.insert_file_path_btn = Button(frame, text="Carpeta", command=self.selectLogFile, width=18)
        self.insert_file_path_btn.grid(row=200,column=1)
        self.qc_start_proccess_btn = Button(frame,text="Ejecutar",command=self.start, width=18)
        self.qc_start_proccess_btn.grid(row=2000,column=1)



        self.logFilePathMessage =StringVar()
        self.labelMessage = Label(frame,textvariable=self.logFilePathMessage)
        self.labelMessage.grid(row=2050,column=1)

        self.logFilePath =StringVar()
        self.label = Label(frame,textvariable=self.logFilePath)
        self.label.grid(row=100,column=1)

    def selectLogFile(self):
        filename = filedialog.askdirectory()
        self.logFilePath.set(filename)


    def start(self):
     if self.logFilePath.get():
        paths=setupPathFiles.setupPaths(self.logFilePath.get())
        dgs = DesignStart.DesignStart(paths)
        process.startProcess(dgs)

     else:
        self.logFilePathMessage.set("Seleccione la Carpeta Resources")


if __name__=="__main__":

    root = Tk()
    root.title("Match team(trans.,soporte)")
    root.geometry("500x400+410+180")
    root.grid_anchor(anchor="nw")
    app = Application(root)
root.mainloop()

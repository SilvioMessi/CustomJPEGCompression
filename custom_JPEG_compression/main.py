from tkinter import Tk

from custom_JPEG_compression.guiUtils import GUIManager

_ = lambda s: s

class Application:
    def __init__(self, root):
        self.guiManger = GUIManager(self, root)
        self.guiManger.mainView()

if __name__ == '__main__':
    root = Tk()
    root.geometry('{}x{}'.format(root.winfo_screenwidth(), 600))
    root.title(_("METHODS OF SCIENTIFIC COMPUTING"))
    Application(root)
    root.mainloop()

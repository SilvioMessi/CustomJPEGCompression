from tkinter import * 
from tkinter import messagebox
from PIL import ImageTk
from tkinter.filedialog import askopenfilename

from custom_JPEG_compression.imgUtils import CompressionCore

_ = lambda s: s

class GUIManager:

    def __init__(self, application, root):
        self.application = application
        self.compressionCore = CompressionCore()
        self.root = root
        self.frame = Frame(self.root)
        self.frame.pack(expand=1, fill=BOTH)
        self.qualityValue = IntVar()
        self.qualityValue.trace("w", callback=self.qualityValueChanged)
        self.NValue = IntVar()
        self.NValue.trace("w", callback=self.NValueChanged)
        self.originalImageZoom = IntVar()
        self.originalImageZoom.set(1)
        self.copressedImageZoom = IntVar()
        self.copressedImageZoom.set(1)

    def qualityValueChanged(self, *args):
        try :
            qualityValue = self.qualityValue.get()
            if qualityValue < 1:
                raise Exception
        except Exception:
            self.qualityValue.set(1)

    def NValueChanged(self, *args):
        try :
            NValue = self.NValue.get()
            if NValue < 1:
                raise Exception
            self.compressionCore.imageSquaring(N=NValue)
            self.drawImage(original=True, zoom=False)
        except Exception:
            self.NValue.set(1)

    def mainView(self): 
        # original image frame
        self.originalImageFrame = Frame(self.frame)
        self.originalImageFrame.pack(expand=1, fill=BOTH, padx=5, pady=5, side=LEFT)
        self.originalImageLabelFrame = LabelFrame(self.originalImageFrame, text=_("Original image"))
        self.originalImageLabelFrame.pack(expand=1, fill=BOTH, padx=5, pady=5)
        self.originalImageContainerFrame = Frame(self.originalImageLabelFrame)
        self.originalImageContainerFrame.pack(expand=1, fill=BOTH)  
        self.originalImageLabel = Label(self.originalImageContainerFrame, text=_("Original image not yet loaded.") + 
                                                                                "\n" + 
                                                                                _("Please press ") + 
                                                                                "\"" + 
                                                                                _("Load image") + 
                                                                                "\"" + 
                                                                                _(" button in options frame."))
        self.originalImageLabel.pack()
        self.originalImageVBar = Scrollbar(self.originalImageContainerFrame, orient=VERTICAL)
        self.originalImageHBar = Scrollbar(self.originalImageContainerFrame, orient=HORIZONTAL)
        self.originalImageCanvas = None

        # options frame
        self.optionsFrame = Frame(self.frame)
        self.optionsFrame.pack(expand=1, fill=BOTH, padx=5, pady=5, side=LEFT)
        self.optionsLabelFrame = LabelFrame(self.optionsFrame, text=_("Options"))
        self.optionsLabelFrame.pack(expand=1, fill=BOTH, padx=5, pady=5)
        self.openFileButton = Button(self.optionsLabelFrame, text=_("Load image"), command=lambda: self.fileDialog())
        self.openFileButton.pack()
        self.NValueFrame = Frame(self.optionsLabelFrame, height=20, width=200)
        self.NValueFrame.pack(padx=5, pady=5)
        self.NValueFrame.pack_propagate(0)
        self.NValueLabel = Label(self.NValueFrame, text=_("N") + ":")
        self.NValueLabel.pack(anchor=W, side=LEFT)
        self.NValueSpinbox = Spinbox(self.NValueFrame, textvariable=self.NValue, from_=1, to=1000, state=DISABLED)
        self.NValueSpinbox.pack(anchor=W, side=LEFT)
        self.qualityValueFrame = Frame(self.optionsLabelFrame, height=20, width=200)
        self.qualityValueFrame.pack(padx=5, pady=5)
        self.qualityValueFrame.pack_propagate(0)
        self.qualityValueLabel = Label(self.qualityValueFrame, text=_("Quality") + ":")
        self.qualityValueLabel.pack(anchor=W, side=LEFT)
        self.qualityValueSpinbox = Spinbox(self.qualityValueFrame, textvariable=self.qualityValue, from_=1, to=100, state=DISABLED)
        self.qualityValueSpinbox.pack(anchor=W, side=LEFT)
        self.compressImageButton = Button(self.optionsLabelFrame, text=_("Compress image"), command=lambda: self.compressImage(), state=DISABLED)
        self.compressImageButton.pack()

        # compressed image frame
        self.compressedImageFrame = Frame(self.frame)
        self.compressedImageFrame.pack(expand=1, fill=BOTH, padx=5, pady=5, side=LEFT)
        self.compressedImageLabelFrame = LabelFrame(self.compressedImageFrame, text=_("Compressed image"))
        self.compressedImageLabelFrame.pack(expand=1, fill=BOTH, padx=5, pady=5)
        self.compressedImageContainerFrame = Frame(self.compressedImageLabelFrame)
        self.compressedImageContainerFrame.pack(expand=1, fill=BOTH)
        self.compressedImageLabel = Label(self.compressedImageContainerFrame, text=_("Original image not yet loaded."))
        self.compressedImageLabel.pack()  
        self.compressedImageVBar = Scrollbar(self.compressedImageContainerFrame, orient=VERTICAL)
        self.compressedImageHBar = Scrollbar(self.compressedImageContainerFrame, orient=HORIZONTAL)
        self.compressedImageCanvas = None

    def fileDialog(self, fileOptions=None, mode='r', openMode=True):
        if fileOptions is None:
            fileOptions = {}
            fileOptions['defaultextension'] = ''
            fileOptions['filetypes'] = []
            fileOptions['initialdir'] = ''
            fileOptions['initialfile'] = ''
            fileOptions['parent'] = self.root
            fileOptions['title'] = ''
        if openMode is True:
            file = askopenfilename(**fileOptions)
            if file is not None and file is not '':
                try :
                    self.compressionCore.openImage(file)
                    self.compressionCore.imageSquaring(self.NValue.get())
                except Exception:
                    messagebox.showerror(
                            _("Error"),
                            "It's impossible open the image.")
                    return 
                self.updateGUI(original=True)
   
    def updateGUI(self, original=True):
        if original is True:
            if self.originalImageCanvas is None:
                self.originalImageCanvas = Canvas(self.originalImageContainerFrame)
                self.originalImageLabel.pack_forget()
                self.compressedImageLabel.config(text=_("Please set N and Quality values and press ") + 
                                                        "\n" + 
                                                        "\"" + 
                                                        _("Compress image") + 
                                                        "\"" + 
                                                        _(" button in options frame."))
                self.qualityValueSpinbox.config(state=NORMAL)
                self.NValueSpinbox.config(state=NORMAL)
                self.compressImageButton.config(state=NORMAL)
                self.originalImageScale = Scale(self.originalImageLabelFrame, variable=self.originalImageZoom, from_=1, to=10, orient=HORIZONTAL)
                self.originalImageScale.bind("<ButtonRelease-1>", lambda x:self.updateImageZoom(True))
                self.originalImageScale.pack()
            self.originalImageZoom.set(1)
            self.NValue.set(1)
        else:
            if self.compressedImageCanvas is None:
                self.compressedImageCanvas = Canvas(self.compressedImageContainerFrame)
                self.compressedImageLabel.pack_forget()
                self.compressedImageScale = Scale(self.compressedImageLabelFrame, variable=self.copressedImageZoom, from_=1, to=10, orient=HORIZONTAL)
                self.compressedImageScale.bind("<ButtonRelease-1>", lambda x:self.updateImageZoom(False))
                self.compressedImageScale.pack()
            self.copressedImageZoom.set(1)            
        self.drawImage(original=original, zoom=False)

    def drawImage(self, original=True, zoom=False,):
        if original is True:
            canvas = self.originalImageCanvas
            imageHBar = self.originalImageHBar
            imageVBar = self.originalImageVBar
            if zoom is False:
                image = self.compressionCore.squareImage
            else:
                image = self.compressionCore.imageZoom(self.originalImageZoom.get(), original=True)
        else: 
            canvas = self.compressedImageCanvas
            imageHBar = self.compressedImageHBar
            imageVBar = self.compressedImageVBar
            if zoom is False:
                image = self.compressionCore.compressedImage
            else:
                image = self.compressionCore.imageZoom(self.copressedImageZoom.get(), original=False)
        image = ImageTk.PhotoImage(image)  
        canvas.delete("all") 
        imageHBar.pack(side=BOTTOM, fill=X)
        imageHBar.config(command=canvas.xview)
        imageVBar.pack(side=RIGHT, fill=Y)
        imageVBar.config(command=canvas.yview)
        canvas.config(scrollregion=(0, 0, image.width(), image.height()),
                                    yscrollcommand=imageVBar.set,
                                    xscrollcommand=imageHBar.set) 
        canvas.create_image(0, 0, image=image, anchor="nw")
        if original is True:
            self.compressionCore.squareImageReference = image
        else:
            self.compressionCore.compressedImageReference = image
        canvas.pack(expand=1, fill=BOTH)

    def updateImageZoom(self, original):
        if original is True:
            self.drawImage(original=True, zoom=True)
        else:
            self.drawImage(original=False, zoom=True)

    def compressImage(self):
        self.compressionCore.compressImage()
        self.updateGUI(original=False)

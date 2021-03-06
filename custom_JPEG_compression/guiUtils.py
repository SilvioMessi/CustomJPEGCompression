from tkinter import * 
from tkinter import messagebox
from PIL import ImageTk
from tkinter.filedialog import askopenfilename, asksaveasfilename

from imgUtils import CompressionCore

_ = lambda s: s

class GUIManager:

    def __init__(self, application, root):
        self.application = application
        self.compressionCore = CompressionCore()
        self.root = root
        self.frame = Frame(self.root)
        self.frame.pack(expand=1, fill=BOTH)
        self.qualityValue = IntVar()
        self.qualityValue.set(50)
        self.NValue = IntVar()
        self.NValue.set(1)
        self.originalImageZoom = IntVar()
        self.originalImageZoom.set(0)
        self.compressedImageZoom = IntVar()
        self.compressedImageZoom.set(0)

    def qualityValueChanged(self, *args):
        qualityValue = self.qualityValue.get()
        self.qualityValueLabel.config(text=_("Quality : {}".format(qualityValue)))

    def NValueChanged(self, *args):
        NValue = self.NValue.get()
        self.NValueLabel.config(text=_("N : {}".format(NValue)))
        if self.compressionCore.originalImage is not None:
            self.compressionCore.imageSquaring(N=NValue)
            self.drawImage(original=True, zoom=False)

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
        self.openImageButton = Button(self.optionsLabelFrame, text=_("Load image"), command=lambda: self.fileDialog())
        self.openImageButton.pack()
        self.imagesSizeFrame = LabelFrame(self.optionsLabelFrame, text=_("Images size"))
        self.infoMessage = Message(self.imagesSizeFrame, width=400, anchor=W)
        self.infoMessage.pack(fill=X)
        self.NAndQualityFrame = LabelFrame(self.optionsLabelFrame, text=_("Compression parameters"))
        self.NValueLabel = Label(self.NAndQualityFrame)
        self.NValueLabel.pack()
        self.NValueScale = Scale(self.NAndQualityFrame, variable=self.NValue, from_=1, to=200, orient=HORIZONTAL, showvalue=False)
        self.NValueScale.pack(fill=X, padx=10, pady=10)
        self.NValueScale.bind("<ButtonRelease-1>", self.NValueChanged)
        self.NValueChanged()  # update scale label
        self.qualityValueLabel = Label(self.NAndQualityFrame)
        self.qualityValueLabel.pack()
        self.qualityValueScale = Scale(self.NAndQualityFrame, variable=self.qualityValue, from_=1, to=100, orient=HORIZONTAL, showvalue=False)
        self.qualityValueScale.pack(fill=X, padx=10, pady=10)
        self.qualityValueScale.bind("<ButtonRelease-1>", self.qualityValueChanged)
        self.qualityValueChanged()  # update scale label
        self.compressImageButton = Button(self.optionsLabelFrame, text=_("Compress image"), command=lambda: self.compressImage())
        self.saveImageButton = Button(self.optionsLabelFrame, text=_("Save compressed image"), command=lambda: self.fileDialog(mode='w', fileOptions={'defaultextension' : 'bmp'}, openMode=False))

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
        defaultFileOptions = {}
        defaultFileOptions['defaultextension'] = ''
        defaultFileOptions['filetypes'] = []
        defaultFileOptions['initialdir'] = ''
        defaultFileOptions['initialfile'] = ''
        defaultFileOptions['parent'] = self.root
        defaultFileOptions['title'] = ''
        if fileOptions is not None:
            for key in fileOptions:
                defaultFileOptions[key] = fileOptions[key]
        if openMode is True:
            file = askopenfilename(**defaultFileOptions)
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
        else:
            file = asksaveasfilename(**defaultFileOptions)
            if file is not None and file is not '':
                try:
                    self.compressionCore.compressedImage.save(fp=file, format="bmp")
                except Exception:
                    messagebox.showwarning(
                        _("Error"),
                        "Fail to save compressed image. Please try again.")
   
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
                self.originalImageScaleLabel = Label(self.originalImageLabelFrame)
                self.originalImageScaleLabel.pack()
                self.originalImageScale = Scale(self.originalImageLabelFrame, variable=self.originalImageZoom, from_=-5, to=5, orient=HORIZONTAL, showvalue=False)
                self.originalImageScale.bind("<ButtonRelease-1>", lambda x:self.updateImageZoom(True))
                self.originalImageScale.pack()
                self.imagesSizeFrame.pack(fill=BOTH, padx=10, pady=10)
                self.NAndQualityFrame.pack(fill=BOTH, padx=10, pady=10)
                self.compressImageButton.pack()
        else:
            if self.compressedImageCanvas is None:
                self.compressedImageCanvas = Canvas(self.compressedImageContainerFrame)
                self.compressedImageLabel.pack_forget()
                self.compressedImageScaleLabel = Label(self.compressedImageLabelFrame)
                self.compressedImageScaleLabel.pack()
                self.compressedImageScale = Scale(self.compressedImageLabelFrame, variable=self.compressedImageZoom, from_=-5, to=5, orient=HORIZONTAL, showvalue=False)
                self.compressedImageScale.bind("<ButtonRelease-1>", lambda x:self.updateImageZoom(False))
                self.compressedImageScale.pack()
                self.saveImageButton.pack()
        self.drawImage(original=original, zoom=False)

    def drawImage(self, original=True, zoom=False):
        self.updateInfoMessage()
        if original is True:
            canvas = self.originalImageCanvas
            imageHBar = self.originalImageHBar
            imageVBar = self.originalImageVBar
            if zoom is False:
                self.originalImageZoom.set(0)
                self.updateZoomLabel(original)
                image = self.compressionCore.squareImage
            else:
                image = self.compressionCore.imageZoom(self.originalImageZoom.get(), original=True)
        else: 
            canvas = self.compressedImageCanvas
            imageHBar = self.compressedImageHBar
            imageVBar = self.compressedImageVBar
            if zoom is False:
                self.compressedImageZoom.set(0)
                self.updateZoomLabel(original)
                image = self.compressionCore.compressedImage
            else:
                image = self.compressionCore.imageZoom(self.compressedImageZoom.get(), original=False)
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
        self.updateZoomLabel(original)
        if original is True:
            self.drawImage(original=True, zoom=True)
        else:
            self.drawImage(original=False, zoom=True)

    def updateZoomLabel(self, original):
        if original is True:
            label = self.originalImageScaleLabel
            zoomValue = self.originalImageZoom.get()
        else:
            label = self.compressedImageScaleLabel
            zoomValue = self.compressedImageZoom.get()
        if zoomValue == 0:
            label.config(text=_("Original size"))
        elif zoomValue > 0:
            label.config(text=_("Zoom in x{}".format(zoomValue + 1)))
        else:
            label.config(text=_("Zoom out x{}".format(abs(zoomValue) + 1)))

    def updateInfoMessage(self):
        text = ''
        originalImage = self.compressionCore.originalImage
        squaredImage = self.compressionCore.squareImage
        compressedImage = self.compressionCore.compressedImage
        if originalImage is not None:
            text = text + _("Original image size: {}x{} \n").format(*originalImage.size)
        if squaredImage is not None:
            text = text + _("Completed image size: {}x{} \n").format(*squaredImage.size)
        if compressedImage is not None:
            text = text + _("Compressed image size: {}x{} \n").format(*compressedImage.size)
        self.infoMessage.config(text=text)

    def compressImage(self):
        self.compressionCore.compressImage(self.qualityValue.get())
        self.updateGUI(original=False)

from tkinter import * 
from PIL import Image, ImageTk

from tkinter.filedialog import askopenfilename

_ = lambda s: s

class GUIManager:

    def __init__(self, application, root):
        self.application = application
        self.root = root
        self.frame = Frame(self.root)
        self.frame.pack(expand=1, fill=BOTH)
        self.qualityValue = IntVar()
        self.NValue = IntVar()
        self.originalImageZoom = IntVar()
        self.originalImageZoom.set(1)

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
            if file is not None:
                self.originalImage = Image.open(file)
                
                # L (8-bit pixels, black and white) it's different from take the Red band of RGB
                # self.originalImage = self.originalImage.convert(mode="L")
                width, height = self.originalImage.size
                # take the Red band of RGB
                self.pixels = list(self.originalImage.getdata(band=0))
                self.pixels = [self.pixels[i * width:(i + 1) * width] for i in range(height)]
                # print a sample
                print (self.pixels[0])
                
                if self.originalImageCanvas is None:
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
                    self.originalImageCanvas = Canvas(self.originalImageContainerFrame)
                    self.originalImageHBar = Scrollbar(self.originalImageContainerFrame, orient=HORIZONTAL)
                    self.originalImageHBar.pack(side=BOTTOM, fill=X)
                    self.originalImageHBar.config(command=self.originalImageCanvas.xview)
                    self.originalImageVBar = Scrollbar(self.originalImageContainerFrame, orient=VERTICAL)
                    self.originalImageVBar.pack(side=RIGHT, fill=Y)
                    self.originalImageVBar.config(command=self.originalImageCanvas.yview)
                    self.originalImageCanvas.pack(expand=1, fill=BOTH)
                    self.originalImageScale = Scale(self.originalImageLabelFrame, variable=self.originalImageZoom, from_=1, to=10, orient=HORIZONTAL, command=self.updateOrginalImage)
                    self.originalImageScale.pack()
                    # self.draw() called by updateOrginalImage
                else:
                    self.originalImageZoom.set(1)
                    self.originalImageCanvas.delete("all")
                    self.draw()

    def compressImage(self):
        self.compressedImage = ImageTk.PhotoImage(self.originalImage)
        if self.compressedImageCanvas is None:
            self.compressedImageLabel.pack_forget()
            self.compressedImageCanvas = Canvas(self.compressedImageContainerFrame)
            self.compressedImageHBar = Scrollbar(self.compressedImageContainerFrame, orient=HORIZONTAL)
            self.compressedImageHBar.pack(side=BOTTOM, fill=X)
            self.compressedImageHBar.config(command=self.compressedImageCanvas.xview)
            self.compressedImageVBar = Scrollbar(self.compressedImageContainerFrame, orient=VERTICAL)
            self.compressedImageVBar.pack(side=RIGHT, fill=Y)
            self.compressedImageVBar.config(command=self.compressedImageCanvas.yview)
            self.compressedImageCanvas.pack(expand=1, fill=BOTH)
        else:
            self.compressedImageCanvas.delete("all")
        self.compressedImageCanvas.config(scrollregion=(0, 0, self.compressedImage.width(), self.compressedImage.height()),
                                        yscrollcommand=self.compressedImageVBar.set,
                                        xscrollcommand=self.compressedImageHBar.set) 
        self.compressedImageCanvas.create_image(0, 0, image=self.compressedImage, anchor="nw")  
 
    def draw(self):
        iw, ih = self.originalImage.size
        size = int(iw * self.originalImageZoom.get()), int(ih * self.originalImageZoom.get())
        self.zoomedImage = ImageTk.PhotoImage(self.originalImage.resize(size))
        self.originalImageCanvas.config(scrollregion=(0, 0, self.zoomedImage.width(), self.zoomedImage.height()),
                                    yscrollcommand=self.originalImageVBar.set,
                                    xscrollcommand=self.originalImageHBar.set) 
        self.originalImageCanvas.create_image(0, 0, image=self.zoomedImage, anchor="nw")

    def updateOrginalImage(self, event):
        self.scale = self.originalImageZoom.get()
        self.draw()
from PIL import Image

STANDARD_JPEG_BLOCK_SIZE = 8 

class CompressionCore:

    def __init__(self):
        # original image
        self.originalImage = None
        self.originalImagePixels = None
        self.originalImageHeight = None
        self.originalImageWidth = None

        # square image
        self.squareImage = None
        self.squareImagePixels = None
        self.squareImageHeight = None
        self.squareImageWidth = None

    def openImage(self, path):
        try:
            self.originalImage = Image.open(path)
            self.getImagePixel()
        except Exception:
            self.originalImage = None
            self.originalImagePixels = None
            raise Exception

    def getImagePixel(self):
        self.originalImageWidth, self.originalImageHeight = self.originalImage.size
        # take the red band if the image use RGB. Evaluate if use convertImageToGrayscale method
        pixelsList = list(self.originalImage.getdata(band=0))
        self.originalImagePixels = [pixelsList[i * self.originalImageWidth:(i + 1) * self.originalImageWidth] for i in range(self.originalImageHeight)]

    def convertImageToGrayscale(self):
        # L (8-bit pixels, black and white)
        self.originalImage = self.originalImage.convert(mode="L")

    def imageSquaring(self, N=1):
        if N < 1:
            N = 1
        # list(self.originalImagePixels) it'very important! Create a COPY of original list
        self.squareImagePixels = list(self.originalImagePixels)
        blockSize = STANDARD_JPEG_BLOCK_SIZE * N 
        widthModulo = self.originalImageWidth % blockSize
        heigthModulo = self.originalImageHeight % blockSize
        if widthModulo != 0:
            reachBlockSize = blockSize - widthModulo
            for index, row in enumerate(self.originalImagePixels):
                self.squareImagePixels[index].extend([row[self.originalImageWidth - 1]] * reachBlockSize)
        if heigthModulo != 0:
            reachBlockSize = blockSize - heigthModulo
            for index in range(self.originalImageHeight, self.originalImageHeight + reachBlockSize):
                self.squareImagePixels.extend([self.originalImagePixels[self.originalImageHeight - 1]]) 
        self.squareImageHeight = len(self.squareImagePixels) 
        self.squareImageWidth = len(self.squareImagePixels[0])
        self.squareImage = Image.new("L", (self.squareImageHeight, self.squareImageWidth))
        self.squareImage.putdata([pixel for row in self.squareImagePixels for pixel in row])

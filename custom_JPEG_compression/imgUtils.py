from PIL import Image
import numpy as np

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
        
        # compressed image
        self.compressedImage = None
        self.compressedImagePixels = None
        self.compressedImageHeight = None
        self.compressedImageWidth = None
        
        self.blockSizeMoltiplicator = 1

    def openImage(self, path):
        try:
            self.originalImage = Image.open(path)
            self.originalImagePixels, self.originalImageWidth, self.originalImageWidth = self.getImagePixel(self.originalImage)
        except Exception:
            self.originalImage = None
            self.originalImagePixels = None
            raise Exception

    def getImagePixel(self, image):
        imageWidth, imageHeight = image.size
        # take the red band if the image use RGB. Evaluate if use convertImageToGrayscale method
        pixelsList = list(image.getdata(band=0))
        pixelsMatrix = [pixelsList[i * imageWidth:(i + 1) * imageWidth] for i in range(imageHeight)]
        return pixelsMatrix, imageWidth, imageHeight

    def convertImageToGrayscale(self, image):
        # L (8-bit pixels, black and white)
        return image.convert(mode="L")
    
    def splitImage(self, image, blockSize):
        imagePixelsMatrix, imageWidth, imageHeight = self.getImagePixel(image)
        imagePixelsMatrix = np.array(imagePixelsMatrix)
        assert (imageWidth % blockSize == 0)
        assert (imageHeight % blockSize == 0) 
        imageBlocksMatrix = []
        for heightIndex in range (0, imageHeight, blockSize):
            blocksRow =[]
            for widthIndex in range (0, imageWidth, blockSize):
                blocksRow.append(imagePixelsMatrix[heightIndex: heightIndex+blockSize, widthIndex: widthIndex+blockSize])
            imageBlocksMatrix.append(blocksRow)
        return imageBlocksMatrix
   
    def imageSquaring(self, N=1):
        if N < 1:
            N = 1
        self.blockSizeMoltiplicator = N
        self.squareImagePixels, width, height = self.getImagePixel(self.originalImage)
        blockSize = STANDARD_JPEG_BLOCK_SIZE * self.blockSizeMoltiplicator
        widthModulo = width % blockSize
        heigthModulo = height % blockSize
        if widthModulo != 0:
            reachBlockSize = blockSize - widthModulo
            for row in self.squareImagePixels:
                row.extend([row[width - 1]] * reachBlockSize)
        if heigthModulo != 0:
            reachBlockSize = blockSize - heigthModulo
            for _ in range(height, height + reachBlockSize):
                self.squareImagePixels.extend([self.squareImagePixels[height - 1]]) 
        self.squareImageHeight = len(self.squareImagePixels) 
        self.squareImageWidth = len(self.squareImagePixels[0])
        self.squareImage = Image.new("L", (self.squareImageWidth, self.squareImageHeight))
        self.squareImage.putdata([pixel for row in self.squareImagePixels for pixel in row])

    def imageZoom(self, zoom=1, original=True):
        if zoom < 1 or zoom > 10:
            zoom = 1
        if original is True:
            image = self.squareImage
        else:
            image = self.compressedImage
        iw, ih = image.size
        size = int(iw * zoom) , int(ih * zoom)
        return image.resize(size)

    def compressImage(self):
        blockSize = STANDARD_JPEG_BLOCK_SIZE * self.blockSizeMoltiplicator
        self.imageBlocksMatrix = self.splitImage(self.squareImage, blockSize)
        self.compressedImage = Image.new("L", (blockSize, blockSize))
        self.compressedImage.putdata([pixel for row in self.imageBlocksMatrix[0][0] for pixel in row])

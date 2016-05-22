from PIL import Image
import numpy as np
import scipy.fftpack

STANDARD_JPEG_BLOCK_SIZE = 8 
Q_MATRIX = np.asarray([[16, 11, 10, 16, 24, 40, 51, 61],
                        [12, 12, 14, 19, 26, 58, 60, 55],
                        [14, 13, 16, 24, 40, 57, 69, 56],
                        [14, 17, 22, 29, 51, 87, 80, 62],
                        [18, 22, 37, 56, 68, 109, 103, 77],
                        [24, 35, 55, 64, 81, 104, 113, 92],
                        [49, 64, 78, 87, 103, 121, 120, 101],
                        [72, 92, 95, 98, 112, 100, 103, 99]])

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
            self.originalImagePixels = self.getImagePixel(self.originalImage)
            self.originalImageWidth, self.originalImageHeight = self.originalImagePixels.shape
        except Exception:
            self.originalImage = None
            self.originalImagePixels = None
            raise Exception

    def getImagePixel(self, image):
        imageWidth, imageHeight = image.size
        # take the red band if the image use RGB. Evaluate if use convertImageToGrayscale method
        pixelsArray = np.asarray(image.getdata(band=0))
        pixelsMatrix = pixelsArray.reshape(imageHeight, imageWidth)
        return pixelsMatrix

    def convertImageToGrayscale(self, image):
        # L (8-bit pixels, black and white)
        return image.convert(mode="L")

    def splitImage(self, image, blockSize):
        imagePixelsMatrix = self.getImagePixel(image)
        imageWidth, imageHeight = imagePixelsMatrix.shape
        assert (imageWidth % blockSize == 0)
        assert (imageHeight % blockSize == 0) 
        imageBlocksMatrix = []
        for heightIndex in range (0, imageHeight, blockSize):
            blocksRow = []
            for widthIndex in range (0, imageWidth, blockSize):
                blocksRow.append(imagePixelsMatrix[heightIndex: heightIndex + blockSize, widthIndex: widthIndex + blockSize])
            imageBlocksMatrix.append(blocksRow)
        return np.asarray(imageBlocksMatrix)

    def imageSquaring(self, N=1):
        if N < 1:
            N = 1
        self.blockSizeMoltiplicator = N
        self.squareImagePixels = self.getImagePixel(self.originalImage)
        height, width = self.squareImagePixels.shape
        blockSize = STANDARD_JPEG_BLOCK_SIZE * self.blockSizeMoltiplicator
        widthModulo = width % blockSize
        heigthModulo = height % blockSize
        self.squareImagePixels = self.squareImagePixels.tolist()
        if widthModulo != 0:
            reachBlockSize = blockSize - widthModulo
            for row in self.squareImagePixels:
                row.extend([row[width - 1]] * reachBlockSize)
        if heigthModulo != 0:
            reachBlockSize = blockSize - heigthModulo
            for _ in range(height, height + reachBlockSize):
                self.squareImagePixels.extend([self.squareImagePixels[height - 1]])
        self.squareImagePixels = np.asarray(self.squareImagePixels)
        self.squareImageHeight, self.squareImageWidth = self.squareImagePixels.shape
        self.squareImage = Image.new("L", (self.squareImageWidth, self.squareImageHeight))
        self.squareImage.putdata(self.squareImagePixels.flatten())

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

    def DCT2(self, pixelsMatrix):
        hight, width = pixelsMatrix.shape
        assert (hight == width)
        dct2PixelsMatrix = np.empty(shape=(hight, width))
        for rowIndex in range(0, hight):
            dct2PixelsMatrix[rowIndex, :] = self.DCT1(pixelsMatrix[rowIndex, :])
        for columIndex in range(0, width):
            dct2PixelsMatrix[ :, columIndex] = self.DCT1(dct2PixelsMatrix[:, columIndex])
        return dct2PixelsMatrix

    def DCT1(self, pixels): 
        return scipy.fftpack.dct(pixels, norm='ortho')

    def computeQualityFactor(self, quality): 
        if quality <= 0:
            quality = 1
        elif quality > 100:
            quality = 100
        if quality >= 50:
            qf = (200 - 2 * quality) / 100
        else:
            qf = (5000 / quality) / 100
        return qf

    def compute8X8QuantizationMaxtrix(self, quality):
        qf = self.computeQualityFactor(quality)
        Q1 = np.round(qf * np.array(Q_MATRIX))
        return Q1

    def compute8NX8NQuantizationMaxtrix(self, quality):
        originalQM = self.compute8X8QuantizationMaxtrix(quality)
        quantizationMatrix = np.zeros([STANDARD_JPEG_BLOCK_SIZE * self.blockSizeMoltiplicator, STANDARD_JPEG_BLOCK_SIZE * self.blockSizeMoltiplicator])
        matrixHeight, matrixWidth = originalQM.shape
        for heightIndex in range (0, matrixHeight):
            for widthIndex in range (0, matrixWidth):
                NheightIndex = heightIndex * self.blockSizeMoltiplicator
                NwidthIndex = widthIndex * self.blockSizeMoltiplicator
                quantizationMatrix[NheightIndex :NheightIndex + self.blockSizeMoltiplicator, NwidthIndex :NwidthIndex + self.blockSizeMoltiplicator] = originalQM[heightIndex, widthIndex]
        return quantizationMatrix

    def compressImage(self, quality):
        blockSize = STANDARD_JPEG_BLOCK_SIZE * self.blockSizeMoltiplicator
        self.imageBlocksMatrix = self.splitImage(self.squareImage, blockSize)
        self.compressedImage = Image.new("L", (blockSize, blockSize))
        self.compressedImage.putdata([pixel for row in self.imageBlocksMatrix[0, 0] for pixel in row])

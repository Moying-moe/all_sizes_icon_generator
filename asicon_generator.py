from PIL import Image
import struct


class SizeException(Exception):
    def __init__(self, errorInfo):
        super().__init__(self)
        self.errorInfo = errorInfo

    def __str__(self):
        return self.errorinfo



class ASIcon:
    def __init__(self, imageFilePath, sizeList=[16,32,64,128,256]):
        self.imgraw = Image.open(imageFilePath)
        self.sizeList = sizeList

        if self.imgraw.size[0] != self.imgraw.size[1]:
            raise SizeException('Expect square image, got image size: %s'%(img.size))

        for e in self.sizeList:
            if e <= 0 or e > 256:
                raise SizeError('illegal size in argument `sizeList`: %s'%e)
        self.sizeList.sort()

        self.generateIcon()

    def __getpixelByBitmapWay(self, imgp, size, x, y):
        pix = imgp[x, size-y-1]
        if pix[3] == 0:
            pix = (0,0,0,0)
        return pix

    def __generateMask(self, imgSize, imgp):
        bitmapImgMask = bytes()
        for y in range(imgSize):
            for x in range(0, imgSize, 8):
                pix = [self.__getpixelByBitmapWay(imgp, imgSize, _i, y)[3] for _i in range(x,x+8)]
                pix = sum(pix)//8
                bitmapImgMask += struct.pack(
                    r'B', pix
                )
        return bitmapImgMask

    def __imageToBitmap(self, img):
        if img.size[0] != img.size[1]:
            raise ValueError('img.size %s'%(img.size))
        
        imgSize = img.size[0]
        img = img.convert('RGBA')
        imgp = img.load()
        
        bitmapInfoHeader = struct.pack(
            r'IllHHIIllII',
            40, imgSize, imgSize*2,
            1, 32, 0, imgSize**2*4,
            0, 0, 0, 0
        )
        
        bitmapImgData = bytes()
        for y in range(imgSize):
            for x in range(imgSize):
                bitmapImgData += struct.pack(
                    r'BBBB',
                    *self.__getpixelByBitmapWay(imgp, imgSize, x, y)
                )

        bitmapImgMask = self.__generateMask(imgSize, imgp)
        
        return bitmapInfoHeader + bitmapImgData + bitmapImgMask

    def generateIcon(self):
        # file header
        iconHeader = struct.pack(
            r'HHH',
            0, 1, len(self.sizeList)
        )

        # bitmap datas
        bitmapDatas = []
        for nsize in self.sizeList:
            img = self.imgraw.resize((nsize,nsize), Image.ANTIALIAS)
            bitmapDatas.append(self.__imageToBitmap(img))

        iconEntries = []
        ptr = 6 + len(self.sizeList)*16
        for nsize, bitmapdata in zip(self.sizeList, bitmapDatas):
            if nsize == 256:
                nsize = 0
            datalen = len(bitmapdata)
            iconEntries.append(
                struct.pack(
                    r'BBBBHHII',
                    nsize, nsize, 0, 0,
                    1, 32, datalen, ptr
                )
            )
            ptr += datalen

        # packaging bytes datas
        self.fileBytes = iconHeader
        for e in iconEntries:
            self.fileBytes += e
        for e in bitmapDatas:
            self.fileBytes += e

        return True

    def save(self, savePath):
        try:
            f = open(savePath, 'wb')
        except OSError as e:
            raise OSError('Failed to open file `%s`'%(savePath))

        f.write(self.fileBytes)

        f.close()

if __name__ == "__main__":
    asi = ASIcon('./icon.png')
    asi.save('./test.ico')
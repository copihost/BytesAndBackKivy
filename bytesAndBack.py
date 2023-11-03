import os
import math
import hashlib


class BytesAndBack():
    def __init__(self):

        self.CHUNK_SIZE = 1048576
        self.barSize = 0
        self.filePath = ""
        self.progressPercent = 0
        self.destPath = ""

    def getPercent(self,listToUpdate):
        while self.progressPercent < 99:
            listToUpdate[0] = self.progressPercent

    def openFile(self, fPath: str):
        self.filePath = fPath
        if self.filePath:
            self.barSize = math.ceil(os.path.getsize(self.filePath) / 1048576)
        return self.filePath


    def openDest(self, dPath: str):
        if self.destPath:
            self.storagePath = self.destPath
        self.destPath = dPath

            



    def unpackFile(self, progressBarImport):
        fi = open(self.filePath, 'rb')
        chunk = fi.read(self.CHUNK_SIZE)
        iterations = 0
        while chunk: #loop until the chunk is empty (the file is exhausted)
            

            
            t2 = open(f"{self.destPath}/{iterations}", "wb")

            self.totalIterations = iterations
            t2.write(bytes(hashlib.md5(chunk).hexdigest(), encoding="utf-8"))
            if len(bytes(hashlib.md5(chunk).hexdigest(), encoding="utf-8")) != 32:
                print("hash did not equal 32 bytes wait for update for me to fix")
                exit()
            t2.write(chunk)
            t2.close()

            chunk = fi.read(self.CHUNK_SIZE) #read the next chunk
            iterations += 1
            self.progressPercent = int(round(iterations/self.barSize,2)*100)
            progressBarImport.value = self.progressPercent
            #progbar.value = self.progressPercent
            if self.progressPercent == 100:
                self.loopback = True
        fi.close()

    def packFile(self, progressBarImport):
        self.progressPercent = 0
        suffix = self.filePath.split('.')[-1]
        iterations = 0
        with open(f"{self.destPath}/final.{suffix}", "wb") as destFile:
            for entry in range(self.totalIterations+1):
                iterations += 1
                self.progressPercent = int(round(iterations/self.barSize,2)*100)
                progressBarImport.value = self.progressPercent
                with open(f"{self.storagePath}/{entry}", "rb") as cur_file:
                    hashBi = cur_file.read(32)
                    testBi = cur_file.read()
                    testBiFormatted = bytes(hashlib.md5(testBi).hexdigest(), encoding="utf-8")
                    if hashBi == testBiFormatted:
                        cur_file.seek(32)
                        destFile.write(cur_file.read())
                os.remove(f'{self.storagePath}/{entry}')

    def delFiles(self):
        for entry in range(self.totalIterations+1):
            os.remove(f'{self.storagePath}/{entry}')


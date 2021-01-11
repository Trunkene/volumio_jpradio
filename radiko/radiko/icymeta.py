# -*- config:utf-8 -*-

import math

class IcyMetadata():
    META_INT = 30000
    META_BLOCK_SIZE = 16
    MAX_LENGTH = META_BLOCK_SIZE * 255
    PADD_DATA = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    NO_METADATA = b'\x00'

    def __init__(
            self, metaInt=-1, bytesBeforeMeta=-1):
        self.metaInt = metaInt if metaInt > 0 else IcyMetadata.META_INT
        self.bytesBeforeMeta = bytesBeforeMeta if bytesBeforeMeta >= 0 else self.metaInt
        self.metaData = None
    
    def setStreamTitle(self, value):
        v = None
        if value:
            v = "StreamTitle='" + value + "';"
        self.metaData = v
    
    def getBufferedMetadata(self):
        if not (self.metaData and self.metaData.strip()):
            return IcyMetadata.NO_METADATA

        meta = bytes(self.metaData, encoding = 'utf-8')
        wlen = min(IcyMetadata.MAX_LENGTH, len(meta) + 1)
        metadataBlockSize = math.ceil(wlen / IcyMetadata.META_BLOCK_SIZE)
        metadataSize =  metadataBlockSize * IcyMetadata.META_BLOCK_SIZE
        result = bytearray(1 + metadataSize)
        result[0] = metadataBlockSize
        result[1:wlen] = meta[0:wlen - 1]
        pad = metadataSize + 1 - wlen
        if pad > 0:
            result[wlen:wlen+pad] =  IcyMetadata.PADD_DATA[0:pad]
        return bytes(result)

    def transform(self, chunk):
        chunkIndex = 0
        chunkLength = len(chunk)
        writtenLen = 0
        result = bytearray(chunkLength + IcyMetadata.MAX_LENGTH)
        if self.bytesBeforeMeta > 0:
            chunkIndex = min(self.bytesBeforeMeta, chunkLength)
            result[0:chunkIndex] = chunk[0:chunkIndex]
            writtenLen = chunkIndex
            self.bytesBeforeMeta -= chunkIndex

            if self.bytesBeforeMeta == 0:
                metaData = self.getBufferedMetadata()
                wlen = len(metaData)
                result[writtenLen:writtenLen + wlen] = metaData
                writtenLen += wlen
                self.bytesBeforeMeta = self.metaInt
        
        while (chunkIndex + self.metaInt) < chunkLength:
            result[writtenLen:writtenLen + self.metaInt] = chunk[chunkIndex: chunkIndex + self.metaInt]
            writtenLen += self.metaInt
            chunkIndex += self.metaInt

            metaData = self.getBufferedMetadata()
            wlen = len(metaData)
            result[writtenLen:writtenLen + wlen] = metaData
            writtenLen += wlen
            self.bytesBeforeMeta = self.metaInt
        if chunkIndex < chunkLength:
            wlen = chunkLength - chunkIndex
            result[writtenLen:writtenLen + wlen] = chunk[chunkIndex:chunkLength]
            writtenLen += wlen
            self.bytesBeforeMeta -= wlen
        if self.bytesBeforeMeta == 0:
            metaData = self.getBufferedMetadata()
            wlen = len(metaData)
            result[writtenLen:writtenLen + wlen] = metaData
            writtenLen += wlen
            self.bytesBeforeMeta = self.metaInt
        return bytes(result[0:writtenLen])
    
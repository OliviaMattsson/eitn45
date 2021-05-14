import collections
import HandIn1
import numpy as np
import heapq
import matplotlib.pyplot as plt


# By Olivia Mattsson
# I took inspiration from: https://bhrigu.me/post/huffman-coding-python-implementation/
# on how to perform the compresison in Python

class HuffmanCode:

    def __init__(self, heap, text):
        self.heap = heap
        self.probabilities = dict()
        self.occurances = dict()
        self.codes = dict()
        self.length = 0
        self._text = text
        self._IT = HandIn1.InfoTheory()

    def countProb(self):
        c = collections.Counter()
        with open('{}'.format(self._text), 'rt') as f:
            for line in f:
                c.update(line)
        with open('{}'.format(self._text), 'rt') as f:
            self.length = len(f.read())
        print('length of original file: {}'.format(self.length))
        for char in c.most_common(len(c)):
            self.occurances.update({char[0] : char[1]})
            self.probabilities.update({char[0] : (char[1]/self.length)})

    def Entropy(self):
        return self._IT.Entropy(np.array([list(self.probabilities.values())]))

    def makeHeap(self):
        for key in self.probabilities:
            leaf = HeapLeaf(key, self.probabilities[key])
            heapq.heappush(self.heap,leaf)
        
        while(len(self.heap) > 1):
            leaf1 = heapq.heappop(self.heap)
            leaf2 = heapq.heappop(self.heap)
            newLeaf = HeapLeaf(None, leaf1.prob + leaf2.prob)
            newLeaf.leftChild = leaf1
            newLeaf.rightChild = leaf2
            
            heapq.heappush(self.heap, newLeaf)

    def createCodes(self, root, current_code):
        if root == None:
            return
        if root.char != None:
            self.codes.update({root.char : current_code})
            return
        self.createCodes(root.leftChild, current_code + "0")
        self.createCodes(root.rightChild, current_code + "1")

    def encode(self):
        enc = ""
        with open('{}'.format(self._text), 'rt') as f:
            wholeText = f.read()
            for char in wholeText:
                enc += self.codes[char]
        return enc

    def pad(self, text):
        padding = 8 - len(text)% 8
        for nr in range(padding):
            text += "0"
        return text

    def printCodes(self):
        for key in sorted(self.probabilities):
            print("{0} : {2}: {1}".format(key, self.probabilities[key], key.encode('ascii')))
        print(len(self.probabilities))


    def printToFile(self, text, path):
        with open('{}'.format(path), 'w') as f:
            for code in (text[i:i+8] for i in range(0, len(text), 8)):
                f.write(str(int(code, 2)))
        return
    
    def toBytes(self, text):
        array = bytearray()
        for i in range(0, len(text), 8):
            byte = text[i:i+8]
            array.append(int(byte, 2))
        print('length of array / original length: {}'.format(len(array)/self.length))
        return array

    def getAvgLength(self):
        avgLength = 0
        for p in self.probabilities:
            avgLength += self.probabilities[p]*len(self.codes[p])
        return avgLength

class HeapLeaf:
    
    def __init__(self, char, prob):
        self.char = char
        self.prob = prob
        self.leftChild = None
        self.rightChild = None
    
    
    def __lt__(self, other):
        if other == None:
            return -1
        return self.prob < other.prob

def main():
    HC = HuffmanCode([], 'Alice29.txt')
    HC.countProb()
    HC.printCodes()
    h_X = HC.Entropy()
    print('entropy of original file: {}'.format(h_X[0]))
    HC.makeHeap()
    HC.createCodes(HC.heap[0], "")
    encodedText = HC.encode()
    paddedText = HC.pad(encodedText)
    byte = HC.toBytes(paddedText)
    HC.printToFile(paddedText, 'compressed.txt')
    print('length after compression: {}'.format(len(byte)))
    print('avg codeword length: {}'.format(HC.getAvgLength()))
    return



if __name__ == '__main__':
    main()

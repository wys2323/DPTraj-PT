import math
import time
import random
import datetime
from preprocess import dataset
from parameters import Parameter

step = 1
hashLen = 20


class Node(object):
    def __init__(self, cellIndexS, timeIndexS, count=0.0, nCount=0.0, eCount=0.0, level=0):
        self.cellIndexS = cellIndexS
        self.timeIndexS = timeIndexS
        self.count = count
        self.nCount = nCount
        self.eCount = eCount
        self.level = level
        self.next = None

    def show(self):
        print('Node parameters：')
        print(self.level, self.cellIndexS, self.timeIndexS)
        print(self.count, self.nCount, self.eCount)


class LinkList(object):
    class LinkListIterator(object):
        def __init__(self, node):
            self.node = node

        def __next__(self):
            if self.node:
                cur_node = self.node
                self.node = cur_node.next
                return cur_node.cellIndexS, cur_node.timeIndexS
            else:
                raise StopIteration

        def __iter__(self):
            return self

    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, node):
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head.next
            self.head.next = node

    def findNode(self, node):
        temp = self.head
        while temp:
            if temp.level == node.level:
                flag = 0
                for i in range(node.level + 1):
                    if (temp.cellIndexS[i] != node.cellIndexS[i]) or (temp.timeIndexS[i] != node.timeIndexS[i]):
                        flag = 1
                        break
                if flag == 0:
                    return temp
            temp = temp.next
        return None

    def __iter__(self):
        return self.LinkListIterator(self.head)

    def __repr__(self):
        return '<<' + ','.join(map(str, self)) + '>>'


class HashTableS(object):

    def __init__(self, size):
        self.size = size
        self.T = [LinkList() for _ in range(self.size)]

    def fold(self, key):
        bin_array = []
        group = int(len(key) / 4)
        for i in range(0, group):
            string = ''
            for j in range(int(i * 4), int(i * 4 + 4)):
                string = '{0:08b}'.format(ord(key[j])) + string
            bin_array.append(string)
        rest = len(key) - group * 4
        if rest != 0:
            string = ''
            for i in range(rest):
                string = '{0:08b}'.format(ord(key[group * 4 + i])) + string
            bin_array.append(string)
        bin_sum = 0
        for i in range(len(bin_array)):
            bin_sum += int(bin_array[i], 2)
        return bin_sum % int(pow(2, hashLen))

    def getHashValue(self, node):
        string = ''
        for i in range(node.level + 1):
            if i is not None:
                string = string + str(node.cellIndexS[i])
        for j in range(node.level + 1):
            if j is not None:
                string = string + str(node.timeIndexS[j])
        index = self.fold(string)
        return index

    def insertNode(self, node):
        hashValue = self.getHashValue(node)
        if self.find(node):
            print('The current incoming node: ')
            print(node.cellIndexS)
            print(node.timeIndexS)
            print('something is wrong: Duplicated Insert')
        else:
            self.T[hashValue].append(node)

    def find(self, node):
        hashValue = self.getHashValue(node)
        n = self.T[hashValue].findNode(node)
        if n is not None:
            return True
        else:
            return False

    def updateCount(self, node, increment):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            print('cellIndex ', node.cellIndexS)
            print('timeIndex ', node.timeIndexS)
            print('level ', node.level)
            st = input("enter a string to stop")
            print(st)
            return False
        temp.count += increment
        return True

    def getCount(self, node):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            print('cellIndex ', node.cellIndexS)
            print('timeIndex ', node.timeIndexS)
            print('level ', node.level)
            st = input("enter a string to stop")
            print(st)
            return -1
        return temp.count

    def setNoiseCount(self, node, noiseCount):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            print('cellIndex ', node.cellIndexS)
            print('timeIndex ', node.timeIndexS)
            print('level ', node.level)
            st = input("enter a string to stop")
            print(st)
            return False
        temp.nCount = hashArray.getCount(temp) + float(noiseCount)
        if temp.nCount < 0:
            temp.nCount = 0
        return True

    def getNoiseCount(self, node):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            print('cellIndex ', node.cellIndexS)
            print('timeIndex ', node.timeIndexS)
            print('level ', node.level)
            st = input("enter a string to stop")
            print(st)
            return -1
        return float(temp.nCount)

    def setENoiseCount(self, node, noiseCount=0.0):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            print('cellIndex ', node.cellIndexS)
            print('timeIndex ', node.timeIndexS)
            print('level ', node.level)
            st = input("enter a string to stop")
            print(st)
            return False
        if noiseCount < 0:
            noiseCount = 0
        temp.eCount = float(noiseCount)
        return True

    def getENoiseCount(self, node):
        hashValue = self.getHashValue(node)
        temp = self.T[hashValue].findNode(node)
        if temp is None:
            print('something is wrong: cannot find the node')
            print('cellIndex ', node.cellIndexS)
            print('timeIndex ', node.timeIndexS)
            print('level ', node.level)
            st = input("enter a string to stop")
            print(st)
            return -1
        return temp.eCount


def createNode(array, timeArray, count=0.0, nCount=0.0, eCount=0.0, level=0):
    temp_A = [_ for _ in array]
    temp_T = [_ for _ in timeArray]
    temp = Node(temp_A, temp_T, count, nCount, eCount, level)
    return temp


def read_tra2(tra):
    value = [_.split(',') for _ in tra.split(';') if _]
    return value


def getCellStay():
    with open('./data/output/cellStay.txt', 'r') as input:
        content = input.readlines()
        stay = [0 for _ in range(para.cellCount)]
        for i in range(len(content)):
            stay[i] = float(content[i].strip())
    return stay


def sign(t):
    if t < 0:
        return -1.0
    else:
        return 1.0


def LapLaceNoise(epsilon, sensitivity):
    d = random.random()
    uniform = d - 0.5
    s = sensitivity
    nc = -s / epsilon * sign(uniform) * math.log(1.0 - 2.0 * math.fabs(uniform))
    return nc


def buildPrefixTree():
    array = ['' for _ in range(para.maxLevel + 2)]
    timeArray = ['' for _ in range(para.maxLevel + 2)]
    for i in range(0, para.cellCount):
        for j in range(0, para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1
            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            hashArray.insertNode(node)
            buildTreeLevel(array, timeArray, level + 1)


def buildTreeLevel(array, timeArray, level):
    if level > para.maxLevel:
        return
    else:
        cellA = int(array[level - 1])
        timeArray[level] = 0
        for i in para.neighbor[cellA]:
            if i == -1:
                break
            if i != cellA:
                array[level] = i
                node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
                hashArray.insertNode(node)
                buildTreeLevel(array, timeArray, level + 1)

        array[level] = para.endSign
        node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
        hashArray.insertNode(node)
        return


def loadPrefixTree():
    path = './data/output/' + dataset + '_' + string + '_index.txt'
    with open(path) as input:
        content = input.readlines()
    array = ['' for _ in range(para.maxLevel + 2)]
    timeArray = ['' for _ in range(para.maxLevel + 2)]
    i = 0
    while i < len(content):
        if (i % 2) != 0:
            tra = read_tra2(content[i][3:-1])
            tLen = len(tra)
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1
            number = 0
            while (level <= para.maxLevel) and (level <= tLen):
                array[level] = int(tra[number][0])
                timeArray[level] = 0
                if level == 1:
                    timeArray[level] = int(tra[number][1])
                node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
                hashArray.updateCount(node, 1.0)
                if level == tLen and tLen < para.maxLevel:
                    array[level + 1] = para.endSign
                    timeArray[level + 1] = 0
                    hashArray.updateCount(node, 1.0)
                level += 1
                number += 1
        i += 1
    return


def getLapLaceNoise(epsilon, sensitivity):
    noise = LapLaceNoise(epsilon, sensitivity)
    return noise


def getEpsilonPrefixLevel(level):
    epsilon = para.epsilonPrefix
    delta, levelNoise = 0.8, 0
    for i in range(para.maxLevel):
        levelNoise += math.log((para.maxLevel - i) + delta)
    value = math.log((para.maxLevel - level) + 1 + delta) / levelNoise
    return epsilon * value


def addNoisePrefixTree():
    array = ['' for _ in range(para.maxLevel + 2)]
    timeArray = ['' for _ in range(para.maxLevel + 2)]
    for i in range(0, para.cellCount):
        for j in range(0, para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1
            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            epsilonPrefixLevel = getEpsilonPrefixLevel(level)
            noise = getLapLaceNoise(epsilonPrefixLevel, para.sensitivity)
            hashArray.setNoiseCount(node, noise)
            addNoiseTreeLevel(array, timeArray, level + 1)


def addNoiseTreeLevel(array, timeArray, level):
    if level > para.maxLevel:
        return
    else:
        cellA = int(array[level - 1])
        timeArray[level] = 0
        for i in para.neighbor[cellA]:
            if i == -1:
                break
            if i != cellA:
                array[level] = i
                node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
                epsilonPrefixLevel = getEpsilonPrefixLevel(level)
                noise = getLapLaceNoise(epsilonPrefixLevel, para.sensitivity)
                hashArray.setNoiseCount(node, noise)
                addNoiseTreeLevel(array, timeArray, level + 1)

        array[level] = para.endSign
        node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
        epsilonPrefixLevel = getEpsilonPrefixLevel(level)
        noise = getLapLaceNoise(epsilonPrefixLevel, para.sensitivity)
        hashArray.setNoiseCount(node, noise)
        return


def enforceConsistency():
    path = './data/output/' + dataset + '_' + string + '_index.txt'
    with open(path) as input:
        content = input.readlines()

    i = 0
    sum = 0
    while i < len(content):
        if (i % 2) != 0:
            sum += 1
        i += 1

    cSum = 0.0
    array = ['' for _ in range(para.maxLevel + 2)]
    timeArray = ['' for _ in range(para.maxLevel + 2)]
    for i in range(para.cellCount):
        for j in range(0, para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1
            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            cSum += hashArray.getNoiseCount(node)

    if math.isclose(cSum, 0.0, rel_tol=1e-5):
        return

    checkSum = 0.0
    temp = [[0 for _ in range(para.numtimeInterval)] for _ in range(para.cellCount)]
    for i in range(0, para.cellCount):
        for j in range(0, para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1
            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            nCount = hashArray.getNoiseCount(node)
            eNCount = int(nCount / cSum * sum)
            checkSum = checkSum + eNCount
            temp[i][j] = nCount

    tempSum = sum
    while checkSum <= sum:
        checkSum = 0
        tempSum = tempSum + 1
        for i in range(0, para.cellCount):
            for j in range(0, para.numtimeInterval):
                checkSum = checkSum + int(temp[i][j] / cSum * tempSum)

    count_tra = 0
    sumT = tempSum - 1
    for i in range(0, para.cellCount):
        for j in range(0, para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1
            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            nCount = hashArray.getNoiseCount(node)
            eNCount = int(nCount / cSum * sumT)
            hashArray.setENoiseCount(node, eNCount)
            count_tra += eNCount
            if eNCount > 0:
                enforceConsistencyLevel(array, timeArray, level + 1, eNCount)


def adjustSum(tempSum, sum, cSum, temp, step):
    checkSum, flag = 0, True
    while checkSum < sum:
        checkSum = 0
        tempSum = tempSum + step
        for i in range(len(temp)):
            checkSum = checkSum + int(temp[i] / cSum * tempSum)
    return tempSum, checkSum


def getSum(sum, cSum, temp, step):
    tempSum, checkSum = adjustSum(sum, sum, cSum, temp, step)
    if checkSum != sum:
        countStep = 0
        countIncre = 1
        while checkSum != sum and countStep <= 5:
            tempSum = tempSum - countIncre
            countIncre = countIncre / 10
            countStep += 1
            tempSum, checkSum = adjustSum(tempSum, sum, cSum, temp, countIncre)
        if countStep > 5 and checkSum != sum:
            tempSum = tempSum - countIncre
    return tempSum


def enforceConsistencyLevel(array, timeArray, level, sum):
    if math.isclose(sum, 0.0, rel_tol=1e-5):
        return
    if level > para.maxLevel:
        return
    else:
        cSum = 0.0
        cellA = int(array[level - 1])
        timeArray[level] = 0
        neighbors = list(filter(lambda x: x != -1, para.neighbor[cellA]))
        neighbors.remove(cellA)
        temp = [0 for _ in range(len(neighbors) + 1)]
        for i in range(len(neighbors)):
            array[level] = neighbors[i]
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            nCount = hashArray.getNoiseCount(node)
            cSum += nCount
            temp[i] = nCount

        array[level] = para.endSign
        node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
        nCount = hashArray.getNoiseCount(node)
        cSum += nCount
        temp[-1] = nCount

        sumT = sum
        if cSum == 0:
            flag = False
        else:
            flag = True
            sumT = getSum(sum, cSum, temp, step)

        count_allocate = 0
        timeArray[level] = 0
        if flag:
            for i in range(len(neighbors)):
                array[level] = neighbors[i]
                node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
                nCount = hashArray.getNoiseCount(node)
                eNCount = int(nCount / cSum * sumT)
                hashArray.setENoiseCount(node, eNCount)
                if eNCount > 0:
                    count_allocate += eNCount
                    enforceConsistencyLevel(array, timeArray, level + 1, eNCount)

            array[level] = para.endSign
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            nCount = hashArray.getNoiseCount(node)
            eNCount = int(nCount / cSum * sumT)
            hashArray.setENoiseCount(node, eNCount)
            count_allocate += eNCount
        else:
            array[level] = para.endSign
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            hashArray.setENoiseCount(node, sum)
            count_allocate += sum
        return


def buildMarkov():
    array = ['' for _ in range(para.tmaxLevel + 2)]
    timeArray = ['' for _ in range(para.tmaxLevel + 2)]
    for i in range(0, para.cellCount):
        level = 0
        array[level] = para.aSign
        timeArray[level] = para.aSign
        level += 1
        array[level] = i
        timeArray[level] = 0
        buildMarkovLevel(array, timeArray, level + 1)


def buildMarkovLevel(array, timeArray, level):
    if level > para.tmaxLevel:
        return
    else:
        cellA = int(array[level - 1])
        timeArray[level] = 0
        for i in para.neighbor[cellA]:
            if i == -1:
                break
            if i != cellA:
                array[level] = i
                if level == para.tmaxLevel:
                    node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
                    hashArray.insertNode(node)
                else:
                    buildMarkovLevel(array, timeArray, level + 1)

        if level == para.tmaxLevel:
            array[level] = para.endSign
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            hashArray.insertNode(node)
        return


def loadMarkov():
    path = './data/output/' + dataset + '_' + string + '_index.txt'
    with open(path) as input:
        content = input.readlines()

    array = ['' for _ in range(para.tmaxLevel + 2)]
    timeArray = ['' for _ in range(para.tmaxLevel + 2)]

    i = 0
    while i < len(content):
        if (i % 2) != 0:
            s = content[i][3:-1]
            tra = read_tra2(s)

            if len(tra) < para.tmaxLevel - 1:
                i += 1
                continue

            for j in range(0, len(tra) - para.tmaxLevel + 2):
                level = 0
                array[level] = para.aSign
                timeArray[level] = para.aSign
                level += 1
                for k in range(j, j + para.tmaxLevel):
                    if k == len(tra):
                        array[level] = para.endSign
                    else:
                        array[level] = int(tra[k][0])
                    timeArray[level] = 0
                    level += 1
                node = createNode(array, timeArray, 0.0, 0.0, 0.0, level - 1)
                hashArray.updateCount(node, 1 / (len(tra) - para.tmaxLevel + 2))
        i += 1


def getNoiseMarkov(epsilon, sensitivity):
    noise = LapLaceNoise(epsilon, sensitivity)
    return noise


def addNoiseMarkov():
    array = ['' for _ in range(para.tmaxLevel + 2)]
    timeArray = ['' for _ in range(para.tmaxLevel + 2)]
    for i in range(0, para.cellCount):
        level = 0
        array[level] = para.aSign
        timeArray[level] = para.aSign
        level += 1
        array[level] = i
        timeArray[level] = 0
        addNoiseMarkovLevel(array, timeArray, level + 1)


def addNoiseMarkovLevel(array, timeArray, level):
    if level > para.tmaxLevel:
        return
    else:
        cellA = int(array[level - 1])
        timeArray[level] = 0
        for i in para.neighbor[cellA]:
            if i == -1:
                break
            if i != cellA:
                array[level] = i
                if level == para.tmaxLevel:
                    node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
                    noise = getNoiseMarkov(para.epsilon - para.epsilonPrefix, para.sensitivity)
                    hashArray.setNoiseCount(node, noise)
                else:
                    addNoiseMarkovLevel(array, timeArray, level + 1)
        if level == para.tmaxLevel:
            array[level] = para.endSign
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            noise = getNoiseMarkov(para.epsilon - para.epsilonPrefix, para.sensitivity)
            hashArray.setNoiseCount(node, noise)
        return


def normalizeMarkov():
    array = ['' for _ in range(para.tmaxLevel + 2)]
    timeArray = ['' for _ in range(para.tmaxLevel + 2)]
    for i in range(0, para.cellCount):
        level = 0
        array[level] = para.aSign
        timeArray[level] = para.aSign
        level += 1
        array[level] = i
        timeArray[level] = 0
        normalizeMarkovLevel(array, timeArray, level + 1)


def normalizeMarkovLevel(array, timeArray, level):
    if level > para.tmaxLevel:
        return
    else:
        cSum = 0
        cellA = int(array[level - 1])
        timeArray[level] = 0
        for i in para.neighbor[cellA]:
            if i == -1:
                break
            if i != cellA:
                array[level] = i
                if level == para.tmaxLevel:
                    node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
                    nCount = hashArray.getNoiseCount(node)
                    cSum += nCount
                else:
                    normalizeMarkovLevel(array, timeArray, level + 1)
        if level == para.tmaxLevel:
            array[level] = para.endSign
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            nCount = hashArray.getNoiseCount(node)
            cSum += nCount
        if cSum > 0:
            cellA = int(array[level - 1])
            timeArray[level] = 0
            for i in para.neighbor[cellA]:
                if i == -1:
                    break
                if i != cellA:
                    array[level] = i
                    if level == para.tmaxLevel:
                        node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
                        nCount = hashArray.getNoiseCount(node)
                        eNCount = nCount / cSum
                        hashArray.setENoiseCount(node, eNCount)
            if level == para.tmaxLevel:
                array[level] = para.endSign
                node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
                nCount = hashArray.getNoiseCount(node)
                eNCount = nCount / cSum
                hashArray.setENoiseCount(node, eNCount)
        return


def generateTra():
    array = ['' for _ in range(para.maxTLen + 2)]
    timeArray = ['' for _ in range(para.maxTLen + 2)]
    for i in range(0, para.cellCount):
        for j in range(0, para.numtimeInterval):
            level = 0
            array[level] = para.startSign
            timeArray[level] = para.startSign
            level += 1
            array[level] = i
            timeArray[level] = j
            node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
            tCount = int(hashArray.getENoiseCount(node))

            if tCount < 1:
                continue

            generateTraLevel(array, timeArray, level + 1, level, tCount)


def all_zeros(lst):
    return all(element == 0 for element in lst)


def adjustMarkovSum(tempArray, tempTimeArray, cCount):
    level = para.tmaxLevel
    cellA = int(tempArray[level - 1])
    tempTimeArray[level] = 0
    neighbors = list(filter(lambda x: x != -1, para.neighbor[cellA]))
    neighbors.remove(cellA)
    temp = [0 for _ in range(len(neighbors) + 1)]
    cSum = 0
    for i in range(len(neighbors)):
        tempArray[level] = neighbors[i]
        node = createNode(tempArray, tempTimeArray, 0.0, 0.0, 0.0, level)
        temp[i] = hashArray.getENoiseCount(node)
        cSum += temp[i]
    tempArray[level] = para.endSign
    node = createNode(tempArray, tempTimeArray, 0.0, 0.0, 0.0, level)
    temp[-1] = hashArray.getENoiseCount(node)
    cSum += temp[-1]
    flag = False
    countT = cCount
    if cSum > 0:
        countT = getSum(cCount, 1, temp, step)
        flag = True
    return countT, flag


def generateTraLevel(array, timeArray, level, curlen, cCount):
    if cCount < 1:
        return

    if (array[level - 1] == para.endSign) or (curlen == para.maxTLen):
        writeTra(array, timeArray, cCount, curlen)
        array[level - 1] = ''
        timeArray[level - 1] = ''
        return

    if level <= para.maxLevel:
        timeArray[level] = 0
        cellA = array[curlen]
        for i in para.neighbor[cellA]:
            if i == -1:
                break
            if i != cellA:
                array[level] = i
                node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
                tCount = int(hashArray.getENoiseCount(node))
                if tCount > 0:
                    generateTraLevel(array, timeArray, level + 1, level, tCount)

        array[level] = para.endSign
        node = createNode(array, timeArray, 0.0, 0.0, 0.0, level)
        tCount = int(hashArray.getENoiseCount(node))
        if tCount > 0:
            generateTraLevel(array, timeArray, level + 1, level, tCount)
    else:
        tempArray = ['' for _ in range(para.tmaxLevel + 2)]
        tempTimeArray = ['' for _ in range(para.tmaxLevel + 2)]
        tempArray[0] = para.aSign
        tempTimeArray[0] = para.aSign
        tempArray[1:para.tmaxLevel] = array[level - para.tmaxLevel + 1:level]
        tempTimeArray[1:para.tmaxLevel] = [0 for _ in range(para.tmaxLevel - 1)]
        countT, flag = adjustMarkovSum(tempArray, tempTimeArray, cCount)
        cellA = array[curlen]
        tempTimeArray[para.tmaxLevel] = 0
        neighbors = list(filter(lambda x: x != -1, para.neighbor[cellA]))
        neighbors.remove(cellA)
        if flag:
            for i in range(len(neighbors)):
                tempArray[para.tmaxLevel] = neighbors[i]
                node = createNode(tempArray, tempTimeArray, 0.0, 0.0, 0.0, para.tmaxLevel)
                tCount = int(hashArray.getENoiseCount(node) * countT)
                if tCount > 0:
                    array[level] = tempArray[para.tmaxLevel]
                    timeArray[level] = tempTimeArray[para.tmaxLevel]
                    generateTraLevel(array, timeArray, level + 1, level, tCount)

            tempArray[para.tmaxLevel] = para.endSign
            node = createNode(tempArray, tempTimeArray, 0.0, 0.0, 0.0, para.tmaxLevel)
            tCount = int(hashArray.getENoiseCount(node) * countT)
            if tCount > 0:
                array[level] = tempArray[para.tmaxLevel]
                timeArray[level] = tempTimeArray[para.tmaxLevel]
                generateTraLevel(array, timeArray, level + 1, level, tCount)
        else:
            array[level] = para.endSign
            timeArray[level] = tempTimeArray[para.tmaxLevel]
            generateTraLevel(array, timeArray, level + 1, level, countT)


def trans(index):
    cellHeight = (para.top - para.bottom) / para.cellH
    cellWidth = (para.right - para.left) / para.cellW
    rowIndex = int(int(index) / para.cellW)
    columnIndex = int(int(index) % para.cellW)
    lat = float(para.bottom + rowIndex * cellHeight + cellHeight / 2)
    lon = float(para.left + columnIndex * cellWidth + cellWidth / 2)
    return lon, lat


def generateLocTra(array, timeArray, curlen, number_Tra):
    output_t.write('#' + str(number_Tra) + ':\n')
    output_t.write('>0:')
    output_l.write('#' + str(number_Tra) + ':\n')
    output_l.write('>0:')
    lon, lat = trans(array[1])
    time_incre = para.timestep * float(timeArray[1])
    time = para.startTime + datetime.timedelta(seconds=time_incre * 60)
    output_t.write(str(lon) + ',' + str(lat) + ',' + str(time) + ';')
    output_l.write(str(lon) + ',' + str(lat) + ';')
    for j in range(2, curlen + 1):
        if array[j] == para.endSign:
            break
        lon, lat = trans(array[j])
        time = time + datetime.timedelta(seconds=cellStay[int(array[j])] * 60)
        output_t.write(str(lon) + ',' + str(lat) + ',' + str(time) + ';')
        output_l.write(str(lon) + ',' + str(lat) + ';')
    output_t.write('\n')
    output_l.write('\n')


def writeTra(array, timeArray, tCount, curlen):
    global number_Tra
    for i in range(0, tCount):
        generateLocTra(array, timeArray, curlen, number_Tra)
        number_Tra += 1
    return


def program():
    buildPrefixTree()
    print('... build prefix tree')
    loadPrefixTree()
    print('... load')
    addNoisePrefixTree()
    print('... add noise')
    enforceConsistency()
    print('... enforce consistency')
    buildMarkov()
    print('... build markov')
    loadMarkov()
    print('... load')
    addNoiseMarkov()
    print('... add noise')
    normalizeMarkov()
    print('... normalize markov')
    generateTra()
    print('... generate trajectories')


if __name__ == '__main__':
    times = 1
    print('> preprocess over')
    for budget in [1]:
        for ratio in [0.6]:
            para = Parameter()
            for run in range(1, times + 1):
                print('> budget', budget, 'ratio', ratio, 'run', run)
                para.epsilon = budget
                para.epsilonPrefix = ratio * budget
                # para.show()
                hashArray = HashTableS(pow(2, hashLen))
                random.seed(time.time())
                cellStay = getCellStay()
                number_Tra = 0
                string = str(para.cellW) + '_' + str(para.numtimeInterval)
                output_t = open(
                    'data/output/syn/' + dataset + '_' + string + '_' + str(budget) + '_' + str(run) + '_tra.txt', 'w')
                output_l = open(
                    'data/output/syn/' + dataset + '_' + string + '_' + str(budget) + '_' + str(run) + '_loc.txt', 'w')
                program()
                output_t.close()
                output_l.close()
                print('> run', str(run), 'over')
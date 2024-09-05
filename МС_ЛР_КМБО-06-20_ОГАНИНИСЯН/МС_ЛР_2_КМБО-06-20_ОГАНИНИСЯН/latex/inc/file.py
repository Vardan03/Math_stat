from ms import formatNumber, makeTable,  calcBinomProbability,  ExpRaspr 
import re
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from camelot.core import Table
from PyPDF2 import PdfFileReader
from math import log2
from collections import OrderedDict
from typing import List, Dict
from scipy import stats
from dataclasses import dataclass
from statistics import NormalDist
from numpy import round_, sqrt, arange
from titlePage import generateTitlePage
import os
import camelot
unordered_sample1 = [
0.24120, 0.20069, 2.49827, 0.34931, 0.70002, 1.02003, 0.13744, 0.41287, 0.18402, 1.50855,
0.50039, 0.32609, 0.25789, 0.08005, 0.02970, 0.69878, 0.03860, 0.13562, 0.94595, 0.79714,
1.07189, 2.04207, 0.55176, 0.13330, 0.04860, 0.09261, 0.73266, 0.39373, 0.03471, 0.59748,
0.00550, 0.10785, 0.48580, 0.12093, 1.23308, 0.40318, 0.59348, 0.15540, 0.01085, 0.65834,
0.46964, 0.57113, 0.33739, 0.78320, 0.61860, 0.09328, 0.05437, 0.27422, 0.13480, 0.55982,
0.16836, 0.08466, 0.03538, 0.68691, 0.31945, 0.32272, 0.95414, 0.00067, 0.78717, 0.59659,
0.55605, 2.15305, 0.49415, 0.02424, 0.89349, 0.80630, 0.37284, 0.31772, 0.04112, 0.32601,
0.26923, 0.12576, 0.07903, 0.03152, 0.41632, 0.04060, 0.13879, 0.12846, 0.01667, 0.72244,
0.54765, 0.16667, 0.07035, 0.02681, 0.54523, 0.53271, 0.45727, 0.19646, 0.46272, 0.90750,
0.67340, 0.10823, 0.04123, 0.68070, 0.07748, 0.11075, 0.18493, 0.13457, 1.18247, 0.38154,
0.06569, 0.16240, 0.04554, 0.80698, 0.26408, 0.18152, 0.02194, 0.01732, 0.07088, 0.50737,
0.42889, 0.34414, 0.38134, 0.40327, 0.79952, 0.27456, 0.25624, 0.06428, 0.29408, 0.36317,
0.09802, 0.46832, 0.11789, 0.03405, 0.00989, 0.16255, 0.13362, 0.35968, 0.16359, 0.24217,
0.14683, 0.00237, 0.75408, 0.88643, 0.30986, 0.31571, 0.19583, 0.16891, 1.63331, 0.12351,
0.40976, 0.08514, 0.27008, 0.37772, 0.15724, 0.29163, 0.26879, 0.09789, 0.07231, 0.23268,
0.04717, 0.38958, 0.43365, 1.27750, 0.90610, 0.75378, 0.48882, 0.08835, 0.35536, 0.03113,
1.40151, 0.07059, 0.38457, 0.31422, 0.20869, 0.07405, 0.14701, 0.10404, 0.61411, 0.13585,
0.07557, 0.06579, 0.98282, 0.21078, 0.09336, 0.94949, 0.60938, 0.09486, 0.66561, 0.17303,
0.06193, 0.12158, 0.97936, 0.19998, 0.05866, 0.60070, 0.63519, 0.13193, 1.91133, 0.96716,
0.45503, 0.21104, 0.23938, 0.28714, 0.02044, 0.08414, 0.60970, 0.16313, 0.13837, 0.03554
]
unordered_sample2 = [
9.77025, 7.84276, 4.05229, 8.04839, 9.41659, 7.57213, 8.61462, 4.95985, 5.77880, 3.12317,
6.49458, 6.94320, 7.57100, 5.36951, 10.55283, 7.51243, 9.63317, 7.53753, 8.82055, 6.50139,
6.49341, 7.28528, 7.70446, 5.49125, 7.63095, 5.17903, 6.71337, 6.80843, 5.16512, 7.49481,
9.30528, 11.52394, 3.91187, 3.55400, 4.16010, 7.72491, 6.91488, 7.51121, 8.76289, 7.19596,
8.78022, 2.82677, 7.01889, 5.42802, 7.18210, 9.69690, 4.96187, 7.61321, 5.05334, 6.95743,
6.33703, 8.43742, 7.40592, 8.14157, 5.76268, 5.62357, 5.76960, 5.52992, 5.71038, 6.96062,
8.28251, 8.01207, 5.86276, 6.09561, 5.62196, 7.47430, 5.87784, 3.23621, 5.41288, 7.68933,
4.20785, 7.28157, 8.33969, 6.13279, 8.24552, 8.80064, 6.69964, 8.66011, 10.73090, 7.39790,
7.59231, 5.37157, 4.72374, 9.13526, 1.96161, 6.31527, 8.98943, 6.05701, 7.56973, 6.31533,
5.11918, 8.28191, 7.52606, 5.52857, 5.88576, 6.16393, 5.44642, 4.29147, 8.30444, 6.62887,
6.47003, 7.02147, 7.61848, 6.99433, 6.89876, 6.14050, 7.73999, 6.04531, 8.87165, 6.89893,
8.27708, 6.89119, 4.35793, 7.42013, 6.58775, 8.27541, 6.87410, 8.53980, 8.56065, 8.22202,
6.22377, 6.89487, 7.74233, 8.80423, 9.33313, 6.57722, 5.06884, 8.40925, 8.12839, 7.98477,
8.26201, 4.93473, 5.12688, 4.41217, 9.51142, 6.40781, 7.50593, 5.35190, 5.74046, 6.14165,
4.97357, 9.22183, 6.04206, 4.40426, 9.51716, 5.25917, 6.73307, 7.01934, 7.13955, 6.28469,
8.26906, 8.16409, 4.80252, 6.95316, 6.76033, 5.75203, 7.32998, 6.77154, 6.79967, 4.34950,
6.22581, 9.33770, 7.04449, 5.20514, 9.45650, 5.22006, 5.42706, 5.96046, 6.29732, 9.65425,
4.20325, 7.23606, 4.52708, 5.60927, 6.47370, 3.43781, 6.61158, 7.68103, 6.63923, 8.43593,
7.74532, 7.13404, 7.65328, 7.21342, 7.00606, 8.11294, 5.81466, 5.60671, 9.30283, 11.38605,
9.06896, 5.46313, 9.29720, 6.04036, 8.29306, 7.72403, 6.48576, 6.43837, 7.49219, 4.69380
]
a3=6.1
b3=9.46
unordered_sample3 = [
8.91018, 8.29374, 8.88958, 7.82780, 7.18405, 8.26589, 6.21151, 7.97928, 7.34325, 6.36996,
9.11988, 6.41875, 8.54347, 7.53926, 7.47544, 8.74177, 7.98634, 8.79624, 7.42303, 6.72877,
8.34361, 8.41191, 9.30401, 9.11602, 7.72913, 6.93243, 7.18277, 7.87913, 8.84123, 6.11534,
7.96888, 6.52646, 8.84283, 6.84004, 8.03695, 6.29181, 7.66479, 8.03671, 9.03393, 7.78612,
8.13577, 7.26322, 8.34620, 6.59104, 6.69418, 6.85422, 7.27710, 7.80982, 9.03941, 6.12182,
8.29152, 8.41330, 8.28312, 7.62500, 9.14764, 7.25201, 9.33478, 7.89168, 8.23778, 6.64248,
7.25703, 7.85996, 6.45092, 8.63611, 9.06575, 9.45048, 6.89406, 8.23378, 8.94944, 8.28389,
6.55950, 6.14309, 7.95383, 7.79261, 9.32830, 6.16251, 6.28815, 6.15730, 6.63312, 8.06298,
6.70774, 7.18827, 8.97618, 8.09306, 8.43732, 8.96131, 9.35969, 6.40913, 6.59176, 9.42594,
9.03436, 7.04502, 9.01711, 6.73079, 6.99592, 8.32178, 6.38252, 8.40200, 8.99550, 7.72097,
6.56796, 9.28245, 7.59856, 8.26254, 7.71560, 6.45940, 6.94121, 6.73281, 8.69295, 6.61194,
8.20903, 7.65358, 9.34045, 8.08651, 8.68740, 8.79739, 8.91552, 8.86526, 6.23377, 6.80823,
9.43452, 8.78930, 7.72378, 8.82037, 8.66729, 6.49833, 7.50621, 9.39192, 7.25589, 8.61802,
7.49210, 8.48937, 7.66874, 8.90013, 8.12496, 7.06294, 8.11783, 7.22483, 6.87096, 8.51242,
6.87425, 7.98371, 7.20591, 9.02850, 7.32478, 6.18167, 8.02286, 8.56844, 7.95505, 8.42831,
8.87303, 6.44637, 7.42033, 8.22613, 6.71621, 8.45465, 8.06748, 8.12885, 9.31020, 7.26715,
9.10767, 7.31474, 7.27326, 9.12497, 9.34991, 9.01500, 8.83140, 6.16709, 8.93067, 6.70706,
6.56325, 9.08311, 7.81939, 8.71664, 7.91669, 8.07958, 6.58481, 9.07679, 8.56668, 9.28042,
8.89296, 8.66596, 7.11508, 6.64348, 8.55324, 9.03839, 8.06943, 8.37293, 7.16686, 7.92852,
8.31200, 6.47938, 9.06770, 9.04886, 8.86859, 7.81672, 6.24946, 8.15619, 9.27625, 8.15770
]
a4=6.1
b4=9.46
unordered_sample4 = [
8.91018, 8.29374, 8.88958, 7.82780, 7.18405, 8.26589, 6.21151, 7.97928, 7.34325, 6.36996,
9.11988, 6.41875, 8.54347, 7.53926, 7.47544, 8.74177, 7.98634, 8.79624, 7.42303, 6.72877,
8.34361, 8.41191, 9.30401, 9.11602, 7.72913, 6.93243, 7.18277, 7.87913, 8.84123, 6.11534,
7.96888, 6.52646, 8.84283, 6.84004, 8.03695, 6.29181, 7.66479, 8.03671, 9.03393, 7.78612,
8.13577, 7.26322, 8.34620, 6.59104, 6.69418, 6.85422, 7.27710, 7.80982, 9.03941, 6.12182,
8.29152, 8.41330, 8.28312, 7.62500, 9.14764, 7.25201, 9.33478, 7.89168, 8.23778, 6.64248,
7.25703, 7.85996, 6.45092, 8.63611, 9.06575, 9.45048, 6.89406, 8.23378, 8.94944, 8.28389,
6.55950, 6.14309, 7.95383, 7.79261, 9.32830, 6.16251, 6.28815, 6.15730, 6.63312, 8.06298,
6.70774, 7.18827, 8.97618, 8.09306, 8.43732, 8.96131, 9.35969, 6.40913, 6.59176, 9.42594,
9.03436, 7.04502, 9.01711, 6.73079, 6.99592, 8.32178, 6.38252, 8.40200, 8.99550, 7.72097,
6.56796, 9.28245, 7.59856, 8.26254, 7.71560, 6.45940, 6.94121, 6.73281, 8.69295, 6.61194,
8.20903, 7.65358, 9.34045, 8.08651, 8.68740, 8.79739, 8.91552, 8.86526, 6.23377, 6.80823,
9.43452, 8.78930, 7.72378, 8.82037, 8.66729, 6.49833, 7.50621, 9.39192, 7.25589, 8.61802,
7.49210, 8.48937, 7.66874, 8.90013, 8.12496, 7.06294, 8.11783, 7.22483, 6.87096, 8.51242,
6.87425, 7.98371, 7.20591, 9.02850, 7.32478, 6.18167, 8.02286, 8.56844, 7.95505, 8.42831,
8.87303, 6.44637, 7.42033, 8.22613, 6.71621, 8.45465, 8.06748, 8.12885, 9.31020, 7.26715,
9.10767, 7.31474, 7.27326, 9.12497, 9.34991, 9.01500, 8.83140, 6.16709, 8.93067, 6.70706,
6.56325, 9.08311, 7.81939, 8.71664, 7.91669, 8.07958, 6.58481, 9.07679, 8.56668, 9.28042,
8.89296, 8.66596, 7.11508, 6.64348, 8.55324, 9.03839, 8.06943, 8.37293, 7.16686, 7.92852,
8.31200, 6.47938, 9.06770, 9.04886, 8.86859, 7.81672, 6.24946, 8.15619, 9.27625, 8.15770
]
lambd5=2.08
unordered_sample5 = [
0.24120, 0.20069, 2.49827, 0.34931, 0.70002, 1.02003, 0.13744, 0.41287, 0.18402, 1.50855,
0.50039, 0.32609, 0.25789, 0.08005, 0.02970, 0.69878, 0.03860, 0.13562, 0.94595, 0.79714,
1.07189, 2.04207, 0.55176, 0.13330, 0.04860, 0.09261, 0.73266, 0.39373, 0.03471, 0.59748,
0.00550, 0.10785, 0.48580, 0.12093, 1.23308, 0.40318, 0.59348, 0.15540, 0.01085, 0.65834,
0.46964, 0.57113, 0.33739, 0.78320, 0.61860, 0.09328, 0.05437, 0.27422, 0.13480, 0.55982,
0.16836, 0.08466, 0.03538, 0.68691, 0.31945, 0.32272, 0.95414, 0.00067, 0.78717, 0.59659,
0.55605, 2.15305, 0.49415, 0.02424, 0.89349, 0.80630, 0.37284, 0.31772, 0.04112, 0.32601,
0.26923, 0.12576, 0.07903, 0.03152, 0.41632, 0.04060, 0.13879, 0.12846, 0.01667, 0.72244,
0.54765, 0.16667, 0.07035, 0.02681, 0.54523, 0.53271, 0.45727, 0.19646, 0.46272, 0.90750,
0.67340, 0.10823, 0.04123, 0.68070, 0.07748, 0.11075, 0.18493, 0.13457, 1.18247, 0.38154,
0.06569, 0.16240, 0.04554, 0.80698, 0.26408, 0.18152, 0.02194, 0.01732, 0.07088, 0.50737,
0.42889, 0.34414, 0.38134, 0.40327, 0.79952, 0.27456, 0.25624, 0.06428, 0.29408, 0.36317,
0.09802, 0.46832, 0.11789, 0.03405, 0.00989, 0.16255, 0.13362, 0.35968, 0.16359, 0.24217,
0.14683, 0.00237, 0.75408, 0.88643, 0.30986, 0.31571, 0.19583, 0.16891, 1.63331, 0.12351,
0.40976, 0.08514, 0.27008, 0.37772, 0.15724, 0.29163, 0.26879, 0.09789, 0.07231, 0.23268,
0.04717, 0.38958, 0.43365, 1.27750, 0.90610, 0.75378, 0.48882, 0.08835, 0.35536, 0.03113,
1.40151, 0.07059, 0.38457, 0.31422, 0.20869, 0.07405, 0.14701, 0.10404, 0.61411, 0.13585,
0.07557, 0.06579, 0.98282, 0.21078, 0.09336, 0.94949, 0.60938, 0.09486, 0.66561, 0.17303,
0.06193, 0.12158, 0.97936, 0.19998, 0.05866, 0.60070, 0.63519, 0.13193, 1.91133, 0.96716,
0.45503, 0.21104, 0.23938, 0.28714, 0.02044, 0.08414, 0.60970, 0.16313, 0.13837, 0.03554
]
@dataclass()
class Distribution:
    orderedSample: List[int] | List[float]
    unorderedSample: List[int] | List[float]
    len: int

    def __init__(self, unorderedSample: List[int] | List[float]):
        self.len = len(unorderedSample)
        self.unorderedSample = unorderedSample

        self.orderedSample =sorted(unorderedSample)

@dataclass()
class Intervals:
    intervals: List[float]
    a_0: float
    a_m: float
    m: int
    d: float

    def __init__(
        self,
        orderedSample: List[float],
        size,
        a_0: None | float = None,
        a_m: None | float = None,
    ):
        if a_0 == None:
            a_0 = min(orderedSample)
        if a_m == None:
            a_m = max(orderedSample)

        if a_m < a_0:
            raise Exception("Error data")

        d = a_m - a_0
        m = 1 + int(log2(size))
        print(m)
        self.intervals = []
        self.intervals.append(a_0)
        for i in range(1, m + 1):
            print(i)
            self.intervals.append(d / m + self.intervals[i - 1])
        self.a_m = a_m
        self.a_0 = a_0
        self.m = m
        self.d = d/m
        if len(self.intervals) <= m:
            raise Exception("Внимение! Где-то про***н интервал")


    def getIntervalNumber(self, number: float):
        if number == self.a_0:
            return 0
        if number == self.a_m:
            return len(self.intervals) - 2
        for i, num in enumerate(self.intervals):
            if number < num:
                return i - 1
        raise Exception("ВСЕ ПРОПАЛО. НЕ ВЕРНУЛСЯ НОМЕР ИНТЕРВАЛА")
def xiSquare(l):
    result = {3:7.8 ,4: 9.5, 5:11.1, 6: 12.6, 7: 14.1, 8:15.5}
    return result[l]

def kolmogKrit(a):
    result = {0.01: 1.63, 0.02:1.57, 0.05:1.36, 0.1: 1.22, 0.2: 1.07}
    return result[a]
@dataclass()
class FloatDistribution(Distribution):
    relativeFrequency: OrderedDict[int, float]
    frequency: OrderedDict[int, int]
    orderedSample: List[float]
    unorderedSample: List[float]
    teorProbability: List[float]
    intervals: Intervals
    middleIntervals: List[float]
    probabilityDensity: List[float]
    cumulativeDistribution: List[float]
    moment1: float
    moment2: float
    centralMoment2: float

    sampleVariance: float
    sampleMean: float

    empericalCumulativeDistribution: List[float]

    def __init__(self, unorderedSample: List[float], a_0: None | float = None, a_m: None| float = None):
        super(FloatDistribution, self).__init__(unorderedSample)

        self.intervals = Intervals(self.orderedSample, self.len, a_0=a_0, a_m = a_m)

        self.relativeFrequency = OrderedDict()
        self.frequency = OrderedDict()

        intervalNumber = 0
        intervalCount = 0
        i = 0
        while i < len(self.orderedSample):
            currInterval = self.intervals.getIntervalNumber(self.orderedSample[i])
            print("currInterval={},i={}, intervalCount={}, intervalNumber={}, intervalMin={}, intervalMax={}, number={}".format(currInterval, i, intervalCount, intervalNumber, 
                    self.intervals.intervals[intervalNumber], self.intervals.intervals[intervalNumber+1], self.orderedSample[i]))
            if currInterval <= intervalNumber:
                intervalCount += 1
            else:
                if intervalCount>0:
                    self.frequency[intervalNumber] = intervalCount 
                intervalCount = 1
                intervalNumber += 1
            i += 1
        if intervalCount>0:
            self.frequency[intervalNumber] = intervalCount

        for key, val in self.frequency.items():
            self.relativeFrequency[key] = val/ self.len


        self.middleIntervals = []
        for i in range(1, len(self.intervals.intervals)):
           self.middleIntervals.append((self.intervals.intervals[i] + self.intervals.intervals[i-1])/2  )

        self.moment1 = 0
        for i,val in self.relativeFrequency.items():
            self.moment1 += val * self.middleIntervals[i]
        self.sampleMean = self.moment1

        self.moment2 = 0
        for i,val in self.relativeFrequency.items():
            self.moment2 += val * ((self.middleIntervals[i])**2)
            print(self.moment2)
        print(self.relativeFrequency)
        print(self.middleIntervals)

        self.centralMoment2= self.moment2 - ((self.moment1)**2)

        self.sampleVariance = 0
        for i, val in self.relativeFrequency.items():
            self.sampleVariance+= ((self.middleIntervals[i] - self.moment1)**2) * val
        self.sampleVariance = self.sampleVariance -  ( (self.intervals.a_m - self.intervals.a_0) / self.intervals.m )**2 /12


@dataclass()
class BinomDistribution(IntegerDistribution):
    n: int
    p_cup: float
    valuesForTable: OrderedDict[int, float]

    def __init__(self, n: int, unorderedSample: List[int]):
        super(BinomDistribution, self).__init__(unorderedSample)

        self.n = n

        # Найдем оценку методом моментов
        self.p_cup = 0
        for x, w in self.relativeFrequency.items():
            self.p_cup += x*w
            print("x={}   w={}  p={}".format(x, w, self.p_cup))
        self.p_cup = self.p_cup / self.n
        if self.p_cup > 1:
            raise Exception("Как вероятность({}) может быть больше 1?".format(self.p_cup))

        # Найдем теоретические вероятности
        self.teorProbability = OrderedDict() 
        for i in self.relativeFrequency.keys():
            self.teorProbability[i]  =calcBinomProbability(i, self.p_cup, self.n) 
            if self.teorProbability[i] > 1:
                raise Exception("Как вероятность({}) может быть больше 1?".format(self.teorProbability[-1]))


        self.valuesForTable = OrderedDict()
        for key in self.relativeFrequency.keys():
            self.valuesForTable[key] = (self.len * (self.relativeFrequency[key] - self.teorProbability[key])**2) / self.teorProbability[key]


        print("--FIRST Distribution---")
        print(self.unorderedSample)
        print(self.orderedSample)
        print(self.frequency)
        print(self.relativeFrequency)
        print("p_cup={}".format(self.p_cup))
        print("teorProbability={}".format(self.teorProbability))
        print("values fot table={}".format(self.valuesForTable))

@dataclass()
class XI_EXP_Distribution(FloatDistribution):
    lambd: float
    dataForTable: list[float]

    # нужно для таблицы
    a: float
    b: float
    D_N: float
    D_NSQRTN: float
    xStar: float
    FxStar: float
    FNxStar: float
    FNxStarMinus0: float | None


    def __init__(self, unorderedSample: List[float], lambd: None | float = None):
        super(XI_EXP_Distribution, self).__init__(unorderedSample, a_0=0)

        self.lambd = 1/self.moment1
        print(self.lambd)

        self.a = min( unorderedSample )
        self.b = max( unorderedSample )

        self.empericalCumulativeDistribution = []
        self.cumulativeDistribution = []
        for i in range(0, self.len ):
            empCumDistrValue = (i+1)/(self.len) 
            self.empericalCumulativeDistribution.append( empCumDistrValue) 
            if lambd is not None:
                self.cumulativeDistribution.append(ExpRaspr.cumulativeDistribution(lambd, self.orderedSample[i]) )

        if lambd is None:
            for i in self.intervals.intervals:
                self.cumulativeDistribution.append(ExpRaspr.cumulativeDistribution(self.lambd, i) )

        self.probabilityDensity= []
        for i in self.intervals.intervals: 
            self.probabilityDensity.append(ExpRaspr.probabilityDensity(self.lambd, i) )

        print("########")
        print(self.cumulativeDistribution)
        print(self.empericalCumulativeDistribution)
        ####
        if lambd is not None:
            tmpMax = -999999
            mod2 = tmpMax
            self.xStar = 0
            self.FNxStarMinus0 = None
            print(self.empericalCumulativeDistribution)
            print(self.cumulativeDistribution)
            for index, value in enumerate(self.orderedSample):
                mod1 = abs( self.empericalCumulativeDistribution[index] - self.cumulativeDistribution[index] )
                if index > 0:
                    mod2 = abs( self.empericalCumulativeDistribution[index-1] - self.cumulativeDistribution[index] )
                maxVal = max(mod1, mod2)
                if maxVal > tmpMax:
                    tmpMax = maxVal

                    self.xStar = value 
                    self.FxStar = self.cumulativeDistribution[index]
                    self.FNxStar = self.empericalCumulativeDistribution[index]
                    self.D_N = tmpMax
                    self.D_NSQRTN = self.D_N * sqrt(self.len)
                    if index>0:
                        self.FNxStarMinus0 = self.empericalCumulativeDistribution[index-1]
                
            print("D_n = {}; D_NSQRTN= {}; xStar= {}; FxStar={}, FNxStar={}, FNxStarMinus0={}".format(
                self.D_N, self.D_NSQRTN, self.xStar, self.FxStar, self.FNxStar, self.FNxStarMinus0))

        ####

        self.teorProbability = []
        for i in range(1,len(self.relativeFrequency.keys())):
            self.teorProbability.append(self.cumulativeDistribution[i] - self.cumulativeDistribution[i-1] )
        self.teorProbability.append(1 - self.cumulativeDistribution[-2] )
        print(self.relativeFrequency)
        print("Интервалы:{}".format(self.intervals.intervals))
        print(self.frequency)
        print(self.teorProbability)
        print(self.cumulativeDistribution)

        self.dataForTable = []
        for i, val in enumerate(self.teorProbability):
            print(i)
            self.dataForTable.append(self.len * (self.relativeFrequency[i] - val)**2 / val)


        print("--SECOND Distribution---")
        print(self.unorderedSample)
        print(self.orderedSample)
        print("frequency:" + str(self.frequency))
        print("relativeFrequency" + str(self.relativeFrequency))

@dataclass()
class ThirdDistribution(FloatDistribution):
    dataForTable13: List[float]
    dataForTable: List[float]
    sigma: float

    def __init__(self, unorderedSample):
        super(ThirdDistribution, self).__init__(unorderedSample)

        self.sampleVariance = self.centralMoment2


        self.sigma = sqrt(self.sampleVariance)

        self.dataForTable13 = []
        for val in self.intervals.intervals:
            self.dataForTable13.append((val - self.sampleMean)/ self.sigma)


        self.cumulativeDistribution = []
        for i in self.intervals.intervals:
            self.cumulativeDistribution.append(stats.norm.cdf(i, self.sampleMean, self.sigma))

        self.probabilityDensity = []
        for i in self.intervals.intervals:
            val = stats.norm.pdf(i, self.sampleMean, self.sigma) 
            self.probabilityDensity.append(val)

        self.teorProbability = []
        for i in range(0, len(self.cumulativeDistribution)-2):
            if i == 0:
                self.teorProbability.append( self.cumulativeDistribution[1])
            else:
                self.teorProbability.append( self.cumulativeDistribution[i+1] - self.cumulativeDistribution[i]  )
        self.teorProbability.append( 1 - self.cumulativeDistribution[-2]  )


        self.dataForTable = []
        for i, val in enumerate(self.relativeFrequency):
            self.dataForTable.append(self.len * (self.relativeFrequency[i] - self.teorProbability[i])**2 / self.teorProbability[i])


            

        print("--Third Distribution---")
        print(self.unorderedSample)
        print(self.orderedSample)
        print("frequency:" + str(self.frequency))
        print("relativeFrequency" + str(self.relativeFrequency))

        print("table data 13: " + str(self.dataForTable13))
        print("cumulativeDistribution: " + str(self.cumulativeDistribution))
        print("probabilityDensity: " + str(self.probabilityDensity))
        print("teorProbability: " + str(self.teorProbability))

@dataclass()
class FourthDistribution(FloatDistribution):
    dataForTable: List[float]
    sigma: float

    def __init__(self, unorderedSample, a:float, b: float):
        super(FourthDistribution, self).__init__(unorderedSample, a_0 = a, a_m = b)

        self.sampleVariance = self.centralMoment2


        #self.sigma = sqrt(self.sampleVariance)

        #self.dataForTable13 = []
        #for val in self.intervals.intervals:
        #    self.dataForTable13.append((val - self.sampleMean)/ self.sigma)




        self.teorProbability = []
        for _ in enumerate(self.relativeFrequency):
            self.teorProbability.append(1/ len(self.relativeFrequency))


        self.dataForTable = []
        for i, val in enumerate(self.relativeFrequency):
            self.dataForTable.append(self.len * ((self.relativeFrequency[i] - self.teorProbability[i])**2) / self.teorProbability[i])
            print("i={}, len={}, w={}, p={}, result={}".format(i, self.len, self.relativeFrequency[i], self.teorProbability[i], self.dataForTable[-1]))
        print(self.dataForTable)


            

        print("--Third Distribution---")
        print(self.unorderedSample)
        print(self.orderedSample)
        print("frequency:" + str(self.frequency))
        print("relativeFrequency" + str(self.relativeFrequency))


@dataclass()
class FifthDistribution(FloatDistribution):
    dataForTable: List[float]
    sigma: float
    a: float
    b: float
    D_N: float
    D_NSQRTN: float
    xStar: float
    FxStar: float
    FNxStar: float
    FNxStarMinus0: float | None

    def __init__(self, unorderedSample, a:float, b: float):
        super(FifthDistribution, self).__init__(unorderedSample, a_0 = a, a_m = b)

        self.a = a
        self.b= b
        self.sampleVariance = self.centralMoment2

        self.empericalCumulativeDistribution = []
        self.cumulativeDistribution = []
        for i in range(0, self.len ):
            empCumDistrValue = (i+1)/(self.len) 
            self.empericalCumulativeDistribution.append( empCumDistrValue) 

            currInterval = self.intervals.getIntervalNumber(self.orderedSample[i])

            #cumDistrValue = (self.orderedSample[i] - self.intervals.intervals[currInterval])/
            #    (self.intervals.intervals[currInterval+1] - self.intervals.intervals[currInterval] ) 
            cumDistrValue = (self.orderedSample[i] - a)/(b-a) 
            print("currInterval={} ; orderedSample={}, cumDistrValue={}, empCumDistrValue={}".format(
                currInterval, self.orderedSample[i], cumDistrValue, empCumDistrValue))
            self.cumulativeDistribution.append( cumDistrValue)

            
        tmpMax = -999999
        mod2 = tmpMax
        self.xStar = 0
        self.FNxStarMinus0 = None
        print(self.empericalCumulativeDistribution)
        print(self.cumulativeDistribution)
        for index, value in enumerate(self.orderedSample):
            mod1 = abs( self.empericalCumulativeDistribution[index] - self.cumulativeDistribution[index] )
            if index > 0:
                mod2 = abs( self.empericalCumulativeDistribution[index-1] - self.cumulativeDistribution[index] )
            maxVal = max(mod1, mod2)
            if maxVal > tmpMax:
                tmpMax = maxVal

                self.xStar = value 
                self.FxStar = self.cumulativeDistribution[index]
                self.FNxStar = self.empericalCumulativeDistribution[index]
                self.D_N = tmpMax
                self.D_NSQRTN = self.D_N * sqrt(self.len)
                if index>0:
                    self.FNxStarMinus0 = self.empericalCumulativeDistribution[index-1]
            
        print("D_n = {}; D_NSQRTN= {}; xStar= {}; FxStar={}, FNxStar={}, FNxStarMinus0={}".format(
            self.D_N, self.D_NSQRTN, self.xStar, self.FxStar, self.FNxStar, self.FNxStarMinus0))

        #self.sigma = sqrt(self.sampleVariance)

        #self.dataForTable13 = []
        #for val in self.intervals.intervals:
        #    self.dataForTable13.append((val - self.sampleMean)/ self.sigma)




        self.teorProbability = []
        for _ in enumerate(self.relativeFrequency):
            self.teorProbability.append(1/ len(self.relativeFrequency))


        self.dataForTable = []
        for i, val in enumerate(self.relativeFrequency):
            self.dataForTable.append(self.len * (self.relativeFrequency[i] - self.teorProbability[i])**2 / self.teorProbability[i])


            

        print("--Third Distribution---")
        print(self.unorderedSample)
        print(self.orderedSample)
        print("frequency:" + str(self.frequency))
        print("relativeFrequency" + str(self.relativeFrequency))


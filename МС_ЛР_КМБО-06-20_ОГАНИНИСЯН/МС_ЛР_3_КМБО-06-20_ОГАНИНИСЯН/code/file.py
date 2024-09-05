from typing import List, Dict
from math import log2
from collections import OrderedDict
from scipy import stats
from ms import formatNumber, makeTable, makeLaTexIntStaticsticalSeries, calcBinomProbability, makeLaTexFloatStaticsticalSeries, ExpRaspr 
import camelot
from camelot.core import Table
from numpy import round_, sqrt, arange
import matplotlib.pyplot as plt
from PyPDF2 import PdfFileReader
from titlePage import generateTitlePage
from dataclasses import dataclass
from dotenv import load_dotenv
import re
from pylatex import  Subsection, NoEscape, basic, Figure
import os
from statistics import NormalDist

def printLatexSeventhNumber(unorderedSample: List[float], firstDistribution:FloatDistribution,
        secondDistribution: FloatDistribution, thirdDistribution: FloatDistribution, variant: int):
    subsection = Subsection('Задание 7')
    subsection = printLatexCommon(subsection, unorderedSample, variant)
    
    tableData = []
    tableData.append("pval")
    tableData.append(NoEscape("$a$"))
    tableData.append("Вывод")

    _, pval = stats.bartlett(firstDistribution.unorderedSample, 
            secondDistribution.unorderedSample, thirdDistribution.unorderedSample)
    tableData.append(formatNumber(pval))
    tableData.append(formatNumber(0.05))

    if pval < 0.05:
        tableData.append("НЕВЕРНА")
    else:
        tableData.append("ВЕРНА")

    subsection.append(NoEscape(r"\begin{changemargin}{-0cm}{0cm}\small{"))
    subsection.append(NoEscape("\\center"))
    subsection = makeTable(tableData, 3, 2, subsection )
    subsection.append(NoEscape(r"}\end{changemargin}"))

    with open("../latex/inc/generated/{}Number.tex".format(7), "w") as file:
        subsection.dump(file)
def printArowForFirstNumberFirstTable(tableData,
        firstDistribution: FloatDistribution, secondDistribution: FloatDistribution):
    tableData.append(formatNumber(firstDistribution.sampleMean))
    tableData.append(formatNumber(secondDistribution.sampleMean))
    tableData.append(formatNumber(firstDistribution.sampleVariance))
    tableData.append(formatNumber(secondDistribution.sampleVariance))
    tableData.append(formatNumber(firstDistribution.S_x2))
    tableData.append(formatNumber(secondDistribution.S_x2))
    TNN = (firstDistribution.sampleMean - secondDistribution.sampleMean)/ \
        (sqrt( firstDistribution.T_N_M_calc_coef + secondDistribution.T_N_M_calc_coef )) * \
        sqrt(( firstDistribution.len * secondDistribution.len * (firstDistribution.len + secondDistribution.len - 2) )/ \
        (firstDistribution.len + secondDistribution.len))
    tableData.append(formatNumber(TNN))

    return tableData,TNN

def printArowForFirstNumberSecondTable(tableData,
        firstDistribution: FloatDistribution, secondDistribution: FloatDistribution, TNN):

    TNN = abs(TNN)
    tableData.append(formatNumber(TNN))

    t_kr: float = stats.t.ppf(1-0.05, 2*firstDistribution.len - 2)
    tableData.append(formatNumber(t_kr))

    if TNN > t_kr:
        tableData.append("НЕВЕРНА")
    else:
        tableData.append("ВЕРНА")

    return tableData

def printArowForThirdNumberTable(tableData,
        firstDistribution: FloatDistribution, secondDistribution: FloatDistribution):

    _,pval = stats.ttest_ind(firstDistribution.unorderedSample, secondDistribution.unorderedSample, equal_var=True)
    tableData.append(formatNumber(pval))
    tableData.append(formatNumber(0.05))

    

    if pval < 0.05:
        tableData.append("НЕВЕРНА")
    else:
        tableData.append("ВЕРНА")

    return tableData

def printArowForFourthNumberTable(tableData,
        firstDistribution: FloatDistribution, secondDistribution: FloatDistribution):

    _,pval = stats.ttest_ind(firstDistribution.unorderedSample, secondDistribution.unorderedSample, equal_var=False)
    tableData.append(formatNumber(pval))
    tableData.append(formatNumber(0.05))

    

    if pval < 0.05:
        tableData.append("НЕВЕРНА")
    else:
        tableData.append("ВЕРНА")

    return tableData

def printArowForSixthNumberFirstTable(tableData,
        firstDistribution: FloatDistribution, secondDistribution: FloatDistribution):
    tableData.append(formatNumber(firstDistribution.S_x2))
    tableData.append(formatNumber(secondDistribution.S_x2))
    k1 = k2 = firstDistribution.len - 1
    tableData.append(formatNumber(k1))
    tableData.append(formatNumber(k2))
    FNN = max(firstDistribution.S_x2, secondDistribution.S_x2) /\
        min(firstDistribution.S_x2, secondDistribution.S_x2) 
    tableData.append(formatNumber(FNN))

    return tableData, FNN, k1, k2

def printArowForSixthNumberSecondTable(tableData,
        firstDistribution: FloatDistribution, secondDistribution: FloatDistribution, FNM, k1, k2):

    tableData.append(formatNumber(FNM))

    z_a: float = stats.f.ppf(1-0.05/2, k1, k2)
    print(f"z_a: {z_a}")
    tableData.append(formatNumber(z_a))

    if FNM > z_a:
        tableData.append("НЕВЕРНА")
    else:
        tableData.append("ВЕРНА")

    return tableData
def printLatexSecondNumber(unorderedSample: List[float], firstDistribution:FloatDistribution,
        secondDistribution: FloatDistribution, thirdDistribution: FloatDistribution, variant: int):
    subsection = Subsection('Задание 2')
    subsection = printLatexCommon(subsection, unorderedSample, variant)
    
    tableData = []
    tableData.append(NoEscape("$S_{\\text{общ}}$"))
    tableData.append(NoEscape("$S_{\\text{факт}}$"))
    tableData.append(NoEscape("$S_{\\text{ост}}$"))
    tableData.append(NoEscape("$S_{\\text{факт}}^2$"))
    tableData.append(NoEscape("$S_{\\text{ост}}^2$"))
    tableData.append(NoEscape("$k_1$"))
    tableData.append(NoEscape("$k_2$"))
    tableData.append(NoEscape("$F_{N,m}$"))

    mean_u = 0
    mean_u = sum(firstDistribution.unorderedSample)
    mean_u += sum(secondDistribution.unorderedSample)
    mean_u += sum(thirdDistribution.unorderedSample)
    mean_u *= 1/(3* firstDistribution.len)

    S_gen = 0
    S_gen = sum(((x-mean_u)**2) for x in firstDistribution.unorderedSample)
    S_gen += sum(((x-mean_u)**2) for x in secondDistribution.unorderedSample)
    S_gen += sum(((x-mean_u)**2) for x in thirdDistribution.unorderedSample)

    S_fact = 0
    S_fact = sum(((firstDistribution.sampleMean -mean_u)**2) for _ in firstDistribution.unorderedSample)
    S_fact += sum(((secondDistribution.sampleMean -mean_u)**2) for _ in secondDistribution.unorderedSample)
    S_fact += sum(((thirdDistribution.sampleMean -mean_u)**2) for _ in thirdDistribution.unorderedSample)
    S_fact *= firstDistribution.len

    S_dif = S_gen - S_fact

    S2_fact = S_fact/(3-1)
    S2_dif = S_dif/(3* (firstDistribution.len - 1))

    k1= 3-1
    k2 = 3*(firstDistribution.len - 1)

    FNM = S2_fact/S2_dif

    print(f"2. mean_u={mean_u}  S_gen={S_gen} S_fact={S_fact} S_dif={S_dif} S2_fact={S2_fact} S2_dif={S2_dif}")

    tableData.append(formatNumber(S_gen))
    tableData.append(formatNumber(S_fact))
    tableData.append(formatNumber(S_dif))
    tableData.append(formatNumber(S2_fact))
    tableData.append(formatNumber(S2_dif))
    tableData.append(formatNumber(k1))
    tableData.append(formatNumber(k2))
    tableData.append(formatNumber(FNM))


    subsection.append(NoEscape(r"\begin{changemargin}{-0cm}{0cm}\small{"))
    subsection.append(NoEscape("\\center"))
    subsection = makeTable(tableData, 8, 2, subsection )
    subsection.append(NoEscape(r"}\end{changemargin}"))

    tableData = []
    tableData.append(NoEscape("$F_{N,m}$"))
    tableData.append(NoEscape("$a$"))
    tableData.append(NoEscape("$t_{\\text{кр}} (k_1, k_2)$"))
    tableData.append("Вывод")

    tableData.append(formatNumber(FNM))
    tableData.append(formatNumber(0.05))
    F_krit: float = stats.f.ppf(0.95, k1, k2)
    tableData.append(formatNumber(F_krit))

    if FNM <= F_krit:
        tableData.append("ВЕРНА")
    else:
        tableData.append("НЕВЕРНА")


    subsection.append(NoEscape(r"\begin{changemargin}{-0cm}{0cm}\small{"))
    subsection.append(NoEscape("\\center"))
    subsection = makeTable(tableData, 4, 2, subsection )
    subsection.append(NoEscape(r"}\end{changemargin}"))

    with open("../latex/inc/generated/{}Number.tex".format(2), "w") as file:
        subsection.dump(file)

def printLatexCommon(subsection, unorderedSample: List[float], variant: int):
    subsection.append("V={}".format(variant))
    subsection.append(NoEscape("$\\quad \\{ u_{ij}|1 \\le i \\le N, 1\\le j \\le 3 \\}, N=16, a =0.05 $\n\n"))
    subsection.append(NoEscape(r"\begin{changemargin}{0cm}{0cm}\small{"))
    subsection.append(NoEscape("\\center"))
    makeTable(
        unorderedSample,
        3,
        int(len(unorderedSample)/3),
        subsection,
    )
    subsection.append(NoEscape(r"}\end{changemargin}"))
    return subsection

def printLatexThirdNumber(unorderedSample: List[float], firstDistribution:FloatDistribution,
        secondDistribution: FloatDistribution, thirdDistribution: FloatDistribution, variant: int):
    subsection = Subsection('Задание 3')
    subsection = printLatexCommon(subsection, unorderedSample, variant)
    
    tableData = []
    tableData.append("Столбцы")
    tableData.append(NoEscape("pval"))
    tableData.append(NoEscape("$a$"))
    tableData.append("Вывод")

    tableData.append(NoEscape("$(1,2)$"))
    tableData = printArowForThirdNumberTable(tableData, firstDistribution, secondDistribution )

    tableData.append(NoEscape("$(1,3)$"))
    tableData = printArowForThirdNumberTable(tableData, firstDistribution, thirdDistribution )

    tableData.append(NoEscape("$(2,3)$"))
    tableData = printArowForThirdNumberTable(tableData, secondDistribution, thirdDistribution )


    subsection.append(NoEscape(r"\begin{changemargin}{-0cm}{0cm}\small{"))
    subsection.append(NoEscape("\\center"))
    subsection = makeTable(tableData, 4, 4, subsection )
    subsection.append(NoEscape(r"}\end{changemargin}"))



    with open("../latex/inc/generated/{}Number.tex".format(3), "w") as file:
        subsection.dump(file)
def printLatexSixthNumber(unorderedSample: List[float], firstDistribution:FloatDistribution,
        secondDistribution: FloatDistribution, thirdDistribution: FloatDistribution, variant: int):
    subsection = Subsection('Задание 6')
    subsection = printLatexCommon(subsection, unorderedSample, variant)
    
    tableData = []
    tableData.append("Столбцы")
    tableData.append(NoEscape("$S_{1}^2$"))
    tableData.append(NoEscape("$S_{2}^2$"))
    tableData.append(NoEscape("$k_1$"))
    tableData.append(NoEscape("$k_2$"))
    tableData.append(NoEscape("$F_{N,M}$"))

    tableData.append(NoEscape("$(1,2)$"))
    tableData, FNM12, k1, k2 = printArowForSixthNumberFirstTable(tableData, firstDistribution, secondDistribution)

    tableData.append(NoEscape("$(1,3)$"))
    tableData, FNM13, k1, k2 = printArowForSixthNumberFirstTable(tableData, firstDistribution, thirdDistribution)

    tableData.append(NoEscape("$(2,3)$"))
    tableData, FNM23, k1, k2 = printArowForSixthNumberFirstTable(tableData, secondDistribution, thirdDistribution)

    subsection.append(NoEscape(r"\begin{changemargin}{-1.5cm}{0cm}\small{"))
    subsection.append(NoEscape("\\center"))
    subsection = makeTable(tableData, 6, 4, subsection )
    subsection.append(NoEscape(r"}\end{changemargin}"))

    tableData = []
    tableData.append("Столбцы")
    tableData.append(NoEscape("$F_{N,N}$"))
    tableData.append(NoEscape("$z_a$"))
    tableData.append("Вывод")

    tableData.append(NoEscape("$(1,2)$"))
    tableData = printArowForSixthNumberSecondTable(tableData, firstDistribution, secondDistribution, FNM12, k1, k2)

    tableData.append(NoEscape("$(1,3)$"))
    tableData = printArowForSixthNumberSecondTable(tableData, firstDistribution, thirdDistribution, FNM13, k1, k2)

    tableData.append(NoEscape("$(2,3)$"))
    tableData = printArowForSixthNumberSecondTable(tableData, secondDistribution, thirdDistribution, FNM23, k1, k2)


    subsection.append(NoEscape(r"\begin{changemargin}{-0cm}{0cm}\small{"))
    subsection.append(NoEscape("\\center"))
    subsection = makeTable(tableData, 4, 4, subsection )
    subsection.append(NoEscape(r"}\end{changemargin}"))


    with open("../latex/inc/generated/{}Number.tex".format(6), "w") as file:
        subsection.dump(file)
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
        self.intervals = []
        self.intervals.append(a_0)
        for i in range(1, m + 1):
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

@dataclass()
class FloatDistribution(Distribution):
    relativeFrequency: OrderedDict[int, float]
    frequency: OrderedDict[int, int]
    orderedSample: List[float]
    unorderedSample: List[float]
    teorProbability: List[float]
    middleIntervals: List[float]
    probabilityDensity: List[float]
    cumulativeDistribution: List[float]
    moment1: float
    moment2: float
    centralMoment2: float

    sampleVariance: float
    sampleMean: float

    empericalCumulativeDistribution: List[float]
    S_x: float
    S_x2 : float
    T_N_M_calc_coef: float

    def __init__(self, unorderedSample: List[float]): 
        super(FloatDistribution, self).__init__(unorderedSample)

        self.sampleMean = sum(self.unorderedSample)/self.len 
        self.sampleVariance = sum(x**2 for x in self.unorderedSample)/self.len 
        self.S_x = self.len * (self.sampleVariance - (self.sampleMean**2))
        self.S_x2 = (self.len/(self.len-1)) * (self.sampleVariance - (self.sampleMean**2))
        self.S_x2 = self.S_x / (self.len - 1)
        self.T_N_M_calc_coef = self.len * (self.sampleVariance - (self.sampleMean**2))
def printLatexFirstNumber(unorderedSample: List[float], firstDistribution:FloatDistribution,
        secondDistribution: FloatDistribution, thirdDistribution: FloatDistribution, variant: int):
    subsection = Subsection('Задание 1')
    subsection = printLatexCommon(subsection, unorderedSample, variant)
    
    tableData = []
    tableData.append("Столбцы")
    tableData.append(NoEscape("$\\overline{x}$"))
    tableData.append(NoEscape("$\\overline{y}$"))
    tableData.append(NoEscape("$\\overline{x^2}$"))
    tableData.append(NoEscape("$\\overline{y^2}$"))
    tableData.append(NoEscape("$S_{x}^2$"))
    tableData.append(NoEscape("$S_{y}^2$"))
    tableData.append(NoEscape("$T_{N,N}$"))

    tableData.append(NoEscape("$(1,2)$"))
    tableData, TNN12 = printArowForFirstNumberFirstTable(tableData, firstDistribution, secondDistribution)

    tableData.append(NoEscape("$(1,3)$"))
    tableData, TNN13 = printArowForFirstNumberFirstTable(tableData, firstDistribution, thirdDistribution)

    tableData.append(NoEscape("$(2,3)$"))
    tableData, TNN23 = printArowForFirstNumberFirstTable(tableData, secondDistribution, thirdDistribution)

    subsection.append(NoEscape(r"\begin{changemargin}{-1.5cm}{0cm}\small{"))
    subsection.append(NoEscape("\\center"))
    subsection = makeTable(tableData, 8, 4, subsection )
    subsection.append(NoEscape(r"}\end{changemargin}"))



    tableData = []
    tableData.append("Столбцы")
    tableData.append(NoEscape("$|T_{N,N}|$"))
    tableData.append(NoEscape("$t_{\\text{кр}} (2N-2)$"))
    tableData.append("Вывод")

    tableData.append(NoEscape("$(1,2)$"))
    tableData = printArowForFirstNumberSecondTable(tableData, firstDistribution, secondDistribution, TNN12)

    tableData.append(NoEscape("$(1,3)$"))
    tableData = printArowForFirstNumberSecondTable(tableData, firstDistribution, thirdDistribution, TNN13)

    tableData.append(NoEscape("$(2,3)$"))
    tableData = printArowForFirstNumberSecondTable(tableData, secondDistribution, thirdDistribution, TNN23)


    subsection.append(NoEscape(r"\begin{changemargin}{-0cm}{0cm}\small{"))
    subsection.append(NoEscape("\\center"))
    subsection = makeTable(tableData, 4, 4, subsection )
    subsection.append(NoEscape(r"}\end{changemargin}"))



    with open("../latex/inc/generated/{}Number.tex".format(1), "w") as file:
        subsection.dump(file)


def main():
    load_dotenv()
    variant = os.getenv('VARIANT')
    group = os.getenv('GROUP')
    fio = os.getenv('FIO')
    if variant == None or group == None or fio == None:
        raise Exception(("\nНе задан файл .env с необходимыми переменными.\n"
                         "Создайте файл .env и задайте переменные VARIANT, FIO, GROUP. Пример:\n"
                         "VARIANT=15\nGROUP=КМБО-0X-XX\nFIO=Петров И.А.")) 

    variant = int(variant)
    print(variant)
    unorderedSample = readNumber(variant)
    firstDistribution, secondDistribution, thirdDistribution= calculateNumber(unorderedSample)
    printLatexFirstNumber(unorderedSample, firstDistribution, secondDistribution, thirdDistribution, variant)
    printLatexSecondNumber(unorderedSample, firstDistribution, secondDistribution, thirdDistribution, variant)
    printLatexThirdNumber(unorderedSample, firstDistribution, secondDistribution, thirdDistribution, variant)
    printLatexFourthNumber(unorderedSample, firstDistribution, secondDistribution, thirdDistribution, variant)
    printLatexFifthNumber(unorderedSample, firstDistribution, secondDistribution, thirdDistribution, variant)
    printLatexSixthNumber(unorderedSample, firstDistribution, secondDistribution, thirdDistribution, variant)
    printLatexSeventhNumber(unorderedSample, firstDistribution, secondDistribution, thirdDistribution, variant)

    titlePagePdf = r'../latex/inc/generated'
    titlePageTemplate = r'../../titlePageTemplate.docx'
    generateTitlePage(variant, 4, "Проверка статистических гипотез о математическом ожидании", 
            "и дисперсии нормально распределенных случайных величин", fio, group,
            titlePageTemplate, 'title.pdf', titlePagePdf);


main()
def printLatexFourthNumber(unorderedSample: List[float], firstDistribution:FloatDistribution,
        secondDistribution: FloatDistribution, thirdDistribution: FloatDistribution, variant: int):
    subsection = Subsection('Задание 4')
    subsection = printLatexCommon(subsection, unorderedSample, variant)
    
    tableData = []
    tableData.append("Столбцы")
    tableData.append(NoEscape("pval"))
    tableData.append(NoEscape("$a$"))
    tableData.append("Вывод")

    tableData.append(NoEscape("$(1,2)$"))
    tableData = printArowForFourthNumberTable(tableData, firstDistribution, secondDistribution )

    tableData.append(NoEscape("$(1,3)$"))
    tableData = printArowForFourthNumberTable(tableData, firstDistribution, thirdDistribution )

    tableData.append(NoEscape("$(2,3)$"))
    tableData = printArowForFourthNumberTable(tableData, secondDistribution, thirdDistribution )


    subsection.append(NoEscape(r"\begin{changemargin}{-0cm}{0cm}\small{"))
    subsection.append(NoEscape("\\center"))
    subsection = makeTable(tableData, 4, 4, subsection )
    subsection.append(NoEscape(r"}\end{changemargin}"))

    with open("../latex/inc/generated/{}Number.tex".format(4), "w") as file:
        subsection.dump(file)
def printLatexFifthNumber(unorderedSample: List[float], firstDistribution:FloatDistribution,
        secondDistribution: FloatDistribution, thirdDistribution: FloatDistribution, variant: int):
    subsection = Subsection('Задание 5')
    subsection = printLatexCommon(subsection, unorderedSample, variant)
    
    tableData = []
    tableData.append("pval")
    tableData.append(NoEscape("$a$"))
    tableData.append("Вывод")

    _,pval = stats.f_oneway(firstDistribution.unorderedSample, 
            secondDistribution.unorderedSample, thirdDistribution.unorderedSample)
    tableData.append(formatNumber(pval))
    tableData.append(formatNumber(0.05))

    if pval < 0.05:
        tableData.append("НЕВЕРНА")
    else:
        tableData.append("ВЕРНА")

    subsection.append(NoEscape(r"\begin{changemargin}{-0cm}{0cm}\small{"))
    subsection.append(NoEscape("\\center"))
    subsection = makeTable(tableData, 3, 2, subsection )
    subsection.append(NoEscape(r"}\end{changemargin}"))

    with open("../latex/inc/generated/{}Number.tex".format(5), "w") as file:
        subsection.dump(file)


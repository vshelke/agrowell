import pandas as pd
import numpy as np
import numpy.polynomial.polynomial as poly
import math
# Business logic here

def getGrowthRate(coef_present, coef_previous):
    return (abs(coef_present[0] - coef_previous[0]) / coef_previous[0])

def getTranspirationRate(data):
    minTemp = data['temperature'].min()
    maxTemp = data['temperature'].max()
    minHumi = data['humidity'].min()
    avgHumi = data['humidity'].mean()
    avgTemp = data['temperature'].mean()
    avgMoist = data['moisture'].mean()
    ahLow = (216.7 * 6.112 * (minHumi/100) * (math.exp((17.62 * minTemp)/(243.12+minTemp)) / (273.15 + minTemp)))
    ahHigh = (216.7 * 6.112 * (avgHumi) * (math.exp((17.62 * avgTemp)/(243.12+avgTemp)) / (273.15 + avgTemp)))
    rate = abs(avgMoist - ahHigh) * 0.15    # 300/2000 = 0.15
    return rate

def getSuitability(data):
    return ((20/data['temperature'].mean()) + (70/data['humidity'].mean()))/2 

def getPredicted(chunk):
    x = chunk['time']
    y = chunk['moisture']
    coefs = poly.polyfit(x, y, 1)
    yfit = poly.Polynomial(coefs)
    return yfit(x), coefs
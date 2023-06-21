import pandas as pd
from haversine import haversine

dataCoords = pd.read_csv("data/koordinaten.csv", delimiter=';')
referenzCoords = pd.read_csv("data/ganzeFahrtReferenz.tcsv", delimiter=';')


# Format Anpassung bei "TIME, Messstartpunkt wird gesetzt, und Index reset zu 0
def sortdata(dataframe):
    dataframe['TIME'] = dataframe['TIME'].str[:19]
    dataframe = dataframe.loc[dataframe["TIME"] > "2022-12-28T08:36:19"]
    dataframe = dataframe.reset_index(drop=True)
    return dataframe


# Zeitüberlappung für genauen Messwert. Die Referenz "TIME" passt sich der von Toll-Now an
def timefiltering(dataframe):
    mask = dataframe["TIME"].isin(tollnow["TIME"])
    dataframe = dataframe[mask]
    dataframe = dataframe.reset_index(drop=True)
    return dataframe


tollnow = sortdata(dataCoords)
referenzCoords = sortdata(referenzCoords)

referenz = timefiltering(referenzCoords)

# Erstelle Subset nur mit den Werten von LAT und LON
tollNowSubset = tollnow.loc[:, ["LAT", "LON", "TIME"]]
referenzSubset = referenz.loc[:, ["LAT", "LON", "TIME"]]


def createPoint(row):
    point = (row["LAT"], row["LON"])
    return point


# Wende die Methode createPoint() für jede Zeile in DF an und speicher den Punkt in einer neuen Spalte
tollNowSubset["TollNow Point"] = tollNowSubset.apply(createPoint, axis=1)
referenzSubset["Referenz Point"] = referenzSubset.apply(createPoint, axis=1)


def haversineFormula(row):
    result = haversine(row["TollNow Point"], row["Referenz Point"])
    return result


# Erstelle ein neues DF mit den Werten von tollNow und referenz
haversineDF = pd.merge(tollNowSubset, referenzSubset, on="TIME")

# Delete the LAT and LON columns
haversineDF = haversineDF.drop(columns=["LAT_x", "LON_x", "LAT_y", "LON_y"])

# Wende Methode haversineFormula() für jede Zeile an, und speicher das Ergebnis in einer neuen Spalte ab
haversineDF["Result"] = haversineDF.apply(haversineFormula, axis=1)
#haversineDist.to_csv("data/haversineDistance.csv")


def avgabweichung():
    avg = haversineDF.loc[:, 'Abweichung beider Distanzen'].mean()
    return print("Durchschnittliche Abweichung:", avg)


def maxminvalue(column, keyword):
    if keyword == max:
        return print(f"Maximaler Wert in: {column}: ", haversineDist[f"{column}"].max())
    elif keyword == min:
        return print(f"Minimaler Wert in: {column}: ", haversineDist[f"{column}"].min())


def lenwithcondition(column, op, value):
    if op == "<":
        return len(haversineDist[haversineDist[column] < value])
    elif op == ">":
        return len(haversineDist[haversineDist[column] > value])


avgabweichung()
maxminvalue("Abweichung beider Distanzen", min)
lenwithcondition("Abweichung beider Distanzen", "<", 1.0)




#haversineDist.to_csv("data/haversineDistance.csv")












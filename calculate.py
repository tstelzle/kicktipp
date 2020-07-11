import csv
import constant


def readFile():
    file = open("spieltage.csv", "r")
    spieltage = {}
    with file:
        reader = csv.DictReader(file)
        line_count = 0
        spieltagID = 0
        spieltag = {}
        for row in reader:
            if row['name'].find('Spieltag') != -1:
                spieltage[spieltagID] = spieltag
                spieltagID += 1
                spieltag = {}
                spieltag[row['name']] = row
            elif not row['name'] or row['name'] == "name":
                continue
            else:
                spieltag[row['name']] = row
            line_count += 1
        spieltage[spieltagID] = spieltag
    return spieltage


def prinDict(dict: dict):
    for spieltag, tabelle in dict.items():
        print('Spieltag ' + str(spieltag) + ":")
        for key, value in tabelle.items():
            print(value)


def getValues(result: str):
    if (not result):
        return None
    else:
        splitter = result.find(':')
        return [int(result[:splitter]), int(result[splitter + 1:])]


def getResult(state, target):
    stateValues = getValues(state)

    if not stateValues:
        return constant.NO_TIP

    stateHome = stateValues[0]
    stateGuest = stateValues[1]

    targetValues = getValues(target)
    targetHome = targetValues[0]
    targetGuest = targetValues[1]

    if (state == target):
        return constant.RIGHT
    elif (targetGuest == targetHome and stateHome == stateGuest):
        return constant.TIE_TREND
    elif (stateHome - stateGuest == targetHome - targetGuest):
        return constant.RATIO
    elif (targetHome > targetGuest and stateHome > stateGuest):
        return constant.WIN_TREND
    elif (targetGuest > targetHome and stateGuest > stateHome):
        return constant.WIN_TREND
    else:
        return constant.WRONG


def calculateNewTable(dict: dict):
    overall = {}
    for spieltag, table in dict.items():
        ref = {}
        for player, values in table.items():
            if player == "Spieltag " + str(spieltag):
                ref = table[player]
            else:
                for event, tipp in values.items():
                    if event == 'name':
                        continue
                    else:
                        if player not in overall:
                            overall[player] = 0
                        else:
                            value = getResult(values[event], ref[event])
                            overall[player] = int(overall[player]) + value
    return overall


def main():
    spieltage = readFile()
    overall = calculateNewTable(spieltage)
    overall_sorted = sorted(overall.items(), key=lambda x: x[1], reverse=True)
    for value in overall_sorted:
        print(value)

if __name__ == "__main__":
    main()

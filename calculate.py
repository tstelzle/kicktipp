import csv
import constant

import main as module_main


def read_file():
    kicktipp_group = module_main.read_kicktipp_group()
    file = open("spieltage_" + kicktipp_group + ".csv", "r")
    spieltage = {}
    with file:
        reader = csv.DictReader(file)
        line_count = 0
        spieltag_id = 0
        spieltag = {}
        for row in reader:
            if row['name'].find('Spieltag') != -1:
                spieltage[spieltag_id] = spieltag
                spieltag_id += 1
                spieltag = {row['name']: row}
            elif not row['name'] or row['name'] == "name":
                continue
            else:
                spieltag[row['name']] = row
            line_count += 1
        spieltage[spieltag_id] = spieltag
    return spieltage


def print_dict(data_dict: dict):
    for spieltag, tabelle in data_dict.items():
        print('Spieltag ' + str(spieltag) + ":")
        for key, value in tabelle.items():
            print(value)


def get_values(result: str):
    if not result:
        return None
    elif result == '-:-':
        return None
    else:
        splitter = result.find(':')
        return [int(result[:splitter]), int(result[splitter + 1:])]


def get_result(state, target):
    state_values = get_values(state)

    if not state_values:
        return constant.NO_TIP

    state_home = state_values[0]
    state_guest = state_values[1]

    target_values = get_values(target)
    target_home = target_values[0]
    target_guest = target_values[1]

    if state == target:
        return constant.RIGHT
    elif target_guest == target_home and state_home == state_guest:
        return constant.TIE_TREND
    elif state_home - state_guest == target_home - target_guest:
        return constant.RATIO
    elif target_home > target_guest and state_home > state_guest:
        return constant.WIN_TREND
    elif target_guest > target_home and state_guest > state_home:
        return constant.WIN_TREND
    else:
        return constant.WRONG


def calculate_new_table(data_dict: dict):
    overall = {}
    for spieltag, table in data_dict.items():
        ref = {}
        for player, values in table.items():
            if player == "Spieltag " + str(spieltag):
                ref = table[player]
            else:
                for event, tipp in values.items():
                    if event == 'name':
                        overall[tipp] = 0
                    else:
                        value = get_result(values[event], ref[event])
                        overall[player] = int(overall[player]) + value
    return overall


def main():
    spieltage = read_file()
    overall = calculate_new_table(spieltage)
    overall_sorted = sorted(overall.items(), key=lambda x: x[1], reverse=True)
    for value in overall_sorted:
        print(value)


if __name__ == "__main__":
    main()

import pandas as pd
import matplotlib.pyplot as plt
import os

import main as module_main
import calculate as module_calculate


def calculate_player_spieltag_stats(data_dict: dict):
    player_stats = {}
    for spieltag, table in data_dict.items():
        ref = {}
        for player, values in table.items():
            if player == "Spieltag " + str(spieltag):
                ref = table[player]
                continue
            else:
                spieltags_sum = 0
                for event, tipp in values.items():
                    if event == 'name':
                        if tipp not in player_stats.keys():
                            player_stats[tipp] = []
                    else:
                        value = module_calculate.get_result(values[event], ref[event])
                        spieltags_sum += value
            player_stats[player].append(spieltags_sum)

    return player_stats


def graph_spieltags_points(data_dict: dict, x_size: int, y_size: int, apply_range_x: bool, graph_name: str,
                           figsize: bool):
    df = pd.DataFrame(data=data_dict)
    kicktipp_group = module_main.read_kicktipp_group()
    if figsize:
        plt.figure(figsize=(x_size, y_size))
    if apply_range_x:
        plt.yticks(range(df.min().min(), df.max().max() + 1))
    plt.xticks(range(1, 35))
    plt.xlabel('Spieltage')
    plt.ylabel('Punkte')
    plt.title('Kicktipp Gruppe: ' + kicktipp_group)

    for player in data_dict.keys():
        plt.plot(df[player].index + 1, df[player], label=player)

    plt.legend(loc=2)
    plt.savefig('graphs/spieltag_points_' + kicktipp_group + "_" + graph_name, dpi=160)
    plt.show()

    print(df)


def add_up_points(data_dict: dict):
    add_up_data_dict = {}
    for player, scores in data_dict.items():
        add_up_scores = []
        for i in range(1, len(scores) + 1):
            splitted_scores = scores[:i]
            add_up_scores.append(sum(splitted_scores))
        add_up_data_dict[player] = add_up_scores

    return add_up_data_dict


def create_graph_dir():
    directory_created = os.path.isdir('graphs')
    if not directory_created:
        os.mkdir('graphs')


def main():
    create_graph_dir()

    data_dict = module_calculate.read_file()

    player_stats = calculate_player_spieltag_stats(data_dict)
    graph_spieltags_points(player_stats, 50, 10, True, 'spieltage', False)

    add_up_data_dict = add_up_points(player_stats)
    graph_spieltags_points(add_up_data_dict, 10, 10, False, 'overall', False)


if __name__ == "__main__":
    main()

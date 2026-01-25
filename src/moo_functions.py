import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import itertools as iter
import math
from sklearn.preprocessing import MinMaxScaler
from tqdm import tqdm

def total_outfits(tops, bottoms, alternate_occasion=None):

    """ Calculates the total number of possible outfits for a given suitcase.
    Args: 
        tops: dictionary of tops
        bottomos: dictionary of bottoms
    Returns: total_num_outfits (int): # of outfits that can be made with given rules
    """

    # clear previous matches
    for top in tops: top["Matches"] = []
    for bottom in bottoms: bottom["Matches"] = []
    
    #set counter
    total_num_outfits = 0

    # loop through each combo and establish rules
    for top in tops:
        if alternate_occasion is None or top[alternate_occasion] == "Yes":
            for bottom in bottoms:
                if alternate_occasion is None or bottom[alternate_occasion] == "Yes":
                    if not (bottom["Patterned?"] != "No" and top["Patterned?"] != "No"):
                        if bottom["Color"] in ["White", "Beige", "Black", "Grey"] or top["Color"] in ["White", "Beige", "Black", "Grey"] or bottom["Color"] == top["Color"]:
                            if top["Length"] - bottom["Highest Rise"] >= 0:
                                total_num_outfits += 1
                                top["Matches"].append(bottom["Name"])
                                bottom["Matches"].append(top["Name"])
    return total_num_outfits

def convert_binary_array_to_item_dicts(array, num_tops, num_bottoms, all_clothes_list):
    
    """ Retrieves the clothing info dictionaries for the clothing times present in a given solution.
    Args:
        array: Solution array (e.g. [0, 0, 1, 1, 0, 1, ...]
        num_tops, num_bottoms (int): number of tops and bottoms respectively in original suitcase
        all_clothes_list (list): List with all original clothing info dictionaries
    Returns: 
        tops, bottoms (list): list of clothing info dictionaries for the tops and bottoms that are in this solution's suitcase
    """

    tops = []
    bottoms = []
    
    for i in range(num_tops):
        if array[:num_tops][i] == 1:
            tops.append(all_clothes_list[i])

    for i in range(num_bottoms):
        if array[num_tops:][i] == 1:
            bottoms.append(all_clothes_list[i+num_tops])

    return tops, bottoms

def get_dict_vals(tops, bottoms, key):
    vals = [x for x in [d[key] for d in tops if key in d]] + [x for x in [d[key] for d in bottoms if key in d]]
    return vals

def evaluate_solution_metrics(array, num_tops, num_bottoms, all_clothes_list, normalize=None):

    """ Generates the three objective metrics (outfits_lost, volume, liking_diff) for a given solution suitcase
    Args:
        array: Solution array (e.g. [0, 0, 1, 1, 0, 1, ...]
        num_tops, num_bottoms (int): number of tops and bottoms respectively in original suitcase
        all_clothes_list (list): List with all original clothing info dictionaries
        normalize (list): Optional, to be used if you want to retrieve normalized metrics. Would be a list with the max values
        for each objective present across all solutions.
    Returns (tuple): num_outfits_lost, total_volume, liking (all ints)
        
    """

    tops, bottoms = convert_binary_array_to_item_dicts(array, num_tops, num_bottoms, all_clothes_list)

    
    # a solution that removes more outfits compared to the full suitcase will be penalized
    total_possible_outfits = total_outfits(all_clothes_list[:num_tops], all_clothes_list[num_tops:])
    num_outfits_lost = total_possible_outfits - total_outfits(tops, bottoms)
    if normalize:
        num_outfits_lost = num_outfits_lost / normalize[0]


    
    # a solution with highest volume will be penalized
    total_volume = sum([d["volume"] for d in tops if "volume" in d]) + sum([d["volume"] for d in bottoms if "volume" in d])
    if normalize:
        total_volume = total_volume / normalize[1]

    

    # a solution that removes better items or includes worse items will be penalized
    # likings = get_dict_vals(tops, bottoms, "Liking Rating")
    # relative_likings = [x-abs(min(likings)) for x in likings]

    # full_suitcase_likings = get_dict_vals(all_clothes_list[:num_tops], all_clothes_list[num_tops:], "Liking Rating")
    # bonus_liking = sum([x-abs(min(full_suitcase_likings)) for x in full_suitcase_likings])

    # liking_diff = bonus_liking - sum(relative_likings)
    # #liking_diff = 10 - (sum(liking_diff) / len(liking_diff))

    # a solution that removes better items or includes worse items will be penalized
    # where "better" items are above average and "worse" are below average
    liking = 0
    for i in range(0, len(all_clothes_list)):
        if all_clothes_list[i]["Name"] in [x["Name"] for x in tops+bottoms]: # if they have it
            if all_clothes_list[i]["Liking Rating"] > 2.5:
                liking -= all_clothes_list[i]["Liking Rating"]
            elif all_clothes_list[i]["Liking Rating"] < 2.5:
                liking += all_clothes_list[i]["Liking Rating"]
        elif all_clothes_list[i]["Name"] not in [x["Name"] for x in tops+bottoms]: # if they dont have it
            if all_clothes_list[i]["Liking Rating"] > 2.5:
                liking += all_clothes_list[i]["Liking Rating"]
            elif all_clothes_list[i]["Liking Rating"] < 2.5:
                liking -= all_clothes_list[i]["Liking Rating"]
    if normalize:
        #liking = (liking + normalize[2]) / normalize[2]
        liking = liking / (normalize[2]*2) + 0.5
        
    
    return num_outfits_lost, total_volume, liking


def pareto_front(df, cols):
    """ Find the Pareto front for given data
    Args:
        df: dataframe
        cols (list): list of the column names to be consider in pareto calculation
    """
    
    data = df[cols].values
    is_dominated = np.zeros(len(data), dtype=bool)

    with tqdm(total=len(data), desc="Processing items") as pbar:
        for i, x in enumerate(data):
                
            if np.any(
                np.all(data <= x, axis=1) &
                np.any(data < x, axis=1)
            ):
                is_dominated[i] = True
            pbar.update(1)

    return df.loc[~is_dominated]
    

def liking_shift(df):
    # shifts the liking_diff column from a range of (-75, 75) to (0, 150) for visualization purposes if necessary
    df["liking_diff"] = df["liking_diff"] + abs(min(df["liking_diff"]))
    return df
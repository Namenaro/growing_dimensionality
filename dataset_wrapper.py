# откроем размеченный датасет
# вытащим здоровых пациентов и разметку
# выровнаяем изолинию
# возьмем только первое отведение
# сохраним новый датасет


import os
import json
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import pyedflib
import numpy as np
import pickle as pkl
import BaselineWanderRemoval as bwr

# Порядок отведений
lead_name = 'i'
pkl_filename = "C:\\ecg_new\\dataset_healthy.pkl"
FREQUENCY_OF_DATASET = 500
signal_len = 5000
raw_dataset_path="C:\\ecg_200\\ecg_data_200.json"

def healthy(diagnos):
    is_heathy =True
    axis_ok = False
    rythm_ok = False
    for key in diagnos.keys():
        if key == 'electric_axis_normal':
            if diagnos[key] == True:
                axis_ok = True
                continue
        if key == 'regular_normosystole':
            if diagnos[key] == True:
                rythm_ok = True
                continue
        if diagnos[key] == True:
            is_heathy = False
            break
    return axis_ok and rythm_ok and is_heathy

def load_raw_dataset():
    with open(raw_dataset_path, 'r') as f:
        data = json.load(f)
    x = []
    for case_id in data.keys():
        leads = data[case_id]['Leads']
        diag = data[case_id]['StructuredDiagnosisDoc']
        if healthy(diag):
            new_entry = leads[lead_name]['Signal']
            new_entry = bwr.fix_baseline_wander(new_entry, FREQUENCY_OF_DATASET)
            x.append(new_entry)
            print(diag)

    x = np.array(x)
    return x


def save_to_pkl(X):
    outfile = open(pkl_filename, 'wb')
    pkl.dump({'x':X}, outfile)
    outfile.close()
    print("dataset saved, number of pacients = " + str(len(X)))

if __name__ == "__main__":
    x = load_raw_dataset()
    print (len(x))
    print(x)
    save_to_pkl(x)

from read_data import simply_read_riders
import numpy as np
import numpy

loc_nums = 30
slot_nums = 60 * 24
days = 31
P_i = np.zeros([loc_nums + 1, slot_nums], dtype=float)
P_ij = np.zeros([loc_nums + 1,loc_nums + 1,slot_nums],dtype=float)

def cal_P_i(file_name):
    # data = read_riders(file_name)
    data = simply_read_riders(file_name)
    for j in data.keys():
        data_frame = data[j]
        slot_grouped_dict = dict(list(data_frame.groupby('tpep_pickup_datetime')))
        cal_P_ij(j, slot_grouped_dict)
        for k in slot_grouped_dict.keys():
            df = slot_grouped_dict[k]
            day_grouped_dict = dict(list(df.groupby('day')))
            P_i[j][k] = len(day_grouped_dict.keys()) / days
    numpy.savetxt(r'data\p_i.csv', P_i, delimiter = ',',fmt = '%f')

def cal_P_ij(i:int, slot_grouped_dict: dict):
    for t in slot_grouped_dict.keys():
        drop_grouped_dict = dict(list(slot_grouped_dict[t].groupby('DOLocationID')))
        for j in drop_grouped_dict.keys():
            P_ij[i][j][t] = len(drop_grouped_dict[j]) / len(slot_grouped_dict[t])

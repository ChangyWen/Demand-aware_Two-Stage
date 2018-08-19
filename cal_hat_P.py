import cal_Probability as cp
import numpy as np
import gen_map
import stage_2 as s2

def cal_hat_P(slot_list) -> dict:
    hat_P = {}
    for i in gen_map.nodes:
        for t in slot_list:
            hat_P[(i,t)] = cp.P_i[i][t]
            temp = 0
            for j in gen_map.nodes:
                if s2.feasible_dict[(i,j,t)][1]:
                    temp += cp.P_ij[i][j][t]
            hat_P[(i,t)] *= temp
    return hat_P




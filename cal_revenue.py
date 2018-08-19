import cal_Probability as cp
import gen_map
import stage_2 as s2
import init_instances as ii
import util
rate = 4
beta = 0.4

def cal_pickup_revenue(v, slot_list) -> dict:
    s = ii.riders[v.picked_up[0]].from_node
    d = ii.riders[v.picked_up[0]].to_node
    t_0 = ii.riders[v.picked_up[0]].appear_slot
    ea_d = t_0 + ii.floyd_path(s,d)[1] / util.average_speed
    w_ij = {}
    for i in gen_map.nodes:
        for j in gen_map.nodes:
            for slot in slot_list:
                (type,flag) = s2.feasible_dict[(i,j,slot)]
                if flag:
                    if type == 1:
                        path_1 = ii.floyd_path(i, j)[1] + ii.floyd_path(j, d)[1]
                        a_d_1 = slot + path_1 / util.average_speed
                        w_ij[(i,j,slot)] = rate * ii.floyd_path(i,j)[1] + rate * ii.floyd_path(s, d)[1]
                        w_ij[(i,j,slot)] -= beta * (a_d_1 - ea_d)
                    else:
                        path_2 = ii.floyd_path(i, d)[1] + ii.floyd_path(d, j)[1]
                        a_d_2 = slot + ii.floyd_path(i,d)[1] / util.average_speed
                        a_drop_2 = slot + path_2 / util.average_speed
                        ea_drop_2 = slot + ii.floyd_path(i,j)[1] / util.average_speed
                        w_ij[(i, j, slot)] = rate * ii.floyd_path(s, d)[1] - beta * (a_d_2 - ea_d)
                        w_ij[(i, j, slot)] += rate * ii.floyd_path(i,j)[1]/util.average_speed - beta * (a_drop_2 - ea_drop_2)
    return w_ij

def cal_expected_revenue(v, hat_P, slot_list) -> dict:
    w_ij = cal_pickup_revenue(v, slot_list)
    w_i = {}
    for i in gen_map.nodes:
        for slot in slot_list:
            w_i[(i, slot)] = 0
            for j in gen_map.nodes:
                (type,flag) = s2.feasible_dict[(i,j,slot)]
                if flag:
                    if hat_P[(i, slot)] == 0:
                        temp = w_ij[(i, j, slot)] * (cp.P_i[i][slot] * cp.P_ij[i][j][slot]) * 1e99
                    else:
                        temp = w_ij[(i, j, slot)] * (cp.P_i[i][slot] * cp.P_ij[i][j][slot]) / hat_P[(i, slot)]
                    w_i[(i, slot)] += temp
                    # temp1 = cp.P_i[i][slot] * cp.P_ij[i][j][slot]
                    # try:
                    #     temp1 = temp1 / hat_P[(i, slot)]
                    # except ZeroDivisionError:
                    #     temp1 = temp1 * 1e99
                    # finally:
                    #     temp = temp1 * w_ij[(i, j, slot)]
                    #     w_i[(i, slot)] += temp
    return w_i
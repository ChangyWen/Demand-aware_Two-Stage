import util
import init_instances as ii
from collections import OrderedDict

def feasible_pick(v:util.Vehicle, rider: int) -> (list , bool):
    ddl_list = []
    des = []
    slot = v.slot
    s = ii.riders[rider].from_node
    multiple_feasible = []
    if v.load >= v.cap:
        return [], False
    else:
        for rider in v.onboard:
            ddl_list.append(ii.riders[rider].deadline)
            des.append(ii.riders[rider].to_node)
        for i in range(len(des)):
            for j in range(len(des)):
                if j == i:
                    continue
                t_i = slot + ii.floyd_path(s, des[i])[1] / util.average_speed
                t_j = t_i + ii.floyd_path(des[i], des[j])[1] / util.average_speed
                if len(des) == 3:
                    for k in range(len(des)):
                        if k == i or k == j:
                            continue
                        # final_des = OrderedDict()
                        t_k = t_j + ii.floyd_path(des[j], des[k])[1] / util.average_speed
                        dis = ii.floyd_path(des[j], des[k])[1] + ii.floyd_path(des[i], des[j])[1] + \
                              ii.floyd_path(s, des[i])[1]
                        if t_i <= ddl_list[i] and t_j <= ddl_list[j] and t_k <= ddl_list[k]:
                            final_des = [des[i], des[j], des[k]]
                            # final_des[v.onboard[i]] = des[i]
                            # final_des[v.onboard[j]] = des[j]
                            # final_des[v.onboard[k]] = des[k]
                            multiple_feasible.append((final_des, dis))
                else:
                    # final_des = OrderedDict()
                    dis = ii.floyd_path(des[i], des[j])[1] + ii.floyd_path(s, des[i])[1]
                    if t_i <= ddl_list[i] and t_j <= ddl_list[j]:
                        final_des = [des[i], des[j]]
                        # final_des[v.onboard[i]] = des[i]
                        # final_des[v.onboard[j]] = des[j]
                        multiple_feasible.append((final_des, dis))
        if len(multiple_feasible) > 0:
            multiple_feasible = sorted(multiple_feasible, key=lambda x: x[1], reverse=False)
            return multiple_feasible[0][0], True
        else:
            return [], False
    return [], False
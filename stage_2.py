import util
import init_instances as ii
import gen_map

feasible_dict = {}

def check_feasible(a_d, ddl_d, a_drop, ddl_drop):
    if a_d <= ddl_d and a_drop <= ddl_drop:
        return True
    else:
        return False

def check(v:util.Vehicle, pre, drop, slot) -> (int, bool):
    d = ii.riders[v.picked_up[0]].to_node
    ddl_d = ii.riders[v.picked_up[0]].deadline
    ddl_drop = slot + ii.floyd_path(pre, drop)[1] / util.average_speed + 40
    path_1 = ii.floyd_path(pre, drop)[1] + ii.floyd_path(drop, d)[1]
    a_d_1 = slot + path_1 / util.average_speed
    a_drop_1 = slot + ii.floyd_path(pre, drop)[1] / util.average_speed
    path_2 = ii.floyd_path(pre, d)[1] + ii.floyd_path(d, drop)[1]
    a_drop_2 = slot + path_2 / util.average_speed
    a_d_2 = slot + ii.floyd_path(pre, d)[1] / util.average_speed
    if check_feasible(a_d_1, ddl_d, a_drop_1, ddl_drop):
        if check_feasible(a_d_2, ddl_d, a_drop_2, ddl_drop):
            if a_d_1 + a_drop_1 < a_d_2 + a_drop_2:
                return 1, True
            else:
                return 2, True
        else:
            return 1, True
    else:
        if check_feasible(a_d_2, ddl_d, a_drop_2, ddl_drop):
            return 2, True
        else:
            return 0, False

def stage_two(v: util.Vehicle):
    slot_list = [slot for slot in range(v.slot, ii.riders[v.picked_up[0]].deadline + 1)]
    global feasible_dict
    for i in gen_map.nodes:
        for j in gen_map.nodes:
            for slot in slot_list:
                feasible_dict[(i, j, slot)] = check(v, i, j, slot)
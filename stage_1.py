import init_instances as ii
import gen_map as gm
import util
import stage_2
import cal_hat_P as chp
import cal_revenue as cr

hat_P = {}
w_i = {}
f = {}
route = []

def Backtrack(v:util.Vehicle, current_node: int, t: int):
    global route
    d = ii.riders[v.picked_up[0]].to_node
    slot_t = ii.riders[v.picked_up[0]].deadline
    if current_node == d:
        route = v.route.copy()
        return
    else:
        for j in gm.out[current_node]:
            if t + gm.delta[(current_node,j)] <= slot_t:
                temp = hat_P[(current_node, t)] * w_i[(current_node, t)] + \
                       (1 - hat_P[(current_node, t)]) * (f[(j, t + gm.delta[(current_node, j)])])
                if temp == f[(current_node, t)]:
                    v.route.append(j)
                    Backtrack(v, j, t + gm.delta[(current_node,j)])
                    v.route.pop(-1)
    return


def stage_one(v:util.Vehicle):
    stage_2.stage_two(v)
    s = ii.riders[v.picked_up[0]].from_node
    d = ii.riders[v.picked_up[0]].to_node
    slot_t = ii.riders[v.picked_up[0]].deadline
    slot_0 = v.slot
    slot_list = [slot for slot in range(slot_0, slot_t + 1)]
    global hat_P, w_i ,f
    hat_P = chp.cal_hat_P(slot_list)
    w_i = cr.cal_expected_revenue(v, hat_P, slot_list)
    for i in gm.nodes:
        for t in slot_list:
            f[(i,t)] = -1
    for t in slot_list:
        if t >= slot_t:
            f[(d, t)] = cr.rate * ii.floyd_path(s,d)[1] - cr.beta * (t - slot_0)

    nodes = gm.nodes.copy()
    nodes.remove(d)
    slot_list = list(reversed(slot_list))
    for t in slot_list:
        for i in nodes:
            for j in gm.out[i]:
                if t + gm.delta[(i, j)] <= slot_t:
                    temp = hat_P[(i, t)] * w_i[(i, t)] + (1 - hat_P[(i, t)]) * (f[(j, t + gm.delta[(i, j)])])
                    f[(i ,t)] = max(f[(i, t)], temp)
    v.route = [s]
    t = slot_0
    Backtrack(v, s, t)
    v.route = route.copy()
    # print(v.route)

# if __name__ == "__main__":
#     ii.init_param()
#     for i in range(3):
#         stage_one(ii.vehicles[i])

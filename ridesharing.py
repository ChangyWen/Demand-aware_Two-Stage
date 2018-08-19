import init_instances as ii
import gen_map as gm
import util
import stage_2
import cal_hat_P as chp
import cal_revenue as cr

def stage_1(v:util.Vehicle):
    stage_2.stage_two(v)
    s = ii.riders[v.picked_up[0]].from_node
    d = ii.riders[v.picked_up[0]].to_node
    slot_0 = v.slot
    slot_t = ii.riders[v.picked_up[0]].deadline
    slot_list = [slot for slot in range(slot_0, slot_t + 1)]
    hat_P = chp.cal_hat_P(slot_list)
    w_i = cr.cal_expected_revenue(v, hat_P, slot_list)
    f = {}
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
    current_node = s
    # print(slot_0)
    # print(slot_t)
    # print(current_node)
    # print(gm.out[current_node])
    # print(gm.delta[18, 15])
    # print(f[current_node, slot_0])
    # test = []
    # while True:
    #     test = []
    #     for j in gm.out[current_node]:
    #         if t + gm.delta[(current_node, j)] <= slot_t:
    #             temp = hat_P[(current_node, t)] * w_i[(current_node, t)] + \
    #                                     (1 - hat_P[(current_node, t)]) * (f[(j, t + gm.delta[(current_node, j)])])
    #             if temp in test:
    #                 print('false')
    #                 break
    #             test.append(temp)
    #             if temp == f[(current_node, t)]:
    #                 to = j
    #     t += gm.delta[(current_node, j)]
    #     current_node = to
    while True:
        for j in gm.out[current_node]:
            if t + gm.delta[(current_node,j)] <= slot_t:
                temp = hat_P[(current_node, t)] * w_i[(current_node, t)] + \
                       (1 - hat_P[(current_node, t)]) * (f[(j, t + gm.delta[(current_node, j)])])
                if temp == f[(current_node, t)]:
                    v.route.append(j)
                    print(j)
                    break
        t += gm.delta[(current_node,j)]
        current_node = j
        if current_node == d:
            break
    print(v.route)
    # print(f[s, slot_0])

if __name__ == "__main__":
    ii.init_param()
    for i in range(3,4):
        stage_1(ii.vehicles[i])

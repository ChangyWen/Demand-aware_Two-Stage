import init_instances as ii
import stage_1 as s1
import stage_2 as s2
import util
import gen_map as gm
import feasible_cheak as fc
import cal_revenue as cr
def simulate(v:util.Vehicle):
    t = v.slot
    v.passed_route = [v.route[0]]
    v.location = v.route[0]
    picked = False
    length1 = len(v.route)
    for i in range(1, length1 - 1):
        v.passed_route.append(v.route[i])
        v.location = v.route[i]
        t += gm.delta[(v.route[i - 1], v.route[i])]
        v.slot = t
        if len(ii.state.s_n[int(t)][v.route[i]]) > 0:
            for rider in ii.state.s_n[int(t)][v.route[i]]:
                j = ii.riders[rider].to_node
                (type, isOk) = s2.feasible_dict[(v.route[i], j, t)]
                if isOk:
                    v.load += 1
                    v.picked_up.append(rider)
                    v.onboard.append(rider)
                    v.replan_route(type)
                    picked = True
                    break
        if picked:
            break
    if i == length1 - 2 and not picked:
        t += gm.delta[(v.route[i], v.route[i + 1])]
        v.slot = t
        v.passed_route.append(v.route[i + 1])
        v.location = v.route[i + 1]
        onboard = v.onboard.copy()
        for rider in onboard:
            if ii.riders[rider].to_node == v.route[i + 1]:
                v.onboard.remove(rider)
                v.drop_off_slot[rider] = t
                v.load -= 1
        return cr.cal_final_revenue(v)
    length2 = len(v.route)
    picked = False
    for i in range(1, length2 - 1):
        v.passed_route.append(v.route[i])
        v.location = v.route[i]
        t += gm.delta[(v.route[i - 1], v.route[i])]
        v.slot = t
        onboard = v.onboard.copy()
        for rider in onboard:
            if ii.riders[rider].to_node == v.route[i]:
                v.onboard.remove(rider)
                v.drop_off_slot[rider] = t
                v.load -= 1
        if len(ii.state.s_n[int(t)][v.route[i]]) > 0:
            for rider in ii.state.s_n[int(t)][v.route[i]]:
                v.onboard.append(rider)
                (des_list, isOk) = fc.feasible_pick(v, rider)
                if isOk:
                    v.load += 1
                    v.picked_up.append(rider)
                    v.re_replan_route(des_list)
                    picked = True
                    break
                else:
                    v.onboard.pop(-1)
        if picked:
            break
    if i == length2 - 2 and not picked:
        t += gm.delta[(v.route[i], v.route[i + 1])]
        v.slot = t
        v.passed_route.append(v.route[i + 1])
        v.location = v.route[i + 1]
        onboard = v.onboard.copy()
        for rider in onboard:
            if ii.riders[rider].to_node == v.route[i + 1]:
                v.onboard.remove(rider)
                v.drop_off_slot[rider] = t
                v.load -= 1
        return cr.cal_final_revenue(v)
    if picked:
        for i in range(1, len(v.route)):
            t += gm.delta[(v.route[i - 1], v.route[i])]
            v.slot = t
            v.passed_route.append(v.route[i])
            v.location = v.route[i]
            onboard = v.onboard.copy()
            for rider in onboard:
                if ii.riders[rider].to_node == v.route[i]:
                    v.onboard.remove(rider)
                    v.drop_off_slot[rider] = t
                    v.load -= 1
    return cr.cal_final_revenue(v)

if __name__ == "__main__":
    ii.init_param()
    # print(ii.floyd_path(9,9)[0])
    # print(ii.floyd_path(9,9)[1])
    for i in range(100):
        s1.stage_one(ii.vehicles[i])
        # print('vehicle %(i)d'%{'i':i})
        print(simulate(ii.vehicles[i]))
        # print('picked_up:')
        # d = 0
        # for rider in ii.vehicles[i].picked_up:
        #     d += 1
        #     print('No.%(i)d'%{'i':d})
        #     print(ii.riders[rider].from_node)
        #     print(ii.riders[rider].to_node)
        # for rider in ii.vehicles[i].picked_up:
        #     print('delay:')
        #     a = ii.vehicles[i].drop_off_slot[rider]
        #     ea = ii.riders[rider].appear_slot + \
        #          ii.floyd_path(ii.riders[rider].from_node, ii.riders[rider].to_node)[1] / util.average_speed
        #     print(a - ea)
        print(ii.vehicles[i].passed_route)
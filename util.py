import init_instances as ii

average_speed = 1

class vertex(object):
    def __init__(self, v_id: int, x, y):
        self.v_id = v_id
        self.x_coor = x
        self.y_coor = y

class Rider(object):
    def __init__(self, r_id, from_node: int, to_node: int, appear_slot: int, deadline: int):
        self.r_id = r_id
        self.from_node = from_node
        self.to_node = to_node
        self.pu_t = 0
        self.deadline = deadline
        self.delay_t = 0
        self.appear_slot = appear_slot
        self.flag = 0


class Vehicle(object):
    def __init__(self, v_id, location: int, slot: int, first_rider: int):
        self.v_id = v_id
        self.location = location
        self.slot = slot
        self.cap = 3
        self.load = 0
        self.picked_up = [first_rider]
        self.pre_pickup = []
        self.route = []
        self.passed_route = []
        self.violation_time = 0
        self.onboard = [first_rider]
        self.drop_off_slot = {}

    def insert_rider(self, rider: int, index: int = -1):
        if index == -1:
            self.picked_up.append(rider)
        else:
            self.picked_up.insert(index, rider)

    def insert_pre_pickup(self, loc: int, index: int = -1):
        if index == -1:
            self.pre_pickup.append(loc)
        else:
            self.pre_pickup.insert(index, loc)

    def update_first(self):
        self.route = [self.location]
        from_node = ii.riders[self.picked_up[0]].from_node
        self.route.append(from_node)
        if len(self.pre_pickup) > 0:
            from_node = ii.riders[self.picked_up[-1]].from_node
            to_node = self.pre_pickup[0]
            self.route += ii.floyd_path(from_node, to_node)[0]
            from_node = to_node
        if len(self.pre_pickup) > 1:
            for i in range(1, len(self.pre_pickup)):
                from_node = self.pre_pickup[i-1]
                to_node = self.pre_pickup[i]
                self.route += ii.floyd_path(from_node, to_node)[0]
                from_node = to_node
        to_node = ii.riders[self.picked_up[0]].to_node
        self.route += ii.floyd_path(from_node, to_node)[0]
        temp_route = self.route.copy()
        n = 0
        nums = len(self.route) - 1
        for i in range(nums):
            if temp_route[i] == temp_route[i+1]:
                self.route.pop(i - n)
                n += 1
    #
    # def update_pick(self,node1:int, des_order:dict):
    #     self.route = []
    #     if len(self.picked_up) == 3:
    #         des_list = list(des_order.items())
    #         self.route = ii.floyd_path(node1, des_list[0][1])[0]
    #         for i in range(len(des_list) - 1):
    #             list_temp = ii.floyd_path(des_list[i][1], des_list[i + 1][1])[0]
    #             list_temp.pop(0)
    #             self.route += list_temp
    #         return
    #     else:
    #         des_list = list(des_order.items())
    #         shortest_path = ii.floyd_path(node1, des_list[0][1])[0]
    #         slack = ii.riders[des_list[0][0]].deadline - (self.slot + ii.floyd_path(node1, des_list[0][1])[1] / average_speed)
    #         neighbor = strategy.gen_neighbor(shortest_path, slack)
    #         best, best_node, temp  = 0, 0 ,0
    #         if len(neighbor) == 0:
    #             self.route = shortest_path
    #             list_temp = ii.floyd_path(des_list[0][1], des_list[1][1])[0]
    #             list_temp.pop(0)
    #             self.route += list_temp
    #         else:
    #             for node in neighbor:
    #                 time = self.slot + ii.floyd_path(node1, node)[1] / average_speed
    #                 temp = strategy.cal_best_one(self, node, int(time))
    #                 if temp > best:
    #                     best_node = node
    #             if best_node == 0:
    #                 self.route = shortest_path
    #                 list_temp = ii.floyd_path(des_list[0][1], des_list[1][1])[0]
    #                 list_temp.pop(0)
    #                 self.route += list_temp
    #             else:
    #                 print('excuse')
    #                 self.route = ii.floyd_path(node1, best_node)[0]
    #                 list_temp = ii.floyd_path(best_node, des_list[0][1])[0]
    #                 list_temp.pop(0)
    #                 self.route += list_temp
    #                 list_temp = ii.floyd_path(des_list[0][1], des_list[1][1])[0]
    #                 list_temp.pop(0)
    #                 self.route += list_temp
    #         return

class State(object):
    def __init__(self, slot_riders: dict):
        self.s_n = slot_riders

    def update(self):
        print()

class Floyd_Path(object):
    def __init__(self, node , node_map, path_map):
        self.node = node
        self.node_map = node_map
        self.path_map = path_map
        self.node_length = len(node_map)
        self._init_Floyd()

    def __call__(self, from_node: int, to_node:int ):
        self.from_node = from_node - 1
        self.to_node = to_node - 1
        return self._format_path(), self.node_map[from_node - 1][to_node - 1]

    def _init_Floyd(self):
        for k in range(self.node_length):
            for i in range(self.node_length):
                for j in range(self.node_length):
                    tmp = self.node_map[i][k] + self.node_map[k][j]
                    if self.node_map[i][j] > tmp:
                        self.node_map[i][j] = tmp
                        self.path_map[i][j] = self.path_map[i][k]

    def _format_path(self):
        node_list = []
        temp_node = self.from_node
        obj_node = self.to_node
        node_list.append(self.node[temp_node])
        while True:
            node_list.append(self.node[self.path_map[temp_node][obj_node]])
            temp_node = self.path_map[temp_node][obj_node]
            if temp_node == obj_node:
                break
        return node_list


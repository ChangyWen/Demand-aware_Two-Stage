import pandas as pd
from random import sample
from gen_map import *
import init_instances as ii
import util

def gen_ori_riders() -> list:
    df = pd.DataFrame(columns=('tpep_pickup_datetime','tpep_dropoff_datetime','PULocationID','DOLocationID','day'))
    for k in range(50000):
        t_p = randint(0, slot_nums - 1)
        pickup = choice(nodes)
        drop_off = choice(nodes)
        d = randint(1, days)
        min_travel_time = ii.floyd_path(pickup, drop_off)[1] / util.average_speed
        t_d = t_p + int(min_travel_time)
        df.loc[k] = [t_p, t_d, pickup, drop_off ,d]
    df.to_csv(r'data\self_gen_riders.csv', index= False,header=True, float_format='%d')

def choose_instances(nums: int):
    df = pd.read_csv(r'data\self_gen_riders.csv')
    riders_list = df.values.tolist()
    riders = sample(riders_list, nums)
    riders = pd.DataFrame(riders, columns=('tpep_pickup_datetime','tpep_dropoff_datetime','PULocationID','DOLocationID','day'))
    return riders

# gen_ori_riders()
# if __name__ == '__main__':
    # ii.init_param()
    # gen_ori_riders()
    # riders_df = choose_instances(500)
    # riders_df_ = choose_instances(5000)
    # riders_df.to_csv(r'data\choosed_instances_500.csv', index=False, header=True, float_format='%d')
    # riders_df_.to_csv(r'data\choosed_instances_5000.csv', index=False, header=True, float_format='%d')
import pandas as pd
from datetime import datetime

def read_riders(file_name) -> dict:
    inputfile = open(file_name, 'rb')
    data = pd.read_csv(inputfile, usecols=['tpep_pickup_datetime','tpep_dropoff_datetime','PULocationID', \
                                           'DOLocationID'], iterator= True)
    loop = True
    chunkSize = 10000
    chunks = []
    i = 0
    while loop:
        try:
            chunk = data.get_chunk(chunkSize)
            chunks.append(chunk)
        except StopIteration:
            loop = False
    data = pd.concat(chunks, ignore_index = True)
    data['day'] = 0
    for i in range(len(data)):
        data.ix[i,'tpep_pickup_datetime'] = datetime.strptime(data.ix[i,'tpep_pickup_datetime'], '%Y-%m-%d %H:%M:%S')
        data.ix[i,'tpep_dropoff_datetime'] = datetime.strptime(data.ix[i,'tpep_dropoff_datetime'], '%Y-%m-%d %H:%M:%S')
        data.ix[i,'day'] = data.ix[i,'tpep_pickup_datetime'].day
        data.ix[i,'tpep_pickup_datetime'] = data.ix[i,'tpep_pickup_datetime'].hour * 60 + \
                                            data.ix[i,'tpep_pickup_datetime'].minute
        data.ix[i,'tpep_dropoff_datetime'] = data.ix[i,'tpep_dropoff_datetime'].hour * 60 + \
                                             data.ix[i,'tpep_dropoff_datetime'].minute
    data.to_csv(r'data\usable_data.csv', sep = ',', header = True, index = False)
    grouped_dict = dict(list(data.groupby('PULocationID')))
    return grouped_dict

def simply_read_riders(file_name) -> dict:
    inputfile = open(file_name, 'rb')
    data = pd.read_csv(inputfile, usecols=['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'PULocationID', \
                                           'DOLocationID', 'day'])
    grouped_dict = dict(list(data.groupby('PULocationID')))
    return grouped_dict
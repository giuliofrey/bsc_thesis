import requests
import numpy as np
import pandas as pd
import warnings
import pickle
import time

#Importing datasets

mm_df=pd.read_csv('../outputs/mm_dataset.csv')
mm_df = mm_df.replace('not found', np.nan)
services_df=pd.read_csv('../outputs/services_df.csv')
dd_dict=mm_df[['CODICE EDIFICIO', 'lat', 'lon']].set_index('CODICE EDIFICIO').T.to_dict('list')

# ignore warnings
warnings.filterwarnings('ignore')

def check_duplicate_values(data):
    values_seen = {}
    result = []

    for key, value in data.items():
        # Convert the list of values to a tuple to use as a key in the dictionary
        value_key = tuple(value)

        # Check if the values have already been seen
        if value_key in values_seen:
            result.append(values_seen[value_key])
        else:
            result.append(np.nan)
            values_seen[value_key] = key

    for i, key in enumerate(data.keys()):
        data[key].append(result[i])

    return data

dd_dict=check_duplicate_values(dd_dict)

def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    # car, bike or foot
    loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
    url = "http://127.0.0.1:5000/route/v1/walking/"
    r = requests.get(url + loc)
    if r.status_code!= 200:
        return {}

    res = r.json()
    duration = res['routes'][0]['duration']
    distance = res['routes'][0]['distance']

    dict_out = {'duration':duration,
                'distance':distance
                }

    return duration



def find_loc(index):
    row_df=services_df.iloc[[index]]
    r_lat=float(row_df['lat'])
    r_long=float(row_df['long'])
    for key, values in dd_dict.items():
        if values[2]!=np.nan:
            d_lat=float(values[0])
            d_long=float(values[1])
            time=get_route(d_long, d_lat, r_long, r_lat)
            row_df[str(key)]=time
        else:
            key_dup=values[2]
            row_df[str(key)]=row_df[str(key_dup)]
    return row_df


def main():
    try:
        calc_df=pd.read_csv('../outputs/calc_dataset.csv')
    except:
        calc_df=pd.DataFrame(columns=services_df.columns)
    last_row=len(calc_df)
    print("Rows to be calculated",len(services_df)-last_row,"(",round(last_row/len(services_df)*100,3),'%)')
    n=20 #save csv file every n rows
    try:
        last_row_txt= pickle.load(open("../outputs/row_file", "rb"))
    except:
        last_row_txt=0
    if  last_row != last_row_txt:
        raise ValueError('CONFLICT DETECTED. Stopping code')

    print("No conflict detected. Process starting form",last_row)
    while last_row<len(services_df):
        t0 = time.time()
        calc_df_last=find_loc(last_row)
        calc_df=pd.concat([calc_df, calc_df_last])
        calc_df = calc_df.reset_index(drop=True)
        if last_row%n==0:
            calc_df.to_csv('../outputs/calc_dataset.csv', index=False)
            pickle.dump(last_row + 1, open("../outputs/row_file", "wb"))
            print("Saving dataset to .csv")
        last_row=last_row+1
        t1 = time.time()
        print('Calculated correctly row', last_row, "in ", round(t1-t0, 3), 'seconds')

if __name__ == "__main__":
    main()

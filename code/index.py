import pandas as pd
import numpy as np
import warnings
from tqdm import tqdm

#importing datasets
calc_df_fixed=pd.read_csv('../outputs/calc_fixed_df.csv', low_memory=False)
mm_df=pd.read_csv('../outputs/mm_dataset.csv')
#removing all non geolocated services
calc_df_fixed = calc_df_fixed.drop(calc_df_fixed[calc_df_fixed['long'].isna()].index)

tqdm.pandas(desc='Index progress bar')

#functions
def penality_function(x, dhat):
    if x <= dhat:
        return 1
    if x > dhat:
        return 1/(x-dhat+1)

def con_index(dist_list, dhat, n_max, alpha, beta):
    if  alpha + beta != 1:
        raise Exception("Alpha and Beta should sum to one")
    d_min = min(dist_list)
    close_list=[d for d in dist_list if d <=dhat]
    n = len(close_list)
    CI = alpha*penality_function(d_min, dhat)+beta*(n/n_max)
    return CI

def best_in_class(df_name, dhat, df=calc_df_fixed):
    e_list=list(df.columns)
    e_list=[item for item in e_list if item not in ['name', 'long', 'lat','df_name', 'cat1', 'cat2', 'cat1_name', 'cat2_name']]
    nmax_dict=dict.fromkeys(e_list)
    if df_name=='all':
        pass
    else:
        df=df[df.df_name==df_name]
    for elem in e_list:
        dist_list=list(df[str(elem)])
        close_list=[d for d in dist_list if d <=dhat]
        nmax_dict[elem]=len(close_list)
    return max(nmax_dict.values())

def fun_run(codice_edificio, dhat, alpha, beta, out_df, df=calc_df_fixed):
    columns_list=list(df.df_name.unique())+['all']
    #out_dict
    out_list=[]
    col_out_list=[]
    for column in columns_list:
        if column=='all':
            df_subset=df

        else:
            df_subset=df[df.df_name==column]
        dist_list=df_subset[str(codice_edificio)].to_list()
        if dist_list==[]:
            out=np.nan
            warnings.warn("Empty list")
        else:
            n_max=best_in_class(column, dhat)
            try:
                out=con_index(dist_list=dist_list, dhat=dhat, n_max=n_max, alpha=alpha, beta=beta)
            except:
                out=np.nan
                warnings.warn("Index not calculated because of some issue")
        col_out_list.append(column)
        out_list.append(out)
    if col_out_list == ['acqua', 'biblio', 'ciclabili','consu','cult', 'edicole', 'farmacie', 'metro', 'parchi', 'posta', 'serd', 'sinf', 'sita', 'sport', 'sprim', 'ss2', 'ssec', 'treni', 'uni', 'wifi', 'distr','all']:
        return out_list
    else:
        raise Exception("Not all columns are outputs of fun run")

def main():
    mm_columns_list=['CODICE EDIFICIO', 'full_address', 'lat', 'lon']
    index_df=mm_df[mm_columns_list]
    columns_list=list(calc_df_fixed.df_name.unique())+['all']
    index_df['list']=index_df['CODICE EDIFICIO'].progress_apply(lambda x: fun_run(x, dhat=60*15, alpha=0.5, beta=0.5, out_df=index_df))
    list_df=pd.DataFrame(index_df['list'].to_list(), columns = columns_list)
    index_df = pd.concat([index_df, list_df], axis=1)
    index_df.to_csv('../outputs/index_df.csv', index=False)
    print('Done!')

main()

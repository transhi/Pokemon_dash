#!/usr/bin/env python
# coding=utf-8
'''
Author: John
Email: johnjim0816@gmail.com
Date: 2020-12-10 20:02:03
LastEditor: John
LastEditTime: 2020-12-13 11:47:24
Discription: 
Environment: 
'''
import pandas as pd 
CSV_FILE_PATH = 'data/Pokedex_Ver6.csv'




def add_power():
    df = pd.read_csv(CSV_FILE_PATH) 
    df_new_cols = df.columns.values.tolist()
    df_new_cols.append('POWER')
    # ['NUMBER', 'CODE', 'SERIAL', 'NAME', 'TYPE1', 'TYPE2', 'COLOR', 'ABILITY1', 'ABILITY2', 'ABILITY HIDDEN', 'GENERATION', 'LEGENDARY', 'MEGA_EVOLUTION', 'HEIGHT', 'WEIGHT', 'HP', 'ATK', 'DEF', 'SP_ATK', 'SP_DEF', 'SPD', 'TOTAL', 'POWER']
    
    df_new = pd.DataFrame(columns=df_new_cols)
    for i in range(len(df)):
        tmp_list = df.loc[:,['HP', 'ATK', 'DEF', 'SP_ATK', 'SP_DEF', 'SPD']][i:i+1].values[0].tolist()
        tmp_total = df.loc[:,['TOTAL']][i:i+1].values[0].tolist()[0]
        df_new=df_new.append(df.iloc[i])
        if max(tmp_list)>=120 or tmp_total>=525:
            df_new.loc[i,'POWER']=1
        else:
            df_new.loc[i,'POWER']=0
    df_new.to_csv('data/Pokedex_Ver6_with_power.csv', index=None)


if __name__ == "__main__":
    add_power()
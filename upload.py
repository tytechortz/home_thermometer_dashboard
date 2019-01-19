#!/usr/bin/python3

import csv, sqlite3
import pandas as pd 

df = pd.read_csv('//Users/jamesswank/tempjan19.txt')

con = sqlite3.connect("/Users/jamesswank/Python_projects/home_thermometer_dashboard/temperatures.db")

df.to_sql("Temps", con, if_exists='append', index=False)

con.close()



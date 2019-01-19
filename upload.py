import csv, sqlite3
import pandas as pd 

df = pd.read_csv('//Users/jamesswank/tempjan19.txt')

con = sqlite3.connect("temperatures.db")

df.to_sql("Temps", con, if_exists='append', index=False)

con.close()



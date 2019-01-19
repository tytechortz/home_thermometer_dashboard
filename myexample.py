import numpy as np 
import pandas as pd 

mat = np.arange(0,50).reshape(5,10)

df = pd.DataFrame(data=mat)
print(df)
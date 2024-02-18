import pandas as pd
dict1 = {'Valores': [0, 1, 2], 'Nombres': ['Juan', 'Maria', 'Jose']}
df = pd.DataFrame(dict1)


for valores in df['Valores']:
    print(valores)
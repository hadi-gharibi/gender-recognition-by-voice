from pathlib import Path
import pandas as pd
import os

raw_data = (Path.cwd() / '..'/ '..' / 'gender-recognation' / 'data' / 'raw').resolve()
files = [i for i in raw_data.glob('*')]

df = None
for file in files:
    temp_waves = pd.DataFrame([i for i in file.rglob('wav/*')],columns=['path'])
    readme = [i for i in file.rglob('*/README')][0]
    info = pd.read_csv(readme, sep=':', header=None, names=['k', 'v'])

    temp_waves['user_name'] = info[info.k == 'User Name'].v.values[0]
    temp_waves['gender'] = info[info.k == 'Gender'].v.values[0]
    if type(df) == type(None):
        df = temp_waves
    else:
        df = pd.concat([df, temp_waves])

csv_path = os.path.join(os.getcwd(),'..','data','csv')
if not os.path.exists(csv_path):
    os.mkdir(csv_path)
df.to_csv(csv_path+'/waves.csv',index=False)
from pathlib import Path
import pandas as pd
import os
import re

raw_data = (Path.cwd() / '..' / '..' / 'gender-recognation' / 'data' / 'raw').resolve()
files = [i for i in raw_data.glob('*')]

df = None
for file in files:
    temp_waves = pd.DataFrame([i for i in file.rglob('wav/*')],columns=['path'])
    readme = None
    for i in file.rglob('*'):
        if (i.is_file()) and ('readme' in str(i).lower().replace(' ','')) :
            readme = i
            break
    #files without readme
    if not readme :
        continue
    info = pd.read_csv(readme,sep=':',header=None,names=['k','v'])

    with open(readme) as readme_file:
        readme = readme_file.readlines()
    for line in readme:
        line = line.lower()[:-2]
        line = re.sub('\[|\]|;', '', line)
        # if the user name is anonymous I will keep the number,else just keep the user name
        if file.name.split('-')[0] == 'anonymous': temp_waves['user_name'] = file.name.split('.')[0]
        else : temp_waves['user_name'] = file.name.split('-')[0]
        if 'gender' in line: temp_waves['gender'] = line.split(' ', 1)[1]
    #drop the folders when :
    #1.dont have gender attr
    #2.cont find them or unkonw
    #3.flac format
    if ((temp_waves.shape[0] == 0)
        or
        (temp_waves.shape[1] < 3)
        or
        (len(temp_waves) > 0 and (temp_waves.gender.iloc[0] in
                                  ['unknow','please selec',
                                   'weiblic', 'masculin', 'adul']))):
        continue
    #fix some typo
    if  temp_waves['gender'].iloc[0] == 'mal' : temp_waves['gender'] = 'male'
    if  temp_waves['gender'].iloc[0] == 'mak' : temp_waves['gender'] = 'male'
    if  temp_waves['gender'].iloc[0] == 'femal' : temp_waves['gender'] = 'female'
    if type(df) == type(None): df = temp_waves
    else: df = pd.concat([df,temp_waves])
csv_path = os.path.join(os.getcwd(),'..','data','csv')
if not os.path.exists(csv_path):
    os.mkdir(csv_path)
df.to_csv(csv_path+'/waves.csv',index=False)
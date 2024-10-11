import pandas as pd

sustainability = pd.read_csv('cleaned_sustainability.csv')
print(sustainability[sustainability['Demographic'] == 'Gender'])

christmas = pd.read_csv('cleaned_christmas.csv')
print(christmas[christmas['Demographic'] == 'Gender'])

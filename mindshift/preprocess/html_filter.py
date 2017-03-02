# standalone script to remove HTML tags from KM articles
import pandas as pd
import re
# need install xlrd and openpyxl packages

data = pd.read_excel('F5_FINAL_DEMO-solutionbase-cases_01092017.xlsx',sheetname='Article Content')
print(data.columns[[5,7,8,11,13,14]])
data.drop(data.columns[[5,7,8,11,13,14]],1,inplace = True)

data['Detail'] = None
for i in range(len(data)):
    if data['Admin/Content Type'][i] == 'Security Advisory':
        data['Detail'][i] = data['Article/Vulnerability Description'][i]
    elif data['Admin/Content Type'][i] == 'Policy':
        data['Detail'][i] = data['Article/Policy Information'][i]
    elif data['Admin/Content Type'][i] == 'Non-Diagnostic':
        data['Detail'][i] = data['Article/Topic'][i]
    elif data['Admin/Content Type'][i] == 'Known Issue':
        data['Detail'][i] = data['Article/Known Issue'][i]
    elif data['Admin/Content Type'][i] == 'Diagnostic':
        data['Detail'][i] = data['Article/Issue'][i]

# drop rows with NA values
data.drop(data[data.Detail.isnull()].index.values,axis=0,inplace=True)
# drop columns used for merging
data.drop(data.columns.values[[4,5,6,7,8]],axis=1, inplace=True)

# d.to_excel('F5_concat_detail.xlsx',encoding='utf8')

# filter html format code
data['clean_detail'] = data.Detail.map(lambda x:''.join(re.split('\n|<.*?>',x)))
# data['clean_detail'] = [''.join(re.split('\n|<.*?>',i)) for i in iter(data.Detail)]

data.drop('Detail',axis=1,inplace=True)

data.to_excel('F5_concat_detail_cleaned.xlsx',encoding='utf8')

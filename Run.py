#Import part
import json
import csv
import requests
#-------------------------
#Definition part
path_csv = open('ouput.csv', 'w+', encoding='utf8')
writer_csv = csv.writer(path_csv)

URL = "https://app.atera.com/api/v3/alerts?page=1&itemsInPage=50&alertStatus=Open"
key = 'fbbe9e0fe4ec457caf89d90dbcaf0ffd'
#------------------------

def get_ID(json_object, writer_csv,Type):
    OutID = []
    for x in Type:
        i = 0
        for a in json_object['items']:
            for key, value in json_object['items'][i].items():   
                if key == 'AlertID':
                    SaveId = value
                if (key == 'Severity' and value == x):
                    OutID.append(SaveId)
            i = i+1
    return OutID

def get_NewJson(httpURL,ApiKey):
    f = open('import.json', 'w', encoding='ISO 8859-2')
    jsonget = requests.get(httpURL,headers={'X-API-KEY': ApiKey,'Accept': 'application/json'})
    jsonget.encoding = 'ISO 8859-2'
    f.write(jsonget.text)
    f.close

def PageLooper(totalPages,ApiKey):
    ApiKey = ApiKey
    usedURLS = []
    for page in range(2,totalPages+1):
            with open ('import.json', 'r', encoding='ISO 8859-2') as path_json:
                json_object = json.load(path_json)
                writer_csv.writerow(get_ID(json_object, writer_csv,['Critical','Information']))
                URL = "https://app.atera.com/api/v3/alerts?page="+str(page)+"&itemsInPage=50&alertStatus=Open"
                get_NewJson(URL,ApiKey)
                usedURLS.append(URL) 
    return usedURLS


#MAIN ----------------------S
get_NewJson(URL,key)

with open ('import.json', 'r', encoding='ISO 8859-2') as path_json:
    json_object = json.load(path_json)

totalPages = (json_object['totalPages']) #get page count to resend html request

print(totalPages)
print(PageLooper(totalPages,key))


#json_object = json.load(path_json)


path_csv.close()

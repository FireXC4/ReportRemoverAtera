#Import part
import json
import csv
import requests
import time
start_time = time.time()
#-------------------------
#Definition part
path_csv = open('ouput.csv', 'w+', encoding='utf8', newline='')
writer_csv = csv.writer(path_csv)

URL = "https://app.atera.com/api/v3/alerts?page=1&itemsInPage=50&alertStatus=Open"
key = ''
#------------------------
def toDate (datein):
    date = datein.split('-')
    time = 0
    for i in date:
        time = time + int(i)
    return time  

def get_ID(json_object):
    OutID = []
    SaveValues = []
    ValuedKeys = ['Severity','Created','CustomerName']
    Type = [['Critical'],'2022-04-13',['Spectrum Franek']]
    i = 0
    for a in json_object['items']:
        for key, value in json_object['items'][i].items():   
            if key == 'AlertID':
                SaveId = value
            if (key in ValuedKeys):
                if (key == ValuedKeys[1]):
                    value = value[:10]
                    SaveValues.append(value)
                else: SaveValues.append(value)
        k = toDate(SaveValues[1])
        p = toDate(Type[1])
        if (SaveValues[0] in Type[0] and k <= p and SaveValues[2] in Type[2]):
                OutID.append(SaveId)
        SaveValues = []
        i = i+1
    return OutID

def get_NewJson(httpURL,ApiKey):
    f = open('import.json', 'w', encoding='ISO 8859-2')
    jsonget = requests.get(httpURL,headers={'X-API-KEY': ApiKey,'Accept': 'application/json'})
    jsonget.encoding = 'ISO 8859-2'
    f.write(jsonget.text)
    f.close

def PageLooper(totalPages,ApiKey):
    usedURLS = []
    for page in range(2,totalPages+1):
            with open ('import.json', 'r', encoding='ISO 8859-2') as path_json:
                json_object = json.load(path_json)
                writer_csv.writerow(get_ID(json_object))
                URL = "https://app.atera.com/api/v3/alerts?page="+str(page)+"&itemsInPage=50&alertStatus=Open"
                get_NewJson(URL,ApiKey)
                usedURLS.append(URL) 
    return usedURLS


#MAIN ----------------------S
get_NewJson(URL,key)

with open ('import.json', 'r', encoding='ISO 8859-2') as path_json:
    json_object = json.load(path_json)

get_ID(json_object)

totalPages = (json_object['totalPages']) #get page count to resend html request

print(totalPages)
PageLooper(totalPages,key)


#json_object = json.load(path_json)
path_csv.close()
print("Process finished --- %s seconds ---" % (time.time() - start_time))

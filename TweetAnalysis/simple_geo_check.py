import csv

range =6 

with open('Resources/crowdbreaks_tweets_jan_jun_2020_has_geo_coordinates.csv') as csv_data:
#with open('Resources/crowdbreaks_tweets_jan_jun_2020_has_place.csv') as csv_data:
    count = 0
    reader = csv.reader(csv_data, delimiter=",")
    for i, row in enumerate(reader):
        if i == 0: continue
        if float(row[2]) < 46.8182 + range and float(row[2]) > 46.8182 - range \
            and float(row[3]) < 8.2275 + range and float(row[3]) > 8.2275 - range:
            print(row)
            count+=1
    print(count)
import pandas as pd
import csv

#conver csv data into list
file = open("website/NVDA.csv")
csvreader = csv.reader(file)
header = next(csvreader)
print(header)
rows = []
for row in csvreader:
    rows.append(row)
print(rows)
file.close()

#display csv data as table
data = pd.read_csv("website/NVDA.csv")

df = pd.DataFrame(data)

print(df)



import csv

filepath = "aisdk-2021-12-23.csv"
count = 0
threshhold = 10000

with open(filepath, "r") as source:
    reader = csv.reader(source)
    with open("minimal.csv", "w") as result:
        writer = csv.writer(result)
        for r in reader:
          if count == threshhold :
            break
          writer.writerow((r[i] for i in range(26)))
          count += 1

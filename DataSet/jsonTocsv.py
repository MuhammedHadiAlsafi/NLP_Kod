import pandas as pd

# JSON dosyasını oku
df = pd.read_json("DataSet/val.json")

#df.to_excel("DataSet/samsum(train).xlsx", index=False)
df.to_csv("DataSet/samsum(val).csv", index=False)

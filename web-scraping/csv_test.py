import pandas as pd

keywords = {"metal", "energy", "team", "sheet", "solar", "financial", 
        "transportation", "electrical", "scientists",
        "electronic", "workers"}  # all your keywords

df = pd.read_csv("cms_scrape.csv", sep=",")

listMatchPosition = []
listMatchDescription = []

for i in range(len(df.index)):
    if any(x in df['headline'][i] or x in df['summary'][i] for x in keywords):
        listMatchPosition.append(df['headline'][i])
        listMatchDescription.append(df['summary'][i])


output = pd.DataFrame({'headline':listMatchPosition, 'summary':listMatchDescription})
output.to_csv("new_data.csv", index=False)

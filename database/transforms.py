import pandas as pd


# Connect here to presto DB, this DF will be imported back to main
conn = sqlite3.connect(r"C:\Users\MTGro\Desktop\coding\wineApp\db\wine_data.sqlite")
c = conn.cursor()

df = pd.read_sql("select * from wine_data", conn)

df = df[['country','description','rating','price','province','title','variety','winery','color','varietyID']]
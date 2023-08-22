import pandas as pd
import crawler



startyear = 2023
endyear = 2021

df = pd.DataFrame()
for year in range(startyear, endyear - 1, -1):
    t = crawler.ScrapeProCollage(year)
    df = pd.concat([df, t], ignore_index=True)

df.to_excel("result.xlsx")

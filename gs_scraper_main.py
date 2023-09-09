import pandas as pd
import gs_scraper_func as gs

#This line will open a new chrome window and start the scraping.

# path = "G:/DataScience_Projects/ds_salary_proj/msedgedriver.exe"
df1 = gs.get_jobs("data scientist", 3, False,6)
df1.to_csv('glassdoor_scrape.csv', index=False)

df = pd.read_csv("glassdoor_jobs.csv")





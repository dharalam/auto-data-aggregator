# auto-data-aggregator
Uses [Scrapy](https://docs.scrapy.org/en/latest/intro/overview.html) + [MongoDB's Atlas API](https://www.mongodb.com/docs/atlas/app-services/mongodb/) with help from [ScraperAPI](https://www.scraperapi.com/) to quickly aggregate tabular information from the web all with a simple Google search query.

## Rationale
Sometimes collecting large amounts of data is a hassle. That's why we have web scrapers to do the work for us. I wanted a convenient way to aggregate general tabular data on a given topic that I would like to know more about to use for my own small project purposes. This can be easily expanded upon to something more heavy-duty and has applications in Machine Learning and Data Science/Analytics.

## Tools and Requirements
As linked above, you'll need to have the following installed on your python distribution (v>=3.11.5): 
- Scrapy
- a MongoDB tool like [pymongo](https://pymongo.readthedocs.io/en/stable/) (any other tool works fine too)
- Pandas
- and dotenv with `pip install python-dotenv`

I recommend you get a ScraperAPI key. They have a 7-day free trial if you don't feel like paying or if you're not planning on using this frequently. ScraperAPI exists primarily to ensure that you don't get IP banned for sending too many requests. Feel free to omit ScraperAPI entirely if you either don't care or if you have some other workaround. You will have to modify `auto-data-aggregator\google_scraper\google_scraper\spiders\google.py`, however.

## Dataflow
The flow is pretty straightforward:
1. From your terminal, in the directory `.../auto-data-aggregator/google_scraper/google_scraper` run the command `scrapy crawl google <queries>`. This should make the spider start crawling and gathering information from google based on the queries you provided. Because of the way Google queries are structured, you will need to use `+` wherever there would normally be a space in your query. If you want multiple queries, separate them with a backslash (ex. `apples/oranges/lemons` will scrape google for all three).
2. The spider will save the results of its crawl to a file named `serps.csv`. We will be pulling the data from this file in a second.
3. In `linkscrape.py`, we load `serps.csv` into a Pandas dataframe and isolate the links column. For each link, we then call `pd.read_html(f'http://api.scraperapi.com?api_key={scraperapi}&url={link}')`. This grabs all tabular data from the webpage automatically and converts it into a Pandas dataframe. For each table on that webpage, we convert it to `.json` format so that we can upload them to MongoDB.
4. We load the `.json` of the table we just stored, and after some reformatting we insert it into a MongoDB collection that has the same name as the title of the website we were scraping. If the collection didn't already exist, MongoDB creates it for us and then performs the insertion.
5. Repeat until every link is exhausted.

## Problems and Future Improvements
There are a handful of problems as it stands with this program that I hope to fix in the future:
1. Pandas grabs ALL the tabular data on a site *indiscriminately*, leading to dubious data quality.
   - Solutions: Train an AI model or rely on heuristics.
   - Difficulties with implementation: Difficult to say what qualifies as "good data" since it's subjective and varies on a case-to-case basis. Also an AI model would require a ridiculous amount of data and labeling, resources to which I do not have access to.
2. Some dataframes are too big for Pandas to turn into `.json` format, apparently.
   - Solutions: Byte-stream it? I guess? MongoDB accepts `.bson` so that could work.
   - Difficulties with implementation: I would have to completely restructure the way that the program pulls and filters the tabular data from the webpage, as Pandas will not be sufficient any longer.
3. The spider and `linkscraper.py` are disjoint, it would feel nicer if it could be done all in one go.
   - Solutions: Consolidate them.
   - Difficulties with Implementation: None, I could do it right now if I felt like it. 

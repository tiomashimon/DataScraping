BOT_NAME = "lab3"

SPIDER_MODULES = ["lab3.spiders"]
NEWSPIDER_MODULE = "lab3.spiders"



ROBOTSTXT_OBEY = True

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


ITEM_PIPELINES = {
    'lab3.pipelines.PostgreSQLPipeline': 300,
}


DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': ' postgress',
    'password': 'labpassscrapy',
    'database': 'labthird'
}

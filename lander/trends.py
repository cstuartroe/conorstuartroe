from urllib import request as ur
import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup as bs

CANDIDATES = {"Cory Booker":         "%2Fm%2F08sry2",
              "Kamala Harris":       "%2Fm%2F08sry2",
              "Bernie Sanders":      "%2Fm%2F01_gbv",
              "Elizabeth Warren":    "%2Fm%2F01qh39",
              "Joe Biden":           "%2Fm%2F012gx2",
              "Pete Buttigieg":      "%2Fm%2F0hhqg37",
              "Julián Castro":       "%2Fm%2F09mhnm",
              "John Delaney":        "%2Fm%2F09g8h5d",
              "Tulsi Gabbard":       "%2Fm%2F0cnyrfq",
              "Kirsten Gillibrand":  "%2Fm%2F0gnfc4",
              "John Hickenlooper":   "%2Fm%2F04g_1z",
              "Jay Inslee":          "%2Fm%2F025bdx",
              "Amy Klobuchar":       "%2Fm%2F05fbpt",
              "Marianne Williamson": "%2Fm%2F042vjb",
              "Andrew Yang":         "%2Fg%2F11c37jsw3y",
              "Andrew Gillum":       "%2Fm%2F02rg1bb",
              "Stacey Abrams":       "%2Fm%2F0k0v28f",
              "Bill de Blasio":      "%2Fm%2F0gjsd3",
              "Beto O'Rourke":       "%2Fm%2F0dty9d",
              "Eric Swalwell":       "%2Fm%2F0ncq55g"}

##class ThreeMonthSpider(scrapy.Spider):
##    def __init__(self, *candidates):
##        assert(len(candidates) <= 5)
##        self.candidates = candidates
##        codes = [CANDIDATES[c] for c in self.candidates]
##        start_urls = [
##            "https://trends.google.com/trends/explore?date=today%201-m&q=" + ",".join(codes)
##            ]
##
##    def parse(self, response):
##        download_button = response.xpath('//button.export')
##        return download_button
##
##def get90days(*candidates):
##    process = CrawlerProcess({
##        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
##    })
##    process.crawl(ThreeMonthSpider)
##    process.start()
##    return process

#if __name__=="__main__":
    #example = get90days("Bernie Sanders","Kamala Harris","Elizabeth Warren","Cory Booker")



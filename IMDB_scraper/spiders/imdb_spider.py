# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt0306414/']

    def parse(self, response):
        """
        Parse method, navigates to the Cast segment of the IMDB page and calls the subsequent function
        """

        #creates new url for the credit page 
        cast_link = response.urljoin("fullcredits/")

        #navigates to said page and call the appropriate function 
        yield scrapy.Request(cast_link, callback= self.parse_full_credits)


    def parse_full_credits(self,response):
        """
        Starts at a Cast page of IMDB, crawl all actors, crew not included, then call the parse_actor_page function 
        """

        #a list of relative paths for each actor   
        rel_paths = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        #craws each link
        if rel_paths:
            for path in rel_paths:
                actor_link = response.urljoin(path)
                yield scrapy.Request(actor_link, callback = self.parse_actor_page)
    
    def parse_actor_page(self, response):
        """
        Crawls each actor page and compiles every work that actor has starred in
        """

        #selects actor name
        actor_name = response.css("span.itemprop::text").get()

        #selects the work from the actor page
        movie_or_TV_name = response.css("div.filmo-row b")
        for movie in movie_or_TV_name:
            yield {"actor" : actor_name, "movie_or_TV_name" : movie.css("a::text").get()}


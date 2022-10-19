import scrapy
import pandas as pd
df = pd.read_csv('F:\Web Scraping\Golabal\manta.csv')
base_url = 'https://www.hotfrog.com/search/{}/restaurants/1'

class HotSpider(scrapy.Spider):
    name = 'hot'
    def start_requests(self):       
        states = df['STATES'].values.tolist()        
        for state in states:            
            yield scrapy.Request(base_url.format(state), cb_kwargs={'state':state})
            
    def parse(self, response, state):         
        links = response.css("a.serps-ci-icon::attr(href)")        
        for link in links:                     
            yield response.follow("https://www.hotfrog.com"+link.get(),  callback=self.parse_item, cb_kwargs={'state':state})  
           
        href = response.xpath("//nav[@aria-label='Pagination']//li[last()]/a/@href").get()
        if href is not None:
            next_page = "https://www.hotfrog.com"+href   
            print(next_page) 
            yield scrapy.Request(next_page, callback=self.parse,cb_kwargs={'state':state})     
            
    def parse_item(self, response, state): 
        print(".................")  
        print(response.url)      
        website = response.xpath("//dd[@class='col-8 col-md-9 py-1']/a/@href").get()
        print(website)        
        name = response.css("strong.lead.hfhl::text").get()
        print(name)  
        location = response.xpath("//dd[@class='col-8 col-md-9 py-1']/span/text()").getall()        
        print(location)
        phone = response.xpath("//dd[@class='col-8 col-md-9 py-1']/text()").get()
        print(phone)
        about = response.xpath('//*[@id="description"]/p/text()').get()
        print(about)  

        yield{   
            'name' : name,  
            'phone' : phone,
            'about_website' : about,
            'location' : location,              
            'state_name' : state,
            'website' : website,
            'hotfrog_url' : response.url,              
                
        }

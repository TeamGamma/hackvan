from crawler import crawler

flickr_crawler = crawler('your_api_key')
flickr_crawler.search("Victoria drinking fountains")
flickr_crawler.write_fountains()

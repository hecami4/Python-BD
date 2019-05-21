# -*- coding: utf-8 -*-
import scrapy


class WikipediaCrawler(scrapy.Spider):
    name = "wikipedia-crawler"
    start_urls = ['https://es.wikipedia.org/wiki/Especial:Aleatoria']

    def start_requests(self):

        for page_counter in range(10):
            yield scrapy.Request(url=self.start_urls[0], callback=self.parse, dont_filter=True)

    def parse(self, response):
        lista_urls = []

        for vinculo in response.css('a::attr(href)'):
            lista_urls.append(vinculo.extract())

        nombre_archivo = response.url.split("/")[-1] + '.html'
        nombre_archivo = nombre_archivo.replace(':', '_')

        with open('crawled/' + nombre_archivo, 'wb') as f:
            f.write(response.body)

        yield {
            str(response.url):
            {
                'ranking': 5,
                'titulo': response.css('title::text').extract()[0],
                'enlaces': lista_urls,
                'ruta': "crawled/" + nombre_archivo
            }
        }

    def guardar_url(self, response):
        print('url: ' + response.url)
        self.start_urls.append(response.url)
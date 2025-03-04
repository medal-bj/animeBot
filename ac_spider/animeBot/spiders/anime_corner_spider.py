import scrapy

class AnimeCornerSpider(scrapy.Spider):
    name = 'anime_corner'
    start_urls = ['https://animecorner.me/']

    def parse(self, response):
        article_links = response.css('h2.entry-title a::attr(href)').getall()
        for link in article_links:
            yield response.follow(link, self.parse_article)

        # Extract all links
        all_links = response.css('a::attr(href)').getall()

        # Filter internal links
        for link in all_links:
            if link and link.startswith('https://animecorner.me/'):
                yield response.follow(link, self.parse)

    def parse_article(self, response):
        # Extract article data
        title = response.css('h1.entry-title::text').get()
        author = response.css('span.author.vcard a.author-url.url.fn.n::text').get()
        date = response.css('time.entry-date.published::text').get()
        content = ''.join(response.css('.entry-content p::text').getall())
        tags = response.css('.post-tags a::text').getall()
        categories = categories = response.css('a.penci-cat-name span::text').getall()

        yield {
            'title': title,
            'author': author,
            'date': date,
            'content': content,
            'tags': tags,
            'categories': categories,
            'url' : response.url,
        }

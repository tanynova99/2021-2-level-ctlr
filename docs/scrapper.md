# Retrieve raw data from World Wide Web

> Python competencies required to complete this tutorial:
> * working with external dependencies, going beyond Python standard library
> * working with external modules: local and downloaded from PyPi
> * working with files: create/read/update
> * downloading web pages
> * parsing web pages as HTML structure

Scraping as a process contains following steps:
1. crawling the web-site and collecting all pages that satisfy given criteria
1. downloading selected pages content
1. extracting specific content from downloaded pages
1. saving necessary information

As a part of the first milestone, you need to implement scrapping logic as a `scrapper.py` module.
When it is run as a standalone Python program, it should perform all aforementioned stages.

## Executing scrapper

Example execution (`Windows`):

```bash
python scrapper.py
```

Expected result:
1. `N` articles from the given URL are parsed
1. all articles are downloaded to the `tmp/articles` directory. `tmp` directory content:
```
+-- 2021-2-level-ctlr
    +-- tmp
        +-- articles
            +-- 1_raw.txt     <- the paper with the ID as the name
            +-- 1_meta.json   <- the paper meta-information
            +-- ...
```

> NOTE: When using CI (Continuous Integration), generated `dataset.zip` is available in
> build artifacts. Go to `Actions` tab in GitHub UI of your fork, open the last job and
> if there is an artifact, you can download it.

## Configuring scrapper

Scrapper behavior is fully defined by a configuration file that is called 
`scrapper_config.json` and it is placed at the same level as `scrapper.py`. It is JSON file,
simply speaking it is a set of key-value pairs. 


|Config parameter|Description|Possible values|
|:---|:---|:---|
|`seed_urls`| Entry points for crawling. Can contain several URLs as there is no guarantee that there will be enough article links on a single page|A list of URLs, for example `["https://www.nn.ru/text/?page=2", "https://www.nn.ru/text/?page=3"]`|
|`total_articles_to_find_and_parse`|Number of articles to parse|Integer values, should potentially work for at least `100` papers, but must not be too big|

## Assessment criteria

You state your ambitions on the mark by editing the file `config/target_score.txt` at the `line 2`. 
For example, such content:
```
# Target score for scrapper:
6

# Target score for pipeline:
0
```
would mean that you have made tasks for mark `6` and request mentors to check if you can get it.

> NOTE: when implementing the first part, make sure that the mark for pipeline is set to 0.
> This will disable tests for the second milestone, and you will be able to get green pull request.
> You will specify the mark different from zero for a pipeline once the first milestone is accepted.

1. Desired mark: **4**:
   1. `pylint` level: `5/10`;
   1. scrapper validates config and fails appropriately if the latter is incorrect;
   1. scrapper downloads articles from the selected newspaper;
   1. scrapper produces only `_raw.txt` files in the `tmp/articles` directory (*no metadata*);
1. Desired mark: **6**:
   1. `pylint` level: `7/10`;
   1. all requirements for the mark **4**;
   1. scrapper produces `_meta.json` files for each article, however, it is allowed for each
      meta file to contain reduced number of keys: `id`, `title`, `author`, `url`;
1. Desired mark: **8**:
   1. `pylint` level: `10/10`;
   2. all requirements for the mark **6**;
   3. scrapper produces `_meta.json` files for each article, meta file should be full: 
      `id`, `title`, `author`, `url`, `date`, `topics`. In contrast to the task for mark **6**,
       it is mandatory to collect a date for each of the articles in the appropriate format.
1. Desired mark: **10**:
   1. `pylint` level: `10/10`;
   1. all requirements for the mark **8**;
   1. given just one seed url, crawler can find and visit all website pages.

> NOTE: date should be in the special format. Read [dataset description](./dataset.md) 
> for technical details

## Implementation tactics

> NOTE: all logic for instantiating and using needed abstractions should be implemented
> in a special block of the module `scrapper.py`
```py
if __name__ == '__main__':
   print('Your code goes here')
```

### Stage 0. Choose the media

Start your implementation by selecting a website you are going to scrap.
Pick the website that interests you the most. If you plan on working on a mark
higher than **4**, make sure all the necessary information is present on your chosen website. 
Read more in the [course overview](../README.md) in the milestones section.

### Stage 1. Validate config first

Scrapper is configured by a special file `config/scrapper_config.json`.
The very first thing that should happen after scrapper is run is validation of the config.

Interface to implement:

```py
def validate_config(crawler_path):
    pass
```

`crawler_path` is the path to the config of the crawler. It is mandatory to call `validate_config()` 
with passing a global variable `CRAWLER_CONFIG_PATH` that should be properly
imported from the [`constants.py`](../constants.py) module.

Example call:

```py
seed_urls, max_articles = validate_config(CRAWLER_CONFIG_PATH)
```

* `seed_urls` - is a list of URLs specified in the config with a parameter 
`seed_urls`
* `max_articles` - is a number of articles to retrieve
specified in the config with a parameter 
`total_articles_to_find_and_parse`

When config is invalid:

1. one of the following errors is thrown (each exception description can be found in `crawler.py`):
   `IncorrectURLError`, `NumberOfArticlesOutOfRangeError`, 
   `IncorrectNumberOfArticlesError`
2. script immediately finishes execution

Alternatively, when config is correct, you should prepare appropriate environment for your scrapper to work.
Basically, you must check that a directory provided by `ASSETS_PATH` does in fact exist and is empty.
In order to do that, implement the following function:

```py
def prepare_environment(base_path):
    pass
```
It is mandatory to call this function after the config file is validated and before crawler is run.

> NOTE: you need to remove the folder if it exists and is not empty, then create an empty folder with this name

### Stage 2. Find necessary number of article URLs

#### Stage 2.1 Introduce Crawler abstraction

Crawler is an entity that visits `seed_urls` with the intention to collect
URLs of the articles that should be parsed later.

> **seed url** - this is a known term, you can read more in 
> [Wikipedia](https://en.wikipedia.org/wiki/Web_crawler#Overview) or any other more reliable source of information
> you trust.

Crawler should be instantiated with the following instruction:

```py
crawler = Crawler(seed_urls=seed_urls, 
                  total_max_articles=max_articles)
```

Crawler instance saves all constructor arguments in attributes with
corresponding names. Each instance should also have an
additional attribute `self.urls`, initialized with empty list.

#### Stage 2.2 Implement a method for collecting article URLs

Once the crawler is instantiated, it can be started by executing its 
method:

```py
crawler.find_articles()
```

The method should iterate over the list of seeds, 
download them and extract article URLs from it. As a result, 
the internal attribute `self.urls` should be filled with collected URLs.


> NOTE: at this point, an approach for extracting articles URLs is different for each website

> NOTE: each URL in `self.urls` should be a valid URL, not just a suffix. For example,
> we need `https://www.nn.ru/text/transport/2022/03/09/70495829/` instead of `text/transport/2022/03/09/70495829/`.

### Stage 3. Extract data from every article page

#### Stage 3.1 Introduce `HTMLParser` abstraction

`HTMLParser` is an entity that is responsible for extraction of all needed information
from a single article web page. Parser is initialized the following way:

```py
parser = HTMLParser(article_url=full_url, article_id=i)
```

> NOTE: For those who have chosen a scientific web resource, the name of a class for your parser should be
> `HTMLWithPDFParser` instead of `HTMLParser`. For the sake of documentation consistency, we will
> still call any parser as `HTMLParser`.

`HTMLParser` instance saves all constructor arguments in attributes with
corresponding names. Each instance should also have an
additional attribute `self.article`, initialized with a new instance of Article class.

Article is an abstraction that is implemented for you. You must use it in your
implementation. A more detailed description of the Article class can be found
[here](./article.md).

#### Stage 3.2 Implement main `HTMLParser` method

`HTMLParser` interface includes a single method `parse` that encapsulates the logic
of extracting all necessary data from the article web page. It should do the following:

1. download the web page;
1. initialize `BeautifulSoup` object on top of downloaded page (we will call it `article_bs`);
1. fill Article instance by calling private methods to extract text 
   (more details in the next sections).

`parse` method usage is straightforward:
```py
article = parser.parse()
```

As you can see, `parse` method returns the instance of `Article` that is stored in 
`self.article` field.

#### Stage 3.3 Implement extraction of text from article page

Extraction of the text should happen in the private `HTMLParser` method
`_fill_article_with_text`:

```py
def _fill_article_with_text(self, article_bs):
   pass
```

> NOTE: a method receives a single argument `article_bs`, which is an instance of 
> `BeautifulSoup` object, and returns `None`

A call to this method results in filling the internal Article instance with text.

> NOTE: it is very likely that the text on pages of a chosen website is split across different
> HTML blocks, make sure to collect text from them all.

For those who have chosen a scientific web resource, your `_fill_article_with_text` should collect 
text of each article from a PDF file. A link to this PDF should be present on each article page.
Then you need to follow certain steps:

1. find a URL to PDF using the `article_bs`
2. create instance of `PDFRawFile` defined in [`core_utils/pdf_utils.py`](../core_utils/pdf_utils.py)
   by passing an url to the PDF file and the article ID (look into the interface of `PDFRawFile.__init__` method)
3. download a file with `PDFRawFile.download` method
4. get a text from PDF by calling `pdf_file.get_text` method

> NOTE: Make sure you have installed `PyMuPDF` library (not `fitz` itself!) so that `PDFRawFile` works correctly

> IMPORTANT: when retrieving text from PDF files, you SHOULD NOT include references section, which contains 
> all related works that were cited in this article. This section is always the last section of a scientific paper

### Stage 4. Save article (Stages 0-4 are required to get the mark 4)

Make sure that you save each `Article` object as a text file on the file system by
using the appropriate API method `save_raw`:

```py
article.save_raw()
```

As we return the `Article` instance from the `parse` method, saving the article is out of
scope of an `HTMLParser`. This means that you need to save the articles in the place where you
call `HTMLParser.parse()`.

### Stage 5. Collect basic article metadata (Stages 0-5 are required to get the mark 6)

According to the [dataset definition](./dataset.md), the dataset that is generated by your code
should contain meta-information about each article including its id, title, author.

You should extend `HTMLParser` with a method `_fill_article_with_meta_information`:

```py
def _fill_article_with_meta_information(self, article_bs):
   pass
```

> NOTE: method receives a single argument `article_bs` which is an instance of 
> `BeautifulSoup` object and returns `None`

A call to this method results in filling the internal Article instance with meta-information.

> NOTE: if there is no author in your newspaper, contact your mentor to find possible workarounds.

> NOTE: if your source provides information about just one author, save it as a string. 
> However, in case there are several authors, you are expected to store their names as a list of strings. 

> NOTE: for those who have chosen a scientific web resource metadata should be extracted from the 
> HTML page, and NOT from PDF file

### Stage 6. Collect advanced metadata: publication date and topics

There is plenty of information that can be collected from each page, much more than title and
author. It is very common to also collect publication date. Working with dates often becomes
a nightmare for a data scientist. It can be represented very differently: `2009Feb17`, 
`2009/02/17`, `20130623T13:22-0500`, or even `48/2009` (do you understand what 48 stand for?). 

The task is to ensure that each article metadata is extended with dates. However, the task is
even harder as you have to follow the required format. In particular, you need to translate 
it to the format shown by example: `2021-01-26 07:30:00`. 
For example, in [this paper](https://www.nn.ru/text/realty/2021/01/26/69724161/) it is stated that 
the article was published at `26 ЯНВАРЯ 2021, 07:30`, but in the meta-information it must 
be written as`2021-01-26 07:30:00`.

> HINT: use [`datetime`](https://docs.python.org/3/library/datetime.html) module for such 
> manipulations. In particular, you need to parse the date from your website that is represented 
> as a string and transform it to the instance of `datetime`. For that it might be useful
> to look into [`datetime.datetime.strptime()`](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)
> method.

> HINT #2: inspect Article class for any date transformations

Except for that, you are also expected to extract information about topics, or 
keywords, which relate to the article you are parsing. You are expected to store
them in a meta-information file as a list-like value for the key `topics`.
In case there are not any topics or keywords present in your source,
leave this list empty. 

You should extend `HTMLParser` method `_fill_article_with_meta_information`
with date manipulations and topics extraction.

### Stage 7. Determine the optimal number of seed URLs (Stages 0-7 are required to get the mark 8)

As it was stated in Stage 2.1, "Crawler is an entity that visits `seed_urls` with the 
intention to collect URLs with articles that should be parsed later." Often you can
reach the situation when there are not enough article links on the given URL. For example,
you may want to collect 100 articles whereas each newspaper page contains links to only 10 articles. 
This brings the need in at least 10 seed URLs to be used for crawling. At this stage
you need to ensure that your Crawler is able to find and parse the required number of articles. 
Do this by determining exactly how many seed URLs it takes.

As before, such settings are specified in the config file.

> IMPORTANT: ensure you have enough seeds in your configuration file to get at least 100 
> articles in your dataset. 100 is a required number of papers for the final part of the
> course.

### Stage 8. Turn your crawler into a real recursive crawler (Stages 0-8 are required to get the mark 10)

Crawlers used in production or even just for collection of documents from a website should be 
much more robust and tricky than what you have implemented during the previous steps. To name
a few challenges:

1. Content is not in HTML. Yes, it can happen that your website is an empty HTML by default and content appears 
   dynamically when you click, scroll, etc. For example, many pages have so-called virtual scroll, it is when new 
   content appears when you scroll the page. You can think of feed in VKontakte, for example.
1. The website's defense against your crawler. Even if data is public, your crawler that sends thousands of requests 
   produces huge load on the server and exposes risks for business continuity. Therefore, websites may 
   reject too much traffic of suspicious origins.
1. There may be no way to specify seed URLs - due to website size or budget constraints. Imagine you need to 
   collect 100k articles of the Wikipedia. Do you think you would be able to copy-paste enough seeds? How 
   about the task of collection 1M articles?
1. Software and hardware limitations and accidents. Imagine you have your crawler running for 24 hours, and 
   it crashes. If you have not mitigated this risk, you lose everything and have to restart your crawler.  

And we are not talking about such objective challenges as impossibility of building universal
crawlers.

Therefore, your Stage 8 is about addressing some of these questions. In particular, you need to 
implement your crawler in a recursive manner: you provide a single seed url of your newspaper, and it
visits every page of the website and collects *all* articles from the website. You need to
make a child of `Crawler` class and name it `CrawlerRecursive`. Follow the interface of Crawler.

A required addition is an ability to stop crawler at any time. When it is started again, it
continues search and crawling process without repetitions. 

> HINT: think of storing intermediate information in one or few files? What information do you
> need to store?

> NOTE: For those who have chosen a scientific web resource when you scrape your website,
> you can get monolithic PDF files, especially when you are working with
> old and respected journals. Generally, if you meet such a PDF and there is a way to collect
> 100 articles without parsing such monolithic PDF files, you are welcome to do that, and you can 
> simply ignore such files. At the same time, if you cannot collect enough articles and there are
> monolithic issues of your journal, you need to implement your own `PDFCrawler` and `PDFParser`
> following all the guidelines for plain versions of crawler and parser.

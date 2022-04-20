# Technical Track of Computer Tools for Linguistic Research (2021/2022)

As a part of a compulsory course 
[Computer Tools for Linguistic Research](https://www.hse.ru/en/edu/courses/494759476)
in [National Research University Higher School of Economics](https://www.hse.ru/).

This technical track is aimed at building basic skills for retrieving data from external
WWW resources and processing it for future linguistic research. The idea is to automatically 
obtain a dataset that has a certain structure and appropriate content, 
perform morphological analysis using various natural language processing (NLP) 
libraries. [Dataset requirements](./docs/dataset.md).

Instructors: 

* [Khomenko Anna Yurievna](https://www.hse.ru/org/persons/65858472) - linguistic track lecturer
* [Lyashevskaya Olga Nikolaevna](https://www.hse.ru/staff/olesar) - linguistic track lecturer
* [Demidovskij Alexander Vladimirovich](https://www.hse.ru/staff/demidovs#sci) - technical track lecturer
* [Uraev Dmitry Yurievich](https://www.hse.ru/org/persons/208529395) - technical track practice lecturer
* [Kazyulina Marina Sergeevna](https://t.me/poemgranate) - technical track assistant

## Project Timeline

1. **Scrapper**
   1. Short summary: Your code can automatically parse a media website you are going to choose, 
      save texts and its metadata in a proper format
   1. Deadline: *March 25th, 2022*
   1. Format: each student works in their own PR
   1. Dataset volume: 5-7 articles
   1. Design document: [./docs/scrapper.md](./docs/scrapper.md)
   1. Additional resources:
      1. List of media websites to select from: at the `Resources` section on this page
1. **Pipeline**
   1. Short summary: Your code can automatically process raw texts from previous step,
      make point-of-speech tagging and basic morphological analysis.
   1. Deadline: *April 29th, 2022*
   1. Format: each student works in their own PR
   1. Dataset volume: 5-7 articles
   1. Design document: [./docs/pipeline.md](./docs/pipeline.md)

## Lectures history

|Date|Lecture topic|Important links|
|:--:|:---|:---|
|21.02.2022|**Lecture:** Exceptions: built-in and custom for error handling and information exchange.|[Introduction tutorial](https://realpython.com/python-exceptions/)|
|25.02.2022|**Practice:** Programming assignment: main concept and implementation details.|**N/A**|
|04.03.2022|**Lecture:** installing external dependencies with `python -m pip install -r requirements.txt`, learning `requests` library: basics, tricks. **Practice:** downloading your website pages, working with exceptions.|[Exceptions practice](./seminars/03.04.2022/try_exceptions.py), [`requests` practice](./seminars/03.04.2022/try_requests.py)|
|11.03.2022|**Lecture:** learning `beautifulsoup4` library: find elements and get data from them. **Practice:** parsing your website pages.|[`beautifulsoup4` practice](./seminars/03.11.2022/try_beautiful_soup.py)|
|18.03.2022|**Lecture:** working with file system via `pathlib`, `shutil`. **Practice:** parsing dates, creating and removing folders.|[Dates practice](./seminars/03.18.2022/try_dates.py), [`pathlib` practice](./seminars/03.18.2022/try_fs.py)|
|25.03.2022|**First deadline:** crawler assignment|**N/A**|
|01.04.2022|**EXAM WEEK:** skipping lecture and seminars|**N/A**|
|08.04.2022|**Lecture:** Programming assignment (Part 2): main concept and implementation details. Lemmatization and stemming. Existing tools for morphological analysis|**N/A**|
|15.04.2022|**Lecture:** morphological analysis via `pymystem3`, `pymorphy2`. **Practice:** analyzing words|[`pymystem3` basics](./seminars/04.15.2022/try_mystem.py), [`pymorphy2` basics](./seminars/04.15.2022/try_pymorphy.py)|

## Technical solution

| Module                                                        | Description                                           | Component | I need to know them, if I want to get at least |
|:--------------------------------------------------------------|:------------------------------------------------------|:---|:---|
| [`pathlib`](https://pypi.org/project/pathlib/)                | module for working with file paths                    | scrapper | 4 |
| [`requests`](https://pypi.org/project/requests/)              | module for downloading web pages                      | scrapper | 4 |
| [`BeautifulSoup4`](https://pypi.org/project/beautifulsoup4/)  | module for finding information on web pages           | scrapper | 4 |
| [`PyMuPDF`](https://pymupdf.readthedocs.io//)                 | **Optional** module for opening and reading PDF files | scrapper | 4 |
| [`lxml`](https://pypi.org/project/lxml/)                      | **Optional** module for parsing HTML as a structure   | scrapper | 6 |
| [`wget`](https://pypi.org/project/wget/)                      | **Optional** module for parsing HTML as a structure   | scrapper | 6 |
| [`pymystem3`](https://pypi.org/project/pymystem3/)            | module for morphological analysis                     | pipeline | 6 |
| [`pymorphy2`](https://pypi.org/project/pymorphy2/)            | module for morphological analysis                     | pipeline | 8 |
| [`pandas`](https://pypi.org/project/pandas/)                  | module for table data analysis                        | pipeline | 10 |

Software solution is built on top of three components:
1. [`scrapper.py`](./scrapper.py) - a module for finding articles from the given media, extracting text and
   dumping it to the file system. Students need to implement it.
1. [`pipeline.py`](./pipeline.py) - a module for processing text: point-of-speech tagging and 
   basic morphological analysis. Students need to implement it.
1. [`article.py`](core_utils/article.py) - a module for article abstraction to encapsulate low-level
   manipulations with the article
   
## Handing over your work

Order of handing over:

1. lab work is accepted for oral presentation.
2. a student has explained the work of the program and showed it in action.
3. a student has completed the min-task from a mentor that requires some slight code modifications.
4. a student receives a mark:
   1. that corresponds to the expected one, if all the steps above are completed and mentor is satisfied with 
      the answer;
   2. one point bigger than the expected one, if all the steps above are completed and mentor is very 
      satisfied with the answer;
   3. one point smaller than the expected one, if a lab is handed over one week later than the deadline and 
      criteria from 4.1 are satisfied;
   4. two points smaller than the expected one, if a lab is handed over more than one week later than 
      the deadline and criteria from 4.1 are satisfied.

> NOTE: a student might improve their mark for the lab, if they complete tasks of the next level after handing over
> the lab.

A lab work is accepted for oral presentation if all the criteria below are satisfied:

1. there is a Pull Request (PR) with a correctly formatted name:
   `Laboratory work #<NUMBER>, <SURNAME> <NAME> - <UNIVERSITY GROUP NAME>`. Example: `Laboratory work #1, Kuznetsova Valeriya - 19FPL1`.
2. has a filled file `target_score.txt` with an expected mark. Acceptable values: 4, 6, 8, 10.
3. has green status.
4. has a label `done`, set by mentor.
 
## Resources

1. Academic performance: [link](https://cloud.mail.ru/public/HwWW/29D1hTApp) 
1. Media websites list: [link](https://cloud.mail.ru/public/P1jw/g48YcWyYz)
1. Python programming course from previous semester: [link](https://github.com/fipl-hse/2021-2-level-labs)
1. Scrapping tutorials: [YouTube series (russian)](https://youtu.be/7hn1_t2ZtJQ)
1. [HOWTO: Running tests](./docs/tests.md)

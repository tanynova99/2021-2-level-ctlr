# Process raw data

> Python competencies required to complete this tutorial:
> * working with external dependencies, going beyond Python standard library
> * working with external modules: local and downloaded from PyPi
> * working with files: create/read/update
> * applying basic cleaning techniques to the raw text: tokenization, lemmatization
> * extracting linguistic data from the raw text: part of speech and its attributes

Processing data breaks down in the following steps:
1. loading raw data
1. tokenizing the text 
1. performing necessary transformations, such as lemmatization or stemming, and extract 
   valuable information from the text, such as detect each word part of speech.
1. saving necessary information

As a part of the second milestone, you need to implement processing logic as a `pipeline.py` module.
When it is run as a standalone Python program, it should perform all aforementioned stages.

## Executing pipeline

Example execution (`Windows`):

```bash
python pipeline.py
```

Expected result:
1. `N` raw texts previously collected by scrapper are processed
1. each article has a processed version (or versions) saved in the `tmp/articles` directory. An example `tmp` directory content for grade 8:
```
+-- 2020-2-level-ctlr
    +-- tmp
        +-- articles
            +-- 1_raw.txt <- the paper with the ID as the name
            +-- 1_meta.json <- the paper meta-information
            +-- 1_cleaned.txt <- lowercased text with no punctuation
            +-- 1_single_tagged.txt <- lemmatized text with one set of tags
            +-- 1_multiple_tagged.txt <- lemmatized text with two sets of tags 
```

> NOTE: When using CI (Continuous Integration), generated `dataset.zip` is available in
> build artifacts. Go to `Actions` tab in GitHub UI of your fork, open the last job and
> if there is an artifact, you can download it.

## Configuring pipeline

Processing behavior must follow several steps:

1. pipeline takes a raw dataset that is collected by
   `scrapper.py` and placed at `ASSETS_PATH` (see `constants.py` for a particular place)
1. pipeline goes through each raw file, for example `1_raw.txt`
1. pipeline cleans the text by lowercasing it and removing punctuation marks, saves the result in file,
   for example, `1_cleaned.txt`
1. pipeline performs tokenization, lemmatization and morphological analysis of the text, saving the resulting 
   text to `1_single_tagged.txt`
1. pipeline performs additional morphological analysis by another python library and saves 
   double-tagged text to `1_multiple_tagged.txt`

## Assessment criteria

You state your ambition on the mark by editing the file `target_score.txt` at the `line 5`. For example, such content:

```bash
...
# Target score for pipeline:
6
```
would mean that you have made tasks for mark `6` and request mentors to check if you can get it.

1. Desired mark: **4**:
   1. `pylint` level: `5/10`
   1. pipeline validates that raw dataset has a proper structure and fails appropriately if the latter is incorrect.
      Criteria:
        1. dataset exists (there is a folder)
        1. dataset is not empty (there are files inside)
        1. dataset is balanced: there are only files that follow the naming conventions:
            1. `N_raw.txt` where N is a valid number
            1. Numbers of articles are from 1 to N without any slips
   1. pipeline tokenizes text in each file, removes punctuation,
      and casts it to the lower case (*no lemmatization or tagging*)
      Example raw text: [config/test_files/0_raw.txt](../config/test_files/0_raw.txt). 
      Desired output: 
      [config/test_files/reference_score_four_test.txt](../config/test_files/reference_score_four_test.txt)
   1. pipeline produces `N_cleaned.txt` files in the `tmp/articles`
1. Desired mark: **6**:
   1. `pylint` level: `7/10`
   1. all requirements for the mark **4**
   1. pipeline produces `N_single_tagged.txt` files for each article, where each word is lemmatized and has a properly formatted tag.
      Example raw text: [config/test_files/0_raw.txt](../config/test_files/0_raw.txt). 
      Desired output: 
      [config/test_files/reference_test.txt](../config/test_files/reference_test.txt).
    1. pipeline uses `pymystem3` library to perform lemmatization and tagging (more details in the description below) 
    1. `pymystem3` tags are represented in angle brackets
1. Desired mark: **8**:
   1. `pylint` level: `10/10`
   1. all requirements for the mark **6**
   1. pipeline additionally uses `pymorphy2` library to perform tagging (more details in the description below)
      Example raw text: [config/test_files/0_raw.txt](../config/test_files/0_raw.txt). 
      Desired output: 
      [config/test_files/reference_score_eight_test.txt](../config/test_files/reference_score_eight_test.txt).
   1. `pymorphy2` tags are represented in brackets
   2. pipeline produces `N_multiple_tagged.txt` files for each article, where each word is lemmatized and followed by two sets of tags
1. Desired mark: **10**:
   1. `pylint` level: `10/10`
   1. all requirements for the mark **8**
   1. an additional pipeline is introduced `pos_pipeline.py` that:
      1. collects frequencies of parts of speech in each text
      1. extends `_meta.json` files with this information
      1. visualizes this distribution as `.png` files that are created for each article
         and saved into `N_image.png` files

## Implementation tactics

> NOTE: all logic for instantiating and using needed abstractions should be implemented
> in a special block of the module `pipeline.py`
```python
def main():
    print('Your code goes here')

if __name__ == '__main__':
    main()
```

### Stage 0. Collect raw dataset with your `scrapper.py`

You will not be able to start your implementation if there is no collected dataset.
Dataset is collected by `scrapper.py`. Therefore, if you still do not have it working,
fix all the issues. Health check would be existence of a raw dataset in the `tmp/articles`
folder on your computer. For more details on how to implement `scrapper.py` refer to the 
[scrapper tutorial](./scrapper.md).

### Stage 1. Validate dataset first

Pipeline expects that dataset is collected. It must not start working if dataset is invalid.
The very first thing that should happen after pipeline is run is the validation of the dataset.

Interface to implement:

```python
def validate_dataset(dataset_path):
    pass
```

`dataset_path` is the path to the dataset. It is mandatory to call this
method with passing a global variable `ASSETS_PATH` that should be properly
imported from the `constants.py` module.

> NOTE: in order to operate paths, it is required to use `pathlib` module

Example call:

```python
validate_dataset(ASSETS_PATH)
```

When dataset is valid, method returns `None`.

When dataset is invalid:

1. one of the following errors is thrown (a description for each exception is provided in `pipeline.py`):
   `FileNotFoundError`, `NotADirectoryError`, `InconsistentDatasetError`,
   `EmptyDirectoryError`.
2. script immediately finishes execution.

### Stage 2. Introduce corpus abstraction: `CorpusManager`

As we discussed multiple times, when we are working from our Python programs with the real world entities, we need to 
emulate their behavior by new abstractions.
If we think of the Pipeline and consider the Single Responsibility Principle, we will quickly
realize that it is not the responsibility of the Pipeline to know where the dataset files
are located and how to read/write to them, etc. Therefore, we need a new abstraction to be
responsible for such tasks. We call it `CorpusManager`.

#### Stage 2.1 Introduce `CorpusManager` abstraction

`CorpusManager` is an entity that knows where the dataset is placed and what are the available
files of this dataset.

`CorpusManager` should be instantiated with the following instruction:

```python
corpus_manager = CorpusManager(path_to_dataset=ASSETS_PATH)
```

`CorpusManager` instance saves all constructor arguments in attributes with
corresponding names. Each instance should also have an
additional attribute `self._storage` of a dictionary type and filled with
information about the files. For filling instructions read more in the next
stage (Stage 2.2).

> NOTE: remember to use `pathlib` to create file path object

#### Stage 2.2 Implement method for filling files storage

During initialization of the `CorpusManager`, it should scan the provided folder
path and register each dataset entry. All the storage is represented as 
`self._storage` attribute. Filling the storage should be done by executing this 
method:

```python
def _scan_dataset(self):
    pass
```

> NOTE: call this method during initialization and save the results in 
> `self._storage` attribute.

> SELF CHECK: Can you explain why the name of the method starts with underscore? 

The method should contain logic for iterating over the content of the folder, finding
all `_raw.txt` files and creating an `Article` instance for each file.

> NOTE: Article constructor expects URL as the first argument. It should be safe
> to pass None instead of the real URL. Pipeline does not need to know where was the 
> article downloaded from.

As it was stated before, `self._storage` attribute is just a dictionary. Keys are
ids of the files, values are instances of the `Article` class. For example,
pipeline finds a file `1_raw.txt`. Then we put new pair to the storage:

```python
self._storage[1] = Article(url=None, article_id=1)
```

#### Stage 2.3 Implement a method for retrieval of files storage

`self._storage` attribute is not a part of the `CorpusManager` interface, therefore we need 
a special getter - a method that just returns that storage value:

```python
def get_articles(self):
    pass
```

> SELF CHECK: Can you explain why we might need getters? 

> NOTE: `CorpusManager` knows where are the files, it can easily find them by id,
> but it is not its responsibility to perform actual file reads and writes - it offloads
> it to the entity responsible for that - to the `Article` abstraction

### Stage 3. Introduce abstraction for elementary tokens in corpus: `MorphologicalToken`

`MorphologicalToken` is responsible for storing morphological analysis results and transforming them
into text format. As you already know, morphological analysis allows to study a particular word.
For example, analyzing `красивая` we can get a lemmatized version: `красивый` and word
attributes `A=им,ед,полн,жен`. `MorphologicalToken` is needed to store all this information.

`MorphologicalToken` should be instantiated with the following instruction:

```python
token = MorphologicalToken(original_word)
```

`MorphologicalToken` instance saves all constructor arguments in attributes with
corresponding names. Each `MorphologicalToken` instance should also have following attributes: `self.normalized_form`,
`self.mystem_tags`, `self.pymorphy_tags`. Initialize them with empty strings.

We will later use `MorphologicalToken` when writing processed text in files.


### Stage 4. Introduce abstraction for processing texts in corpus: `TextProcessingPipeline`

Pipeline is responsible for applying processing techniques to the raw text, such as
tokenization, lemmatization, etc.

`TextProcessingPipeline` should be instantiated with the following instruction:

```python
corpus_manager = CorpusManager(...)
...
pipeline = TextProcessingPipeline(corpus_manager=corpus_manager)
```

`TextProcessingPipeline` instance constructor argument `corpus_manager` in attribute with
the same name.

### Stage 5. Perform basic text preprocessing and save results (Stages 0-5 are required to get the mark 4)

To get a mark not lower than 4, your pipeline must perform basic text preprocessing and save results in the files with 
the names following the pattern `N_cleaned.txt`.
See examples for a better understanding:
Raw text: [0_raw.txt](../config/test_files/0_raw.txt). 
Desired output: [0_cleaned.txt](../config/test_files/reference_score_four_test.txt)

> NOTE: if you decide to do a work for mark 4, then you should know that the dataset that you are going to generate will
>not follow the guidelines and requirements of your final project that you will make in groups.
> Please consider doing the work for mark 6 at least.   

#### Stage 5.1. Implement simplified logic of `TextProcessingPipeline`

`TextProcessingPipeline` is executed with a simple interface method that you need to implement:

```python
pipeline.run()
```

Once executed, `pipeline.run()` iterates through the available articles taken from `CorpusManager`, reads each file, 
performs processing depending on the mark you want to get (more details below) and writes processed text to files.

To get at least mark 4, you need to implement following processing:
1. tokenization (split into words),
1. punctuation removal

> NOTE: it is mandatory to get articles with the `CorpusManager.get_articles` method

> NOTE: it is mandatory to read article with the `Article.get_raw_text` method

> Health check: try to implement `pipeline.run()` in a way that is goes through the articles 
> collected by `CorpusManager.get_articles`, reads each of them with `Article.get_raw_text`
> and then writes to the file as a processed article with the `Article.save_as` method.
> At least you will see that everything works to this moment and you can proceed to implementing
> core logic of pipeline.


All processing logic is encapsulated in the following protected method:
```py
def _process(text):
    pass
```
It returns the list of `MorphologicalToken` instances where each instance is initialized with the word in the same form 
you took from the text, for example: 

```py
MorphologicalToken(original_word="красивая")
```

> NOTE: `_process` method should be called in the `run` method

#### Stage 5.2. Implement a method for correct cleaned token display

Given the fact that we want to save the results of preprocessing, it is necessary to set up correct display of 
morphological tokens.
Considering single responsibility principle, it is not `TextProcessingPipeline` that should know how exactly each token 
must be represented. Instead, implement the following method in `MorphologicalToken` abstraction:
```python
def get_cleaned(self):
    pass
```

This getter returns a lowercased version of a word form stored in `self.original_word`.

#### Stage 5.3. Save the results of text preprocessing

In order to save each article to its separate file, inspect the method `Article.save_as(kind)` in the `article.py` module.
Pay attention to the fact that this method is able to produce different sorts of files depending on the argument `kind` 
that you pass to it.

> NOTE: it is mandatory to use `ArtifactType` attributes as a `kind` argument for `Article.save_as()`

For example, if you store your preprocessed text in the variable `text` while working with a particular Article instance 
stored in the variable `article`, you should call saving method the following way:
```python
article.save_as(text=text, kind=ArtifactType.cleaned)
```

It will generate a file with a name `N_cleaned.txt` where `N` is the index of your article.

> NOTE: in is mandatory to save generated text to files in the `run()` method.

### Stage 6. Perform morphological analysis and save results (Stages 0-6 are required to get the mark 6)

To get a mark not lower than 6, your pipeline, in addition, must perform morphological text analysis using `pymystem3` 
and save results in the files with the names following the pattern `N_single_tagged.txt`.
See examples for a better understanding:
Raw text: [0_raw.txt](../config/test_files/0_raw.txt). 
Desired output: [0_single_tagged.txt](../config/test_files/reference_score_eight_test.txt)

#### Stage 6.1. Extend logic of `TextProcessingPipeline` with morphological analysis

For mark 6, apart from tokenization, punctuation removal and casting to lowercase, you must implement the following processing:
1. lemmatization,
1. morphological analysis,
1. tagging

Strong requirement is to use [pymystem3](https://pypi.org/project/pymystem3/) library for this task.

> NOTE: it is recommended to rely on `pymystem3` ability to process text as a whole and perform
> lemmatization and morphological analysis at once. There are several reasons to do that,
> but from the linguistic perspective it would be interesting for you to remember that 
> context-aware lemmatization works better that lemmatization of each word separately.

Use the following way to analyze the text:

```python
result = Mystem().analyze(text)
```

Here, `text` is the text that you want to process, e.g. raw text of the article, and `result` is the
result of morphological analysis. Inspect the `result` as you need.

> NOTE: use debug or print the content of `result` - you will find everything you need there. 

> HINT: `result['text']` is likely to have the original word. Use the same approach to find tags and normalized form

Keep in mind that all processing logic is encapsulated in the protected `_process(text)` method, which returns the list 
of `MorphologicalToken`.
Do not forget to fill in `normalized_form` and `mystem_tags` fields.

#### Stage 6.2. Implement a method for correct single-tagged token display

Again, it is `MorphologicalToken`'s responsibility to control tokens' display. Therefore, in order to be able to generate 
correct single-tagged files, it is necessary to implement the following method: 
```python
def get_single_tagged(self):
    pass
```
This getter returns a single string composed of a word lemma stored in 
`self.normalized_form` and `pymystem3` tags. Tags must be in angle brackets. 

#### Stage 6.3. Save the results of text tagging

In order to save each article to its separate `N_single_tagged.txt` file, call the method `Article.save_as(kind)`from the 
`article.py` module for each of your parsed articles. Use an appropriate `ArtifactType` attribute as `kind` argument.


### Stage 7. Deepen morphological analysis and save results (Stages 0-7 are required to get the mark 8)

To get a mark not lower than 8, you should also analyze text using `pymorphy2` and save results in the files with the 
names following the pattern `N_multiple_tagged.txt`.
See examples for a better understanding:
> Raw text: [0_raw.txt](../config/test_files/0_raw.txt). 
> Desired output: 
> [0_multiple_tagged.txt](../config/test_files/reference_score_eight_test.txt).

#### Stage 7.1. Extend logic of `TextProcessingPipeline` with additional morphological analysis

For mark 8 you need to implement processing from Stage 5.2 plus:
1. morphological analysis with `pymorphy2`.

Strong requirement is to use [pymorphy2](https://pypi.org/project/pymorphy2/) library for morphological analysis.

> NOTE: it is recommended to have morphological analysis done after `pymystem3`. In other words, 
> you extract a list of `MorphologicalToken` with `pymystem3` and then iterate through them, 
> filling each token with `pymorphy2` tags.

You will need `MorphAnalyzer.parse` [docs](https://pymorphy2.readthedocs.io/en/stable/user/guide.html#id3).

> NOTE: make sure you have filled `pymorphy2` tags in the token:
> ```python
> token.pymorphy_tags = ...
> ```

> NOTE: It is still `_process` method that contains all the processing logic, including additional analysis 
> done with `pymorphy2`.


#### Stage 7.2. Set up correct multiple-tagged token display

 In order to be able to generate correct multiple-tagged texts, it is necessary to implement the following method in the 
 `MorphologicalToken` abstraction: 
```py
def get_multiple_tagged(self):
    pass
```
This getter returns a single string composed of:
- a word lemma stored in `self.normalized_form` 
- `pymystem3` tags in angle brackets
- `pymorphy2` tags in round brackets

#### Stage 7.3. Save the results of text double-tagging

In order to save each article to its separate `N_multiple_tagged.txt` file, call the method `Article.save_as(kind)`from 
the `article.py` module for each of your parsed articles. Use an appropriate `ArtifactType` attribute as `kind` argument.


### Stage 8. Implement analytical pipeline: `POSFrequencyPipeline` (Stages 0-6 are required to get the mark 10)

We have just made the text processing pipeline. However, this is only the beginning of your 
linguistic research: you have the data and now need to start analyzing it, gaining insights, understanding it
and finding hidden meanings. During this stage we will make a small pipeline that will compute
distribution of various parts of speech in our texts, visualize it and, maybe, it will give better understanding of the text.

This is a sample result we are going to obtain: 
![](./sample_visualization.png)

#### Stage 8.1. Introduce `POSFrequencyPipeline` abstraction

Create a file `pos_frequency_pipeline.py` with a class `POSFrequencyPipeline`. All code should be written in the
`main` function. `POSFrequencyPipeline` is instantiated in the similar manner as the `TextProcessingPipeline`:

```python
corpus_manager = CorpusManager(...)
...
pipeline = POSFrequencyPipeline(corpus_manager=corpus_manager)
```

#### Stage 8.2. Implement core logic of `POSFrequencyPipeline`

`POSFrequencyPipeline` is executed with the same interface method that you need to implement:

```python
pipeline.run()
```

Once executed, `pipeline.run()`:
1. iterates through the available articles taken from `CorpusManager`,
1. reads each file,
1. calculates frequencies of each part of speech
1. writes them to the meta file
1. visualizes them (frequencies) in a form of images with names following this convention: `N_image.png`.

> NOTE: it is mandatory to get articles with the `CorpusManager.get_articles` method

> NOTE: it is mandatory to use `Article.get_file_path` method

> NOTE: make sure that resulting .json files are valid: they must contain no more than one dictionary-line object


For visualization, you need to use `visualize` method from `visualizer.py` module available
in the root folder of the project. Sample usage:

```python
visualize(statistics=frequencies_dict, path_to_save=ASSETS_PATH / '1_image.png')
```

#### Stage 8.3. Ensure you only use `pathlib` to work with file paths

As we discussed during lectures it is always better to have something designed specifically for the
given task. Comparing `os` and `pathlib` modules, the latter is the one that is designed for most of
file system related operations.

Make sure you use only `pathlib` in the code you write.

> NOTE: do not change modules external to your code, for example `article.py` - consider them as
> not available for installation. If you see a way to improve external modules, propose them in a 
> separate PR - mentors will review them separately and give you bonuses as any improvements are appreciated
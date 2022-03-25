# Web scraper

A web scraper for getting the sentences from a website.

## How to use

**Requires [Python](https://www.python.org/) to run.**

### Install dependencies

Open a terminal in the root folder of this project, and run the following command to install the dependencies:

```
python -m pip install -r requirements.txt
```

### Run the script

To run the script, use the following command:

```
python main.py <base-url> <output>
```

The arguments `base-url` and `output` are required to run the script.

- `base-url`: The URL that the web scraper will scrape from.
- `output`: The name of the file that the scraped text will be written to.

There are also some optional arguments.

- `--class-name`: Specifies a class name to scrape sentences from.
- `--min`: Specifies the minimum amount of words a sentence needs to be saved. Default value is 5.
- `--max`: Specifies the maximum amount of words a sentence can have to be saved. Default value is 30.
- `--limit`: Specifies the maximum numbers of sentences to retrieve from a text. Default value is 20.
- `--paths`: Specifies paths from a website to scrape data from as space-separated list. If this argument is set, the specified paths will be appended to the `base-url`.
- `--paths-file`: Specifies a file that contains a line-separated list of paths to be appended to the end of the `base-url`.

### An example

To gather sentences from the paths `/about` and `/articles/123` on a website `example.com` and store them in a file `output.json`, the following command can be used:

```
python main.py example.com output.json --paths="/about /articles/123"
```

A file can also be used to specify paths. If you have a text file `paths.txt` that contains the following content:

```
/about
/articles/123
```

You can use the following command:

```
python main.py example.com output.json --paths-file=paths.txt
```

If you want to only get sentences from inside elements with the class name `article-section`, the `class-name` argument can be used:

```
python main.py example.com output.json --paths="/about /articles/123" --class-name=article-section
```

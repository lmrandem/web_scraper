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
python main.py <base-url> <output> <paths-file> <key>
```

The arguments `base-url`, `output`, `paths-file`, and `key` are required to run the script.

- `base-url`: The URL that the web scraper will scrape from.
- `output`: The name of the file that the scraped text will be written to.
- `paths-file`: A JSON file containing paths to retrieve text from.
- `key`: The key from the JSON file that points to the paths to use.

There are also some optional arguments.

- `--class-name`: Specifies a class name to scrape sentences from.
- `--min`: Specifies the minimum amount of words a sentence needs to be saved. Default value is 5.
- `--max`: Specifies the maximum amount of words a sentence can have to be saved. Default value is 30.
- `--limit`: Specifies the maximum numbers of sentences to retrieve from a text. Default value is 20.
- `--verbose`: Shows what the script is currently doing.

### An example

To gather sentences from the paths `/about` and `/articles/123` on a website `example.com` and store them in a file `output.json`, an input file is needed. Our `input.json` file looks like this:

```json
[
  {
    "item": "1",
    "path": "/about"
  },
  {
    "item": "2",
    "path": "/articles/123"
  }
]
```

The `item` is used an ID.

To extract sentences from the paths, the following command can be used:

```
python main.py example.com output.json input.json path
```

The first argument provided is `example.com`, which tells the script to use `example.com` as the base URL. The next argument tells the script to write to the file `output.json`. The third argument tells the script to read paths from `input.json`. And finally, the last arguments means that the script is going to use the `path` key from the JSON file.

If you want to retrieve text only from a certain part of a website, the optional `--class-name` argument can be used to tell the script to only gather text from child elements of elements with the given class name. For example, if you only want to retrieve text from elements under the class "article", the command would look like this:

```
python main.py example.com output.json input.json path --class-name=article
```

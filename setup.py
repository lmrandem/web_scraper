#!/usr/bin/env python
import setuptools
import sys
import os

assert sys.version_info >= (3, 6, 0), "Python 3.6+"
from pathlib import Path  # noqa E402

CURRENT_DIR = Path(__file__).parent
sys.path.insert(0, str(CURRENT_DIR))  # for setuptools.build_meta


def get_long_description() -> str:
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


USE_MYPYC = False
# To compile with mypyc, a mypyc checkout must be present on the PYTHONPATH
if len(sys.argv) > 1 and sys.argv[1] == "--use-mypyc":
    sys.argv.pop(1)
    USE_MYPYC = True

if USE_MYPYC:
    mypyc_targets = [
        "main.py",
    ]

    from mypyc.build import mypycify

    opt_level = os.getenv("MYPYC_OPT_LEVEL", "3")
    ext_modules = mypycify(mypyc_targets, opt_level=opt_level)
else:
    ext_modules = []

setuptools.setup(
    name="Web scraper",
    version="1.0.0",
    description="Scrape lexicon pages.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/lmrandem/web_scraper",
    ext_modules=ext_modules,
    python_requires=">=3.6",
    zip_safe=False,
    test_suite="tests.test"
)

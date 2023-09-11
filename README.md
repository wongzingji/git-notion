Markdown file synchronization
==========

Syncs Gitlab markdown files to Notion.

The scripts are modified based on the [git-notion](https://github.com/NarekA/git-notion) repository. It makes use of the [`md2notion` module](https://github.com/Cobertos/md2notion), which relies on the [unofficial Notion API for Python](https://github.com/jamalex/notion-py) (i.e. `https://www.notion.so/api/v3` where login info is not needed).

Modifications:
- Creating nested pages according to the folder hierarchy
- Giving an option to rewrite or append the content to the pages

----

### Installation
```bash
cd git-notion
pip install -e .
```

### Preparation
To import the markdown files to a **subpage** in Notion, you need to edit the `limit` parameter in `notion-py` library according to [this](https://github.com/NarekA/git-notion/issues/1#issuecomment-1171158725).


### Configuring

`NOTION_TOKEN_V2` - Can be found in your [browser cookies](https://www.redgregory.com/notion/2020/6/15/9zuzav95gwzwewdu1dspweqbv481s5) for the Notion page.
`NOTION_ROOT_PAGE` - URL for notion page. Repo docs will be a new page under this page.
`NOTION_IGNORE_REGEX` - Regex for paths to ignore.

These environment variables can be set.
```bash
export NOTION_TOKEN_V2=<YOUR_TOKEN>
export NOTION_ROOT_PAGE="https://www.notion.so/..."  # Can be in setup.cfg as well
export NOTION_IGNORE_REGEX="models/.*"               # Can be in setup.cfg as well
```

These parameters can be set in the `setup.cfg` for the repo.
```
[git-notion]
ignore_regex = models/.*
notion_root_page = https://www.notion.so/...
```

### Usage

```bash
# To upload your current directory
git-notion

# To upload another directory
git-notion --dir path/to/your/repo
```

### Issue
Issue could happen when uploading the files (images, pdfs, ...) since Notion API does not support file uploading, and we need to use cloud services as intermediate transmission, while there might be errors due to its request limit.


### Pushing to PYPI

```bash
bumpversion patch   # Look-up bumpversion
rm -rf dist/
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
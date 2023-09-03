Markdown file synchronization
==========

Syncs Gitlab markdown files to Notion.

The scripts are modified based on the [git-notion](https://github.com/NarekA/git-notion) repository. It makes use of the [`md2notion` module](https://github.com/Cobertos/md2notion), and relies on the [unofficial Notion API for Python](https://github.com/jamalex/notion-py).

The modification is mainly creating nested pages according to the folder hierarchy.


### Installation
```bash
cd git-notion
pip install -e .
```

### Preparation
To import the markdown files to a **subpage** in Notion, you need to edit the `limit` parameter in `notion-py` library according to [this](https://github.com/NarekA/git-notion/issues/1#issuecomment-1171158725).


### Configuring

`NOTION_TOKEN_V2` - Can be found in your [browser cookies](https://www.redgregory.com/notion/2020/6/15/9zuzav95gwzwewdu1dspweqbv481s5) for Notion's website.
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
Error related to [Notion request limits](https://developers.notion.com/reference/request-limits) could occur when uploading the images, so we might need to upload the images manually; Or rewrite the code with official API in the future.

If it is necessary to rewrite the code, the work might can be done on top of [this reporsitory](https://github.com/Arsenal591/notionfier), which uses official Notion API while its functions are not as perfect as `md2notion`. 


### Pushing to PYPI

```bash
bumpversion patch   # Look-up bumpversion
rm -rf dist/
python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
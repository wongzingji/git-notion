import hashlib
import os
import glob
from configparser import ConfigParser
import re
import logging

from notion.block import PageBlock
from notion.client import NotionClient
from md2notion.upload import upload


TOKEN = os.getenv("NOTION_TOKEN_V2", "")
_client = None


def get_client():
    global _client
    if not _client:
        _client = NotionClient(token_v2=TOKEN)
    return _client


def get_or_create_page(base_page, title):
    page = None
    for child in base_page.children.filter(PageBlock):
        if child.title == title:
            # get page
            page = child

    if not page:
        # create page
        page = base_page.children.add_new(PageBlock, title=title)
    return page


def upload_file(base_page, filename: str, page_title=None):
    page_title = page_title or filename # if no title specified, use file name
    page = get_or_create_page(base_page, page_title)
    hasher = hashlib.md5()
    with open(filename, "rb") as mdFile:
        buf = mdFile.read()
        hasher.update(buf)
    if page.children and hasher.hexdigest() in str(page.children[0]):
        return page

    for child in page.children:
        child.remove()
    # page.children.add_new(TextBlock, title=f"MD5: {hasher.hexdigest()}")

    with open(filename, "r", encoding="utf-8") as mdFile:
        upload(mdFile, page) # TODO: clear-previous/append/img tag
    
    return page


def sync_to_notion(md_folder: str = "."):
    '''
    strategy: overwrite
    '''
    os.chdir(md_folder)
    config = ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'setup.cfg'))
    name = os.path.basename(md_folder)

    root_page_url = os.getenv("NOTION_ROOT_PAGE") or config.get('git-notion', 'notion_root_page')
    ignore_regex = os.getenv("NOTION_IGNORE_REGEX") or config.get('git-notion', 'ignore_regex', fallback=None)
    root_page = get_client().get_block(root_page_url)
    page = get_or_create_page(root_page, name)
    for file in glob.glob("**/*.md", recursive=True):
        if ignore_regex is None or not re.match(ignore_regex, file):
            logging.info(file)
            if '/' in file: # nested path
                subpage = get_or_create_page(page, os.path.dirname(file))
                upload_file(subpage, file, page_title=os.path.basename(file))
            else:
                upload_file(page, file)


import requests
import os
import logging

from utils import response_or_error

class Issue2Notion():
    def __init__(self, token, issue_database_id):
        """
        Issue database properties:
        # TODO: These are properties which I think is important, to be checked
        # epic, labels, weight, timetracking, confidentiality, tasks, linked items, comment
        # `created time` is created automatically
        - id
        - iid
        - Name 
        - URL
        - Status
        - Project
        - Reviewer
        - Assignees
        - Milestone
        - Period
        - Due date
        """
        self.headers = {
            "Authorization": "Bearer " + token,
            "Notion-Version": "2022-02-22"
        }
        self.base_url = 'https://api.notion.com/v1'
        self.issue_database_id = issue_database_id
        self.properties = {
                    'id': {
                        'rich_text': [
                            {
                                'type': 'text',
                                'text': {
                                    'content': None
                                }
                            }
                        ]
                    },
                    'iid': {
                        "number": None
                    },
                    'Name': {
                        'title': [
                            {
                                'text': {
                                    'content': None
                                }
                            }
                        ]
                    },
                    'URL': {
                        "url": None
                    },
                    'Status': {
                        "status": {
                            "name": None
                        }
                    },
                    'Project': {
                        "relation": [
                            {
                            "id": None
                            }
                        ]
                    },
                    'Reviewer': {
                            "people": None
                    },
                    'Assignees': {
                        "people": None
                    },
                    'Milestone': {
                        'rich_text': [
                            {
                                'type': 'text',
                                'text': {
                                    'content': None
                                }
                            }
                        ]
                    },
                    'Period': {
                        "date": {
                            "start": None,
                            # "end": None
                        }
                    },
                    'Due date': {
                        "date": {
                            "start": None
                        }
                    },
                }
    
    def change_database(self, new_issue_database_id):
        self.issue_database_id = new_issue_database_id

    ## deal with page properties
    # def search_page(self, page_title):
    #     body = {}
    #     if page_title is not None:
    #         body['query'] = page_title

    #     search_url = os.path.join(self.base_url, 'search')
    #     resp = requests.request('POST', search_url, headers=self.headers, json=body)
    #     return response_or_error(resp)

    
    def query_page(self, database_id, item_id):
        '''
        Query page in the database by issue id
        '''
        query_url = os.path.join(self.base_url, 'databases', database_id, 'query')
        payload = {
            "filter": {
                "property": "id",
                "text": {
                    "equals": item_id
                }
            }
        }
        resp = requests.post(query_url, json=payload, headers=self.headers)
        resp = response_or_error(resp)
        if resp != -1:
            res = resp["results"]
            assert res["object"] == "page"
            return res["id"]
        else:
            return None


    def create_page(
        self,
        data,
        ):
        '''
        Create pages for issues in a database.
        '''
        body = {
            'parent': {'type': 'database_id', 'database_id': self.issue_database_id},
            'properties': data
        }
        create_url = os.path.join(self.base_url, 'pages')
        resp = requests.request('POST', create_url, json=body, headers=self.headers)
        return response_or_error(resp)


    def update_page(self, page_id: str, updated_data: dict):
        '''
        Update page properties.
        '''
        update_url = os.path.join(self.base_url, 'pages', page_id)

        payload = {"properties": updated_data}

        resp = requests.patch(update_url, json=payload, headers=self.headers)
        return response_or_error(resp)


    # def delete_page(self, page_id: str):
    #     delete_url = os.path.join(self.base_url, 'pages', page_id)

    #     payload = {"archived": True}

    #     res = requests.patch(delete_url, json=payload, headers=self.headers)
    #     return res


    ## deal with page content
    def add_block(self, parent_id, children):
        '''
        basic function: append block children
        '''
        url = self.base_url + f'/blocks/{parent_id}/children'
        resp = requests.request('PATCH', url, json={'children': children}, headers=self.headers)

        return response_or_error(resp)


    def add_text(self, page_id, type, text, annotations=None):
        children = [
            {
                "type": type,
                type: {
                    "rich_text": [{
                        "type": "text",
                        "text": {
                            "content": text,
                        },
                        "annotations": {
                            "bold": False,
                            "italic": False,
                            "underline": False,
                            "code": False,
                            "color": "default"
                        }
                    }]
                },
            }
        ]
        if annotations:
            for k, v in annotations.items():
                try:
                    children[0][type]['rich_text'][0]['annotations'][k] = v
                except Exception as e:
                    logging.error(str(e)+f"No such key as '{k}' in annotations")
        resp = self.add_block(page_id, children)
        return resp


    def add_paragraph(self, page_id, paragraph):
        '''
        based on add_text -- append long paragraph
        '''
        chunk_num = len(paragraph) // 1500 + 1
        for i in range(chunk_num):
            chunk = paragraph[1500 * i:1500 * (i + 1)]
            self.add_text(page_id, 'paragraph', chunk)


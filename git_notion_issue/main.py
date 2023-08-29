from flask import Flask
from flask import request
import logging
import click

from notion import Issue2Notion

 
app = Flask(__name__)
# app.secret_key = 'development key'
@click.command()
@click.option('--notion_token')
@click.option('--issue_database_id')
@click.option('--project_database_id')
def run_server(notion_token, issue_database_id, project_database_id):
    n = Issue2Notion(notion_token, issue_database_id)
    
    @app.route('/issue', methods = ['POST'])
    def JsonHandler():
        if request.is_json:
            content = request.get_json()
            logging.info("Just got {0} event!".format(content['event_type']))

            object_attributes = content['object_attributes']
            action = object_attributes['action']
            issue_id = object_attributes['id']
            issue_page_id = n.query_page(issue_database_id, issue_id)
            if action == 'open':           
                issue_iid = object_attributes['iid']
                issue_title = object_attributes['title']
                description = object_attributes['description'] # TODO: append to the page content
                url = object_attributes['url']
                status = "In Progress"
                project_id = object_attributes['project_id']
                project_page_id = n.query_page(project_database_id, project_id)
                reviewer_id = object_attributes['author_id']
                assignee_ids = object_attributes['assignee_ids']
                milestone_id = object_attributes['milestone_id'] # TODO: process null?
                # TODO: get milestone name according to milestone id
                due_date = object_attributes['due_date'] # TODO: process null & datetime?
                created_at = object_attributes['created_at'] # TODO: process null & datetime?

                data = n.properties
                data['id']['rich_text'][0]['text']['content'] = str(issue_id)
                data['iid']['number'] = issue_iid
                data['Name']['title'][0]['text']['content'] = issue_title
                data['URL']['url'] = url
                data['Status']['status']['name'] = status
                data['Project']['relation']['id'] = project_page_id
                data['Reviewer']['people'] = [{
                            "object": "user",
                            "id": reviewer_id
                        }]
                data['Assignees']['people'] = [{
                            "object": "user",
                            "id": id
                        } for id in assignee_ids]
                data['Milestone']['rich_text'][0]['text']['content'] = milestone_name
                data['Period']['date']['start'] = created_at
                data['Due date']['date']['start'] = due_date

                n.create_page(data)
                if issue_page_id is not None:          
                    n.add_text(issue_page_id, 'text', description)
            elif action == 'update':
                if issue_page_id is not None:
                    changes = content['changes']

                    updated_data = {}
                    properties = n.properties
                    for change in changes:
                        key = list(change.keys())[0]
                        if key == 'title': # change title
                            updated_data['Name'] = properties['Name']
                            updated_data['Name']['title'][0]['text']['content'] = list(change.values())[0]['current']
                        elif key == 'description':
                            n.add_text(issue_page_id, 'text', list(change.values())[0]['current'])
                        # TODO: change asignees, epic, labels, milestone, weight, due date
                        # timetracking, confidentiality, tasks, linked items, comment

                    if updated_data:
                        n.update_page(issue_page_id, updated_data)
                    
            elif action == 'close':
                closed_at = object_attributes['closed_at'] # TODO: process null & datetime?
                updated_data = {
                    'Period': {
                        "date": {
                            "end": closed_at,
                        }
                    },
                    'Status': {
                        "status": {
                            "name": 'Done'
                        }
                    },
                }
                n.update_page(updated_data)
            elif action == 'reopen':
                updated_data = {
                    'Period': {
                        "date": {
                            "end": None,
                        }
                    },
                    'Status': {
                        "status": {
                            "name": 'In Progress'
                        }
                    },
                }
                n.update_page(updated_data)
            
            return 'OK'
        else:
            return 'OK'

    app.run(host='0.0.0.0', port= 8888, debug=True)


if __name__ == "__main__":
    run_server()
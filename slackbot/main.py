import requests
import json
import random
from datetime import date

headers = {
    "Authorization": "Bearer af4e68fdefc8ed75643ff3604bde4f1de54c77ce",
    "Content-Type": "application/json", 
    "Accept": "application/vnd.github.inertia-preview+json"
    }

# Graphql query 엑세스 값
query = """
query{
    user(login: "jiyoonbak"){
        repositories(last: 100){
            totalCount nodes{
                name defaultBranchRef{
                    target{
                        ...on Commit{
                            history(since: "2020-02-16T09:00:00+00:00"){
                                totalCount
                            }
                        }
                    }
                }
            }
        }
    }
}
"""

def make_query(user_info):
    pass
    


def run_query(query):
    # GitHub Request
    git_req = requests.post("https://api.github.com/graphql", json={'query':query}, headers=headers)
    if git_req.status_codes == 200: # Request code 200 means ok.
        return git_req.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(git_req.status_codes, query))


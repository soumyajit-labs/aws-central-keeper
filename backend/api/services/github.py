import os
import json
import requests
from requests.adapters import HTTPAdapter, Retry
from dotenv import load_dotenv
load_dotenv()

githubToken = os.environ['GITHUB_TOKEN']
owner =  os.environ['GITHUB_REPO_OWNER']

LOCAL_HTTP_CONN = requests.Session()
MAX_RETRY_STRAT = Retry(total = 5, backoff_factor = 0.1)
LOCAL_HTTP_CONN.mount('https://', HTTPAdapter(max_retries = MAX_RETRY_STRAT))

def workflow_retrigger(repository, buildArg):
    url = 'https://api.github.com/repos/{0}/{1}/dispatches'.format(owner, repository)
    headers = { 'Authorization': 'Bearer {0}'.format(githubToken),
                'Accept': 'application/vnd.github+json',
                'X-GitHub-Api-Version': '2022-11-28' }
    response = LOCAL_HTTP_CONN.request( method = 'POST', url = url, headers = headers,
                                        data = json.dumps({'event_type': buildArg}) )
    if response.status_code == 204:
        return {'status': response.status_code, 
                'message': 'Retriggered successfully. Check on the "Actions" tab in the repository.'}
    else:
        return {'status': response.status_code, 
                'message': json.loads(response.text)['message']}
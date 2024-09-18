from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from app.extensions import collection

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

@webhook.route('/receiver', methods=['POST'])
def receiver():
    if request.headers['Content-Type'] == 'application/json':
        data = request.json
        
        event_type = request.headers.get('X-GitHub-Event', '')
        
        if event_type == 'push':
            commit_hash = data['head_commit']['id']
            payload = {
                'request_id': commit_hash,
                'author': data['pusher']['name'],
                'from_branch': '',
                'to_branch': data['ref'].split('/')[-1],
                'timestamp': datetime.now(timezone.utc).isoformat()
            }
            collection.insert_one({'action': 'push', **payload})
            
        elif event_type == 'pull_request':
            pr_id = data['pull_request']['id']
            action = data['action']
            if action == 'closed' and data['pull_request'].get('merged', False):
              
                payload = {
                    'request_id': pr_id,
                    'author': data['pull_request']['user']['login'],
                    'from_branch': data['pull_request']['head']['ref'],
                    'to_branch': data['pull_request']['base']['ref'],
                    'timestamp': datetime.now(timezone.utc).isoformat() 
                }
                collection.insert_one({
                    'action': 'merge', **payload
                    # 'message': f'{payload["author"]} merged branch {payload["from_branch"]} to {payload["to_branch"]} on {payload["timestamp"]}'
                })
            else:
            
                payload = {
                    'request_id': pr_id,
                    'author': data['pull_request']['user']['login'],
                    'from_branch': data['pull_request']['head']['ref'],
                    'to_branch': data['pull_request']['base']['ref'],
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
                collection.insert_one({'action': 'pull_request', **payload})
        
        elif event_type == 'pull_request_review':
            
            action = data['action']
            pr_id = data['pull_request']['id']

            if action == 'submitted' and data['review']['state'] == 'approved':
               
                payload = {
                    'request_id': pr_id,
                    'author': data['review']['user']['login'],
                    'from_branch': data['pull_request']['head']['ref'],
                    'to_branch': data['pull_request']['base']['ref'],
                    'timestamp': datetime.now(timezone.utc).isoformat()
                }
                collection.insert_one({'action': 'pull_request_review', **payload})
        
        return jsonify({'status': 'success'}), 200
    else:
        return 'Content-Type must be application/json', 400

@webhook.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find({}, {'_id': 0}))  
    return jsonify(events)

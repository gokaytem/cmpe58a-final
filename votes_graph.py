import json
import networkx as nx

def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def add_user_nodes(G, users):
    for user in users:
        G.add_node(user['id'], username=user['username'], role=user['role'])

def process_votes(G, post, users_dict):
    author_id = post['user_id']
    timestamp = post['timestamp']
    # Upvotes
    for voter_id in post.get('upvoted_by', []):
        if voter_id in users_dict and voter_id != author_id:
            if G.has_edge(voter_id, author_id):
                G[voter_id][author_id]['weight'] += 1
                G[voter_id][author_id]['timestamps'].append(timestamp)
            else:
                G.add_edge(voter_id, author_id, weight=1, timestamps=[timestamp])
    # Downvotes
    for voter_id in post.get('downvoted_by', []):
        if voter_id in users_dict and voter_id != author_id:
            if G.has_edge(voter_id, author_id):
                G[voter_id][author_id]['weight'] -= 1
                G[voter_id][author_id]['timestamps'].append(timestamp)
            else:
                G.add_edge(voter_id, author_id, weight=-1, timestamps=[timestamp])

def traverse_comments(G, comments, users_dict):
    for comment in comments:
        process_votes(G, comment, users_dict)
        traverse_comments(G, comment.get('comments', []), users_dict)

def build_votes_graph(data):
    G = nx.DiGraph()
    users = data['users']
    users_dict = {u['id']: u for u in users}
    add_user_nodes(G, users)
    for post in data['posts']:
        process_votes(G, post, users_dict)
        traverse_comments(G, post.get('comments', []), users_dict)
    return G

if __name__ == "__main__":
    # Replace with the JSON file path
    data = load_data('openbrew_data.json')
    G = build_votes_graph(data)
    # Save graph to GraphML
    nx.write_graphml(G, "votes_graph.graphml")

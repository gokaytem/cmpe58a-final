import json
import networkx as nx

def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def add_user_nodes(G, users):
    for user in users:
        G.add_node(user['id'], username=user['username'], role=user['role'])

def process_comments(G, parent_author_id, comments, users_dict):
    for comment in comments:
        commenter_id = comment['user_id']
        timestamp = comment['timestamp']
        if commenter_id in users_dict and parent_author_id in users_dict and commenter_id != parent_author_id:
            if G.has_edge(commenter_id, parent_author_id):
                G[commenter_id][parent_author_id]['weight'] += 1
                G[commenter_id][parent_author_id]['timestamps'].append(timestamp)
            else:
                G.add_edge(commenter_id, parent_author_id, weight=1, timestamps=[timestamp])
        # Recursively process nested comments
        process_comments(G, commenter_id, comment.get('comments', []), users_dict)

def build_comments_graph(data):
    G = nx.DiGraph()
    users = data['users']
    users_dict = {u['id']: u for u in users}
    add_user_nodes(G, users)
    for post in data['posts']:
        process_comments(G, post['user_id'], post.get('comments', []), users_dict)
    return G

if __name__ == "__main__":
    # Replace with the JSON file path
    data = load_data('openbrew_data.json')
    G = build_comments_graph(data)
    # Save graph to GraphML
    nx.write_graphml(G, "comments_graph.graphml")

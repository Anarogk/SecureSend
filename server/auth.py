import yaml

def load_users():
    with open('config/users.yaml', 'r') as f:
        return yaml.safe_load(f)

def authenticate_user(username, password):
    users = load_users()
    if username in users and users[username]['password'] == password:
        return True
    return False
from dotenv import load_dotenv
from os import path

def load_env():
    env_path = path.join(path.dirname(__file__), '..', '.env')
    load_dotenv(env_path)
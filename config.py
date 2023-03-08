import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRECT_KEY') or "yomommasofatshebendslight"
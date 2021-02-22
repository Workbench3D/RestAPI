class Config(object):
    DEBUG = False
    TESTING = False

class Development(Config):
    DEBUG = True
    DATABASE = 'SQLite'
    # DATABASE = 'Storage'

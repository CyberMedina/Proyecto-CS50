class Config:
    SECRET_KEY = '6e7df11b4569d2374ef1b35c8a35a0c1'


class DevelopmentConfig(Config):
    DEBUG=True
    host="localhost",
    user="root",
    password="1233456",
    database="proyectocs50"


config={
    'development': DevelopmentConfig
    
}
class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://linxi2252:123123123@8.130.21.186:3306/smartdesk"
    SESSION_REFRESH_EACH_REQUEST = True
    SECRET_KEY = "abc"
    MQTT_BROKER_URL = 'mqtt.ri-co.cn'
    MQTT_BROKER_PORT = 1883

    MQTT_KEEPALIVE = 5
    MQTT_TLS_ENABLED = False


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class ProductionConfig(Config):
    DATABASE_URL = ""


class TestingConfig(Config):
    TESTING = True


config_map = {
    "develop": DevelopmentConfig,
    "product": ProductionConfig,
    "test": TestingConfig
}

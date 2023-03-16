
from flask import Flask, session
from flask_cors import CORS
from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy
from config import config_map

db = SQLAlchemy()
mqtt = Mqtt()


def register_blueprints(app: Flask):
    """
    注册蓝图
    :param app: Flask
    :return:
    """
    from app.api.v1_0.hums import hum_bp
    from app.api.v1_0.login import login_bp
    from app.api.v1_0.apis import apis
    from app.api.v1_0.weather import weather
    app.register_blueprint(hum_bp, url_prefix="/api/v1.0")
    app.register_blueprint(login_bp, url_prefix="/api/v1.0")
    app.register_blueprint(apis, url_prefix="/api/v1.0")
    app.register_blueprint(weather, url_prefix="/api/v1.0")


def creat_app(config_name):
    """
    创建Flask对象
    :param config_name: str
    :return: Flask
    """
    app = Flask(__name__, static_folder='static')
    # 加载配置
    config_class = config_map[config_name]
    # Session(app)
    app.config.from_object(config_class)
    # 挂载数据库
    db.init_app(app)
    # 加载第三方库
    # mqtt.init_app(app)
    # from app import mqtt_handler
    # 加载路由
    register_blueprints(app)
    # 全局跨域
    CORS(app, supports_credentials=True)
    return app

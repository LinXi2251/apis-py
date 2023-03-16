import json
from datetime import datetime

from app import mqtt, db
from app.models import MonitorData


@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    print("连接成功")
    mqtt.subscribe('NodeMCU-DESK/Pub')


COUNT = 0


@mqtt.on_message()
def handle_mqtt_message(client, userdata, msg):
    global COUNT
    COUNT = COUNT + 1
    if COUNT == 5:
        COUNT = 0
        print("主题:" + msg.topic + " 消息:" + str(msg.payload.decode('utf-8')))
        data = str(msg.payload.decode('utf-8'))
        json_data = json.loads(data)
        hum_value = json_data['Hum']
        temp_value = json_data['Temp']

        monitor_data = MonitorData(time=datetime.now(), temp_value=temp_value, hum_value=hum_value)
        try:
            print(data)
            from manager import app
            db.app = app
            db.session.add(monitor_data)
            db.session.commit()
            print("插入成功")
        except Exception as e:
            print(e)
            db.session.rollback()
            print("插入失败")

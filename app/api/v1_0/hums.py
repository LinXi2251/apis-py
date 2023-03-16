# coding: utf-8
from flask import Blueprint, jsonify
from app.models import MonitorData

hum_bp = Blueprint("hum_bp", __name__)


@hum_bp.route("/hums")
def get_hum_list():
    hums = MonitorData.query.all()[-100:]
    # print(hums)
    time_ls = []
    value_ls = []
    for hum in hums:
        time_ls.append(hum.time.strftime("%m-%d %H:%M:%S"))
        value_ls.append(hum.hum_value)
    result = {"time": time_ls, "value": value_ls}
    return jsonify(code=200, result=result)


@hum_bp.route("/temps")
def get_temp_list():
    temps = MonitorData.query.all()[-100:]
    # print(hums)
    time_ls = []
    value_ls = []
    for temp in temps:
        time_ls.append(temp.time.strftime("%m-%d %H:%M:%S"))
        value_ls.append(temp.temp_value)
    result = {"time": time_ls, "value": value_ls}
    return jsonify(code=200, result=result)

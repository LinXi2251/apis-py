import hashlib

from flask import jsonify, request, session, Blueprint, Response
from werkzeug.utils import secure_filename
import uuid
import os
from app import db
from app.models import Message, Admin, Tag, User

apis = Blueprint("apis", __name__)
# 设置允许上传的文件格式
ALLOW_EXTENSIONS = ['png', 'jpg', 'jpeg']

# 设置图片保存文件夹
image_path = 'static/images/'


# 加密函数
def spw(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()  # 返回加密的密码


# 判断文件后缀是否在列表中
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1] in ALLOW_EXTENSIONS


def save_image(file):
    # 检测文件格式
    if file and allowed_file(file.filename):
        # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
        file_name_hz = secure_filename(file.filename).split('.')[-1]
        # 使用uuid生成唯一图片名
        first_name = str(uuid.uuid4())
        # 将 uuid和后缀拼接为 完整的文件名
        file_name = first_name + '.' + file_name_hz
        # 保存原图
        file.save(os.path.join(image_path, file_name))
        return file_name
    else:
        return ""


# 管理员初始化 //
@apis.route("/init/admin")
def init_admin():
    """
    账号：admin
    密码：default

    :return:
    """
    admin = Admin(username="admin", password="default")
    try:
        db.session.add(admin)
        db.session.commit()
        return jsonify(code=200, msg="初始化管理员成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="初始化管理员失败")


# 管理员登录 //
@apis.route("/admin/login", methods=["POST"])
def login_admin():
    """
    传 账号 和 密码
    :return:
    """
    session.parmanent = True
    req_data = request.get_json()
    username = req_data.get("username")  # 获取账号
    password = req_data.get("password")  # 获取密码
    print(username, password)
    if not all([username, password]):
        return jsonify(code=400, msg="参数不完整")

    admin = Admin.query.filter(Admin.username == username).first()

    # 查找数据库管理员 # 验证密码
    if admin is None or password != admin.password:
        return jsonify(code=400, msg="账号或密码错误")

    session["admin_name"] = username
    session["admin_id"] = admin.id

    return jsonify(code=200, msg="登录成功")


# 检查登录状态 //
@apis.route("/admin/session", methods=["GET"])
def check_admin_session():
    username = session.get("admin_name")
    admin_id = session.get("admin_id")

    if admin_id is not None:
        # 操作逻辑 数据库什么的
        # 数据库里面 把你的头像 等级 金币数量 查询出来
        return jsonify(username=username, admin_id=admin_id)
    else:
        return jsonify(msg="出错了，没登录")


# 管理员退出登录 //
@apis.route("/admin/logout", methods=["POST"])
def logout_admin():
    # session.modified = True
    session.clear()
    # session.pop("admin_id")
    session.modified = True
    return jsonify(msg="成功退出登录!")


# 管理员增标签 //
@apis.route("/admin/tag", methods=["POST"])
def add_tag():
    """
    tag_name
    :return:
    """

    req_data = request.get_json()
    tag_name = req_data.get("tag_name")  # 获取标签名
    admin_id = session.get("admin_id")  # 获取管理员的id

    # 参数不完整或者没登录
    if not all([tag_name, admin_id]):
        return jsonify(code=400, msg="参数不完整或未登录")

    tag = Tag(name=tag_name, admin_id=admin_id)
    try:
        db.session.add(tag)
        db.session.commit()
        return jsonify(code=200, msg="添加板块成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="添加板块失败")


# 管理员删板块 //
@apis.route("/admin/tag", methods=["DELETE"])
def delete_tag():
    req_data = request.get_json()
    tag_name = req_data.get("tag_name")  # 获取板块名
    admin_id = session.get("admin_id")  # 获取管理员的id

    # 参数不完整或者没登录
    if not all([tag_name, admin_id]):
        return jsonify(code=400, msg="参数不完整或未登录")

    try:
        Tag.query.filter(Tag.name == tag_name).delete()

        db.session.commit()
        return jsonify(code=200, msg="删除板块成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="删除板块失败")


# 管理员删留言  //
@apis.route("/admin/message", methods=["DELETE"])
def admin_delete_message():
    req_data = request.get_json()
    message_id = req_data.get("message_id")
    admin_id = session.get("admin_id")

    if not all([message_id, admin_id]):
        return jsonify(code=400, msg="参数不完整")

    # 判断留言存在吗
    msg = Message.query.get(message_id)
    if msg is None:
        return jsonify(code=400, msg="分享不存在，无法删除操作")

    try:
        Message.query.filter(Message.id == message_id).delete()
        db.session.commit()
        return jsonify(code=200, msg="删除成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="删除失败")


# 用户注册 //
@apis.route("/user/register", methods=["POST"])
def user_register():
    """
    账号
    密码
    用户名
    :return:
    """
    req_data = request.get_json()
    print(req_data)
    username = req_data.get("username")
    password = req_data.get("password")
    password = spw(password)
    print(username, password)
    nickname = "用户" + username
    user = User(username=username, password=password, nickname=nickname, logo_url="")

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify(code=200, msg="注册成功", username=username, user_id=user.id)
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="注册失败")


# 用户登录 //
@apis.route("/user/login", methods=["POST"])
def user_login():
    req_data = request.get_json()
    username = req_data.get("username")  # 获取账号
    password = req_data.get("password")  # 获取密码
    if not all([username, password]):
        return jsonify(code=400, msg="参数不完整")

    user = User.query.filter(User.username == username).first()

    # 查找数据库管理员 # 验证密码
    if user is None or spw(password) != user.password:
        return jsonify(code=400, msg="账号或密码错误")

    session["user_name"] = username
    session["user_id"] = user.id

    return jsonify(code=200, username=username, user_id=user.id)


# 检查登录状态 //
@apis.route("/user/session", methods=["GET"])
def check_user_session():
    username = session.get("user_name")
    user_id = session.get("user_id")

    if username is not None:
        # 操作逻辑 数据库什么的
        return jsonify(username=username, user_id=user_id)
    else:
        return jsonify(msg="出错了，没登录")


# 获取用户信息
@apis.route("/user/info", methods=['GET'])
def get_user_info():
    user_id = request.args.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify(code=400)
    phone = user.username
    nickname = user.nickname
    logo_url = user.logo_url
    payload = {
        "phone": phone,
        "nickname": nickname,
        "logo_url": logo_url
    }
    print(payload)

    return jsonify(code=200, msg="查询用户", data=payload)


# 用户退出登录 //
@apis.route("/user/logout", methods=["POST"])
def user_logout():
    session.clear()
    session.modified = True
    user_id = session.get("user_id")
    print(user_id)
    return jsonify(msg="成功退出登录!")


# 修改用户信息
@apis.route("user/modifyInfo", methods=["POST"])
def user_modify():
    req_data = request.get_json()
    user_id = request.args.get("user_id")
    # 要修改需要先将记录查出来
    user = User.query.filter_by(id=user_id).first()
    logo_url = req_data['logo_url']
    user.logo_url = logo_url
    db.session.add(user)
    db.session.commit()
    return jsonify(code=200)


# 图片获取地址 用于存放静态文件
@apis.route("/image/<imageId>")
def get_frame(imageId):
    # 图片上传保存的路径
    try:
        file_path = r'static/images/{}'.format(imageId)
        with open(file_path, 'rb') as f:
            image = f.read()
            result = Response(image, mimetype="image/jpg")
            return result
    except BaseException as e:
        return {"code": '503', "data": str(e), "message": "图片不存在"}


@apis.route("user/modifyLogo", methods=["POST"])
def user_modify_logo():
    if request.method == 'POST':
        # 获取文件
        file = request.files['file']
        user_id = request.args.get("user_id")
        # 检测文件格式
        if file and allowed_file(file.filename):
            # secure_filename方法会去掉文件名中的中文，获取文件的后缀名
            file_name_hz = secure_filename(file.filename).split('.')[-1]
            # 使用用户id生成唯一图片名
            # first_name = user_id
            first_name = str(uuid.uuid4())
            # 将 uuid和后缀拼接为 完整的文件名
            file_name = first_name + '.' + file_name_hz
            # 保存原图
            file.save(os.path.join(image_path, file_name))

            # 要修改需要先将记录查出来
            user = User.query.filter_by(id=user_id).first()
            file_name_old = user.logo_url
            try:
                user.logo_url = file_name
                db.session.add(user)
                db.session.commit()
                if file_name_old != "":
                    os.remove(os.path.join(image_path, file_name_old))
            except Exception as e:
                print(e)
                db.session.rollback()
                return jsonify(code=400, msg="修改失败")
                # 返回原本和缩略图的 完整浏览链接
            return {"code": '200', "image_url": file_name, "message": "上传成功"}
        else:
            return "格式错误，仅支持jpg、png、jpeg格式文件"
    return {"code": '503', "data": "", "message": "仅支持post方法"}


@apis.route("user/modifyNickname", methods=["POST"])
def user_modify_nickname():
    user_id = request.args.get("user_id")
    nickname = request.get_json().get("nickname")
    try:
        user = User.query.filter_by(id=user_id).first()
        user.nickname = nickname
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="修改失败")
    return jsonify(code=200, nickname=nickname)


# 用户发布分享 //
@apis.route("/user/message", methods=["POST"])
def user_post_message():
    req_data = request.get_json()
    user_id = session.get("user_id")
    if not user_id:
        user_id = req_data.get("user_id")
    print(user_id)
    tags = req_data.get("tags")  # ["a","aa","aaa"]
    print(tags)
    content = req_data.get("content")

    if not all([user_id, tags, content]):
        return jsonify(code=400, msg="参数不完整")

    try:
        print("try")
        tags = Tag.query.filter(Tag.name.in_(tags)).all()
        message = Message(content=content, user_id=user_id)
        message.tags = tags
        db.session.add(message)
        db.session.commit()
        return jsonify(code=200, msg="发布分享成功")

    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="发布分享失败")


# 用户删除分享 //
@apis.route("/user/message", methods=["DELETE"])
def user_delete_message():
    """
    上传分享对应的id
    作者的user_id判断作者
   :return:
    """
    req_data = request.get_json()
    message_id = req_data.get("message_id")
    user_id = session.get("user_id")
    if not user_id:
        user_id = req_data.get("user_id")
    print(user_id)

    if not all([message_id, user_id]):
        return jsonify(code=400, msg="参数不完整")

    # 判断分享存在吗
    msg = Message.query.get(message_id)
    if msg is None:
        return jsonify(code=400, msg="分享不存在，无法删除操作")
    # 判断用户是不是作者
    if user_id != msg.user_id:
        return jsonify(code=400, msg="你不是作者，无法删除操作")

    try:
        m = Message.query.filter(Message.id == message_id).delete()
        db.session.commit()
        return jsonify(code=200, msg="删除成功")
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify(code=400, msg="删除失败")


# 用户查看自己分享记录 //
@apis.route("/user/message/history", methods=["GET"])
def user_messages_history():
    user_id = session.get("user_id")
    if user_id is None:
        return jsonify(code=400, msg="请登录")
    user = User.query.get(user_id)
    print(user)
    if user is None:
        return jsonify(code=400, msg="用户不存在")

    # 获取分享 ////////////
    payload = []
    messages = user.messages
    print(messages)
    for message in messages:
        content = message.content,
        # 获取tags
        tag_names = []
        tags = message.tags,
        for tag in tags:
            for t in tag:
                print(t.name, "a")
                tag_names.append(t.name)
        # 生成器
        # tag_names = [t.name for t in tag for tag in tags]

        create_time = message.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        user_id = message.user_id
        data = {"content": content,
                "message_id": message.id,
                "tags": tag_names,
                "create_time": create_time,
                "user_id": user_id}
        print(data)
        payload.append(data)
    return jsonify(code=200, msg="查询成功", data=payload)


# 对应板块板分享消息 //
@apis.route("/user/message/board", methods=["GET"])
def user_messages_board():
    messages = Message.query.all()
    payload = []
    for message in messages:
        content = message.content,
        # 获取tags
        tag_names = []
        tags = message.tags,
        for tag in tags:
            for t in tag:
                print(t.name, "a")
                tag_names.append(t.name)
        # 生成器
        # tag_names = [t.name for t in tag for tag in tags]

        create_time = message.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        user_id = message.user_id
        data = {"content": content,
                "message_id": message.id,
                "tags": tag_names,
                "create_time": create_time,
                "user_id": user_id}
        print(data)
        payload.append(data)
    return jsonify(code=200, msg="查询成功", data=payload)


# 对应板块板分享消息 //
@apis.route("/messageList", methods=["GET"])
def user_messages_by_tag():
    tag_req = request.args.get("tag")
    tag = Tag.query.filter_by(name=tag_req).first()
    payload = []
    for message in tag.messages:
        print(message.content)
        user_logo = message.user.logo_url
        user_nickname = message.user.nickname
        user_id = message.user.id
        content = message.content
        message_time = message.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        message_id = message.id
        # data = {user_id, user_name, user_nickname, message_id, content}
        data = {'user_id': user_id, 'user_nickname': user_nickname, 'user_logo': user_logo, 'message_id': message_id,
                'message_time': message_time,
                'content': content}
        payload.append(data)
    return jsonify(code=200, msg="查询成功", data=payload)


@apis.route("/tagList", methods=["GET"])
def get_all_tag_list():
    payload = []
    tags = Tag.query.all()
    print(tags)
    for tag in tags:
        tmp = {'name': tag.name}
        payload.append(tmp)
    return jsonify(code=200, msg="查询成功", data=payload)


@apis.route("/deviceList", methods=["GET"])
def get_all_device_list():
    payload = ["SMART-DESK-C4:5B:BE:5D:69:1F"]
    return jsonify(code=200, msg="查询成功", data=payload)

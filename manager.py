import os

from flask_migrate import Migrate

from app import creat_app, db

logfile = "{0}/logs/{1}".format(os.path.abspath('.'), "log")

def_format = '%(asc_time)s %(name) 12s-%(level_name)-8s: %(message)s'

# logging.basicConfig(
#     filename=logfile,
#     filemode="a",
#     format='%(asctime)s %(name) 12s-%(levelname)-8s: %(message)s',
#     level=logging.INFO
# )

# ro = RotatingFileHandler(logfile, maxBytes=100 * 1024 * 1024, backupCount=10)
# ro.setLevel(logging.INFO)

app = creat_app("develop")
Migrate(app, db)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

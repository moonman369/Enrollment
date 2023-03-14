import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRECT_KEY') or "yOmOmMaSoFaTsHeBeNdSlIgHt"

    MONGODB_SETTINGS = {
        'db' : 'UTA_Enrollment',
        # 'host': 'mongodb://localhost:27017/UTA-Enrollment'
    }



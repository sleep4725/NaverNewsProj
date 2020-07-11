import requests

#
# 작성자 : 김준현 선임 연구원
#
class SessionObj:

    @classmethod
    def urlSess(cls):
        sess = requests.Session()
        return sess


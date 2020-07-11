import yaml
#
# 작성자 : 김준현 선임 연구원
# 네이버 뉴스 정치
class PoliticsProj:

    def __init__(self):
        self.politicsIndex = "naver_index_politics"
        self.politsObj  = PoliticsProj.getConfig()

    @classmethod
    def getConfig(cls):
        try:
            f=open("../config/politis.yml", "r", encoding="utf-8")
        except FileNotFoundError as err:
            print(err)
            exit(1)
        else:
            polInfo = yaml.safe_load(f)
            f.close()
            return polInfo
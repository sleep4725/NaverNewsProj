import yaml
#
# 작성자 : 김준현 선임 연구원
# 네이버 뉴스 경제
class EconomicProj:

    def __init__(self):
        self.economicIndex = "naver_index_economic"
        self.economicObj  = EconomicProj.getConfig()

    @classmethod
    def getConfig(cls):

        try:
            f=open("../config/economic.yml", "r", encoding="utf-8")
        except FileNotFoundError as err:
            print(err)
            exit(1)
        else:
            ecoInfo = yaml.safe_load(f)
            f.close()
            return ecoInfo
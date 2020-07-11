from newsSession.PoliticsProj import PoliticsProj
from newsSession.EconomicProj import EconomicProj

#
# 작성자 : 김준현 선임 연구원
#
class Args(EconomicProj, PoliticsProj):

    def __init__(self):
        self.newsUrl = "https://news.naver.com/main/list.nhn?"
        EconomicProj.__init__(self)
        PoliticsProj.__init__(self)




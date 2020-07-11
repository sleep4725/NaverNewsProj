from urllib.parse import urlencode
from time import strftime, localtime
from bs4 import BeautifulSoup
import requests
from elasticsearch import helpers

from projCode.Args import Args
from projCode.SessionObj import SessionObj
from esConn.EsClient import EsClient

#
# 작성자 : 김준현 선임 연구원
#
class Code(Args, EsClient):

    def __init__(self):

        Args.__init__(self)
        EsClient.__init__(self)
        self.timeGet = strftime("%Y%m%d", localtime())

    """ 정치면 sid1=100
    #########################################################################
    """
    def getPoliticsNews(self):

        print (self.politsObj["section"])
        page_ = 1
        politicList = []
        for k, v in dict(self.politsObj["section"]).items():
            ## 페이지 처리
            while True:
                print("page => {}".format(page_))
                encode_params = urlencode({
                    "mode": "LS2D",
                    "mid": "shm",
                    "sid2": v,
                    "sid1": self.politsObj["politics"],
                    "date": self.timeGet,
                    "page": page_
                })

                url = self.newsUrl + encode_params
                print(url)
                sess = SessionObj.urlSess()
                try:
                    html = sess.get(url=url)
                except requests.exceptions.ConnectionError as err:
                    print(err)
                    pass
                else:
                    hrefList = list()
                    if html.status_code == 200 and html.ok:
                        bsObj = BeautifulSoup(html.text, "html.parser")
                        headline = bsObj.select_one("ul.type06_headline").select("li > dl")
                        for h in headline:
                            dtList = h.select("dt")
                            ## poto 가 있는 경우
                            if len(dtList) > 1:
                                dtList = dtList[1].select_one("a").attrs["href"]
                                hrefList.append(dtList)
                            ## poto 가 없는 경우
                            else:
                                dtList = dtList[0].select_one("a").attrs["href"]
                                hrefList.append(dtList)

                        if hrefList[-1] in politicList:
                            page_ = 1
                            politicList.clear()
                            break
                        else:
                            self.subTextGet(self.politicsIndex, hrefList)
                            politicList.append(hrefList[-1])
                            page_ = page_ + 1
                #---------------
                finally:
                    sess.close()

    """ 기사에 detail 한 정보들을 수집
    """
    def subTextGet(self, index, subUrl):

        actions = list()

        for s in subUrl:
            sess = SessionObj.urlSess()
            try:
                html = sess.get(s)
            except requests.exceptions.ConnectionError as err:
                print (err)
                pass
            else:
                if html.status_code == 200 and html.ok:
                    # =====================================================================
                    article = {
                        "article_title"    : None,
                        "article_sponsor"  : None,
                        "article_contents" : None
                    }
                    # =====================================================================

                    bsObj = BeautifulSoup(html.text, "html.parser")
                    articleHeader = bsObj.select_one("div.article_header")
                    articleInfo = articleHeader.select_one("div.article_info")

                    articleTitle = articleInfo.select_one("h3#articleTitle")
                    articleSponsor = articleInfo.select_one("div.sponsor > span.t11")
                    articleContents = bsObj.select_one("#articleBodyContents")

                    article["article_title"] = articleTitle.text
                    article["article_sponsor"] = articleSponsor.text
                    article["article_contents"] = str(articleContents.text).replace("\n","").strip()
                    #print(article)

                    actions.append({ "_index": index, "_source": article})

        ## ================================================
        # elasticsearch bulk data insert
        ## ================================================
        try:
            helpers.bulk(client=self.es, actions=actions)
        except:
            print ("bulk insert error")


## ======================================================
# project main start
## ======================================================
if __name__ == "__main__":
    o = Code()
    o.getPoliticsNews()



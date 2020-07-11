from elasticsearch import Elasticsearch
import yaml
import requests

#
# 작성자 : 김준현 선임 연구원
#
class EsClient():

    def __init__(self):
        self.esConfig = self.getElasticConfig()
        self.es = EsClient.isElasticAlive(esConfig=self.esConfig)

    def getElasticConfig(self):
        try:
            f=open("../config/elasticConfig.yml", "r", encoding="utf-8")
        except FileNotFoundError as err:
            print(err)
            f.close()
            exit(1)
        else:
            esConfig = yaml.safe_load(f)
            f.close()
            return esConfig

    @classmethod
    def isElasticAlive(cls, esConfig):
        sess = requests.Session()
        try:
            html = sess.get("http://" + esConfig["esHost"] + ":{}".format(esConfig["esPort"]))
        except requests.exceptions.ConnectionError as err:
            print(err)
            sess.close()
            exit(1)
        else:
            if html.status_code == 200 and html.ok:
                es = Elasticsearch(hosts=[esConfig["esHost"]+":{port}".format(port=esConfig["esPort"])])
                return es
            else:
                exit(1)




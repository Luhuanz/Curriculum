import re
import jieba
import jieba.posseg as pseg
import logging
import csv
import py2neo
from py2neo import Graph,Node,Relationship,NodeMatcher
import paddle

paddle.enable_static()
jieba.enable_paddle()
logging.basicConfig(level=logging.ERROR)

class PokemonKGQA(object):
    def __init__(self):
        super().__init__()
        self.graph = Graph("bolt://localhost:7687", auth=("neo4j", "mathssuifeng6"))
    def cut_words(self, sentence):

        words_flags = pseg.cut(sentence, use_paddle=True)

        pokemon = ''
        query_type = ''
        for word, flag in words_flags:
            if flag == 'PER':
                pokemon = word
            elif word in ['进化', '特性']:
                query_type = word
        return pokemon, query_type

    def answer(self, sentence):
        sentence = re.sub("[A-Za-z0-9\!\%\[\]\,\。?]", "", sentence)
        pokemon, query_type = self.cut_words(sentence)
        if not pokemon or not query_type:
            return '无法理解问题'

        query = ""
        if query_type == '进化':
            query = f"MATCH (p:宝可梦{{name: '{pokemon}'}})-[:{query_type}]->(evolution) RETURN evolution.name"
        elif query_type == '特性':
            query = f"MATCH (p:宝可梦{{name: '{pokemon}'}})-[:{query_type}]->(trait) RETURN trait.name"

        data = self.graph.run(query)
        result = list(data)
        if query_type=="进化":
            property_name='evolution.name'
        elif query_type == '特性':
            property_name = 'trait.name'
        else:
            property_name = ''
        if not result:
            return '没有答案'
        return f"{pokemon}的{query_type}是{result[0][property_name]}"



    def test(self, sentence):
        answer = self.answer(sentence)
        print(answer)

if __name__ == '__main__':
    QA = PokemonKGQA()
    QA.test("喷火龙的进化是什么？")
    QA.test("皮卡丘的进化是什么？")

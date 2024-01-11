import os
import json
import pandas as pd
from py2neo import Graph, Node, Relationship
g_default = Graph("bolt://localhost:7687", auth=("neo4j", "mathssuifeng6"))
g_default.run("MATCH (n) DETACH DELETE n") # 删除旧表中元素
class EvolutionGraph:
    def __init__(self, evolution_path, trait_path):
        self.evolution_path = evolution_path
        self.trait_path = trait_path
        self.g = Graph("bolt://localhost:7687", auth=("neo4j", "mathssuifeng6"))  # 请替换成您的密码

    def load_data(self):
        # 加载进化数据
        with open(self.evolution_path, "r", encoding="utf-8") as file:
            evolution_lines = file.readlines()
        # 加载特性数据
        with open(self.trait_path, "r", encoding="utf-8") as file:
            trait_lines = file.readlines()

        characters = set() #实体
        evolutions = [] # 进化关系
        traits = [] # 特性
        for line in evolution_lines:
            src, dst = line.strip().split()
            characters.add(src)
            characters.add(dst)
            evolutions.append((src, dst))
        for line in trait_lines:
            src, dst = line.strip().split()
            characters.add(src)
            characters.add(dst)
            traits.append((src, dst))

        return list(characters), evolutions, traits

    def create_character_nodes(self, characters):
        print(" 开始导入实体")
        try:
            tx = self.g.begin()  # 开始一个 实体 关系 实体
            for i, char in enumerate(characters):
                node = Node("宝可梦", name=char)
                tx.create(node)
                print(f"{i}-th node of 宝可梦")
            tx.commit()  # 提交
        except Exception as e:
            print(f"对不起！，发生了: {e}")
            self.g.rollback(tx)  # 如果出现错误，回滚事务

    def create_relationships(self, evolutions, traits):
        print("开始导入关系")
        try:
            tx = self.g.begin()
            # 创建进化关系
            for i, (src, dst) in enumerate(evolutions):
                a = self.g.nodes.match("宝可梦", name=src).first()
                b = self.g.nodes.match("宝可梦", name=dst).first()
                if a is not None and b is not None:
                    r = Relationship(a, "进化", b)
                    tx.create(r)
                    print(f"{i}-th evolution edge")
                else:
                    print(f"进化关系匹配错误: {i}: {src} -> {dst}")
            # 创建特性关系
            for i, (src, dst) in enumerate(traits):
                a = self.g.nodes.match("宝可梦", name=src).first()
                b = self.g.nodes.match("宝可梦", name=dst).first()
                if a is not None and b is not None:
                    r = Relationship(a, "特性", b)
                    tx.create(r)
                    print(f"{i}-th trait edge")
                else:
                    print(f"特性关系匹配错误: {i}: {src} -> {dst}")
            tx.commit()
        except Exception as e:
            print(f"发生错误: {e}")
            self.g.rollback(tx)
if __name__ == '__main__':
    evolution_path = "进化kg.txt"  #  您的进化数据文件路径
    trait_path = "特征kg.txt"  # 替换为您的特性数据文件路径
    handler = EvolutionGraph(evolution_path, trait_path)
    characters, evolutions, traits = handler.load_data()
    print("Step 1: 导入图谱节点")
    handler.create_character_nodes(characters)
    print("Step 2: 导入图谱关系")
    handler.create_relationships(evolutions, traits)

# MATCH (p:`宝可梦` {name: '皮卡丘'})
# RETURN p;

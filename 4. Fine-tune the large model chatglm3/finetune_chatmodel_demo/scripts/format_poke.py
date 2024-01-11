#!/usr/bin/env python
import json
from collections import Counter
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument("--path", type=str, required=True)

args = parser.parse_args()

with open(args.path) as f:
    pokemon_data = json.load(f)

train_examples = []
err_count = 0

for pokemon in pokemon_data:
    try:
        # Simulating a conversation flow about the pokemon description
        conversation = [
            {"role": "system", "content": f"请描述一个宝可梦：{pokemon['姓名']}。"},
            {"role": "user", "content": "它有什么特性和弱点？"},
            {"role": "assistant", "content": f"{pokemon['姓名']}的属性是{pokemon['属性']}，它的弱点是{pokemon['弱点']}，特性是{pokemon['特征']}。"},
            {"role": "user", "content": "有更多的信息吗？"},
            {"role": "assistant", "content": pokemon['数据']}
        ]
        train_examples.append({"conversations": conversation})
    except Exception as e:
        err_count += 1

# Display error count and number of processed examples
print("err_count:", err_count)
print("train_examples:", len(train_examples))

# 写入处理后的数据到一个新的文件
output_path = "formatted_data/pokemon_conversations.jsonl"
with open(output_path, 'w', encoding='utf-8') as f:
    for example in train_examples:
        f.write(json.dumps(example, ensure_ascii=False) + '\n')


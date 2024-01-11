#! /usr/bin/env python

import json
from collections import Counter
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument("--path", type=str, required=True)

args = parser.parse_args()

with open(args.path) as f:
    data = json.load(f)

train_examples = []
err_count = 0

for conversation in data:
    try:
        # 这里假设每个项目是一个宝可梦的对话实例
        conv = []
        for message in conversation['conversations']:
            # 直接复制对话结构
            conv.append({
                "role": message["role"],
                "content": message["content"]
            })
        train_examples.append({"conversations": conv})
    except Exception as e:
        err_count += 1
        print(f"Error processing conversation: {e}")

print("err_count:", err_count)
print("train_examples:", len(train_examples))
print("conversation distribution:", Counter([len(e["conversations"]) for e in train_examples]))

# 创建输出文件夹
os.makedirs("formatted_data", exist_ok=True)

# 写入处理后的数据到一个新的文件
output_path = "formatted_data/pokemon_conversations.jsonl"

with open(output_path, "w") as f:
    for example in train_examples:
        f.write(json.dumps(example, ensure_ascii=False) + "\n")

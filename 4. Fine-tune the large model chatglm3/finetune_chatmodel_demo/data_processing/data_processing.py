import json
import pandas as pd

df = pd.read_csv("./data.csv")

train_examples = []

for index, row in df.iterrows():
    # 创建对话
    conversation = [
        {"role": "system", "content": f"描述一个宝可梦：{row['姓名']}。"},
        {"role": "user", "content": "它有什么特性和弱点？"},
        {"role": "assistant", "content": f"{row['姓名']}的属性是{row['属性']}，弱点是{row['弱点']}，特性是{row['特征']}。"},
        {"role": "user", "content": "有更多的信息吗？"},
        {"role": "assistant", "content": row['数据']}
    ]
    
    train_examples.append({"conversations": conversation})

 
with open('formatted_pokemon_data.json', 'w', encoding='utf-8') as f:
    json.dump(train_examples, f, ensure_ascii=False, indent=2)

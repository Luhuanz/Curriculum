
 

# CLIP宝可梦图像探索

🐉 使用CLIP模型探索宝可梦的世界！本项目通过图片与对应的中文名字，使用多模态学习方法来识别和分析宝可梦图片。项目基于Chinese-CLIP模型，专为处理中文文本而优化。我们通过图片与图片名进行多模态探索。

例如 imgs： 0001妙蛙种子.png

考虑到clip对于中文支持不那么优秀。本项目基于 [Chinese-CLIP ](https://github.com/OFA-Sys/Chinese-CLIP)。  

Chinese-CLIP 是CLIP模型的**中文**版本，使用大规模中文数据进行训练（~2亿图文对），旨在帮助用户快速实现中文领域的[图文特征&相似度计算](https://github.com/OFA-Sys/Chinese-CLIP#API快速上手)、[跨模态检索](https://github.com/OFA-Sys/Chinese-CLIP#跨模态检索)、[零样本图片分类](https://github.com/OFA-Sys/Chinese-CLIP#零样本图像分类)等任务。(参考Chinese-Clip readme)



## 安装要求 🛠

开始本项目前，需先检查是否满足下列环境配置要求:

- python >= 3.6.4
- pytorch >= 1.8.0 (with torchvision >= 0.9.0)
- CUDA Version >= 10.2

运行下列命令即可安装本项目所需的三方库。

```python
pip install -r requirements.txt
```

## 快速开始 🚀

安装Chinese-CLIP后，您可以轻松地调用API，进行图文特征提取和相似度计算。首先，安装cn_clip：

```bash
# 通过pip安装
pip install cn_clip

# 或者从源代码安装
cd Chinese-CLIP
pip install -e .
```

安装成功后，即可通过如下方式轻松调用API，传入指定图片（[示例](https://github.com/OFA-Sys/Chinese-CLIP/blob/master/examples/pokemon.jpeg)）和文本，提取图文特征向量并计算相似度：

```python
import torch 
from PIL import Image

import cn_clip.clip as clip
from cn_clip.clip import load_from_name, available_models
print("Available models:", available_models())  
# Available models: ['ViT-B-16', 'ViT-L-14', 'ViT-L-14-336', 'ViT-H-14', 'RN50']

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = load_from_name("ViT-B-16", device=device, download_root='./')
model.eval()
image = preprocess(Image.open("examples/pokemon.jpeg")).unsqueeze(0).to(device)
text = clip.tokenize(["杰尼龟", "妙蛙种子", "小火龙", "皮卡丘"]).to(device)

with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    # 对特征进行归一化，请使用归一化后的图文特征用于下游任务
    image_features /= image_features.norm(dim=-1, keepdim=True) 
    text_features /= text_features.norm(dim=-1, keepdim=True)    

    logits_per_image, logits_per_text = model.get_similarity(image, text)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

print("Label probs:", probs)  # [[1.268734e-03 5.436878e-02 6.795761e-04 9.436829e-01]]
```

注意这里的pokemon.jpeg 是Chinese-clip目录中的。

## 训练您自己的数据集 🌟

本项目支持使用您自己的数据集进行模型训练。请遵循以下步骤来组织您的代码和数据：

### 代码组织

下载本项目后, 请创建新的文件夹 `${DATAPATH}` 以存放数据集、预训练ckpt、以及finetune产生的模型日志&ckpt。推荐工作区目录结构如下：

```
Chinese-CLIP/
├── run_scripts/
│   ├── muge_finetune_vit-b-16_rbt-base.sh   #官方是多卡，我这里修改为单卡
│   ├── flickr30k_finetune_vit-b-16_rbt-base.sh
│   └── ...           # 更多finetune或评测脚本...
└── cn_clip/
    ├── clip/
    ├── eval/
    ├── preprocess/
    └── training/

${DATAPATH}  #这里我放在 Chinese-CLIP/
├── pretrained_weights/
├── experiments/   #改为  ${DATAPATH}/logs/ 就是 Chinese-CLIP/logs
├── deploy/	      # 用于存放ONNX & TensorRT部署模型
└── datasets/   #  Chinese-CLIP/datasets
    ├── MUGE/     # 2G   
    ├── Flickr30k-CN/  2G 大小
    └── .../          # 更多自定义数据集...  这里加入pokemon数据集
```



### 制作自己的数据集

您可以在 `datasets` 文件夹下找到 `pokemon` 数据集。使用 `data_processing` 脚本来调整您的数据格式：

- `data_t2s.py`: 如果您的数据是繁体中文，使用此脚本转换为简体中文。
- `data_processing.py`: 负责加载并处理数据，最终生成 `.tsv` 和 `.jsonl` 文件。

### 模型微调

使用以下命令进行模型微调：

```bash
cd Chinese-CLIP/
bash run_scripts/muge_finetune_vit-b-16_rbt-base.sh ${DATAPATH}
```

请根据您的需要调整 `muge_finetune_vit-b-16_rbt-base.sh` 脚本。

### 训练细节

-  使用3090 24 G batch_size设置为64， 显存占有22G,初始epochs  acc特别低 1% 这样子，多台机子都是这个表现。 在epochs 414 acc到达95%, 我断掉了服务器。 前414epochs : [epochs-best.pt](https://pan.baidu.com/s/15bw8LKaEuHX2u5XiIL6OEg?pwd=3032 )  提取码 ： 3032 

-  V100  32 G   batch_size设置为 128   显存占有26G， 初始acc 83% ，训练30 epochs  text2imge 和 imge2text都到达 98%作用， 当epochs=50   时候text2imge 和 imge2text 超过99%  ，前 50epochs :    [epochs-best.pt ](https://pan.baidu.com/s/14gP-eM7Pegg6quEpEpFgsw )  提取码：gogf 

 

## 推理与评估 🕵️‍♂️

由于Chinese-clip并没有说明自己训练数据后推理的细节 ，接下来的推理细节可以认为是原项目的补充。

### 1.官方代码推理自己训练集中的图片

```python


*import* torch 

*from* PIL *import* Image



*import* cn_clip.clip *as* clip

*from* cn_clip.clip *import* load_from_name, available_models

print("Available models:", available_models())  

*# Available models: ['ViT-B-16', 'ViT-L-14', 'ViT-L-14-336', 'ViT-H-14', 'RN50']*



device *=* "cuda" *if* torch.cuda.is_available() *else* "cpu"

model, preprocess *=* load_from_name("ViT-B-16", *device**=*device, *download_root**=*'./')

model.eval()

image *=* preprocess(Image.open("imgs/皮卡丘.png").convert("RGBA")).unsqueeze(0).to(device)  *#Label probs: [[0.003006 0.974   0.01017  0.01265 ]]*

*# image = preprocess(Image.open("imgs/皮卡丘.png")).unsqueeze(0).to(device)*

text *=* clip.tokenize(["杰尼龟", "妙蛙种子", "小火龙", "皮卡丘"]).to(device)



*with* torch.no_grad():

  image_features *=* model.encode_image(image)

  text_features *=* model.encode_text(text)

  *# 对特征进行归一化，请使用归一化后的图文特征用于下游任务*

  image_features */=* image_features.norm(*dim**=-*1, *keepdim**=*True) 

  text_features */=* text_features.norm(*dim**=-*1, *keepdim**=*True)   



  logits_per_image, logits_per_text *=* model.get_similarity(image, text)

  probs *=* logits_per_image.softmax(*dim**=-*1).cpu().numpy()



print("Label probs:", probs)     # Label probs: [[0.002913 0.974    0.01017  0.01266 ]]  预测为妙蛙种子  明显错误
```

 ` Available models: ['ViT-B-16', 'ViT-L-14', 'ViT-L-14-336', 'ViT-H-14', 'RN50'] Loading vision model config from /root/autodl-tmp/project/cn_clip/clip/model_configs/ViT-B-16.json Loading text model config from /root/autodl-tmp/project/cn_clip/clip/model_configs/RoBERTa-wwm-ext-base-chinese.json Model info {'embed_dim': 512, 'image_resolution': 224, 'vision_layers': 12, 'vision_width': 768, 'vision_patch_size': 16, 'vocab_size': 21128, 'text_attention_probs_dropout_prob': 0.1, 'text_hidden_act': 'gelu', 'text_hidden_dropout_prob': 0.1, 'text_hidden_size': 768, 'text_initializer_range': 0.02, 'text_intermediate_size': 3072, 'text_max_position_embeddings': 512, 'text_num_attention_heads': 12, 'text_num_hidden_layers': 12, 'text_type_vocab_size': 2} Label probs: [[0.002913 0.974    0.01017  0.01266 ]]` 



### 2. 微调后使用epochs_best.pt推理自己的数据集

```python
 import torch
import torch.nn.functional as F
import cn_clip.clip as clip
from PIL import Image

# 加载微调后的模型权重
model_path = 'epoch_latest.pt'
saved_model = torch.load(model_path, map_location=torch.device('cpu'))
model_state_dict = saved_model['state_dict']

# 调整状态字典的键
adjusted_state_dict = {}
for key in model_state_dict.keys():
    new_key = key[7:] if key.startswith('module.') else key
    adjusted_state_dict[new_key] = model_state_dict[key]

# 创建模型实例
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load_from_name("ViT-B-16", device=device)

# 加载调整后的状态字典
try:
    model.load_state_dict(adjusted_state_dict)
except RuntimeError as e:
    print("Error:", e)
    model.load_state_dict(adjusted_state_dict, strict=False)

# 设置模型为评估模式
model.eval()

# 图像预处理
image_path = "imgs/皮卡丘.png"
image = preprocess(Image.open(image_path).convert("RGBA")).unsqueeze(0).to(device)

# 文本处理
text = clip.tokenize(["杰尼龟", "妙蛙种子", "小火龙", "皮卡丘"]).to(device)

# 推理
with torch.no_grad():
    image_features, text_features, logit_scale = model(image, text)

    # 归一化特征
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    # 计算相似度分数
    logits_per_image = logit_scale * image_features @ text_features.t()

    # 转换为概率
    probs_per_image = F.softmax(logits_per_image, dim=-1).cpu().numpy()

print("Label probabilities:", probs_per_image) #[[0.e+00 0.e+00 6.e-08 1.e+00]] 预测为皮卡丘 ！

```

`Loading vision model config from /root/autodl-tmp/project/cn_clip/clip/model_configs/ViT-B-16.json Loading text model config from /root/autodl-tmp/project/cn_clip/clip/model_configs/RoBERTa-wwm-ext-base-chinese.json Model info {'embed_dim': 512, 'image_resolution': 224, 'vision_layers': 12, 'vision_width': 768, 'vision_patch_size': 16, 'vocab_size': 21128, 'text_attention_probs_dropout_prob': 0.1, 'text_hidden_act': 'gelu', 'text_hidden_dropout_prob': 0.1, 'text_hidden_size': 768, 'text_initializer_range': 0.02, 'text_intermediate_size': 3072, 'text_max_position_embeddings': 512, 'text_num_attention_heads': 12, 'text_num_hidden_layers': 12, 'text_type_vocab_size': 2} Label probabilities: [[0.e+00 0.e+00 6.e-08 1.e+00]]`

一个提醒： 当你训练完模型进行推理时候，训练后pt权重的顺序会错乱 ，**需要加载调整后的状态字典** 。


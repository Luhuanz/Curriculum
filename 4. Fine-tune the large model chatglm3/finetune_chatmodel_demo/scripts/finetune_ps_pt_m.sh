#! /usr/bin/env bash

set -ex

# 定义训练参数
PRE_SEQ_LEN=128
LR=2e-5  # 可以根据需要调整学习率
NUM_GPUS=1
MAX_SEQ_LEN=512  # 宝可梦数据可能不需要太长的序列长度
DEV_BATCH_SIZE=4  # 可以根据您的GPU性能调整批大小
GRAD_ACCUMULATION_STEPS=4
MAX_STEP=1000
SAVE_INTERVAL=200

# 生成日期字符串作为运行的一部分
DATESTR=$(date +%Y%m%d-%H%M%S)
RUN_NAME=pokemon_training

# 指定模型路径和数据集路径
BASE_MODEL_PATH=THUDM/chatglm3-6b  # 需要更新
DATASET_PATH=formatted_data/pokemon1.jsonl  # 需要更新
OUTPUT_DIR=output/${RUN_NAME}-${DATESTR}-${PRE_SEQ_LEN}-${LR}

# 创建输出目录
mkdir -p $OUTPUT_DIR

# 运行训练脚本
torchrun --standalone --nnodes=1 --nproc_per_node=$NUM_GPUS finetune.py \
    --train_format multi-turn \
    --train_file $DATASET_PATH \
    --max_seq_length $MAX_SEQ_LEN \
    --preprocessing_num_workers 1 \
    --model_name_or_path $BASE_MODEL_PATH \
    --output_dir $OUTPUT_DIR \
    --per_device_train_batch_size $DEV_BATCH_SIZE \
    --gradient_accumulation_steps $GRAD_ACCUMULATION_STEPS \
    --max_steps $MAX_STEP \
    --logging_steps 1 \
    --save_steps $SAVE_INTERVAL \
    --learning_rate $LR \
    --pre_seq_len $PRE_SEQ_LEN 2>&1 | tee ${OUTPUT_DIR}/train.log

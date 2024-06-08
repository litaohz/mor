# The name of experiment
name=VLT5

output=snap/vqa/$name
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

PYTHONPATH=$PYTHONPATH:./src \
python -m torch.distributed.launch \
    --nproc_per_node=$1 \
    src/vqa.py \
        --distributed --multiGPU \
        --train karpathy_train \
        --valid karpathy_val \
        --test OpenEnded_mscoco_train2014_questions_new_labelled_rationales \
        --optim adamw \
        --warmup_ratio 0.1 \
        --clip_grad_norm 5 \
        --lr 5e-5 \
        --epochs 20 \
        --num_workers 7 \
        --backbone 't5-base' \
        --output $output ${@:2} \
        --load snap/pretrain/VLT5/Epoch30 \
        --num_beams 5 \
        --batch_size 1 \
        --valid_batch_size 1 \
        --max_text_length 40 \

json_root = '/vc_data/users/taoli1/VL-T5-Ori/datasets/vqa/OpenEnded_mscoco_train2014_questions_new_labelled.json'
output_root = '/vc_data/users/taoli1/VL-T5-Ori/datasets/vqa/OpenEnded_mscoco_train2014_questions_new_labelled_rationales.json'

# json_root = 'test.json'
# rationale_root = '/vc_data/users/taoli1/mm/okvqa/annotations/rationale_ok_vqa_test2014_2023_6_3_23_32_2'
rationale_root = '/vc_data/users/taoli1/mm/okvqa/annotations/rationale_ok_vqa_train2014_2023_6_4_11_25_58'
ann = {}
import json,os,sys

from itertools import  groupby
from operator import itemgetter


#check if a rational is to accepted
def checker_itl(itl):
    return "answer" in itl and not itl["answer"].lower() in ("yes", "no")
with open(json_root, 'r') as f:
    ann = json.load(f)
print("ann:", len(ann))
_rationals_js = json.load(open(rationale_root, 'r'))
rationals_js = {}
for question_id, rtls in groupby (_rationals_js, key = itemgetter("question_id")):
    rationals_js[question_id] = [rtl for rtl in list(rtls) if checker_itl(rtl)]

print("rationals_js:", len(rationals_js))
for i, x in enumerate(ann):

    # print("x: ", x)
    ques = x['question_id']
    rationals = rationals_js[ques]
    intermidiate = [x['sent']]
    for rtl in rationals:
        # print("rtl:", rtl)
        intermidiate_txt = rtl["prompt"] + ("" if rtl["prompt"].endswith(',') else ", ") + rtl["answer"] + ".\n" + x['sent']
        intermidiate.append(intermidiate_txt)
    # print("intermidiate:", intermidiate)
    x['sent'] = intermidiate

with open(output_root, 'w') as f:
    json.dump(ann, f)
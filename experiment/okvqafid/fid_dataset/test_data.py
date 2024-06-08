import json

with open('OpenEnded_mscoco_train2014_questions_new.json', 'r') as f:
    orig_data = json.load(f)


with open('mscoco_train2014_annotations.json', 'r') as f:
    data = json.load(f)

quesid2ans = {}
for datum in data['annotations']:
    quesid2ans[datum['question_id']] = datum

print("len(quesid2ans):", len(quesid2ans))
import re
from collections import Counter
from itertools import combinations

def process_answer(answer):
    answer = answer.lower()
    answer = re.sub(r'\.(?!\d)', '', answer)
    answer = re.sub(r'\b(a|an|the)\b', '', answer)
    answer = re.sub(r'\b(dont)\b', "don't", answer)
    answer = re.sub(r'([^\w\s\'\:])', r' ', answer)
    return answer.strip()

def calculate_label(answers):
    processed_answers = [process_answer(answer['answer']) for answer in answers]
    label = {}
    for combination in combinations(processed_answers, 9):
        # print("combination:", combination)
        counts = Counter(combination)
        # print("counts:", counts)
        for key, value in counts.items():
            v = round(min(max(label.get(key, 0), value / 3), 1), 1)
            if v >= 0.3:
                label[key] = v
    return  label

answers = [{"answer": "down", "answer_confidence": "yes", "answer_id": 1}, {"answer": "down", "answer_confidence": "yes", "answer_id": 2}, {"answer": "at table", "answer_confidence": "yes", "answer_id": 3}, {"answer": "skateboard", "answer_confidence": "yes", "answer_id": 4}, {"answer": "down", "answer_confidence": "yes", "answer_id": 5}, {"answer": "table", "answer_confidence": "yes", "answer_id": 6}, {"answer": "down", "answer_confidence": "yes", "answer_id": 7}, {"answer": "down", "answer_confidence": "yes", "answer_id": 8}, {"answer": "down", "answer_confidence": "yes", "answer_id": 9}, {"answer": "down", "answer_confidence": "yes", "answer_id": 10}]
# label = calculate_label(answers)
# print(label)




found = 0
for x in orig_data:
    if x['question_id']  in quesid2ans:
        found += 1
        answers = quesid2ans[x['question_id']]['answers']
        label = calculate_label(answers)
        x['label'] = label
 
print("found:", found)

with open('OpenEnded_mscoco_train2014_questions_new_labelled.json', 'w') as f:
    json.dump(orig_data, f)

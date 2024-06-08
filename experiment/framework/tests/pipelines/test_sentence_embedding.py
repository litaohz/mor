# Copyright (c) Alibaba, Inc. and its affiliates.
import shutil
import unittest

from modelscope.hub.snapshot_download import snapshot_download
from modelscope.models import Model
from modelscope.models.nlp import BertForSentenceEmbedding
from modelscope.pipelines import pipeline
from modelscope.pipelines.nlp import SentenceEmbeddingPipeline
from modelscope.preprocessors import SentenceEmbeddingTransformersPreprocessor
from modelscope.utils.constant import Tasks
from modelscope.utils.test_utils import test_level


class SentenceEmbeddingTest(unittest.TestCase):
    model_id = 'damo/nlp_corom_sentence-embedding_english-base'
    ecom_base_model_id = 'damo/nlp_corom_sentence-embedding_chinese-base-ecom'
    medical_base_model_id = 'damo/nlp_corom_sentence-embedding_chinese-base-medical'
    general_base_model_id = 'damo/nlp_corom_sentence-embedding_chinese-base'

    inputs = {
        'source_sentence': ["how long it take to get a master's degree"],
        'sentences_to_compare': [
            "On average, students take about 18 to 24 months to complete a master's degree.",
            'On the other hand, some students prefer to go at a slower pace and choose to take ',
            'several years to complete their studies.',
            'It can take anywhere from two semesters'
        ]
    }

    inputs2 = {
        'source_sentence': ["how long it take to get a master's degree"],
        'sentences_to_compare': [
            "On average, students take about 18 to 24 months to complete a master's degree."
        ]
    }

    inputs3 = {
        'source_sentence': ["how long it take to get a master's degree"],
        'sentences_to_compare': []
    }

    inputs4 = {
        'source_sentence': ["how long it take to get a master's degree"]
    }

    inputs5 = {
        'source_sentence': [
            'how long it take to get a master degree',
            'students take about 18 to 24 months to complete a degree'
        ]
    }

    ecom_inputs1 = {
        'source_sentence': ['毛绒玩具'],
        'sentences_to_compare': ['大熊泰迪熊猫毛绒玩具公仔布娃娃抱抱熊', '背心式狗狗牵引绳']
    }

    ecom_inputs2 = {'source_sentence': ['毛绒玩具', '毛绒玩具儿童款']}

    medical_inputs1 = {
        'source_sentence': ['肠道不适可以服用益生菌吗'],
        'sentences_to_compare': ['肠胃不好能吃益生菌,益生菌有调节肠胃道菌群的作用', '身体发烧应该多喝水']
    }

    medical_inputs2 = {'source_sentence': ['肠道不适可以服用益生菌吗', '肠道不适可以服用益生菌吗']}

    el_model_id = 'damo/nlp_bert_entity-embedding_chinese-base'
    el_inputs = {
        'source_sentence': ['宋小宝小品《美人鱼》， [ENT_S] 大鹏 [ENT_E] 上演生死离别，关键时刻美人鱼登场'],
        'sentences_to_compare': [
            '董成鹏； 类型： Person； 别名： Da Peng， 大鹏;',
            '超级飞侠； 类型： Work； 别名： 超飞， 출동!슈퍼윙스， Super Wings;',
            '王源； 类型： Person； 别名： Roy;',
        ]
    }

    @unittest.skipUnless(test_level() >= 2, 'skip test in current test level')
    def test_run_by_direct_model_download(self):
        cache_path = snapshot_download(self.model_id)
        tokenizer = SentenceEmbeddingTransformersPreprocessor(cache_path)
        model = BertForSentenceEmbedding.from_pretrained(cache_path)
        pipeline1 = SentenceEmbeddingPipeline(model, preprocessor=tokenizer)
        pipeline2 = pipeline(
            Tasks.sentence_embedding, model=model, preprocessor=tokenizer)
        print(f'inputs: {self.inputs}\n'
              f'pipeline1:{pipeline1(input=self.inputs)}')
        print()
        print(f'pipeline2: {pipeline2(input=self.inputs)}')
        print()
        print(f'inputs: {self.inputs2}\n'
              f'pipeline1:{pipeline1(input=self.inputs2)}')
        print()
        print(f'pipeline2: {pipeline2(input=self.inputs2)}')
        print(f'inputs: {self.inputs3}\n'
              f'pipeline1:{pipeline1(input=self.inputs3)}')
        print()
        print(f'pipeline2: {pipeline2(input=self.inputs3)}')
        print(f'inputs: {self.inputs4}\n'
              f'pipeline1:{pipeline1(input=self.inputs4)}')
        print()
        print(f'pipeline2: {pipeline2(input=self.inputs4)}')
        print(f'inputs: {self.inputs5}\n'
              f'pipeline1:{pipeline1(input=self.inputs5)}')
        print()
        print(f'pipeline2: {pipeline2(input=self.inputs5)}')

    @unittest.skipUnless(test_level() >= 2, 'skip test in current test level')
    def test_ecom_model_run_by_direct_model_download(self):
        cache_path = snapshot_download(self.ecom_base_model_id)
        tokenizer = SentenceEmbeddingTransformersPreprocessor(cache_path)
        model = BertForSentenceEmbedding.from_pretrained(cache_path)
        pipeline1 = SentenceEmbeddingPipeline(model, preprocessor=tokenizer)
        pipeline2 = pipeline(
            Tasks.sentence_embedding, model=model, preprocessor=tokenizer)
        print(f'inputs: {self.ecom_inputs1}\n'
              f'pipeline1:{pipeline1(input=self.ecom_inputs1)}')
        print()
        print(f'pipeline2: {pipeline2(input=self.ecom_inputs1)}')

    @unittest.skipUnless(test_level() >= 2, 'skip test in current test level')
    def test_medical_model_run_by_direct_model_download(self):
        cache_path = snapshot_download(self.medical_base_model_id)
        tokenizer = SentenceEmbeddingTransformersPreprocessor(cache_path)
        model = BertForSentenceEmbedding.from_pretrained(cache_path)
        pipeline1 = SentenceEmbeddingPipeline(model, preprocessor=tokenizer)
        pipeline2 = pipeline(
            Tasks.sentence_embedding, model=model, preprocessor=tokenizer)
        print(f'inputs: {self.medical_inputs1}\n'
              f'pipeline1:{pipeline1(input=self.medical_inputs1)}')
        print()
        print(f'pipeline2: {pipeline2(input=self.medical_inputs1)}')

    @unittest.skipUnless(test_level() >= 0, 'skip test in current test level')
    def test_run_with_model_from_modelhub(self):
        model = Model.from_pretrained(self.model_id)
        tokenizer = SentenceEmbeddingTransformersPreprocessor(model.model_dir)
        pipeline_ins = pipeline(
            task=Tasks.sentence_embedding, model=model, preprocessor=tokenizer)
        print(pipeline_ins(input=self.inputs))

    @unittest.skipUnless(test_level() >= 1, 'skip test in current test level')
    def test_run_with_model_name(self):
        pipeline_ins = pipeline(
            task=Tasks.sentence_embedding, model=self.model_id)
        print(pipeline_ins(input=self.inputs))

    @unittest.skipUnless(test_level() >= 2, 'skip test in current test level')
    def test_run_with_default_model(self):
        pipeline_ins = pipeline(task=Tasks.sentence_embedding)
        print(pipeline_ins(input=self.inputs))

    @unittest.skipUnless(test_level() >= 0, 'skip test in current test level')
    def test_run_ecom_model_with_model_name(self):
        pipeline_ins = pipeline(
            task=Tasks.sentence_embedding, model=self.ecom_base_model_id)
        print(pipeline_ins(input=self.ecom_inputs2))

    @unittest.skipUnless(test_level() >= 0, 'skip test in current test level')
    def test_run_medical_model_with_model_name(self):
        pipeline_ins = pipeline(
            task=Tasks.sentence_embedding, model=self.medical_base_model_id)
        print(pipeline_ins(input=self.medical_inputs1))

    @unittest.skipUnless(test_level() >= 2, 'skip test in current test level')
    def test_run_with_el_model(self):
        pipeline_ins = pipeline(
            task=Tasks.sentence_embedding, model=self.el_model_id)
        print(pipeline_ins(input=self.el_inputs))


if __name__ == '__main__':
    unittest.main()

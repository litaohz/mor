

import os
import openai
openai.api_type = "azure"
openai.api_base = "https://hellotaoli.openai.azure.com/"
openai.api_version = "2022-12-01"
openai.api_key = "fd6d1b1b35624cb7b83984d0a52fc760"

response = openai.Embedding.create(
  input="porcine pals say",
  engine="emb"
)

print(response)
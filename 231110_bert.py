from pytorch_pretrained_bert import OpenAIGPTDoubleHeadsModel, OpenAIGPTTokenizer

model = OpenAIGPTDoubleHeadsModel.from_pretrained('openai-gpt')
tokenizer = OpenAIGPTTokenizer.from_pretrained('openai-gpt')


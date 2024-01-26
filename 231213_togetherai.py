"""
reference: https://docs.together.ai/docs/inference-python
"""
import pprint
import together
together.api_key = "0bdecbfa2eff08660fc9c1fe7e20c3a466c9c19ecd9bc231b0fcd640add97ebd"


# see available models
model_list = together.Models.list()

print(f"{len(model_list)} models available")

# print the first 10 models on the menu
model_names = [model_dict['name'] for model_dict in model_list]
print (model_names[:10])

#=================================================================================
# output = together.Complete.create(
#   prompt = "<human>: What is the impact of daily eating burger to human health?\n<bot>:", 
#   model = "togethercomputer/RedPajama-INCITE-7B-Instruct", 
#   max_tokens = 256,
#   temperature = 0.8,
#   top_k = 60,
#   top_p = 0.6,
#   repetition_penalty = 1.1,
#   stop = ['<human>', '\n\n']
# )

# # print generated text
# # print(output['output']['choices'][0]['text'])
# pprint.pprint (output)

#=================================================================================
output = together.Complete.create(
  prompt = "can you have a chitchat?", 
  model = "togethercomputer/llama-2-70b-chat", 
  max_tokens = 64,
  temperature = 0.7,
  top_k = 50,
  top_p = 0.7,
  repetition_penalty = 1.0,
  stop = ['<human>', '\n\n']
)

# print generated text
# print(output['output']['choices'][0]['text'])
pprint.pprint (output)
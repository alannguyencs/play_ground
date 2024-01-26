"""
https://python.langchain.com/docs/integrations/llms/together
"""
from langchain.llms import Together
import pprint

# llm = Together(
#     model="togethercomputer/RedPajama-INCITE-7B-Base",
#     temperature=0.7,
#     max_tokens=128,
#     top_k=1,
#     together_api_key="0bdecbfa2eff08660fc9c1fe7e20c3a466c9c19ecd9bc231b0fcd640add97ebd"
# )

# input_ = """What is the impact of daily eating burger to human health?"""
# print(llm(input_))




llm = Together(
    model="togethercomputer/llama-2-70b-chat",
    temperature=0.7,
    max_tokens=128,
    top_k=1,
    together_api_key="0bdecbfa2eff08660fc9c1fe7e20c3a466c9c19ecd9bc231b0fcd640add97ebd"
)

question = "What is the impact of daily eating burger to human health?"
prompt_template = "You are a friendly bot, answer the following question: {question}"
print(llm(prompt_template))


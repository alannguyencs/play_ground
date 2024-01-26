"""
https://medium.com/@datadrifters/the-worlds-fastest-llm-inference-engine-3x-faster-than-vllm-and-tgi-a2ed9e33c55f
"""
from langchain.llms import Together
import os
import time
import json
import logging
from datetime import datetime
from typing import Any

import together
from langchain.llms.base import LLM
from langchain import PromptTemplate,  LLMChain

TOGETHER_API_KEY = "0bdecbfa2eff08660fc9c1fe7e20c3a466c9c19ecd9bc231b0fcd640add97ebd"
together.api_key = TOGETHER_API_KEY

prompt = "<human>: What do you think about Large Language Models?\n<bot>:"
model = "togethercomputer/llama-2-7b-chat"

output = together.Complete.create(
  prompt = prompt,
  model = model, 
  max_tokens = 256,
  temperature = 0.8,
  top_k = 60,
  top_p = 0.6,
  repetition_penalty = 1.1,
  stop = ['<human>', '\n\n']
)

print(json.dumps(output, indent = 4))
print ("----------------------------------")


class TogetherLLM(LLM):
    """
    Together LLM integration.

    Attributes:
        model (str): Model endpoint to use.
        together_api_key (str): Together API key.
        temperature (float): Sampling temperature to use.
        max_tokens (int): Maximum number of tokens to generate.
    """
    
    model: str = "togethercomputer/llama-2-7b-chat"
    together_api_key: str = TOGETHER_API_KEY
    temperature: float = 0.7
    max_tokens: int = 512

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "together"

    def _call(self, prompt: str, **kwargs: Any) -> str:
            """Call to Together endpoint."""
            try:
                logging.info("Making API call to Together endpoint.")
                return self._make_api_call(prompt)
            except Exception as e:
                logging.error(f"Error in TogetherLLM _call: {e}", exc_info=True)
                raise

    def _make_api_call(self, prompt: str) -> str:
        """Make the API call to the Together endpoint."""
        together.api_key = self.together_api_key
        output = together.Complete.create(
            prompt,
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        logging.info("API call successful.")
        return output['output']['choices'][0]['text']
    
llm = TogetherLLM(
    model = model,
    max_tokens = 256,
    temperature = 0.8
)

prompt_template = "You are a friendly bot, answer the following question: {question}"
prompt = PromptTemplate(
    input_variables=["question"], template=prompt_template
)

chat = LLMChain(llm=llm, prompt=prompt)

print (chat("Can AI take over developer jobs?"))
print ("----------------------------------")


from typing import List

class LLMChain:
    def __init__(self, llm, prompt):
        self.llm = llm
        self.prompt = prompt
        self.history: List[str] = []  # Initialize an empty list to keep track of the conversation history

    def add_to_history(self, user_input: str, bot_response: str):
        self.history.append(f"<human>: {user_input}")
        self.history.append(f"<bot>: {bot_response}")

    def generate_prompt(self, question: str) -> str:
        history_str = "\n".join(self.history)  # Convert the history list into a single string
        return f"{history_str}\n<human>: {question}\n<bot>:"

    def ask(self, question: str) -> str:
        full_prompt = self.generate_prompt(question)
        response = self.llm._call(full_prompt)  # Assuming _call method handles the actual API call
        self.add_to_history(question, response)
        return response
    
# Usage
llm = TogetherLLM(
    model = model,
    max_tokens = 256,
    temperature = 0.8
)

prompt_template = "You are a friendly bot, answer the following question: {question}"
prompt = PromptTemplate(
    input_variables=["question"], template=prompt_template
)

chat = LLMChain(llm=llm, prompt=prompt)

patterns = ['\n\nIn this', '\n\nThis', '\n<human>']
while True:
    question = input("User: ")
    response = chat.ask(question)
    for patern in patterns:
        response = response.split(patern)[0]
    print(f"Bot: {response}")

# # Example interaction
# response = chat.ask("hello there, I am sick today?")
# print ("\n\n\n1:")
# print(response)  # Bot's response

# # The next call to chat.ask will include the previous interaction in the prompt
# response = chat.ask("cough and sneeze")
# print ("\n\n\n2:")
# print(response)
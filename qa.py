#!/usr/bin/env python

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
assert(openai.api_key)
user1= 'user001'
max_tokens = 300


def iteract(prompt):
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt, temperature=0.2,
                                        max_tokens=max_tokens, user=user1,
                                        stream=True)
    for v in response:
        try:
            print(v['choices'][0]['text'])
        except Exception as e:
            print(e)


def loop_qa(fn, esc='\x1b'):
    while True:
        prompt= input('?')
        if prompt == esc:
            break
        elif not prompt:
            continue
        try:
            print(fn(prompt))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    loop_qa(iteract)

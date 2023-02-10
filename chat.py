#!/usr/bin/env python

import os
import openai
from utils import loop_qa

openai.api_key = os.getenv("OPENAI_API_KEY")
assert(openai.api_key)
user1= 'user001'
max_tokens = 300


def iteract(prompt, user=None, temp=0):
    print(user, temp)
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt, temperature=temp,
                                        max_tokens=max_tokens, user=user,
                                        stream=True)
    for v in response:
        if not v:
            print('')
        else:
            w = v['choices'][0]['text']
            if w:
                print(w, end='')


if __name__ == "__main__":
    loop_qa(iteract, user='user001', temp=0.2)

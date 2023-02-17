#!/usr/bin/env python

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
assert(openai.api_key)
max_tokens = 300


def iteract(prompt, user='', temp=0):
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt, temperature=temp,
                                        max_tokens=max_tokens, user=user,
                                        stream=True)

    for v in response:
        yield v['choices'][0]['text']


def show(gen):
    for w in gen:
        print(w, end='')
    print('')


if __name__ == "__main__":
    from utils import loop_qa
    loop_qa(iteract, show, user='user001', temp=0.2)

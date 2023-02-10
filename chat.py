#!/usr/bin/env python

import os
import openai
from utils import loop_qa

openai.api_key = os.getenv("OPENAI_API_KEY")
assert(openai.api_key)
max_tokens = 300


def iteract(prompt, user=None, temp=0):
    response = openai.Completion.create(model="text-davinci-003",
                                        prompt=prompt, temperature=temp,
                                        max_tokens=max_tokens, user=user,
                                        stream=True)
    for v in response:
        """
            "created": 1676048333,
            "id": "cmpl-6iR1ZbmG0O3uRIgxAsPjjTwm5hUOW",
            "model": "text-davinci-003",
            "object": "text_completion"
        """
        print(v['choices'][0]['text'], end='')
    print('')


if __name__ == "__main__":
    loop_qa(iteract, user='user001', temp=0.2)

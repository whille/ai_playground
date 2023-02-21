#!/usr/bin/env python
import logging


def loop_qa(fn, callback, esc='\x1b', **kwargs):
    while True:
        prompt = input('?')
        if prompt == esc:
            break
        elif not prompt:
            continue
        try:
            callback(fn(prompt, **kwargs))
        except Exception as e:
            print(f"e: {e}")


# init
logger = logging.getLogger()
logging.basicConfig(format='[%(asctime)-15s] [%(funcName)s()][%(levelname)s] %(message)s')
logger.setLevel(logging.DEBUG)

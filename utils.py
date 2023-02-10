#!/usr/bin/env python


def loop_qa(fn, esc='\x1b', **kwargs):
    while True:
        prompt= input('?')
        if prompt == esc:
            break
        elif not prompt:
            continue
        try:
            fn(prompt, **kwargs)
        except Exception as e:
            print(f"e: {e}")

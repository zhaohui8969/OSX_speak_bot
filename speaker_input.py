#!/usr/bin/env python2
# coding: utf-8

from __future__ import print_function

import subprocess
import sys
import threading
import time


class speaker_and_typeer(object):
    def __init__(self, delay, lock):
        self.delay = delay
        self.lock = lock

    def dynamic_char_output(self, msg, delay):
        for _char in msg:
            print(_char, end='')
            sys.stdout.flush()
            time.sleep(delay)

    def osx_say(self, msg):
        subprocess.call(["say", msg])

    def speak_and_type(self, msg, delay=None):
        if not delay:
            delay = self.delay
        self.lock.acquire()
        t = threading.Thread(target=self.dynamic_char_output, kwargs={'msg': msg, 'delay': delay})
        t.start()
        self.osx_say(msg)
        t.join()
        self.lock.release()


def spliter(_string):
    split_char = u',.!\n，。！；、'
    last_postion = 0
    index = 0
    _string = unicode(_string, 'utf-8')
    for char in _string[last_postion:]:
        index += 1
        if char in split_char:
            yield _string[last_postion:index]
            last_postion = index


if __name__ == '__main__':
    lock = threading.Lock()
    lock.acquire()

    ss = speaker_and_typeer(0.05, lock)

    fop = sys.stdin
    line_str = fop.readline()
    while line_str:
        for i in spliter(line_str):
            lock.release()
            ss.speak_and_type(i)
            lock.acquire()

        line_str = fop.readline()

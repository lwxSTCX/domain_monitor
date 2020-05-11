#coding=utf-8
import sys
import argparse
import os
from subprocess import PIPE,Popen
import time
import config

def sub_domain_teemo(domain):
    popen=Popen(['python','C:\Users\TR\Desktop\sfile\domain\\teemo.py','-d','{name}'.format(name=domain)],stdout=PIPE)
    while True:
        next_line=popen.stdout.readline()
        if next_line == '' and popen.poll()!=None:
            break
        sys.stdout.write(next_line)

if __name__ == '__main__':
    sub_domain_teemo('www.baidu.com')



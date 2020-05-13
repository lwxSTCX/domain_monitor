#coding=utf-8
import sys
import argparse
import os
from subprocess import PIPE,Popen
import time
import threading
import Queue
import json
import difflib

subdomain_jiejie=[]

class Domain_monitor(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self._queue=queue
    def run(self):
        while not self._queue.empty():
            scan_domain = self._queue.get()
            try:
                run_scan(scan_domain)
                print scan_domain
            except Exception,e:
                print e
                pass
def make_domain():
    #os.system("copy sub.txt/b+teemo.txt/b+kongge.txt/b+kongge.txt/b  all_reqult.log  && del *.txt")
    os.system("copy *.txt  all_reqult.log  && del *.txt")
    list_domain=[]
    f=open("all_requst.log","r")
    while True:
        line = f.readline()
        if '.' in line:
            line = line.strip('').strip('\r').strip('"').strip(',').strip('            \r\r\n",').strip('\r\r\n')
        print line
        if line:
            pass
            line=line.strip()
            if '.' in line and '[S]' in line:
                list_domain.append(line.split('\t')[2])
            else:
                if '.' in line and '[R]' in line:
                    list_domain.append(line.split('\t')[3])
                else:
                    if '.' in line:
                        list_domain.append(line.replace(' ', '').strip("\\r").replace("\\r\\r\\n",''))
        else:
            break
    f.close()
#    os.system("del all_reqult.log")
    list_domain = list(set(( list_domain )))
    print list_domain,len(list_domain)
#    txt=time.clock()+'.xls'
    with open("result",'a+') as outfile:
        outfile.write('\n'.join(list_domain))
    fopen1 = open('report/result.txt','a+')
    fopen1.write('\n'.join(list_domain))
    fopen1.close()

def read_file(file_name):
    try:
        file_desc=open(file_name,'r')
        text=file_desc.read().splitlines()
        file_desc.close()
        return text
    except Exception,e:
        print e
        sys.exit()

def txt_check(filenew,filelast):#比较前后文件的异同
    if filenew=="" or filelast == "":
        print '文件路径不能为空'
        sys.exit()
    else:
        print 'start txt check....'
    text1_lines=read_file(filenew)
    text2_lines=read_file(filelast)
    diff=difflib.HtmlDiff()
    result=diff.make_file(text1_lines,text2_lines)
    try:
        with open('result.html','w') as result_file:
            result_file.write(result)
            print 'success'
    except Exception,e:
        print 'false'
        sys.exit()

def sub_domain_sublist(domain):
    popen=Popen(['python','C:\Users\TR\Desktop\sfile\domain\\sublist3r.py','-d','{name}'.format(name=domain),'-o {name}_sublistdir.txt'.format(name=domain)],stdout=PIPE)
    while True:
        next_line=popen.stdout.readline()
        if next_line == '' and popen.poll()!=None:
            break
        sys.stdout.write(next_line)
def sub_domain_teemo(domain):
    popen=Popen(['python','C:\Users\TR\Desktop\sfile\domain\\teemo.py','-d','{name}'.format(name=domain)],stdout=PIPE)
    while True:
        next_line=popen.stdout.readline()
        if next_line == '' and popen.poll()!=None:
            break
        sys.stdout.write(next_line)

def sub_domain_jiejie(domain):
    popen=Popen(['python','C:\Users\TR\Desktop\sfile\domain\\subDomainsBrute1.py','{name}'.format(name=domain),'--full'],stdout=PIPE)
    while True:
        next_line=popen.stdout.readline()
        if next_line == '' and popen.poll()!=None:
            break
        sys.stdout.write(next_line)
        subdomain_jiejie.append(next_line)
    return list(set(subdomain_jiejie))

def save_result(filename, args):
    try:
        fd = open(filename, 'a+')
        json.dump(args, fd, indent=4)
    finally:
        fd.close()

def run_scan(domain):
    filenew="teemo.txt"
    filelast="teemo1.txt"
    if not domain:
        print('usage: main.py -u www.xxx.com')
        sys.exit(1)
    try:
        print "\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] first INTERFACE\nwaiting 5s ......\n\n"
        time.sleep(1)
        sub_domain_teemo(domain)
        print "\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] second interface\nwaiting 5s ......\n\n"
        time.sleep(1)
        # sub_domain_jiejie(domain)
        # result=sub_domain_jiejie(domain)
        # save_result('jiejie.txt',result)
        # print "\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] fourth interface\nwaiting 5s ......\n\n"
        # time.sleep(1)
        # sub_domain_sublist(domain)
        # print("\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] make domain result\nwaiting 5s ......\n\n")
        # time.sleep(1)
        # make_domain()
        txt_check(filenew,filelast)
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == '__main__':
    queue=Queue.Queue()
    parser = argparse.ArgumentParser(description='Monitor SRC domain name changes')
    parser.add_argument('-u','--url', dest='domain',help='scan url')
    parser.add_argument('-d', '--domain', dest='domain_file', help='domain_file')
    parser.add_argument('-f','--file', dest='file', help='file')
    parser.add_argument('-t', '--threads', dest='threads',default=30, help='scan threads')
    parser.add_argument('-s', '--status_code', dest='status_code', help='target status_code')
    parser.add_argument('-o', '--output', dest='output',help='output file')
    args = parser.parse_args()
    try:
        threads=[]
        thread_count=5
        with open('C:\Users\TR\Desktop\sfile\domain\\aaa.txt','r') as domains:
            for domain in domains.readlines():
                queue.put(domain.strip())
        for i in range(thread_count):
            threads.append(Domain_monitor(queue))
        for i in threads:
            i.start()
        for i in threads:
            i.join()
    except KeyboardInterrupt:
        sys.exit(1)




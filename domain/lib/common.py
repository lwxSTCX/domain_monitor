# common functions
#encoding=utf-8
import sys
import os
from gevent.pool import Pool
import dns.resolver
from lib.consle_width import getTerminalSize

console_width = getTerminalSize()[0] - 2
import re
import socket
from config import *

import json
import subprocess

import requests as requests
import requests as __requests__
import colorama

# from tldextract import extract, TLDExtract

import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

if allow_http_session:
    requests = requests.Session()

def is_domain(domain):
    domain_regex = re.compile(
        r'(?:[A-Z0-9_](?:[A-Z0-9-_]{0,247}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,}(?<!-))\Z', 
        re.IGNORECASE)
    return True if domain_regex.match(domain) else False

def proxy_verify(proxy):
    OK_proxy= {}
    if isinstance(proxy, dict) and len(proxy)!=0:
        for item in proxy.keys():
            ip = proxy.get(item).split("//")[-1].split(":")[0]
            port = proxy.get(item).split("//")[-1].split(":")[1]
            try:
                sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sk.settimeout(2)
                sk.connect((ip, int(port)))
                sk.close
                OK_proxy[item] = proxy.get(item)
            except:
                pass
    return OK_proxy

def http_request_get(url, body_content_workflow=False, allow_redirects=allow_redirects, custom_cookie="", proxies = None):
    try:
        if custom_cookie:
            headers['Cookie']=custom_cookie
        result = requests.get(url, 
            stream=body_content_workflow, 
            headers=headers, 
            timeout=timeout, 
            proxies=proxies,
            allow_redirects=allow_redirects,
            verify=allow_ssl_verify)
        return result
    except Exception, e:
        # return empty requests object
        return __requests__.models.Response()

def http_request_post(url, payload, body_content_workflow=False, allow_redirects=allow_redirects, custom_cookie="", proxies = None):
    """ payload = {'key1': 'value1', 'key2': 'value2'} """
    try:
        if custom_cookie:
            headers['Cookie']=custom_cookie
        result = requests.post(url, 
            data=payload, 
            headers=headers, 
            stream=body_content_workflow, 
            timeout=timeout, 
            proxies=proxies,
            allow_redirects=allow_redirects,
            verify=allow_ssl_verify)
        return result
    except Exception, e:
        # return empty requests object
        return __requests__.models.Response()

def curl_get_content(url):
    try:
        cmdline = 'curl "{url}"'.format(url=url)
        logging.info("subprocess call curl: {}".format(url))
        run_proc = subprocess.Popen(
            cmdline,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        (stdoutput,erroutput) = run_proc.communicate()
        response = {
            'resp': stdoutput.rstrip(),
            'err': erroutput.rstrip(),
        }
        return response
    except Exception as e:
        pass

def save_result(filename, args):
    try:
        fd = open(filename, 'w')
        json.dump(args, fd, indent=4)
    finally:
        fd.close()

def read_json(filename):
    if FileUtils.exists(filename):
        try:
            fd = open(filename, 'r')
            args = json.load(fd)
            return args
        finally:
            fd.close()
    else:
        return []

def banner():
    colorama.init()
    G = colorama.Fore.GREEN  # green
    Y = colorama.Fore.YELLOW  # yellow
    B = colorama.Fore.BLUE  # blue
    R = colorama.Fore.RED  # red
    W = colorama.Fore.WHITE  # white
    version = 'V 0.5'
    waring = "[!] legal disclaimer: Usage of Teemo for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program\n"

    print """%s

          #####  ######  ######  #    #   ####
            #    #       #       ##  ##  #    #
            #    #####   #####   # ## #  #    #
            #    #       #       #    #  #    #
            #    #       #       #    #  #    #
            #    ######  ######  #    #   ####

            %s%s

         # Coded By bit4 - https://github.com/bit4woo
         # %s
         
%s
  """ % (G, W, Y, version, waring) #must inport colorama to ensure G、W、Y works fine

def strip_list(inputlist):
    if isinstance(inputlist,list):
        resultlist =[]
        for x in inputlist:
            x = x.strip()
            resultlist.append(x)
        return resultlist
    else:
        print "The input should be a list"

def is_intranet(ip):
    ret = ip.split('.')
    if len(ret) != 4:
        return True
    if ret[0] == '10':
        return True
    if ret[0] == '172' and 16 <= int(ret[1]) <= 32:
        return True
    if ret[0] == '192' and ret[1] == '168':
        return True
    return False


def print_msg(msg=None, left_align=True, line_feed=False):
    if left_align:
        sys.stdout.write('\r' + msg + ' ' * (console_width - len(msg)))
    else:  # right align
        sys.stdout.write('\r' + ' ' * (console_width - len(msg)) + msg)
    if line_feed:
        sys.stdout.write('\n')
    sys.stdout.flush()


def test_server(server, dns_servers):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.lifetime = resolver.timeout = 6.0
    try:
        resolver.nameservers = [server]
        answers = resolver.query('public-dns-a.baidu.com')    # test lookup an existed domain
        if answers[0].address != '180.76.76.76':
            raise Exception('Incorrect DNS response')
        try:
            resolver.query('test.bad.dns.lijiejie.com')    # Non-existed domain test
            with open('bad_dns_servers.txt', 'a') as f:
                f.write(server + '\n')
            print_msg('[+] Bad DNS Server found %s' % server)
        except:
            dns_servers.append(server)
        #print_msg('[+] Server %s < OK >   Found %s' % (server.ljust(16), len(dns_servers)))
    except:
        print_msg('[+] Server %s <Fail>   Found %s' % (server.ljust(16), len(dns_servers)))


def load_dns_servers():
    #print_msg('[+] Validate DNS servers', line_feed=True)
    dns_servers = []
    pool = Pool(10)
    for server in open('dict/dns_servers.txt').readlines():
        server = server.strip()
        if server:
            pool.apply_async(test_server, (server, dns_servers))
    pool.join()

    dns_count = len(dns_servers)
    #print_msg('\n[+] %s available DNS Servers found in total' % dns_count, line_feed=True)
    if dns_count == 0:
        print_msg('[ERROR] No DNS Servers available!', line_feed=True)
        sys.exit(-1)
    return dns_servers


def load_next_sub(options):
    next_subs = []
    _set = set()
    _file = 'dict/next_sub_full.txt' if options.full_scan else 'dict/next_sub.txt'
    with open(_file) as f:
        for line in f:
            sub = line.strip()
            if sub and sub not in next_subs:
                tmp_set = {sub}
                while tmp_set:
                    item = tmp_set.pop()
                    if item.find('{alphnum}') >= 0:
                        for _letter in 'abcdefghijklmnopqrstuvwxyz0123456789':
                            tmp_set.add(item.replace('{alphnum}', _letter, 1))
                    elif item.find('{alpha}') >= 0:
                        for _letter in 'abcdefghijklmnopqrstuvwxyz':
                            tmp_set.add(item.replace('{alpha}', _letter, 1))
                    elif item.find('{num}') >= 0:
                        for _letter in '0123456789':
                            tmp_set.add(item.replace('{num}', _letter, 1))
                    elif item not in _set:
                        _set.add(item)
                        next_subs.append(item)
    return next_subs


def get_out_file_name(target, options):
    if options.output:
        outfile = options.output
    else:
        _name = os.path.basename(options.file).replace('subnames', '')
        if _name != '.txt':
            _name = '_' + _name
        outfile = target + _name if not options.full_scan else target + '_full' + _name
    return outfile


def user_abort(sig, frame):
    exit(-1)

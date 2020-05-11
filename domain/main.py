#coding=utf-8
import sys
import argparse
import os
from subprocess import PIPE,Popen
import time

subdomain_jiejie=[]

def make_domain():
    os.system("copy sub.txt/b+teemo.txt/b+kongge.txt/b+wy.txt/b+kongge.txt/b  all_reqult.log  && del jiejie.txt && del wy.txt")
    list_domain=[]
    f=open("all_requst_log","r")
    while True:
        line = f.readline()
        if '.' in line:
            line = line.strip('').strip('\r').strip('"').strip(',').strip('            \r\r\n",').strip('\r\r\n')
        print line
        if line:
            pass    # do something here
            line=line.strip()
            if '.' in line and '[S]' in line:
                list_domain.append(line.split('\t')[2])
            else:
                if '.' in line and '[R]' in line:
                    list_domain.append(line.split('\t')[3])
                else:
                    if '.' in line:
                        list_domain.append(line.replace(' ', '').strip("\\r").replace("\\r\\r\\n",''))
                        #print line
        else:
            break
    f.close()
    os.system("del all_reqult.log")
    list_domain = list(set(( list_domain )))
    print list_domain,len(list_domain)
    txt=time.clock()+'.xls'
    with open(txt,'w') as outfile:
        outfile.write('\n'.join(list_domain))
    fopen1 = open('report/result.txt','w')
    fopen1.write('\n'.join(list_domain))
    fopen1.close()

def diff():
    if os.path.exists(syspath + '/out/Result.txt'):
        oldlist = []
        with open(syspath + '/out/Result.txt') as f:
            for line in f:
                oldlist.append(line.strip())
        old_change_list = list(set(oldlist).difference(set(result_info)))
        if old_change_list:
            Public_nmap(old_change_list)
            change_del_list = list(set(oldlist).difference(set(self.result_info)))
        change_add_list = list(set(self.result_info).difference(set(oldlist)))
        return change_del_list,change_add_list

def send_mail(change_del_list,change_add_list):
    logger = LogInfo(syspath + '/log/process.log')
    logger.infostring('start sending mail...')
    msg = MIMEMultipart()
    msg["Subject"] = "每日域名信息变化详情"
    msg["From"] = 'domain_scan'
    msg["To"] = '95948663@qq.com'

    if change_add_list or change_del_list or weakpass_result:
        msgAlternative = MIMEMultipart('alternative')
        msg.attach(msgAlternative)
        html_format = """
        <p>{title}</p>
        <style>table,table tr th, table tr td {{border:1px solid #0094ff;}}
        table {{  min-height: 25px; line-height: 25px; text-align: center; border-collapse: collapse; padding:2px;}}</style>
        <table border="1" cellspacing="0"><tr><th>IP地址</th><th>端口</th><th>服务名称</th><th>{protocol}</th><th>{status}</th></tr>{info}</table>
          """
        add_port_info = ""
        for result in change_add_list:
            value = re.split('[:]', result)
            add_port_info += """<tr><td>%s</td><td>%s</td><td>%s</td><td>TCP</td><td>开放</td></tr>""" % (
                value[0], value[1], value[2])
        html_add = html_format.format(title="新增端口服务如下：", protocol='协议', status='状态', info=add_port_info)

        del_port_info = ""
        for result in change_del_list:
            value = re.split('[:]', result)
            del_port_info += """<tr><td>%s</td><td>%s</td><td>%s</td><td>TCP</td><td>关闭</td></tr>""" % (
                value[0], value[1], value[2])
        html_del = html_format.format(title="关闭端口服务如下：", protocol='协议', status='状态', info=del_port_info)

        if weakpass_result:
            weakpass_info = ""
            for result in self.weakpass_result:
                weakpass_info += """<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>""" % (
                    result['host'], result['port'], result['server'], result['user'], result['password'])
            html_weak = html_format.format(title="弱口令端口服务信息如下：", protocol='账户', status='密码', info=weakpass_info)
        else:
            html_weak = "<p></p><p>不存在服务弱口令信息。</p>"

        msg_html = "<p>公网端口服务详情请参照附件信息。</p>"
        msg_html += html_add if add_port_info else ""
        msg_html += html_del if del_port_info else ""
        msg_html += html_weak

        msgAlternative.attach(MIMEText(msg_html, 'html', 'utf-8'))
    else:
        part = MIMEText("端口服务详情请参照附件信息。\n注：端口服务信息并未改变，且不存在弱口令信息")
        msg.attach(part)
    if xlsfile:
        part = MIMEApplication(open(xlsfile, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=xlsfile)
        msg.attach(part)
    error = 0
    while True:
        if error == 3:
            break
        try:
            s = smtplib.SMTP(self.smtp_server, timeout=30)
            s.login(self.user, self.password)
            s.sendmail(self.user, self.toemail, msg.as_string())
            s.close()
            break
        except smtplib.SMTPException, e:
            error += 1
            logger.infostring('sending mail failure,error: %s' % e.message)
            continue
    logger.infostring('sending mail success')

def sub_domain_sublist(domain):
    popen=Popen(['python','sublist3r.py','-d','{name}'.format(name=domain),'-o {name}_sublistdir.txt'.format(name=domain)],stdout=PIPE)
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

def sub_doman_jiejie(domain):
    popen=Popen(['python','C:\Users\TR\Desktop\sfile\domain\\brute\\subDomainsBrute.py','-d','{name}'.format(name=domain)],stdout=PIPE)
    while True:
        next_line=popen.stdout.readline()
        if next_line == '' and popen.poll()!=None:
            break
        sys.stdout.write(next_line)
        subdomain_jiejie.append(next_line)
    return list(set(subdomain_jiejie))
def run(args):
    #domain=args.domain
    domain='baidu.com'
    if not domain:
        print('usage: main.py -u www.xxx.com')
        sys.exit(1)
    try:
        print "\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] first INTERFACE\nwaiting 5s ......\n\n"
        time.sleep(1)
        sub_domain_teemo(domain)
        print "\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] second interface\nwaiting 5s ......\n\n"
        time.sleep(1)
        result=sub_doman_jiejie(domain)
        save_result('demo_geili.txt',result)
        print "\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] fourth interface\nwaiting 5s ......\n\n"
        time.sleep(1)
        sub_domain_sublist(domain)
        print("\n[+++++++++++++++++++++++++++++++++++++++++++++++++++++++++] make domain result\nwaiting 5s ......\n\n")
        time.sleep(1)
        make_domain()
        diff()
        send_mail(change_del_list,change_add_list)
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Monitor SRC domain name changes')
    parser.add_argument('-u','--url', dest='domain',help='scan url')
    parser.add_argument('-d', '--domain', dest='domain_file', help='domain_file')
    parser.add_argument('-f','--file', dest='file', help='file')
    parser.add_argument('-t', '--threads', dest='threads',default=30, help='scan threads')
    parser.add_argument('-s', '--status_code', dest='status_code', help='target status_code')
    parser.add_argument('-o', '--output', dest='output',help='output file')
    args = parser.parse_args()
    try:
        run(args)
    except KeyboardInterrupt:
        sys.exit(1)




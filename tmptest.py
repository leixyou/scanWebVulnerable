#!/usr/bin/env python
import sys
import socket
import requests
import os
import subprocess
import re
from bs4 import BeautifulSoup
#----------------------------------------------------------------------
ls=os.linesep
def detectHost(ip):
    """detect the alive host"""
    ping = subprocess.call('ping %s' %ip)
    if ping==0:
        print 'alive!'
        flag=True
    elif ping==1:
        print 'not alive!'
        flag=False
    else:
        flag=False
    return flag

#----------------------------------------------------------------------
def judgeStatus(domain):
    """judge the domian status"""
    url='http://'+domain
    try:
        respone=requests.get(url).status_code
    except Exception,ex:
        print 'ERROR:',ex
        return False
    except requests.exceptions.MissingSchema,e2:
        print 'ERROR,NO this domain!'
        return False
    else:
        return True
    
        
def reDNS(host):
    target='http://dns.aizhan.com/'
    url=target+host
    respone=requests.get(url)
    soup=BeautifulSoup(respone.text)
    ss=soup.findAll(class_='dns-links')
    pattern='\w+\.\w+\.\w+[^\d+\."/<(\'\\\\]'
    dns_links=list(ss)
    #
    #print dns_links
    domains=[]
    for x in dns_links:
        j=str(x)
        m=re.search(pattern,j)
        if m:
            domains.append(m.group())
    return domains
#----------------------------------------------------------------------
def reDNS2(ip):
    try:
        target='domains.yougetsignal.com'
        port=80
        fhClient=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        fhClient.connect((target,port))
        remoteAddress=ip
        data='''POST /domains.php HTTP/1.1
Host: domains.yougetsignal.com
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0
Accept: text/javascript, text/html, application/xml, text/xml, */*
Accept-Language: zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3
X-Requested-With: XMLHttpRequest
X-Prototype-Version: 1.6.0
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Referer: http://www.yougetsignal.com/tools/web-sites-on-web-server/
Content-Length: 32
origin: http://www.yougetsignal.com
Connection: keep-alive

remoteAddress='''+'%s&key=&_=' %(str(remoteAddress))
        fhClient.send(data)
        respone=fhClient.recv(4096)
        pattern='{.+}'
        tmp=re.match(pattern, respone)
        pattern2='\w+[^\d+="\'\.\\\\]\.\w+[^\d+]\.\w+[^\d+\.\'/<("\\r]'
        domain=re.findall(pattern2, respone)
    except socket.error,e:
        print 'the api is busying  please use it later!'
        return None
    return domain
#----------------------------------------------------------------------
def parseIP():
    start=raw_input("the start:")
    end=raw_input("the End:")
    startAddr=start.split('.')
    endAddr=end.split('.')    
    return startAddr,endAddr
#----------------------------------------------------------------------

def SIP():
    """"""
    start,end=parseIP()
    start=[int(q) for q in start]
    end=[int(q) for q in end]
    C1addr=start[2]+1
    C2addr=end[2]+1
    try:
        removeFile('ip.txt')
        f=open('ip.txt','w+')
        
    except IOError,e:
        print "ERROR!!",e
    except WindowsError,we:
        print "the file not exist!"
    else:
        ip=[]
        if start[2]==end[2]:
            for k in range(start[3],end[3]+1):
                host='%s.%s.%s.%s'%(start[0],start[1],start[2],k)
                ip.append(host)
        else:
            for k in range(start[3],255):
                host='%s.%s.%s.%s'%(start[0],start[1],start[2],k)
                ip.append(host)                
        for x in range(C1addr,C2addr):
            for i in range(1,255):
                host2='%s.%s.%s.%s'%(start[0],start[1],x,i)
                ip.append(host2)
        f.writelines(['%s%s'%(a,ls) for a in ip])
        f.close()
        #---------detect alive host
        alive=[]
        removeFile('aliveIP.txt')
        falive=open('aliveIP.txt','w+')
        for x in ip:
            flag=detectHost(x)
            if flag:
                alive.append(x)
            else:
                continue
        falive.writelines(['%s%s'%(b,ls) for b in alive])
        falive.close()
        #-----------reverseDNS----------
        for x in alive:
            domain=reDNS(x)
            if domain is None:
                continue
        if domain==[]:
            return None
        for j in domain:
            m=re.search("oa|a8",j.lower())
            if  m is not None:
                BOO=judgeStatus(j)
                if BOO:
                    exploit(j)
            else:
                urlpart=j.split('.')
                urlpart[0]='a8'
                url='.'.join(urlpart)
                if judgeStatus(url)==False:
                    urlpart[0]='oa'
                    url2='.'.join(urlpart)
                    if judgeStatus(url2):
                        exploit(url2)
                else:
                    exploit(url)
    return None

#----------------------------------------------------------------------
def SH():
    """"""
    domain=raw_input('domain:')
    exploit(domian)
    return
#----------------------------------------------------------------------
def removeFile(filename):
    """remove one file"""
    try:
        os.remove(filename)
        return None
    except WindowsError,e:
        return None
        
#----------------------------------------------------------------------
def exploit(domian):
    """"""
    #explot the website
    #-------------explot--------------------
    #-------------explot--------------------
    #-------------explot--------------------
    #-------------explot--------------------
    if respone.status_code==200:
        removeFile('weak.txt')
        vul=open('weak.txt','w+')
        vul.writelines('%s%s'%(domian,ls))
        vul.close()
    else:
        print 'No the vulnerable!'
#----------------------------------------------------------------------

def usage():
    """"""
    print '''
    [1]Scan the net ,please enter the arrange of IP address!
    [2]Scan the host or single IP
    [q]quit
    '''
#----------------------------------------------------------------------    
def main():
    """"""
    CMDs={'1':SIP,'2':SH}
    
    if len(sys.argv)==1:
        usage()
    while True:
        choice=raw_input(">").strip()
        if choice not in ['1','2','q']:
            print 'Invaild option!'
        if choice=='q':
            break
        print choice
        CMDs[choice]()
        
if __name__=='__main__':
    main()
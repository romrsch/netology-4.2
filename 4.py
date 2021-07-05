#!/usr/bin/env python3

import socket as s
import time as t
import datetime as dt

# set variables 
i = 1
server = {'drive.google.com':'None', 'mail.google.com':'None', 'google.com':'None'}
init=0


while True: 
  for host in server:
    ip = s.gethostbyname(host)
    if ip != server[host]:
      if i==1 and init !=1:
        print(str(dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) +' [ERROR] ' + str(host) +' IP mistmatch: '+server[host]+' '+ip)
      server[host]=ip

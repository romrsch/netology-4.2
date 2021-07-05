#!/usr/bin/env python3

import os
import sys

path_repo = os.getcwd()

if len(sys.argv)>=2:
    path_repo = sys.argv[1]

bash_command = ["cd " +path_repo, "git status 2>&1"]

print('\033[31m')

result_os = os.popen(' && '.join(bash_command)).read()


for result in result_os.split('\n'):
    if result.find('fatal') != -1:
        print('\033[31m Каталог \033[1m '+path_repo+'\033[0m\033[31m не является GIT репозиторием\033[0m')    
    if result.find('изменено') != -1:
        prepare_result = result.replace('\tmodified: ', '')

# замена пробелов в строке для вывода

        prepare_result = prepare_result.replace(' ', '') 
        print(path_repo+prepare_result)

print('\033[0m')


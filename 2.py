#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/4.2", "pwd", "git status"]

print("Path GIT:")
path_git = os.system(bash_command[1])

result_os = os.popen(' && '.join(bash_command)).read()


#is_change = False

for result in result_os.split('\n'):
    if result.find('изменено') != -1:
        
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        
#        break


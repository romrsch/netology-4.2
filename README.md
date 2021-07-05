###  "Использование Python для решения типовых DevOps задач"
#### Задание 1

Есть скрипт:

`#!/usr/bin/env python3`
`a = 1`
`b =: '2'`
`c = a + b`

- Какое значение будет присвоено переменной c?
- Как получить для переменной c значение 12?
- Как получить для переменной c значение 3?

**Ответ:**

- Будет ошибка: TypeError: unsupported operand type(s) for +: 'int' and 'str',  т.к. типы данных не соответствуют для операции
- Чтобы получить "12" - нужно сложить две строки, т.е. представить переменную "a" тип данных строка (str):
`c=str(a)+b`
- Чтобы получить "3" - нужно сложить два числа, следовательно представить переменную "b" как целое число тип данных (int) :
`c=a+int(b)`

---
### Задание 2

Мы устроились на работу в компанию, где раньше уже был DevOps Engineer.
Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений.
Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся.
Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

   ```
   !/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```
   
**Ответ:**

- Указал в скрипте свою рабочую директорию `~/netology/4.2`, 
- Закомментарил оператор `break`, который завершал работу цикла, после того как найдет первое изменение. 
- Закомментарил переменную `is_change`
- Изменил шаблон поиска `modified` на "изменено", т.к. git ,в моем случае, содержит записи на русском языке.
- Добавил в список `bash_command` команду `pwd` чтобы отобразить текущий рабочий каталог.

```
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
```

 Результат работы скрипта:

`user@ubuntu:~/netology/4.2$ python3 2.py`
`Path GIT:`
`/home/user/netology/4.2`
`        изменено:      1.py`
`        изменено:      2.py`
`        изменено:      3.py`

---
### Задание 3
 Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

**Ответ:**

```
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
```
Результат работы скрипта:
`user@ubuntu:~/netology/4.2$ python3 3.py`

`/home/user/netology/4.2 изменено:1.py`
`/home/user/netology/4.2 изменено:2.py`
`/home/user/netology/4.2 изменено:3.py`

Если запускаем скрипт в другой директории без контроля версий
`user@ubuntu:/tmp$ python3 ~/netology/4.2/3.py`

 `Каталог  /tmp не является GIT репозиторием`

---
### Задание 4
Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: drive.google.com, mail.google.com, google.com.

**Ответ:**
``` 
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
```
Результат работы скрипта:
```
2021-07-06 01:32:14 [ERROR] drive.google.com IP mistmatch: None 142.251.1.194
2021-07-06 01:32:14 [ERROR] mail.google.com IP mistmatch: None 173.194.222.83
2021-07-06 01:32:14 [ERROR] google.com IP mistmatch: None 74.125.205.138
2021-07-06 01:32:14 [ERROR] google.com IP mistmatch: 74.125.205.138 74.125.205.113
2021-07-06 01:32:19 [ERROR] mail.google.com IP mistmatch: 173.194.222.83 173.194.222.18
2021-07-06 01:32:19 [ERROR] google.com IP mistmatch: 74.125.205.113 74.125.205.102
2021-07-06 01:32:19 [ERROR] google.com IP mistmatch: 74.125.205.102 74.125.205.101
2021-07-06 01:32:24 [ERROR] mail.google.com IP mistmatch: 173.194.222.18 173.194.222.83
2021-07-06 01:32:24 [ERROR] google.com IP mistmatch: 74.125.205.101 74.125.205.102
2021-07-06 01:32:24 [ERROR] google.com IP mistmatch: 74.125.205.102 74.125.205.113
2021-07-06 01:32:29 [ERROR] mail.google.com IP mistmatch: 173.194.222.83 173.194.222.18
2021-07-06 01:32:29 [ERROR] google.com IP mistmatch: 74.125.205.113 74.125.205.138
2021-07-06 01:32:29 [ERROR] google.com IP mistmatch: 74.125.205.138 74.125.205.139
2021-07-06 01:32:34 [ERROR] google.com IP mistmatch: 74.125.205.139 74.125.205.101
```

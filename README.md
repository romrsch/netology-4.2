### Задание 1

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

   ```#!/usr/bin/env python3

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

Указал в скрипте свою рабочую директорию, но представленный скрипт не заработал. Получил ошибку:

  ```user@ubuntu:~/netology/4.2$ python3 2.py

      File "/home/user/netology/4.2/2.py", line 10
        is_change = False
    IndentationError: unexpected indent
```

Результат появился,  после того как убрал из скрипта  переменную `is_change`
и оператор `breake`, который завершает работу цикла `for` после того как найдёт первое "изменение".
Ещё изменил шаблон поиска `modified` на "изменено", т.к. git в моем случае
содержит записи на русском языке.


```
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/4.2", "git status"]

result_os = os.popen(' && '.join(bash_command)).read()


for result in result_os.split('\n'):
    if result.find('изменено:') != -1:
        prepare_result = result.replace('\tизменено::   ', '')
        print(prepare_result)

```

 Результат работы скрипта:

`user@ubuntu:~/netology/4.2$ python3 2.py`
` изменено:      README.md`

---
### Задание 3
 Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

**Ответ:**

```
#!/usr/bin/env python3
import os
import sys

cmd = os.getcwd()

if len(sys.argv)>=2:
    cmd = sys.argv[1]
bash_command = ["cd "+cmd, "git status 2>&1"]
print('\033[31m')
result_os = os.popen(' && '.join(bash_command)).read()

for result in result_os.split('\n'):
    if result.find('fatal') != -1:
        print('\033[31m Каталог \033[1m '+cmd+'\033[0m\033[31m не GIT репозиторий\033[0m')
    if result.find('изменено') != -1:
        prepare_result = result.replace('\tизменено: ', '')

# замена пробелов в строке для вывода
        prepare_result = prepare_result.replace(' ', '')
        print(cmd+prepare_result)

print('\033[0m')
```

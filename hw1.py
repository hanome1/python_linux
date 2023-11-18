"""Задание 1.

Условие:
Написать функцию на Python, которой передаются в качестве параметров команда и текст. Функция должна возвращать True,
если команда успешно выполнена и текст найден в её выводе и False в противном случае. Передаваться должна только одна
 строка, разбиение вывода использовать не нужно.

Задание 2. (повышенной сложности)

Доработать функцию из предыдущего задания таким образом, чтобы у неё появился дополнительный режим работы, в котором
вывод разбивается на слова с удалением всех знаков пунктуации (их можно взять из списка string.punctuation модуля string).
В этом режиме должно проверяться наличие слова в выводе.

"""
import subprocess
import re

if __name__ == '__main__':
    def commander(cmd, text):
        res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        if res.returncode == 0:
            out = res.stdout
            if out.__contains__(text):
                return True
        return False

    def commander1(cmd, text):
        res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        if res.returncode == 0:
            words = re.sub(r'[^\w\s]', ' ', res.stdout.lower()).split()
            # print(words)
            if text in words:
                return True
        return False


    # print(commander('cat /etc/os-release', 'VERSION_CODENAME=jammy'))
    # print(commander(input('input the command: '), input('input the text you\'re looking for: ')))

    print(commander1('cat /etc/os-release', 'jammy'))
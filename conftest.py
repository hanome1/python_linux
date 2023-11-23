import random
import string
import subprocess
from datetime import datetime

import pytest
import yaml
from checkers import checkout, ssh_checkout, ssh_run
from for_files import upload_files

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return ssh_checkout("127.0.0.1", "test", "123", "mkdir {} {} {} {}".format(data["folder_in"], data["folder_out"],
                                                                               data["folder_ext"], data["folder_ext2"]),
                        "")


@pytest.fixture()
def clear_folders():
    ssh_checkout("127.0.0.1", "test", "123",
                       "rm -rf {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                                   data["folder_ext2"]), "")


@pytest.fixture()
def make_files():
    ssh_checkout("127.0.0.1", "test", "123", f'cd {data["folder_in"]}; touch qwe', '')
    ssh_checkout("127.0.0.1", "test", "123", f'cd {data["folder_in"]}; touch rty', '')
    list_of_files = ['qwe', 'rty']
    for i in range(2, data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if ssh_checkout("127.0.0.1", "test", "123",
                        "cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"],
                                                                                               filename,
                                                                                               data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not ssh_checkout("127.0.0.1", "test", "123", "cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not ssh_checkout("127.0.0.1", "test", "123",
                        "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"],
                                                                                                  subfoldername,
                                                                                                  testfilename), ""):
        return subfoldername, None
    else:
        return subfoldername, testfilename


@pytest.fixture(autouse=True, scope='function')
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print("Finish: {}".format(datetime.now().strftime("%H:%M:%S.%f")))


@pytest.fixture(autouse=True, scope='module')
def stat_clear():
    ssh_checkout("127.0.0.1", "test", "123", 'rm {}stat.txt'.format(data['home']), '')


@pytest.fixture(autouse=True, scope='function')
def add_str_to_stat():
    loadavg = subprocess.run('cat /proc/loadavg', shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout[:-1:]
    yield ssh_checkout("127.0.0.1", "test", "123",
                       'echo "{}\t{}\t{}\t{}" >> {}stat.txt'.format(datetime.now(), data['count'], data['bs'], loadavg,
                                                                    data['home']), '')


@pytest.fixture(autouse=True, scope='session')
def deploy():
    res = []
    upload_files("127.0.0.1", "test", "123", "/home/lemonah/p7zip-full.deb", "/home/test/p7zip-full.deb")
    res.append(ssh_checkout("127.0.0.1", "test", "123", "echo '123' | sudo -S dpkg -i /home/user2/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("127.0.0.1", "test", "123", "echo '123' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok installed"))
    return all(res)

    # if deploy():
    #     print("Деплой успешен")
    # else:
    #     print("Ошибка деплоя")


# @pytest.fixture()
# def time_start():
#     return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


@pytest.fixture(autouse=True, scope='module')
def save_to_log():
    start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(f'\n\n{start = }\n\n')
    log = ssh_run('127.0.0.1', 'test', '123', f'journalctl --since "{start}"')
    # print(log)
    ssh_checkout("127.0.0.1", "test", "123",
                 'echo "{}" >> {}stat1.txt'.format(f'\n\nTEST #{start}\n', data['home']), '')
    yield ssh_checkout("127.0.0.1", "test", "123",
                       'echo "{}" >> {}stat1.txt'.format(log, data['home']), '')

import random
import string
import subprocess
from datetime import datetime

import pytest
import yaml
from checkers import checkout

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
    return checkout(
        "mkdir {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"], data["folder_ext2"]), "")


@pytest.fixture(scope="session")
def clear_folders():
    yield checkout("rm -rf {} {} {} {}".format(data["folder_in"], data["folder_out"], data["folder_ext"],
                                               data["folder_ext2"]), "")


@pytest.fixture()
def make_files():
    checkout(f'cd {data["folder_in"]}; touch qwe', '')
    checkout(f'cd {data["folder_in"]}; touch rty', '')
    list_of_files = ['qwe', 'rty']
    for i in range(3, data["count"]):
        filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        if checkout("cd {}; dd if=/dev/urandom of={} bs={} count=1 iflag=fullblock".format(data["folder_in"], filename,
                                                                                           data["bs"]), ""):
            list_of_files.append(filename)
    return list_of_files


@pytest.fixture()
def make_subfolder():
    testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    if not checkout("cd {}; mkdir {}".format(data["folder_in"], subfoldername), ""):
        return None, None
    if not checkout(
            "cd {}/{}; dd if=/dev/urandom of={} bs=1M count=1 iflag=fullblock".format(data["folder_in"], subfoldername,
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
    checkout('rm {}stat.txt'.format(data['home']), '')


@pytest.fixture(autouse=True, scope='function')
def add_str_to_stat():
    loadavg = subprocess.run('cat /proc/loadavg', shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout[:-1:]
    yield checkout('echo "{}\t{}\t{}\t{}" >> {}stat.txt'.format(datetime.now(), data['count'], data['bs'], loadavg, data['home']), ''

                   # а куда илд то ставить и что он должен возвращать?!

import subprocess

if __name__ == '__main__':
    res = subprocess.run("cat /etc/os-release", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    out = res.stdout
    if res.returncode == 0:
        lst = out.split('\n')
        if 'VERSION="22.04.3 LTS (Jammy Jellyfish)"' in lst and 'VERSION_CODENAME=jammy' in lst:
            print('success')
    else:
        print('fail')
49qpfv2mgbi76ez
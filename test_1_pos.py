import subprocess

main = "/home/lemonah/tests"
tst = "/home/lemonah/tests/tst"
out = "/home/lemonah/tests/out"
folder1 = "/home/lemonah/tests/folder1"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        # print(result.stdout)
        return True
    else:
        return False


# def test_step1():
#     # test1 =================== create archive
#     assert checkout("cd /home/lemonah/tests/tst; 7z a ../out/arx2", "Everything is Ok"), "Test1 FAIL"


# def test_step2():
#     # test2 ======== take docs from folder: out and copy this docs to folder1
#     assert checkout("cd /home/lemonah/tests/out; 7z e arx2.7z -o/home/lemonah/tests/folder1 -y", "Everything is Ok"), "Test2 FAIL"


def test_step3():
    # test3 =========show info about arx2.7z
    assert checkout("cd /home/lemonah/tests/out; 7z t arx2.7z", "Everything is Ok"), "Test3 FAIL"


def test_step4():
    # test4 ========= add archive update
    assert checkout("cd /home/lemonah/tests/tst; 7z u ../out/arx2.7z", "Everything is Ok"), "Test4 FAIL"


def test_step5():
    # test5 ========= delete docs one and two from archive in folder out
    assert checkout("cd /home/lemonah/tests/out; 7z d arx2.7z", "Everything is Ok"), "Test5 FAIL"

# ==================================================================================================================

def test_step1():
    # test1 =================== create archive
    result1 = checkout("cd /home/lemonah/tests/tst; 7z a ../out/arx2", "Everything is Ok")
    # check if arx2.7z in out
    result2 = checkout("cd /home/lemonah/tests/out; ls", "arx2.7z")
    assert result1 and result2, "Test1 FAIL"


def test_step2():
    # test1 ======== take docs from folder: out and copy these docs to folder1
    result1 = checkout("cd /home/lemonah/tests/out; 7z e arx2.7z -o/home/lemonah/tests/folder1 -y", "Everything is Ok")
    result2 = checkout("cd /home/lemonah/tests/folder1; ls", "qwe")
    result3 = checkout("cd /home/lemonah/tests/folder1; ls", "rty")
    assert result1 and result2 and result3, "Test2 FAIL"
    # assert checkout("cd /home/lemonah/tests/folder1; ls", ["qwe", "rty"]) # ne robit


def test_step6():
    """TESTING FLAG l"""

    stock_files = subprocess.run(f'ls {tst}', shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.split()
    # print('\n', stock_files)
    for item in stock_files:
        assert checkout(f'cd {out}; 7z l arx2.7z', item)


def test_step7():
    """TESTING FLAG x"""

    subprocess.run(f'cd {main}; 7z a {out}/arc_subfol', shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    stock_files = subprocess.run(f'ls {main}', shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout.split()
    # print('\n\nSTOCK\n', stock_files)
    # print(subprocess.run(f'cd {out}; 7z l arc_subfol.7z').stdout)
    for item in stock_files:
        assert checkout(f'cd {out}; 7z l arc_subfol.7z', item)


def test_step8():
    pass

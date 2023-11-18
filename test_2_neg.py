import subprocess

tst = "/home/lemonah/tests/tst"
out = "/home/lemonah/tests/out"
folder1 = "/home/lemonah/tests/folder1"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
    # print('\nSTDERR:\n', result.stderr)
    if (text in result.stdout or text in result.stderr) and result.returncode != 0:
        return True
    else:
        return False


def test_step1():
    # test1 ======== take docs from folder: out and copy this docs to folder1
    # assert checkout("cd /home/lemonah/tests/out; 7z e bad_arx.7z -o/home/lemonah/tests/folder1 -y", 'ERRORS')
    assert checkout("cd {}; 7z e bad_arx.7z -o/{} -y".format(out, folder1), 'ERRORS')
    assert checkout(f'cd {out}; 7z e bad_arx.7z -o{folder1} -y', 'ERRORS')


def test_step2():
    # test3 =========show info about arx2.7z
    # assert checkout("cd /home/lemonah/tests/out; 7z t bad_arx.7z", "ERRORS"), "Test3 FAIL"
    # assert checkout("cd {}; 7z t bad_arx.7z".format(out), "ERRORS"), "Test3 FAIL"
    assert checkout(f"cd {out}; 7z t bad_arx.7z", "ERRORS"), "Test3 FAIL"

# def test_step1():
#     # test1 =================== create archive
#     assert checkout("cd /home/user/tst; 7z a ../out/arx2", "Everything is Ok"), "Test1 FAIL"
#
#
# def test_step2():
#     # test1 ======== take docs from folder: out and copy this docs to folder1
#     assert checkout("cd /home/user/out; 7z e arx2.7z -o/home/user/folder1 -y", "Everything is Ok"), "Test2 FAIL"
#
#
# def test_step3():
#     # test1 =========show info about arx2.7z
#     assert checkout("cd /home/user/out; 7z t arx2.7z", "Everything is Ok"), "Test3 FAIL"
#
#
# def test_step4():
#     # test1 ========= add archive update
#     assert checkout("cd /home/user/tst; 7z u ../out/arx2.7z", "Everything is Ok"), "Test4 FAIL"
#
#
# def test_step5():
#     # test1 ========= delete docs one and two from archive in folder out
#     assert checkout("cd /home/user/out; 7z d arx2.7z", "Everything is Ok"), "Test5 FAIL"


# def test_step1():
#     # test1 ======== take docs from folder: out and copy this docs to folder1
#     assert checkout("cd /home/lemonah/tests/out; 7z e bad_arx.7z -o/home/lemonah/tests/folder1 -y",
#                     "ERRORS"), "Test1 FAIL"

# def test_step2():
#      # test3 =========show info about arx2.7z
#      assert checkout("cd /home/user/out; 7z t bad_arx.7z", "ERRORS"), "Test2 FAIL"


# def test_step1():
#     # test1 ======== take docs from folder: out and copy this docs to folder1
#     assert checkout("cd {}; 7z e bad_arx.7z -o{} -y".format(out, folder1), "ERRORS"), "Test1 FAIL"
#
#
# def test_step2():
#     # test2 =========show info about arx2.7z
#     assert checkout("cd {}; 7z t bad_arx.7z".format(out), "ERRORS"), "Test2 FAIL"

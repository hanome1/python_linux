import subprocess


tst = "/home/user/tst"
out = "/home/user/out"
folder1 = "/home/user/folder1"


def checkout(cmd, text):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    if text in result.stdout and result.returncode == 0:
        return True
    else:
        return False


# def test_step1():
#     # test1 =================== create archive
#     assert checkout("cd /home/user/tst; 7z a ../out/arx2", "Everything is Ok"), "Test1 FAIL"
#
#
# def test_step2():
#     # test1 ======== take docs from folder: out and copy this docs to folder1
#     assert checkout("cd /home/user/out; 7z e arx2.7z -o/home/user/folder1 -y", "Everything is Ok"), "Test2 FAIL"
#
#
# def test_step3():
#     # test1 =========show info about arx2.7z
#     assert checkout("cd /home/user/out; 7z t arx2.7z", "Everything is Ok"), "Test3 FAIL"
#
#
# def test_step4():
#     # test1 ========= add archive update
#     assert checkout("cd /home/user/tst; 7z u ../out/arx2.7z", "Everything is Ok"), "Test4 FAIL"
#
#
# def test_step5():
#     # test1 ========= delete docs one and two from archive in folder out
#     assert checkout("cd /home/user/out; 7z d arx2.7z", "Everything is Ok"), "Test5 FAIL"

# ==================================================================================================================

# def test_step1():
#     # test1 =================== create archive
#     result1 = checkout("cd /home/user/tst; 7z a ../out/arx2", "Everything is Ok")
#     # check if arx2.7z in out
#     result2 = checkout("cd /home/user/out; ls", "arx2.7z")
#     assert result1 and result2, "Test1 FAIL"
#
#
# def test_step2():
#     # test1 ======== take docs from folder: out and copy this docs to folder1
#     result1 = checkout("cd /home/user/out; 7z e arx2.7z -o/home/user/folder1 -y", "Everything is Ok")
#     result2 = checkout("cd /home/user/folder1; ls", "one")
#     result3 = checkout("cd /home/user/folder1; ls", "two")
#     assert result1 and result2 and result3, "Test2 FAIL"
#
#
# def test_step3():
#     # test3 =========show info about arx2.7z
#     assert checkout("cd /home/user/out; 7z t arx2.7z", "Everything is Ok")
#
#
# def test_step4():
#     # test4 ========= add archive update
#     assert checkout("cd /home/user/tst; 7z u ../out/arx2.7z", "Everything is Ok")
#
#
# def test_step5():
#     # test5 ========= delete docs one and two from archive in folder out
#     assert checkout("cd /home/user/out; 7z d arx2.7z", "Everything is Ok")


def test_step1():
    # test1 =================== create archive
    result1 = checkout("cd {}; 7z a {}/arx2".format(tst, out), "Everything is Ok")
    # check if arx2.7z in out
    result2 = checkout("cd {}; ls".format(out), "arx2.7z")
    assert result1 and result2, "Test1 FAIL"


def test_step2():
    # test1 ======== take docs from folder: out and copy this docs to folder1
    result1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(out, folder1), "Everything is Ok")
    result2 = checkout("cd {}; ls".format(folder1), "one")
    result3 = checkout("cd {}; ls".format(folder1), "two")
    assert result1 and result2 and result3, "Test2 FAIL"


def test_step3():
    # test3 =========show info about arx2.7z
    assert checkout("cd {}; 7z t arx2.7z".format(out), "Everything is Ok"), "Test3 FAIL"


def test_step4():
    # test4 ========= add archive update
    assert checkout("cd {}; 7z u {}/arx2.7z".format(tst, out), "Everything is Ok"), "Test4 FAIL"


def test_step5():
    # test5 ========= delete docs one and two from archive in folder out
    assert checkout("cd {}; 7z d arx2.7z".format(out), "Everything is Ok"), "Test5 FAIL"
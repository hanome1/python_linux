from lec_files.checkers import checkout, getout


folder_in = "/home/zerg/tst"
folder_out = "/home/zerg/out"
folder_ext = "/home/zerg/folder1"
folder_ext2 = "/home/zerg/folder2"
list_of_files = ["file1.txt", "file2.txt", "file3.txt"]

@pytest.fixture()
def make_folders():
    return checkout("mkdir {} {} {} {}".format(folder_in, folder_out, folder_ext, folder_ext2), "")
@pytest.fixture()
def clear_folders():
    return checkout("rm -rf {}/* {}/* {}/* {}/*".format(folder_in, folder_out, folder_ext, folder_ext2), "")

def test_step1():
    # test1
    res1 = checkout("cd {}; 7z a {}/arx2".format(folder_in, folder_out), "Everything is Ok")
    res2 = checkout("ls {}".format(folder_out), "arx2.7z")
    assert res1 and res2, "test1 FAIL"
def test_step2():
    # test2
    res1 = checkout("cd {}; 7z e arx2.7z -o{} -y".format(folder_out, folder_ext), "Everything is Ok")
    res2 = checkout("ls {}".format(folder_ext), "test1")
    res3 = checkout("ls {}".format(folder_ext), "test2")
    assert res1 and res2 and res3, "test2 FAIL"

def test_step3():
    # test3
    assert checkout("cd {}; 7z t arx2.7z".format(folder_out), "Everything is Ok"), "test3 FAIL"

def test_step4():
    # test4
    assert checkout("cd {}; 7z u arx2.7z".format(folder_in), "Everything is Ok"), "test4 FAIL"

folder_ext2 = "/home/zerg/folder2"

def test_step5():
    # test5
    res1 = checkout("cd {}; 7z l arx2.7z".format(folder_out, folder_ext), "test1.txt")
    res2 = checkout("cd {}; 7z l arx2.7z".format(folder_out, folder_ext), "test2.txt")
    assert res1 and res2, "test5 FAIL"

def test_step6():
    # test6
    res1 = checkout("cd {}; 7z x arx2.7z -o{} -y".format(folder_out, folder_ext2), "Everything is Ok")
    res2 = checkout("ls {}".format(folder_ext2), "test1")
    res3 = checkout("ls {}".format(folder_ext2), "test2")
    res4 = checkout("ls {}".format(folder_ext2), "testfldr")
    res5 = checkout("ls {}".format(folder_ext2), "test3")
    assert res1 and res2 and res3 and res4 and not res5, "test6 FAIL"

def test_step7():
    # test7
    assert checkout("cd {}; 7z d arx2.7z".format(folder_out), "Everything is Ok"), "test7 FAIL"

def test_step8():
    # test8
    res1 = checkout("cd {}; 7z h test1.txt".format(folder_in), "Everything is Ok")
    hash = getout("cd {}; crc32 test1.txt".format(folder_in)).upper()
    res2 = checkout("cd {}; 7z h test1.txt".format(folder_in), hash)
    assert res1 and res2, "test8 FAIL"
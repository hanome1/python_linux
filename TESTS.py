import subprocess
import yaml
from checkers import checkout

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self):
        # test1 =================== create archive
        result1 = checkout(f'cd {data["folder_in"]}; 7z a {data["folder_out"]}arx2', "Everything is Ok")
        # check if arx2.7z in out
        result2 = checkout(f'cd {data["folder_out"]}; ls', 'arx2.7z')
        assert result1 and result2, "Test1 FAIL"

    def test_step2(self):
        # test1 ======== take docs from folder: out and copy these docs to folder1
        result1 = checkout("cd /home/lemonah/tests/out; 7z e arx2.7z -o/home/lemonah/tests/folder1 -y",
                           "Everything is Ok")
        result2 = checkout("cd /home/lemonah/tests/folder1; ls", "qwe")
        result3 = checkout("cd /home/lemonah/tests/folder1; ls", "rty")
        assert result1 and result2 and result3, "Test2 FAIL"
        # assert checkout("cd /home/lemonah/tests/folder1; ls", ["qwe", "rty"]) # ne robit

    def test_step3(self):
        # test3 =========show info about arx2.7z
        assert checkout("cd /home/lemonah/tests/out; 7z t arx2.7z", "Everything is Ok"), "Test3 FAIL"

    def test_step4(self):
        # test4 ========= add archive update
        assert checkout("cd /home/lemonah/tests/tst; 7z u ../out/arx2.7z", "Everything is Ok"), "Test4 FAIL"

    def test_step5(self):
        # test5 ========= delete docs one and two from archive in folder out
        # assert checkout("cd /home/lemonah/tests/out; 7z d arx2.7z", "Everything is Ok"), "Test5 FAIL"
        pass

    def test_step6(self):
        """TESTING COMMAND l"""

        stock_files = subprocess.run(f'ls {data["folder_in"]}', shell=True, stdout=subprocess.PIPE,
                                     encoding='utf-8').stdout.split()
        # print('\n', stock_files)
        for item in stock_files:
            assert checkout(f'cd {data["folder_out"]}; 7z l arx2.7z', item)

    def test_step7(self):
        """TESTING COMMAND x"""

        subprocess.run(f'cd {data["home"]}; 7z a {data["folder_out"]}/arc_subfol', shell=True, stdout=subprocess.PIPE,
                       encoding='utf-8')
        stock_files = subprocess.run(f'ls {data["home"]}', shell=True, stdout=subprocess.PIPE,
                                     encoding='utf-8').stdout.split()
        # print('\n\nSTOCK\n', stock_files)
        # print(subprocess.run(f'cd {out}; 7z l arc_subfol.7z').stdout)
        for item in stock_files:
            assert checkout(f'cd {data["folder_out"]}; 7z l arc_subfol.7z', item)

    def test_step8(self):
        """TESTING COMMAND h"""

        crc = subprocess.run(f'cd {data["folder_out"]}; crc32 arx2.7z', shell=True, stdout=subprocess.PIPE,
                             encoding='utf-8')
        crc = crc.stdout.upper()
        # print(crc)
        assert checkout(f'cd {data["folder_out"]}; 7z h arx2.7z', crc)


class TestNegative:
    def test_step1(self):
        # test1 ======== take docs from folder: out and copy this docs to folder1
        # assert checkout("cd /home/lemonah/tests/out; 7z e bad_arx.7z -o/home/lemonah/tests/folder1 -y", 'ERRORS')
        assert checkout("cd {}; 7z e bad_arx.7z -o/{} -y".format({data["folder_out"]}, {data["folder_ext"]}), 'ERRORS')
        assert checkout(f'cd {data["folder_out"]}; 7z e bad_arx.7z -o{data["folder_ext"]} -y', 'ERRORS')

    def test_step2(self):
        # test3 =========show info about arx2.7z
        # assert checkout("cd /home/lemonah/tests/out; 7z t bad_arx.7z", "ERRORS"), "Test3 FAIL"
        # assert checkout("cd {}; 7z t bad_arx.7z".format(out), "ERRORS"), "Test3 FAIL"
        assert checkout(f'cd {data["folder_out"]}; 7z t bad_arx.7z', "ERRORS"), 'Test3 FAIL'

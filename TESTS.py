import subprocess
import yaml
from checkers import ssh_checkout, ssh_checkout_negative, ssh_run

with open('config.yaml') as f:
    # читаем документ YAML
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, clear_folders, make_folders, make_files):
        """COMMAND A CREATES ARCHIVE"""
        result1 = ssh_checkout("127.0.0.1", "test", "123",f'cd {data["folder_in"]}; 7z a {data["folder_out"]}arx2', "Everything is Ok")
        # check if arx2.7z in out
        result2 = ssh_checkout("127.0.0.1", "test", "123",f'cd {data["folder_out"]}; ls', 'arx2.7z')
        assert result1 and result2, "Test1 FAIL"

    def test_step2(self):
        """COMMAND E EXTRACTS FILES"""
        result1 = ssh_checkout("127.0.0.1", "test", "123",f'cd {data["folder_out"]}; 7z e arx2.7z -o/{data["folder_ext"]} -y',
                           "Everything is Ok")
        result2 = ssh_checkout("127.0.0.1", "test", "123","cd /home/lemonah/tests/folder1; ls", "qwe")
        result3 = ssh_checkout("127.0.0.1", "test", "123","cd /home/lemonah/tests/folder1; ls", "rty")
        assert result1 and result2 and result3, "Test2 FAIL"
        # assert ssh_checkout("127.0.0.1", "test", "123","cd /home/lemonah/tests/folder1; ls", ["qwe", "rty"]) # ne robit

    def test_step3(self):
        # test3 =========show info about arx2.7z
        assert ssh_checkout("127.0.0.1", "test", "123",f"cd {data['folder_out']}; 7z t arx2.7z", "Everything is Ok"), "Test3 FAIL"

    def test_step4(self):
        # test4 ========= add archive update
        assert ssh_checkout("127.0.0.1", "test", "123",f"cd {data['folder_in']}; 7z u {data['folder_out']}arx2.7z", "Everything is Ok"), "Test4 FAIL"

    def test_step5(self):
        # test5 ========= delete docs one and two from archive in folder out
        assert ssh_checkout("127.0.0.1", "test", "123",f"cd {data['folder_out']}; 7z d arx2.7z", "Everything is Ok"), "Test5 FAIL"
        pass

    def test_step6(self, clear_folders, make_folders, make_files):
        """TESTING COMMAND l"""
        subprocess.run(f'cd {data["folder_in"]}; 7z a {data["folder_out"]}arx2', shell=True, stdout=subprocess.PIPE,
                       encoding='utf-8')
        stock_files = subprocess.run(f'ls {data["folder_in"]}', shell=True, stdout=subprocess.PIPE,
                                     encoding='utf-8').stdout.split()
        # print('\n', stock_files)
        for item in stock_files:
            assert ssh_checkout("127.0.0.1", "test", "123",f'cd {data["folder_out"]}; 7z l arx2.7z', item)

    def test_step7(self):
        """TESTING COMMAND x"""

        ssh_checkout("127.0.0.1", "test", "123", f'cd {data["home"]}; 7z a {data["folder_out"]}/arc_subfol', '')
        stock_files = ssh_run("127.0.0.1", "test", "123", f'ls {data["home"]}')
        # print('\n\nSTOCK\n', stock_files)
        # print(subprocess.run(f'cd {out}; 7z l arc_subfol.7z').stdout)
        for item in stock_files:
            assert ssh_checkout("127.0.0.1", "test", "123",f'cd {data["folder_out"]}; 7z l arc_subfol.7z', item)

    def test_step8(self):
        # """TESTING COMMAND h"""

        crc = ssh_run("127.0.0.1", "test", "123", f'crc32 {data["folder_out"]}arc_subfol.7z').upper()
        # crc = crc.stdout.upper()
        print(f'\n\n{crc = })\n\n')
        assert ssh_checkout("127.0.0.1", "test", "123", f'cd {data["folder_out"]}; 7z h arc_subfol.7z', crc)

    def test_fin(self):
        pass


class TestNegative:
    def test_step1(self):
        # test1 ======== take docs from folder: out and copy this docs to folder1
        # assert ssh_checkout("127.0.0.1", "test", "123","cd /home/lemonah/tests/out; 7z e bad_arx.7z -o/home/lemonah/tests/folder1 -y", 'ERRORS')
        assert ssh_checkout_negative("127.0.0.1", "test", "123", f'cd {data["folder_out"]}; 7z e bad_arx.7z -o/{data["folder_ext"]} -y','ERRORS')
        assert ssh_checkout_negative("127.0.0.1", "test", "123",f'cd {data["folder_out"]}; 7z e bad_arx.7z -o{data["folder_ext"]} -y', 'ERRORS')

    def test_step2(self):
        # test3 =========show info about arx2.7z
        # assert ssh_checkout("127.0.0.1", "test", "123","cd /home/lemonah/tests/out; 7z t bad_arx.7z", "ERRORS"), "Test3 FAIL"
        # assert ssh_checkout("127.0.0.1", "test", "123","cd {}; 7z t bad_arx.7z".format(out), "ERRORS"), "Test3 FAIL"
        assert ssh_checkout_negative("127.0.0.1", "test", "123",f'cd {data["folder_out"]}; 7z t bad_arx.7z', "ERRORS"), 'Test3 FAIL'

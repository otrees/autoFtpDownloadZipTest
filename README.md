打包：pyinstaller --onefile --icon icon_256.ico _ftp_getExeConfig.py
1）执行文件dist/_ftp_copy_exe.bat
2）在当前目录按照bat的参数连接FTP服务器，删除不含_前缀的文件，并连接服务器下载zip，解压缩文件，删除zip，下载config文件移动到指定目录，完成测试测试包准备工作。
3）可以使用主控程序控制解压缩的测试包的执行文件，完成自动化运行测试。

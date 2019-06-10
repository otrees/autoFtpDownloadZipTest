自动ftp下载，拷贝配置文件，准备测试
====
打包应该包含文件夹icon\icon_256.ico 要求ico是256*256分辨率 <br/>
打包命令(不显示控制台)：pyinstaller --onefile --icon icon\icon_256.ico _ftp_getExeConfig.py --noconsole <br/>
打包命令(显示控制台)：pyinstaller --onefile --icon icon\icon_256.ico _ftp_getExeConfig.py <br/>
  1)修改配置文件_ftp_getExeConfig.ini
  2）执行文件dist/_ftp_copy_exe.bat<br/>
  3）在当前目录按照bat的参数连接FTP服务器，删除不含_前缀的文件，并连接服务器下载zip，解压缩文件，删除zip，下载config文件移动到指定目录，完成测试测试包准备工作。<br/>
  4）可以使用主控程序控制解压缩的测试包的执行文件，完成自动化运行测试。<br/>

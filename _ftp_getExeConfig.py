import os
import sys
import shutil
import logging
import zipfile
from ftplib import FTP
import configparser

# 初始化日志
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='_ftp.log', level=logging.DEBUG, format=LOG_FORMAT)

class MyFtp():
    # 类变量
    encode=['UTF-8','gbk','GB2312','GB18030','Big5','HZ']

    def __init__(self):
        self.ftp_client = FTP()

    # 些函数实现ftp登录
    def ftp_login(self,host_ip,username,password):
        try:
            self.ftp_client.connect(host_ip,port=21,timeout=10)
        except :
            logging.warning('network connect time out')
            return 1001
        try:
            self.ftp_client.login(user=username, passwd=password)
            # 选定字符集为当前UTF-8
            self.ftp_client.encoding = self.encode[0]
        except:
            logging.warning('username or password error')
            return 1002
        return 1000
    # 此函数获取目录文件
    def get_dirs_files(self,mydir):
        u''' 得到当前目录和文件, 放入dir_res列表 '''
        dir_res = []
        self.ftp_client.dir(mydir, dir_res.append)
        files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
        dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
        return (files, dirs)

    # 此函数执行ftp命令，并打印命令执行结果
    def execute_download_file_command(self,remote_dir,fn):
        # 记录目录列表
        dir_res = []
        # 通运sendcmd方法形式执行pwd命令，为使用形式统一起见不推荐使用此种形式，而且其实大多数命令都是支持这种形式的
        command_result = self.ftp_client.sendcmd('pwd')
        logging.info('command_result:%s'% command_result)
        # 通过直接使用pwd方法执行pwd命令，推荐统一使用此种形式
        command_result = self.ftp_client.pwd()
        logging.info('command_result:%s' % command_result)
        # 上传文件；'stor ftp_client.py'告诉服务端将上传的文件保存为ftp_client.py，open()是以二进制读方式打开本地要上传的文件
        #command_result = self.ftp_client.storbinary('stor ftp_client.py',open("ftp_client.py",'rb'))
        #logging.info('command_result:%s' % command_result)
        # 切换目录
        command_result = self.ftp_client.cwd(remote_dir)
        logging.info('command_result:%s' % command_result)

        # 下载文件；'retr .bash_profile'告诉服务端要下载服务端当前目录下的.bash_profile文件，open()是以二进制写方式打开本地要存成的文件
        command_result = self.ftp_client.retrbinary('retr '+fn, open(fn, 'wb').write)
        logging.info('command_result:%s' % command_result)
    # 此函数执行ftp命令，并打印命令执行结果
    def execute_download_dir_command(self,remote_dir):
        # 通运sendcmd方法形式执行pwd命令，为使用形式统一起见不推荐使用此种形式，而且其实大多数命令都是支持这种形式的
        command_result = self.ftp_client.sendcmd('pwd')
        logging.info('command_result:%s'% command_result)
        # 通过直接使用pwd方法执行pwd命令，推荐统一使用此种形式
        command_result = self.ftp_client.pwd()
        logging.info('command_result:%s' % command_result)
        # 切换目录
        command_result = self.ftp_client.cwd(remote_dir)
        logging.info('command_result:%s' % command_result)
        # 此函数获取目录文件
        files, dirs = self.get_dirs_files(remote_dir)
        res_files = []
        res_file = []
        for f in files:
            #print next_dir, ':', f
            print(remote_dir+' download :',os.path.abspath(f))
            res_files.append(os.path.abspath(f))
            res_file.append(f)
            outf = open(f, 'wb')
            try:
                command_result = self.ftp_client.retrbinary('RETR %s' % f, outf.write)
                logging.info('command_result:%s' % command_result)
            finally:
                    outf.close()
        return res_file,res_files
    # 此函数实现退出ftp会话
    def ftp_logout(self):
        logging.warning('now will disconnect with server')
        self.ftp_client.close()
class MyZip():
    # 解压文件
    def extractFile(self,fn,isDel=False):
        zfile = zipfile.ZipFile(fn)
        zfile.extractall()
        zfile.close()
        if isDel :
            os.remove(fn)
            return 2001
        else :
            #logging.warning('delete error')
            return 2002

# 移动目录下文件到指定目标
def moveConfigFiles(resultFiles,resultPathFiles,localTargetDir):
    # 遍历需要移动的文件
    for f in resultFiles:
        targetPathFile = localTargetDir+'//'+f
        logging.info('targetPathFile is %s ',targetPathFile)
        print(targetPathFile)
        try:
            if os.path.exists(targetPathFile):
                # 删除
                os.remove(targetPathFile)
                logging.info('exists target file:%s %s ---- removed', localTargetDir, f)
                # 移动文件
                dst = shutil.move(f, localTargetDir)
                logging.info("move file %s ---- success ",dst)
            else:
                # 移动文件
                dst = shutil.move(f, localTargetDir)
                logging.info("move file %s ---- success ",dst)
        except shutil.Error as err:
            logging.error(err)

# 删除目录下文件
def removeDirFiles(localPath,filter_prefix):
    rootdir = localPath
    filelist=os.listdir(rootdir)
    #print(filelist)
    for f in filelist:
        filepath = os.path.join(rootdir,f)
        if f.startswith(filter_prefix):
            print(f,"--- filter prefix, no remove ")
        else:
            if os.path.isfile(filepath):
                os.remove(filepath)
                print(filepath," ---- removed!")
            elif os.path.isdir(filepath):
                shutil.rmtree(filepath,True)
                print("dir ",filepath," ---- removed!")
# 读取配置文件
def readConfigFile(file):
    # 读取Config文件
    config = configparser.ConfigParser()
    secs = config.read(file)  # 读取配置文件，如果配置文件不存在则创建
    return config

# Main
if __name__ == '__main__':
    logging.info('start program')
    # 当前脚本住在本地目录
    localdir = os.path.abspath(os.path.dirname(__file__))
    # 读取配置文件
    config = readConfigFile(localdir+'\\_ftp_config.ini')
    print(config["FTP"]["host_ip"])
    #sys.exit(0)
    # 要连接的主机ip
    host_ip = config["FTP"]["host_ip"]
    # 用户名
    username = config["FTP"]["username"]
    # 密码
    password = config["FTP"]["password"]
    # 最新执行文件目录
    remote_dir_download_release = config["FTP"]["remote_dir_download_release"]
    # 配置文件
    remote_dir_download_config_file = config["FTP"]["remote_dir_download_config_file"]
    #remote_dir_download_config_file = '/project/mnxl/config/client_2'
    # method下载工程文件名称
    fn_exe = config["FTP"]["fn_exe"] # 文件名称
    localConfigTargetPath = config["FTP"]["localConfigTargetPath"]
    # 实例化
    my_ftp = MyFtp()
    # 如果登录成功则执行命令，然后退出
    if my_ftp.ftp_login(host_ip,username,password) == 1000:
        logging.info('login success , now will execute some command')
        # 删除
        removeDirFiles(localdir,'_')
        os.chdir(localdir)
        # 执行工程下载
        my_ftp.execute_download_file_command(remote_dir_download_release,fn_exe)
        # method本地下载配置文件存储目录
        resultFiles,resultPathFiles = my_ftp.execute_download_dir_command(remote_dir_download_config_file)
        print("dir result:",resultFiles)
        my_ftp.ftp_logout()
        logging.info('ftp logout')
        # 在工作目录解压文件，请确认解压完成给出提示，再移动配置文件至目录
        if MyZip().extractFile(fn_exe,True) == 2001:
            logging.info('delete '+ fn_exe +' success')
        print("current dir list : %s" %os.listdir(os.getcwd()))
        # 移动配置文件到data目录
        localTargetDir = localdir+"/"+localConfigTargetPath
        moveConfigFiles(resultFiles,resultPathFiles,localTargetDir)
        logging.info('end program.')

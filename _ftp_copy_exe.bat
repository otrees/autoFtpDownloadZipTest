@echo off  
::FTP服务器地址
SET host_ip=192.168.254.200
::FTP用户名
SET username=wyl
::FTP密码
SET password=129991
::FTP远程打包zip文件路径
SET remote_dir_download_release=/project/mnxl/test
::FTP远程配置文件夹路径
SET remote_dir_download_config_file=/project/mnxl/config/client_2
::FTP远程打包zip文件名称
SET fn_exe=mnxl_latest.zip
::zip解压后配置文件拷贝目标路径
SET localConfigTargetPath=MoNiXunLian_Data



start python _ftp_getExeConfig.py %host_ip% %username% %password% %remote_dir_download_release% %remote_dir_download_config_file% %fn_exe% %localConfigTargetPath%
exit
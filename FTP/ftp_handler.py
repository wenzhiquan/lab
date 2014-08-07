# -*- encoding: utf8 -*-

import os
import sys
from ftplib import FTP
import time
from datetime import datetime

class FTPHandler(object):

    def __init__(self):
        self.timecount = 0
        self.log_file_name = "/home/wenzhiquan/下载/test//log.txt"

    def main_server_connect(self):
        try:
            self.conn = FTP('10.108.104.82', 'anonymous', '')
            self.conn.cwd('/MSSLogData')        # 远端FTP目录
            os.chdir('/home/wenzhiquan/下载/test/')                # 本地下载目录
            print "Main FTP server connected..."
        except:
            print "Main FTP server connecting faild..."

    def backup_server_connect(self):
        print "Trying to connect to the backup FTP server..."
        try:
            self.conn = FTP('10.108.106.124', 'anonymous', '')
            self.conn.cwd('/MSSLogData')        # 远端FTP目录
            os.chdir('/home/wenzhiquan/下载/test/')                # 本地下载目录
            print "Backup FTP server connected..."
        except:
            print "Backup FTP server connecting faild..."
            self.backup_server_connect()

    def get_dirs_files(self):
        u''' 得到当前目录和文件, 放入dir_res列表 '''
        dir_res = []
        self.conn.dir('.', dir_res.append)
        files = [f.split(None, 8)[-1] for f in dir_res if f.find('<DIR>') == -1]
        dirs = [f.split(None, 8)[-1] for f in dir_res if f.find('<DIR>') >= 0]
        return (files, dirs)

    def walk(self, next_dir):
        # print 'Walking to', next_dir
        self.conn.cwd(next_dir)
        try:
            os.mkdir(next_dir)
        except OSError:
            pass
        os.chdir(next_dir)

        ftp_curr_dir = self.conn.pwd()
        local_curr_dir = os.getcwd()

        files, dirs = self.get_dirs_files()
        # print "FILES: ", files
        # print "DIRS: ", dirs
        for f in files:
            if os.path.exists(f):
                # print f, "exists!"
                continue
            # print next_dir, ':', f
            outf = open(f, 'wb')
            try:
                self.conn.retrbinary('RETR %s' % f, outf.write)
            finally:
                outf.close()
                readf = open(f, 'rb')
                readf.seek(-5, 2)
                data = readf.readline()
                readf.close()
                now = datetime.now()
                log_file = open(self.log_file_name, 'ab')
                if data != "[END]":
                    os.remove(f)
                    log_file.write("%26s%30s%10s\n" %(now, f, 'False'))
                    log_file.close()
                else:
                    self.timecount = 0
                    log_file.write("%26s%30s%10s\n" %(now, f, 'True'))
                    log_file.close()
        for d in dirs:
            os.chdir(local_curr_dir)
            self.conn.cwd(ftp_curr_dir)
            self.walk(d)

    def run(self):
        self.walk('.')
        self.timecount += 60
        print "Transport finished..."

def main():
    f = FTPHandler()
    f.main_server_connect()
    while True:
        try:
            f.run()
            time.sleep(60)
            if f.timecount >= 600:
                f.timecount = 0
                print "No update in main server for a long time..."
                f.backup_server_connect()
            else:
                f.main_server_connect()
        except:
            print "Some error accured in main server..."
            f.backup_server_connect()

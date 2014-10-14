# -*- encoding: utf8 -*-

import os, stat, sys, syslog
from ftplib import FTP
import time
from datetime import datetime
from FTP.lib.nosql.mongo_util import MongoUtil

class FTPHandler(object):

    def __init__(self):
        global sleeptime
        sleeptime = 20

        self.directory_name = r"/home/wen/local/git/hadoop-tran/FTP/test/"
        self.subdirectory_name = r"FTP/doc/subdirectory.txt"
        self.log_directory_name = self.directory_name + r"Log/"
        self.subdirectory = open(self.subdirectory_name, 'rb').readlines()
        
    	self.ftp_host = "119.57.167.243"
	self.ftp_port = 10022
	self.ftp_username = "anonymous"
	self.ftp_password = ""
	self.ftp_category = "/MSSLogData"

        try:
            self.mongo = MongoUtil("FTP", "filename")
        except:
            print "Faild to connect to the database..."
        os.chdir(self.directory_name)
        if not os.path.exists("Log"):
            os.mkdir("Log")
        for i in range(len(self.subdirectory)):
            self.subdirectory[i] = self.subdirectory[i][:-1]
            tmp = str(self.subdirectory[i])
            if not os.path.exists(tmp):
                try:
                    os.mkdir(tmp)
                except OSError:
                    print "Faild to make directory..."
        syslog.openlog("ftp client", syslog.LOG_PID|syslog.LOG_PERROR, syslog.LOG_DAEMON)
        syslog.syslog(syslog.LOG_INFO, "Program started...")


    def main_server_connect(self):
        try:
            self.conn = FTP()
            self.conn.connect(self.ftp_host, self.ftp_port)
	    self.conn.login(self.ftp_username, self.ftp_password)
            self.conn.cwd(self.ftp_category)        # 远端FTP目录
            print "Main FTP server connected..."
        except:
            print "Main FTP server connecting faild..."

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
        # try:
        #     os.mkdir(next_dir)
        # except OSError:
        #     pass
        # os.chdir(next_dir)

        ftp_curr_dir = self.conn.pwd()
        # local_curr_dir = os.getcwd()

        files, dirs = self.get_dirs_files()
        # print "FILES: ", files
        # print "DIRS: ", dirs
        for f in files:
            filename = r"./%s" % (f[4:-17] + r"/" + f)
            fin_filename = f[4:-17] + r"/" + f[:-4] + "_fin" + f[-4:]
            db_name = self.directory_name + f[4:-17] + r"/" + f


            if os.path.exists(filename) or os.path.exists(fin_filename) or self.mongo.get_one({"name": db_name}):
                #print f, "exists!"
                continue
            # print next_dir, ':', f
            try:
                tmp_filename = f[4:-17] + r"/" + f + r'.COMPLETED'
                outf = open(tmp_filename, 'wb')
                # os.chmod(tmp_filename, stat.S_IRWXU)
            except:
                print "Faild to create local file..."
            try:
                self.conn.retrbinary('RETR %s' % f, outf.write)
            finally:
                outf.close()
                try:
                    readf = open(tmp_filename, 'rb')
                except Exception, e:
                    raise e
                readf.seek(-32, 2)
                data = readf.readlines()
                readf.close()
                now = datetime.now()
                try:
                    tmp_log_file_name = self.log_directory_name + f[:-16] + "log.txt"
                    log_file = open(tmp_log_file_name, 'ab')
                except:
                    print "Faild to create local log file..."
                if "[END] %s" %f not in data:
                    # print "Data not ended, remove the file..."
                    os.remove(tmp_filename)
                    syslog.syslog(syslog.LOG_INFO, "%s\t%s" % (f, 'Transport faild...'))
                    log_file.write("%26s%30s%10s\n" % (now, f, 'False'))
                    log_file.close()
                else:
                    # os.chmod(tmp_filename, stat.S_IREAD|stat.S_IWRITE|stat.S_IRGRP|stat.S_IWGRP|stat.S_IROTH)
                    self.mongo.save({"name": db_name})
                    rename = f[4:-17] + r"/" + f[:-4] + "_fin" + f[-4:]
                    os.rename(tmp_filename, rename)
                    syslog.syslog(syslog.LOG_INFO, "%s\t%s" % (f, 'Transport successful...'))
                    log_file.write("%26s%30s%10s\n" % (now, f, 'True'))
                    log_file.close()
        for d in dirs:
            # os.chdir(local_curr_dir)
            self.conn.cwd(ftp_curr_dir)
            self.walk(d)

    def run(self):
        self.walk('.')
        print "Transport finished..."

def main():
    f = FTPHandler()
    f.main_server_connect()
    while True:
        try:
            print "Client started..."
            f.run()
            time.sleep(sleeptime)
        except:
            print "Some error accured in main server..."
            break

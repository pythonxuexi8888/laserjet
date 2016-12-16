#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    @Author:        yyg
    @Create:        2016MMDD
    @LastUpdate:    2016MMDD HH:MM:SS
    @Version:       0.0
    @Description    
        #
"""
import sys
from ConfigParser import ConfigParser
from os.path import *
from logging import INFO, DEBUG, CRITICAL, WARN, NOTSET
from json import load

# Dir Path
# ROOT_DIR = abspath(join(split(realpath(sys.argv[0]))[0]))
ROOT_DIR_NAME = 'laserjet'
_cwd = abspath(join(split(realpath(sys.argv[0]))[0]))
path_list = _cwd.split(sep)
tmp = list()
for element in path_list:
    if element == ROOT_DIR_NAME:
        break
    else:
        tmp.append(element)

ROOT_DIR = abspath(join(sep.join(tmp), ROOT_DIR_NAME))
CONF_DIR = join(ROOT_DIR, 'conf')
LOGS_DIR = join(ROOT_DIR, 'logs')
RESOURCE_DIR = join(ROOT_DIR, 'resource')
PYPI_DIR = join(RESOURCE_DIR, 'pypi')
SCRIPT_DIR = join(RESOURCE_DIR, 'scripts')
TEMPLATE_DIR = join(RESOURCE_DIR, 'templates')
LIB_DIR = join(ROOT_DIR, 'lib')
CORE_DIR = join(LIB_DIR, 'core')
TEST_DIR = join(ROOT_DIR, 'test')

# Config File Names
BATCH_HOSTS_FILE_NAME = 'batch-hosts.conf'  # 集群主机列表
BATCH_PARAMS_FILE_NAME = 'batch_params.ini'  # 基本配置参数列表
BATCH_CMD_FILE_NAME = 'batch_cmd.conf'  # 批量执行命令列表
BATCH_SYNC_FILE_NAME = 'batch_sync.conf'  # 批量同步文件列表
BATCH_FETCH_FILE_NAME = 'batch_fetch.conf'  # 批量采集文件列表

# Config File Path
BATCH_HOSTS_FILE_PATH = join(CONF_DIR, BATCH_HOSTS_FILE_NAME)
BATCH_PARAMS_FILE_PATH = join(CONF_DIR, BATCH_PARAMS_FILE_NAME)
BATCH_CMD_FILE_PATH = join(CONF_DIR, BATCH_CMD_FILE_NAME)
BATCH_SYNC_FILE_PATH = join(CONF_DIR, BATCH_SYNC_FILE_NAME)
BATCH_FETCH_FILE_PATH = join(CONF_DIR, BATCH_FETCH_FILE_NAME)

# Log File Name
#LOGGER_NAME = 'laserjet'
LOGGER_NAME = ''
LOG_FILE_NAME = 'laserjet.log'
LOG_CONF_FILE_NAME = 'logging-cfg.json'

# Log File path
LOG_FILE = join(LOGS_DIR, LOG_FILE_NAME)
LOG_CONF_FILE = join(CONF_DIR, LOG_CONF_FILE_NAME)

# LOG cfg

LOG_LVL_INFO = INFO
LOG_LVL_DEBUG = DEBUG
LOG_LVL_WARN = WARN
LOG_LVL_CRITICAL = CRITICAL
LOG_LVL_NOTSET = NOTSET
LOG_LVL = LOG_LVL_INFO

LOG_FMT = "%(asctime)s[%(levelname)s] - %(message)s"
LOG_DAT_FMT = "%Y/%m/%d-%H:%M:%S"


# Templates File name

# Templates File Path


class SingletonBaseClass(object):
    def __new__(cls, *args, **kwargs):
        if hasattr(cls, '_instance') is False:
            cls._instance = super(SingletonBaseClass, cls).__new__(cls)
        return cls._instance


class BatchConf(SingletonBaseClass):
    def __init__(self):
        super(BatchConf, self).__init__()
        self.batch_hosts_file = BATCH_HOSTS_FILE_PATH
        self.batch_cmd_file = BATCH_CMD_FILE_PATH
        self.batch_fetch_file = BATCH_FETCH_FILE_PATH
        self.batch_sync_file = BATCH_SYNC_FILE_PATH
        self._batch_param = BatchParams()

    def set_batch_hosts_file(self, file_path):
        if isfile(file_path):
            self.batch_hosts_file = file_path

    def set_batch_cmd_file(self, file_path):
        if isfile(file_path):
            self.batch_cmd_file = file_path

    def set_batch_fetch_file(self, file_path):
        if isfile(file_path):
            self.batch_fetch_file = file_path

    def set_batch_sync_file(self, file_path):
        if isfile(file_path):
            self.batch_sync_file = file_path

    def batch_hosts_generator(self):
        """ Read cluster host pairs from BATCH_HOSTS_FILE
        :arg str batch_hosts_generator:
                absolute path to file 'batch-hosts.conf'
        :return generator ssh_client_auth:
                [{"hostname": "XXX", "username": "XXX", "password":"XXX"},]
        :raise IOError
        """

        try:
            with open(self.batch_hosts_file) as cluster_hosts_conf:
                for line in cluster_hosts_conf:
                    if is_comment(line):
                        continue
                    else:
                        line = line.split()
                        if len(line) == 1:
                            ssh_client_auth = {
                                "hostname": line[0],
                                "username": self._batch_param.get_account_info()["username"],
                                "password": self._batch_param.get_account_info()["password"]
                            }
                            yield ssh_client_auth
                        elif len(line) == 3:
                            ssh_client_auth = {
                                "hostname": line[0],
                                "username": line[1],
                                "password": line[2]
                            }
                            yield ssh_client_auth
                        else:
                            print("file <{0}> contains incorrect info: \'{1}\'".format(
                                self.batch_hosts_file, line))
        except IOError as e:
            print(e)

    def get_batch_cmds(self):
        """ Read commands from BATCH_CMD_FILE
        :arg str batch_cmd_file:
        :return list cmds:
        :raise IOError
        """

        try:
            with open(self.batch_cmd_file) as batch_cmd_conf:
                cmds = list()
                for line in batch_cmd_conf:
                    if is_comment(line):
                        continue
                    else:
                        line = line.strip()
                        cmds.append(line)
                return cmds
        except IOError, e:
            print(e)

    def get_batch_sync(self):
        """ Read src & dst location from BATCH_SYNC_FILE
        :arg str batch_sync_file:
        :return generator localpath_to_remotepath
        :raise IOError
        """
        try:
            with open(self.batch_sync_file) as batch_sync_conf:
                src_to_dst = list()
                for line in batch_sync_conf:
                    if is_comment(line):
                        continue
                    else:
                        line = line.split(',')
                        tmp = {
                            "localpath": line[0].strip(),
                            "remotepath": line[1].strip()
                        }
                        # yield tmp
                        src_to_dst.append(tmp)
                return src_to_dst
        except IOError as e:
            print(e)

    def get_batch_fetch(self):
        """ Read src & dst location from BATCH_FETCH_FILE

        :arg batch_fetch_file:
        :return: list src_to_dst
        """
        with open(self.batch_fetch_file) as batch_fetch_conf:
            src_to_dst = list()
            for line in batch_fetch_conf:
                if is_comment(line):
                    continue
                else:
                    line = line.split(',')
                    tmp = {
                        "remotepath": line[0].strip(),
                        "localpath": line[1].strip()
                    }
                    src_to_dst.append(tmp)
            return src_to_dst


def singleton_decorator(cls, *args, **kwargs):
    __instance = dict()

    def _singleton():
        if cls not in __instance:
            __instance[cls] = cls(*args, **kwargs)
        return __instance[cls]

    return _singleton





@singleton_decorator
class BatchParams(object):
    def __init__(self):
        self.param_file = BATCH_PARAMS_FILE_PATH
        self._cfg = ConfigParser()

    def load_param_file(self, param_file):
        if param_file is not BATCH_PARAMS_FILE_PATH:
            self.param_file = param_file

    def get_account_info(self):
        self._cfg.read(self.param_file)
        session_account_info = 'AccountInfo'
        if self._cfg.has_section(session_account_info):
            return {
                "username": self._cfg.get(session_account_info, 'username'),
                "password": self._cfg.get(session_account_info, 'password')
            }
        else:
            print("file {0} does not contain {1}".format(
                self.param_file, session_account_info))

    def get_yum_repo_addr(self):
        return self._cfg.get('YumRepository', 'yum_repo_addr')


def is_comment(line):
    if line.strip().startswith('#'):
        return True
    elif line.strip() == '':
        return True
    else:
        return False


def only_contain_addr(host_pair):
    if isinstance(host_pair, list):
        if len(host_pair) == 1:
            return True
        else:
            return False
    else:
        print("{} is not a list".format(host_pair))


def only_contain_username(host_pair):
    if isinstance(host_pair, list):
        if len(host_pair) == 3 and host_pair[1].strip() != '' and host_pair[2].strip() == '':
            return True
        else:
            return False
    else:
        print("{} is not a list".format(host_pair))


def only_contain_password(host_pair):
    if isinstance(host_pair, list):
        if (len(host_pair) == 3 and host_pair[1].strip() == '' and host_pair[2].strip != ''):
            return True
        else:
            return False
    else:
        print("{} is not a list".format(host_pair))


def contain_both_username_password(host_pair):
    if isinstance(host_pair, list):
        if len(host_pair) == 3 and host_pair[1] != '' and host_pair[2] != '':
            return True
        else:
            return False
    else:
        print("{} is not a list".format(host_pair))


if __name__ == '__main__':
    test = SingletonObject()
    test2 = SingletonObject()
    test3 = object()
    test4 = object()
    test5 = SingletonBaseClass()
    test6 = SingletonBaseClass()
    print id(test)
    print id(test2)
    print id(test3)
    print id(test4)
    print id(test5)
    print id(test6)
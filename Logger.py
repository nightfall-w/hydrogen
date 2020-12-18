# -*- coding: utf-8 -*-
import logging
import os
import sys

# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger("AppName")

# 指定logger输出格式
formatter = logging.Formatter(
    '%(asctime)s - ProcessID:%(process)d - ThreadID:%(thread)d - ThreadName:%(threadName)s - %(filename)s - Func:%(funcName)s - len[%(lineno)d] : %(levelname)s  %(message)s')

# 文件日志
current_path = os.path.abspath(".")
if sys.argv[0] == 'pytest':
    try:
        current_path = os.path.abspath(sys.argv[1].split('.')[0])
    except IndexError:
        current_path = os.path.abspath(sys.argv[0].split('.')[0])
file_handler = logging.FileHandler(os.path.join(current_path, "all.log"), encoding='utf-8')
file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.DEBUG)

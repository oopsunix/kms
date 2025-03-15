#!/usr/bin/python3 -u

# This replaces the old start.sh and ensures all arguments are bound correctly from the environment variables...
import logging
import os
import subprocess
import sys
import time

# 定义 Python3 解释器的路径
PYTHON3 = '/usr/bin/python3'

# 定义命令行参数与环境变量的映射关系
argumentVariableMapping = {
  '-l': 'LCID',                   # 语言代码
  '-c': 'CLIENT_COUNT',           # 客户端数量
  '-a': 'ACTIVATION_INTERVAL',    # 激活间隔
  '-r': 'RENEWAL_INTERVAL',       # 续订间隔
  '-w': 'HWID',                   # 硬件ID
  '-V': 'LOGLEVEL',               # 日志级别
  '-F': 'LOGFILE',                # 日志文件路径
  '-S': 'LOGSIZE',                # 日志文件大小
  '-e': 'EPID'                    # EPID
}

# 定义数据库文件的路径
db_path = os.path.join(os.sep, 'app', 'db', 'kms.db')
log_file = os.environ.get('LOGFILE', 'STDOUT')   # 获取日志文件路径，默认为 STDOUT（标准输出）
listen_ip = os.environ.get('IP', '::').split()   # 获取监听的 IP 地址，默认为 '::'（IPv6 的任意地址），并将其拆分为列表
listen_port = os.environ.get('PORT', '1688')     # 获取监听的端口号，默认为 '1688'
want_webui = os.environ.get('WEBUI', '0') == '1' # 获取是否启用 WebUI 的配置，默认为 '0'（不启用），如果为 '1' 则启用

def start_kms(logger):
   # 如果启用了 WebUI 并且数据库路径的父目录不存在，则创建该目录
  if want_webui and not os.path.exists(os.path.dirname(db_path)):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

  # 构建启动 KMS 服务器的命令
  command = [PYTHON3, '-u', 'pykms_Server.py', listen_ip[0], listen_port]
  # 遍历参数映射表，将环境变量中的值添加到命令中
  for (arg, env) in argumentVariableMapping.items():
    if env in os.environ and os.environ.get(env) != '':
      command.append(arg)
      command.append(os.environ.get(env))

  # 如果启用了 WebUI，则添加数据库路径参数
  if want_webui:
    command.append('-s')
    command.append(db_path)

  # 如果有多个 IP 地址，则添加连接参数
  if len(listen_ip) > 1:
    command.append("connect")
    for i in range(1, len(listen_ip)):
      command.append("-n")
      command.append(listen_ip[i] + "," + listen_port)

    # 如果配置了双栈模式，则添加双栈参数
    if dual := os.environ.get('DUALSTACK'):
      command.append("-d")
      command.append(dual)

  logger.debug("server_cmd: %s" % (" ".join(str(x) for x in command).strip()))

  pykms_process = subprocess.Popen(command)
  pykms_webui_process = None

  try:
    if want_webui:
      time.sleep(2) # Wait for the server to start up
      pykms_webui_env = os.environ.copy()
      pykms_webui_env['PYKMS_SQLITE_DB_PATH'] = db_path
      pykms_webui_env['PORT'] = '8080'
      pykms_webui_env['PYKMS_LICENSE_PATH'] = '/LICENSE'
      pykms_webui_env['PYKMS_VERSION_PATH'] = '/VERSION'
      pykms_webui_process = subprocess.Popen(['gunicorn', '--log-level', os.environ.get('LOGLEVEL'), 'pykms_WebUI:app'], env=pykms_webui_env)
  except Exception as e:
    logger.error("Failed to start webui (ignoring and continuing anyways): %s" % e)

  try:
    pykms_process.wait()
  except Exception:
    # In case of any error - just shut down
    pass
  except KeyboardInterrupt:
    pass

  if pykms_webui_process:
    pykms_webui_process.terminate()
  pykms_process.terminate()


# Main
if __name__ == "__main__":
  log_level_bootstrap = log_level = os.environ.get('LOGLEVEL', 'INFO')
  if log_level_bootstrap == "MININFO":
    log_level_bootstrap = "INFO"

  # 配置日志记录器
  loggersrv = logging.getLogger('start.py')
  loggersrv.setLevel(log_level_bootstrap)
  streamhandler = logging.StreamHandler(sys.stdout)
  streamhandler.setLevel(log_level_bootstrap)
  formatter = logging.Formatter(fmt='\x1b[94m%(asctime)s %(levelname)-8s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S')
  streamhandler.setFormatter(formatter)
  loggersrv.addHandler(streamhandler)

  # 记录当前用户的 ID
  loggersrv.debug("user id: %s" % os.getuid())

  start_kms(loggersrv)

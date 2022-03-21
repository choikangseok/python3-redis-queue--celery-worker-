# python3-redis-queue-celery-worker
Asynchronous task queue/job queue


# Ubuntu 20.04 서버 + Python3.8 환경

```
$ sudo apt update -y
$ sudo apt upgrade -y

$ sudo apt-get install python3.8 -y
$ sudo apt-get install python3-pip -y

$ alias python=python3.8
$ alias pip=pip3
$ sudo update-alternatives --install /usr/bin/python3 python /usr/bin/python3.8 1


$ sudo apt install python-celery-common -y
$ sudo apt-get install redis-server -y
```

# celery.conf 설정
- /home/user/project/ 경로에 프로젝트가 있다는 설정으로 가정
- user, project, group 프로젝트에 맞게 설정
 

```
[celery.conf]
  
# Names of nodes to start
CELERYD_NODES="w1"

# Absolute or relative path to 'celery' command
#CELERY_BIN="/home/user/.local/bin/celery"
CELERY_BIN="/usr/bin/celery"

# App instance to use
CELERY_APP="tasks"

# Where to chdir at start.
CELERYD_CHDIR="/home/user/project/"

#CELERYD_TASK_TIME_LIMIT=30
# Extra command-line arguments to the worker
CELERYD_OPTS="--time-limit=500 --concurrency=60"

CELERYD_MAX_TASKS_PER_CHILD = 10

# Set logging level to DEBUG
CELERYD_LOG_LEVEL="INFO"

# %n : will be replaced with the first part of the nodename.
# %I : current child process index
CELERYD_LOG_FILE="./_log/%n%I.log"
CELERYD_PID_FILE="./_proc/%n.pid"

# Worker should run as an unprivileged user.
# You need to create this user manually (or you can choose
# a user/group combination that already exists
CELERYD_USER= user
CELERYD_GROUP= group

# If enabled pid and log directories will be created if missing,
# and owned by the userid/group configured.
CELERY_CREATE_DIRS=1          

```
celery service 설정
```
sudo vi /etc/systemd/system/celery.service
```
```
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=user
Group=group
EnvironmentFile=/home/user/project/celery.conf
WorkingDirectory=/home/user/project/

ExecStart=/bin/sh -c '${CELERY_BIN} multi start ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait ${CELERYD_NODES} \
  --pidfile=${CELERYD_PID_FILE}'
ExecReload=/bin/sh -c '${CELERY_BIN} multi restart ${CELERYD_NODES} \
  -A ${CELERY_APP} --pidfile=${CELERYD_PID_FILE} \
  --logfile=${CELERYD_LOG_FILE} --loglevel=${CELERYD_LOG_LEVEL} ${CELERYD_OPTS}'
StandardError=syslog
Restart=on-failure
LimitNOFILE=80000

[Install]
WantedBy=multi-user.target
```
  
테스트
```
sudo systemctl enable celery
sudo systemctl daemon-reload
sudo systemctl start celery
sudo systemctl stop celery
```


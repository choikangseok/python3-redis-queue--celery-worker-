# Python3-Redis-queue-Celery-worker-MongoDB
 Asynchronous Process using Python3 (Redis + Celery + MongoDB)
### 구성정보

- OS server : Ubuntu(20.04)
- Language : Python3.8
- Database : MongoDB + MongoExpress (Docker-compose)


## Ubuntu 20.04 server +  Python3.8 구성
```
$ sudo apt update -y
$ sudo apt upgrade -y

$ sudo apt-get install python3.8 -y
$ sudo apt-get install python3-pip -y


$ alias python=python3.8
$ alias pip=pip3
$ sudo update-alternatives --install /usr/bin/python3 python /usr/bin/python3.8 1


$ pip install celery==4.4.6
$ pip install redis==3.5.3
$ pip install bson
$ sudo apt install python-celery-common -y
$ sudo apt-get install redis-server -y
```
## Celery 구성

#### celery.conf
- /home/user/project/ : project PATH
- Modify user, project, group 
- CELERYD_OPTS="--time-limit=500 --concurrency=60" celery worker 수(60), time-limit(500초)

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
#### systemd(systemctl) celery.service 설정
- EnvironmentFile = celery.conf Path 
- WorkingDirectory = Project Path
- ExecStart : celery start
- ExecStop : celery stop
- ExecReload : celery reload
```
$ sudo vi /etc/systemd/system/celery.service
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
  
#### celery 실행
```
$ sudo systemctl enable celery # 서버 부팅시 자동 실행 disable : 자동 실행 X
$ sudo systemctl daemon-reload # 편집한 설정파일 반영
$ sudo systemctl start celery 
$ sudo systemctl stop celery
```

## MongoDB (Docker)

#### .env (mongodb environment)
```
## Mongodb
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password
MONGO_INITDB_DATABASE=my_database

```


#### .env_ex (mongo-express environment)
https://github.com/mongo-express/mongo-express
```
Name                              | Default         | Description
----------------------------------|-----------------|------------
`ME_CONFIG_MONGODB_URL`           | `mongodb://admin:pass@localhost:27017/db?ssl=false`
`ME_CONFIG_MONGODB_ENABLE_ADMIN`  | `false`         | Enable administrator access. Send strings: `"true"` or `"false"`.
`ME_CONFIG_MONGODB_AUTH_DATABASE` | `db`            | Database name (only needed if `ENABLE_ADMIN` is `"false"`).
`ME_CONFIG_MONGODB_AUTH_USERNAME` | `admin`         | Database username (only needed if `ENABLE_ADMIN` is `"false"`).
`ME_CONFIG_MONGODB_AUTH_PASSWORD` | `pass`          | Database password (only needed if `ENABLE_ADMIN` is `"false"`).
`ME_CONFIG_SITE_BASEURL`          | `/`             | Set the express baseUrl to ease mounting at a subdirectory. Remember to include a leading and trailing slash.
`ME_CONFIG_SITE_COOKIESECRET`     | `cookiesecret`  | String used by [cookie-parser middleware](https://www.npmjs.com/package/cookie-parser) to sign cookies.
`ME_CONFIG_SITE_SESSIONSECRET`    | `sessionsecret` | String used to sign the session ID cookie by [express-session middleware](https://www.npmjs.com/package/express-session).
`ME_CONFIG_BASICAUTH_USERNAME`    | ``              | mongo-express web login name. Sending an empty string will disable basic authentication.
`ME_CONFIG_BASICAUTH_PASSWORD`    | ``              | mongo-express web login password.
`ME_CONFIG_REQUEST_SIZE`          | `100kb`         | Used to configure maximum mongo update payload size. CRUD operations above this size will fail due to restrictions in [body-parser](https://www.npmjs.com/package/body-parser).
`ME_CONFIG_OPTIONS_EDITORTHEME`   | `rubyblue`      | Web editor color theme, [more here](http://codemirror.net/demo/theme.html).
`ME_CONFIG_OPTIONS_READONLY`      | `false`         | if readOnly is true, components of writing are not visible.
`ME_CONFIG_OPTIONS_NO_DELETE`      | `false`         | if noDelete is true, components of deleting are not visible.
`ME_CONFIG_SITE_SSL_ENABLED`      | `false`         | Enable SSL.
`ME_CONFIG_MONGODB_SSLVALIDATE`   | `true`          | Validate mongod server certificate against CA
`ME_CONFIG_SITE_SSL_CRT_PATH`     | ` `             | SSL certificate file.
`ME_CONFIG_SITE_SSL_KEY_PATH`     | ` `             | SSL key file.
`ME_CONFIG_SITE_GRIDFS_ENABLED`   | `false`         | Enable gridFS to manage uploaded files.
`VCAP_APP_HOST`                   | `localhost`     | address that mongo-express will listen on for incoming connections.
`VCAP_APP_PORT`                   | `8081`          | port that mongo-express will run on.
`ME_CONFIG_MONGODB_CA_FILE`       | ``              | CA certificate File
`ME_CONFIG_BASICAUTH_USERNAME_FILE`     | ``        | File version of ME_CONFIG_BASICAUTH_USERNAME
`ME_CONFIG_BASICAUTH_PASSWORD_FILE`     | ``        | File version of ME_CONFIG_BASICAUTH_PASSWORD
`ME_CONFIG_MONGODB_ADMINUSERNAME_FILE`  | ``        | File version of ME_CONFIG_MONGODB_ADMINUSERNAME
`ME_CONFIG_MONGODB_ADMINPASSWORD_FILE`  | ``        | File version of ME_CONFIG_MONGODB_ADMINPASSWORD
`ME_CONFIG_MONGODB_AUTH_USERNAME_FILE`  | ``        | File version of ME_CONFIG_MONGODB_AUTH_USERNAME
`ME_CONFIG_MONGODB_AUTH_PASSWORD_FILE`  | ``        | File version of ME_CONFIG_MONGODB_AUTH_PASSWORD
```
```
## Mongo Express Env Sample
ME_CONFIG_MONGODB_PORT=27017
ME_CONFIG_MONGODB_ADMINUSERNAME=admin
ME_CONFIG_MONGODB_ADMINPASSWORD=password
ME_CONFIG_MONGODB_ENABLE_ADMIN=true
ME_CONFIG_MONGODB_SERVER=mongodb
ME_CONFIG_BASICAUTH_USERNAME=web_login_id
ME_CONFIG_BASICAUTH_PASSWORD=web_login_pass
```

#### docker-compose.yml

```
version: '3'
services:
  mongodb:
    image: mongo
    ports:
      - "${MONGO_PORT}:27017"
    volumes:
      - ./data/db:/data/db
      - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js
    container_name: "docker-mongodb"
    env_file:
      - .env
  mongo-express:
    image: mongo-express:0.54.0
    ports:
      - 8081:8081
    # depends_on:
    #   - mongodb
    container_name: "docker-mongo-express"
    env_file:
      - .env_ex
    restart: always
```


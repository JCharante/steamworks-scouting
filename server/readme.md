achilles server
===============

The achilles app uploads matches to this server, and this server allows you to go on here and download a csv file with the match data.

## Running on Docker

### Environmental Variables.

#### db_address

The address of the mysql server in the format of:

`db_address=mysql+pymysql://<username>:<password>@<host>/<database_name>?charset=utf8mb4`

Example:

```bash
$ export db_address=mysql+pymysql://root:root@localhost/steamworks_scouting?charset=utf8mb4
```

#### serverPassword

The password for the server (will also have to be manually set in client)

```bash
$ export serverPassword=yee
```

### Running

Then to run on docker
```bash
$ docker run -d --restart=always -e "db_address=$db_address" -e "serverPassword=$serverPassword" -p 80:80 --name achilles-api-server jcharante/achilles-server
```

Deploying to hyper.sh
```bash
$ hyper run -d --restart=always -e "db_address=$db_address" -e "serverPassword=$serverPassword" -p 80:80 --size=s4 --name achilles-api-server jcharante/achilles-server
```

achilles server
===============

The achilles app uploads matches to this server, and this server allows you to go on here and download a csv file with the match data.

## Running on Docker

First setup your environmental variables.

The address of the mysql server in the format of:

`db_address=mysql+pymysql://<username>:<password>@<host>/<database_name>`

Example:

```bash
$ export db_address=mysql+pymysql://achilles:achilles@localhost/achilles
```

Then to run on docker
```bash
$ docker run -d --restart=always -e "db_address=$db_address" -p 80:80 --name achilles-api-server jcharante/achilles-server
```

Deploying to hyper.sh
```bash
$ hyper run -d --restart=always -e "db_address=$db_address" -p 80:80 --size=s4 --name achilles-api-server jcharante/achilles-server
```

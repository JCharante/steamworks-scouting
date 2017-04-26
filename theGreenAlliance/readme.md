The Green Alliance
==================

An invite only website to bet\* on frc matches.

\* with virtual tokens that have no real world value other than bragging rights.


# 1. Setup

## 1.1 Ubuntu 17.04 requirements

```bash
$ sudo apt install virtualenv python3.6
```

## 1.2 Setting up virtualenv

```bash
$ virtualenv -p python3.6 .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

## 1.3 Environmental Variables

```bash
$ export dba=mysql+pymysql://tga:tga@localhost/tga?charset=utf8mb4  # Database address
$ export tba=JCharante:github.com/jcharante/achilles:1.0  # Your The Blue Alliance Agent String for the v2 api
```

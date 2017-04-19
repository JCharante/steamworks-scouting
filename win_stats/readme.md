Setup
=====

Assuming you're running Ubuntu 17.04

#### Dependencies

```bash
sudo apt install python3.6 virtualenv mysql-server
```

#### Setup Project

Setting up mysql database to use (modify settings.json w/ address)

Example:

```bash
$ mysql -u root -p
Enter Password: root
mysql> CREATE USER 'achilles' IDENTIFIED BY 'achilles';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'achilles';
mysql> FLUSH PRIVILEGES;
mysql> create database achilles;
mysql> quit;
```

Getting python dependencies

```bash
git clone git@github.com:JCharante/achilles.git
cd achilles/win_stats
virtualenv -p python3.6 .venv
source .venv
pip install -r requirements.txt
```

Running
=======

### Rank Fetcher

#### Description

This calculates the 2016 statistical probabilities* of winning an event at a certain rank.

\* This is flawed, because events vary wildly in their number of participating teams. For example take Cleveland's Team (120) who ranked 62nd place in the Carver Division.

#### Results

[Available Here](exports/2016-chances-of-winning-at-a-ranking.csv)


#### Running for yourself

```bash
python rank_fetcher.py
```

The results will be available at `exports/2016-chances-of-winning-at-a-ranking.csv`

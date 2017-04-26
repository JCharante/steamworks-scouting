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
$ mysql -u root -proot
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

### TrueSkill Network Graph

#### Description

A network node graph, where the size of the node is based on the trueskill score, the color is based off of the region, and the edges are based off of matches played between notes/teams.

#### Results

[A very resource intensive graph using data for all teams from 2017-04-20-05:23:10.747165](connections/index.html)

### TrueSkill Ratings for 2017

#### Description

This uses the TrueSkill library to see how teams rank against each other if FRC were an xbox live game (TrueSkill's main purpose).

#### Results

[Available Here](exports/world-trueskill-rankings-2017-04-25-03:56:34.107261.csv)

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

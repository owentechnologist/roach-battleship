# roach-battleship
This repo is a reworking and expansion on the otVectorBattleship repo.  This version uses CockroachDB as the vectorDB


## Python-preparation Steps for running the program on your machine:


1. Create a virtual environment:

```
python3 -m venv rbenv
```

2. Activate it:  [This step is repeated anytime you want this venv back]

```
source rbenv/bin/activate
```

On windows you would do:

```
rbenv\Scripts\activate
```
If no permission in Windows
 The Fix (Temporary, Safe, Local):
In PowerShell as Administrator, run:
```

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
Then confirm with Y when prompted.



## Python will utilize this requirements.txt in the project:

```
psycopg[binary]

```

3. Install the libraries: [only necesary to do this one time per environment]

```
pip3 install -r requirements.txt
```


## install and Initialize a cockroach database to act as a vectorDB:


** download cockroachdb binary (you can use a single instance for testing) 

for mac you do:
```
brew install cockroachdb/tap/cockroach
```

You can then check for location/existence of cockroachDB:
```
which cockroach
```

<em> See full instructions here:  https://www.cockroachlabs.com/docs/v25.2/install-cockroachdb-mac.html 

(There are options there for Linux and Windows as well)
</em>

## You can start a single node instance of cockroachDB in the following way:

to keep things as simple as possible, start an instance requiring no TLS (Transport Layer Security):

```
cockroach start-single-node --insecure --accept-sql-without-tls --background
```

<em>See full instructions here:  https://www.cockroachlabs.com/docs/stable/cockroach-start-single-node  </em>

By default:

This local instance of cockroachDB will run listening on port 26257 (for SQL and commandline connections)

This local instance will also listen on port 8080 with its web-browser-serving dbconsole UI 

## From a separate shell you can connect to this instance, create a database and the tables needed to begin:

to execute all the SQL commands needed plus some test queries from the root of this project do:
```
cockroach sql --insecure -f crdb_setup.sql
```

If you wish to execute other sql -- The following command connects using the provided SQL CLI:

```
cockroach sql --insecure
```

## Run a battle bot that repeatedly generates ship vectors and then tests for their overlap in the vector space do:

```
python3 battle_bot.py
```

## NB: the battle_bot runs until it hits a ship with an exact match on type, location, and quadrant

example:
```
📡 Attempting to place a 'submarine' in quadrant 3 at anchor (2, 3)
ORIGINAL anchorX = 2  anchorY = 3
CORRECTED anchorX = 2  anchorY = 3 anchor_point = 22
 Target generated submarine has anchor_point of 22
| *  *  *  *  *  *  *  *  *  *  |
| *  *  *  *  *  *  *  *  *  *  |
| *  .  *  *  *  *  *  *  *  *  |
| *  .  *  *  *  *  *  *  *  *  |
| *  .  *  *  *  *  *  *  *  *  |
| *  .  *  *  *  *  *  *  *  *  |
| *  .  *  *  *  *  *  *  *  *  |
| *  .  *  *  *  *  *  *  *  *  |
| *  *  *  *  *  *  *  *  *  *  |
| *  *  *  *  *  *  *  *  *  *  |



[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
✅ No collisions — placement is clear.

📡 Attempting to place a 'submarine' in quadrant 1 at anchor (7, 3)
ORIGINAL anchorX = 7  anchorY = 3
CORRECTED anchorX = 7  anchorY = 3 anchor_point = 27
 Target generated submarine has anchor_point of 27
| *  *  *  *  *  *  *  *  *  *  |
| *  *  *  *  *  *  *  *  *  *  |
| *  *  *  *  *  *  .  *  *  *  |
| *  *  *  *  *  *  .  *  *  *  |
| *  *  *  *  *  *  .  *  *  *  |
| *  *  *  *  *  *  .  *  *  *  |
| *  *  *  *  *  *  .  *  *  *  |
| *  *  *  *  *  *  .  *  *  *  |
| *  *  *  *  *  *  *  *  *  *  |
| *  *  *  *  *  *  *  *  *  *  |



[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
🚨 Potential collision detected:
  - Class: submarine           , Match: 100.0%, Anchor: 27


PERFECT HIT -- EXITING PROGRAM
```

## to view the activity in the database you can open the dbconsole in a browser:
```
https://localhost:8080
````


#### random vector details:
-- NB there are options in terms of the search algorithm chosen:

-- L2 (Euclidean)  [default]
SELECT ... ORDER BY vector <-> '[query_vector]' LIMIT 5

-- Cosine
SELECT ... ORDER BY vector <=> '[query_vector]' LIMIT 5

-- Inner Product
SELECT ... ORDER BY vector <#> '[query_vector]' LIMIT 5

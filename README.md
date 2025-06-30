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

4. To run a battle bot that repeatedly generates ship vectors and then tests for their overlap in the vector space do:

```
python battle_bot.py
```

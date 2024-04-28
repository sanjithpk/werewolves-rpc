# Group 22, CSE 536 Final Project

Sanjith Kalveerappanavar, Pawan Kondebai, Chandan Nooli

To install

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

To compile protobuff

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. werewolf.proto
```

To start the game, run server and multiple clients

To run server

```
python server.py
```

To run client

```
python client.py [username] [password]
Ex: python client.py user1 pass1
```

## Screenshots from the Game

1. Connection

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/connection.png)

2. Round 1 Night

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/Round-1-Night.png)

3. Round 1 Day

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/Round-1-Day.png)

4. Round 2

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/Round-2.png)

5. Result

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/Result.png)

**Note**

- Updated changes are in **master** branch
- Github link: https://github.com/sanjithpk/werewolves-rpc/tree/dev
- Video DEMO : https://youtu.be/wAynHZktPvk

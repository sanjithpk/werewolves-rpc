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
python client.py user1 pass1
```

**Note**

- Updated changes are in **dev** branch
- Github link: https://github.com/sanjithpk/werewolves-rpc/tree/dev
- Video DEMO : https://youtu.be/wAynHZktPvk

```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. werewolf.proto
```

```
pip install -r requirements.txt
```

```
python3 -m venv env

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
- Updated changes in **dev** branch
- Github link: https://github.com/sanjithpk/werewolves-rpc/tree/dev
- Video DEMO : https://youtu.be/wAynHZktPvk

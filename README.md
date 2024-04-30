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

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/1_Connection.png)

2. Round 1 Night - Werewolves Discussion

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/2_Round_1_Night_Werewolves_Discussion.png)

3. Round 1 Night - Werewolves Vote

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/3_round1_night_werewoves_vote.png)

4. Villager killed

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/4_villager_killed.png)

5. Round 1 Day - All townspeople Discussion

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/5_Round1_day_discussion.png)

6. Round 1 Day - All townspeople Vote

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/6_round1_day_vote.png)

7. Round 2 begins...

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/7_round2_night.png)

8. Round 2 Voting ...

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/8_round2_vote.png)

9. Finally Werewolves win in this game 🐺

![Connection](https://github.com/sanjithpk/werewolves-rpc/blob/master/screenshots/9_final.png)


**Note**

- Updated changes are in **master** branch
- Github link: https://github.com/sanjithpk/werewolves-rpc
- Video DEMO : https://youtu.be/EYTvpqYU8-Q

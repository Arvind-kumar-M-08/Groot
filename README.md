# guardAIns

---

### Setup

1. Download the Repository to your local machine <br>
2. Setup the server by running [setup.sh](./setup.sh) folder with this command below <br>
   `bash setup.sh`
3. Source the created venv by running `source venv/bin/activate`. Note this must be done everytime a new terminal is opened <br>

### Running the Server

1. Run the server by running this command (_Run the command where [run.sh](./run.sh) is
   located_) <br>
   `python main.py 0.0.0.0 8000`

### Testing

1. We have provided [client.py](./client.py) which can be used for testing. [client.py](./client.py) is a random bot.
2. Testing credentials are
   1. Room id: `gameRoom`
   2. For Player 1:  `player_id`: `player1` and `password`: `player1`
   3. For Player 2:  `player_id`: `player2` and `password`: `player2`
3. Start the Environment by mentioned the command mentioned above
4. Run the client.py by running this command <br>
   `python client.py 1` for running it as Player 1 and <br>
   `python client.py 2` for running it as Player 2
5. You can see the output in the terminal
6. After the game is over, you need to restart the environment to start a new again. Use Ctrl+C to stop the environment program.
   

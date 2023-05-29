import phoenix
from time import sleep
import json
import time
import threading
import getports
import classes as cl
import ctypes
import random

class Player:
    def __init__(self):
        self.name = ""
        self.port = ""
        self.api = 0
        self.devil_spawned = False
        self.devil_id = "unknown"
        self.deaths = 0

def initializeApi(Player):
    Player.port = getports.returnCorrectPort(Player.name)
    Player.api = phoenix.Api(Player.port)

def revive(Player):
    api = Player.api
    
    if Player.devil_spawned:
        min = cl.user_settings.min_delay
        max = cl.user_settings.max_delay

        random_value = float(random.randint(int(min)*1000,int(max)*1000)/1000)
        print(str(time.strftime('[%H:%M:%S]'))+" "+Player.name+ " died, he will respawn in: "+str(random_value)+" seconds.")
        random_value_decimal = random_value-int(random_value)
        for i in range(int(random_value)):
            time.sleep(1)
            if not Player.devil_spawned:
                break
        time.sleep(random_value_decimal)
        api.send_packet("#revival^8")
    else:
        random_value = float(random.randint(1*1000,2*1000)/1000)
        print(str(time.strftime('[%H:%M:%S]'))+" "+Player.name+ " died, he will respawn in: "+str(random_value)+" seconds.")
        api.send_packet("#revival^8")
    

def packetLogger(Player):
    # Logs all the packets that are sent/received from the client
    while Player.api.working():
        if not Player.api.empty():
            msg = Player.api.get_message()
            json_msg = json.loads(msg)

            if str(json_msg["type"]) == "0" or str(json_msg["type"]) == "1":
                packet = str(str(json_msg["type"]) + " " + json_msg["packet"])
                if packet.startswith("1 dlgi #revival"):
                    Player.deaths += 1
                    t = threading.Thread(target=revive, args=(Player,))
                    t.start()
                if packet.startswith("1 in 3 443"):
                    splitPacket = packet.split()
                    Player.devil_spawned = True
                    Player.devil_id = splitPacket[4]
                    if Player.name == players[0].name:
                        print(str(time.strftime('[%H:%M:%S]'))+" ""Devil spawned")
                if packet.startswith("1 out 3") and Player.devil_id in packet:
                    Player.devil_spawned = False
                    if Player.name == players[0].name:
                        print(str(time.strftime('[%H:%M:%S]'))+" ""Devil despawned")
                    

        else:
            sleep(0.01)

    Player.api.close()



if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW("auto-revive lod bot by stradiveri#9377")
    players = []
    players_names = []

    if cl.user_settings.characters != "":
        splitCharactes=cl.user_settings.characters.split(",")

        for name in splitCharactes:
            player = Player()
            player.name = name
            initializeApi(player)
            t = threading.Thread(target=packetLogger, args=(player,))
            t.start()
            players.append(player)
    else:
        print("Your characters: ")
        ports_and_names_unsorted = getports.returnAllPorts()

        # Sort the array based on the first element of each sub-array
        ports_and_names = sorted(ports_and_names_unsorted, key=lambda x: x[0])

        for i in range(len(ports_and_names)):
            ports_and_names[i].append(i+1)

        for i in range(len(ports_and_names)):
            print(str(ports_and_names[i][2])+") "+str(ports_and_names[i][0]))

        print("")
        print("Leave empty and press Enter, to stop")
        while True:
            print("Type name(or index) of your character: ", end="")
            index = input()
            if str(index)=="":
                    break
                
            for element in ports_and_names:
                if str(index) == str(element[0]) or index == str(element[2]):
                    index = str(element[0])
                    if index in players_names:
                        print(index+" already in the list.")
                    else:
                        player = Player()
                        player.name = index
                        initializeApi(player)
                        t = threading.Thread(target=packetLogger, args=(player,))
                        t.start()
                        players_names.append(index)
                        players.append(player)
                else:
                    pass
        print("")
    print("Lod auto-revive sucesfully started at: "+str(time.strftime('%H:%M:%S')))
    print("selected characters: ", end="")
    for i in range(len(players)-1):
        print(players[i].name, end=", ")
    print(players[-1].name)
    print("")
    while True:
        user_input = input()
        if user_input == "":
            print("")
            print("Character deaths: ")
            for i in range(len(players)):
                print(players[i].name+" deaths: "+str(players[i].deaths))
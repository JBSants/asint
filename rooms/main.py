from flask import Flask
from flask import request
from flask import abort
from flask import render_template
from flask import jsonify
import json
import requests
import roomDB

app = Flask(__name__)
db = roomDB.RoomDB("IST Rooms")

def get_building(node, URI = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"):
    """
    Gets the building of the room by recursively accessing parents info 
    """
    if "error" in node.keys():
        if node["error"] == "id not found":
            return None
    
    elif node["parentSpace"]["type"] == 'BUILDING':
        return node["parentSpace"]["name"]

    else:
        id_parent = node["parentSpace"]["id"]
        URI += id_parent
        r = requests.get(URI)
        node = r.json()
        building = get_building(node)

    return building

def notFound():
    resp = jsonify(error = "Room, not found.")
    resp.status_code = 404
    return resp

@app.route("/Rooms/", methods = ["GET"])
def listRooms():
    roomsDict = list(map(lambda r: r.__dict__, db.listAllRooms()))
    resp = jsonify(roomsDict)
    resp.status_code = 200
    
    return resp

@app.route('/getRoom/<identifier>', methods=['GET'])
def getRoom(identifier, URI = "https://fenix.tecnico.ulisboa.pt/api/fenix/v1/spaces/"):
    r_id = int(identifier)

    try:
        room = db.showRoom(r_id).__dict__
    
    except AttributeError:
        URI += str(identifier)
        r = requests.get(URI)
        room = r.json()
        
        building = get_building(room)

        if building is not None: #TODO: change criterion by checking error previously 
            
            if "events" not in room.keys(): #TODO: is it needed?
                timetable = None

            room = db.createRoom(room["name"],
                                 room["id"],
                                 room["topLevelSpace"]["name"],
                                 building,
                                 timetable)

            resp = jsonify(room.__dict__)
            resp.statusCode = 201
        
        else:
            return notFound()

    else:
        resp = jsonify(room)
        resp.statusCode = 200

    return resp


if __name__ == '__main__':
    app.run(port=8081)
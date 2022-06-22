from dataclasses import dataclass
from ntpath import join
from posixpath import dirname
import uuid
import dotenv
from os import path
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


api = Flask(__name__)


@api.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the API', 'status': '200'})

#READ ALL USERS - [GET] /users
@api.route('/users', methods=['GET'])
def getUsers():

    if path.isfile('users.json'):
        with open('users.json') as f:
            users = json.load(f)
        if users:
            return jsonify({'users': users, 'status': '200'})
        else:
            return jsonify({'message': 'No users found', 'status': '404'})
    else:
        return jsonify({'message': 'User File not found', 'status': '404'})


#READ USER - [GET] /user/<id>
@api.route('/user/<id>', methods=['GET'])
def getUser(id):
    if path.isfile('users.json'):
        with open('users.json') as f:
            users = json.load(f)
        if users:
            for user in users:
                if user['id'] == id:
                    return jsonify({'user': user, 'status': '200'})
                else:
                    return jsonify({'message': 'User not found', 'status': '404'})    
        else:
            return jsonify({'message': 'No users found', 'status': '404'})
    else:
        return jsonify({'message': 'User File not found', 'status': '404'})


# CREATE USER - [PUT] /user - {"name":"dincer","surname":"degre","email":"dincerdegre@gmail.com"}
@api.route('/user', methods=['PUT'])
def createUser():
    if path.isfile('users.json'):
        userData = request.get_json()
        i = uuid.uuid4().hex
        with open('users.json') as f:
            usersData = json.load(f)
        if not usersData:
            userData['id'] = i
            data = [userData]
            with open('users.json', 'w') as f:
                json.dump(data, f)
            return jsonify({'message': 'User created', 'status': '200'})
        else:   
            for user in usersData:
                if userData['email'] == user['email']:
                    return jsonify({'message': 'User already exists', 'status': '400'})
        userData['id'] = i
        data = usersData + [userData]
        with open('users.json', 'w') as f:
            json.dump(data, f)
            return jsonify({'message': 'User created', 'status': '200'})          
    else:
        return jsonify({'message': 'User File not found', 'status': '404'})

             
# CREATE OR UPDATE USER - [POST] /user - {"name":"dincer","surname":"degre","email":"dincerdegre@gmail.com"}
@api.route('/user', methods=['POST'])
def createOrUpdateUser():
    if path.isfile('users.json'):
        userInputData = request.get_json()
        i = uuid.uuid4().hex
        data = []
        with open('users.json') as f:
            usersFileData = json.load(f)
            if not usersFileData:
                userInputData['id'] = i
                data.append(userInputData)
                with open('users.json', 'w') as f:
                    json.dump(data, f)
                return jsonify({'message': 'User created', 'status': '200'})
            else:    
            
                index = 0
                fIndex = None
                for userData in usersFileData:
                    if userData['email'] == userInputData['email']:
                        fIndex = index           
                    index = index + 1   
            
                if fIndex != None:
                    userInputData['id'] = usersFileData[fIndex]['id']
                    usersFileData[fIndex] = userInputData
                    data = usersFileData
                    userMessage = "User updated"
                else:
                    data = usersFileData
                    userInputData['id'] = i
                    data.append(userInputData)
                    userMessage = "User created"
            
                with open('users.json', 'w') as f:
                    json.dump(data, f)  
                return jsonify({'message': userMessage, 'status': '200','data':data})  
    else:
        return jsonify({'message': 'User File not found', 'status': '404'})       
          


           
# DELETE - [DELETE] /user/<id>     
@api.route('/user/<id>', methods=['DELETE'])      
def deleteUser(id):     
    if path.isfile('users.json'):
        data = []
        deletedUser = {}
        with open('users.json') as f:
            usersFileData = json.load(f)
        if usersFileData:
            for user in usersFileData:
                if user['id'] == id:
                    deletedUser = user
                    continue
                else:
                    data.append(user)
            if (deletedUser):        
                with open('users.json', 'w') as f:
                    json.dump(data, f)  
                return jsonify({'message': 'User deleted', 'status': '200','data':deletedUser})  
            else:
                return jsonify({'message': 'No users found', 'status': '404'})        
        else:
            return jsonify({'message': 'No users found', 'status': '404'})
    else:
        return jsonify({'message': 'User File not found', 'status': '404'})

api.run(debug=True)



import socket
import os
import threading
import re
import json
from PIL import Image

# Create Socket (TCP) Connection
ServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
HOST = '127.0.0.1'
PORT = 1233
FORMAT = 'utf-8'

try:
    ServerSocket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))

ServerSocket.listen()


clients = []
users = []

# Function : For each client
special_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')


def checkSpecialChar(string):
    if (special_char.search(string)):
        return True
    return False


def check(username, password):
    if len(username) < 5:
        return False
    if re.findall('[A-Z]', username) or checkSpecialChar(username):
        return False
    if len(password) < 3:
        return False
    return True


def user_data_init(username):
    file = open("note.json")
    users_note = json.load(file)
    users_note[f"{username}"] = {
        "note": [],
        "file": [],
        "image": []
    }
    json_obj = json.dumps(users_note, indent=4)
    with open("note.json", "w") as outfile:
        outfile.write(json_obj)
    file.close()


def add_new_note(username, title, content, note_id):
    file = open("note.json")
    users_note = json.load(file)
    users_note[username]["note"].append(
        {"_id": note_id, "title": title, "content": content})
    json_obj = json.dumps(users_note, indent=4)
    with open("note.json", "w") as outfile:
        outfile.write(json_obj)
    file.close()


def add_new_image(username, image, imageID):
    file = open("note.json")
    users_image = json.load(file)
    users_image[username]["image"].append({"_id": imageID, "name": image})
    json_obj = json.dumps(users_image, indent=4)
    with open("note.json", "w") as outfile:
        outfile.write(json_obj)
    file.close()


def add_new_file(username, files, fileID):
    file = open("note.json")
    users_file = json.load(file)
    users_file[username]["file"].append({"_id": fileID, "name": files})
    json_obj = json.dumps(users_file, indent=4)
    with open("note.json", "w") as outfile:
        outfile.write(json_obj)
    file.close()


def del_note(username, note_index, type):
    input_file = open("note.json")
    users_note = json.load(input_file)
    #-------------------------------------------------#
    if type == "Text":
        for note in users_note[username]["note"]:
            if note["_id"] == note_index:
                users_note[username]["note"].remove(note)
                break
    elif type == "Image":
        for img in users_note[username]["image"]:
            if img["_id"] == note_index:
                os.remove(f"./user_data/{username}/{img['name']}")
                users_note[username]["image"].remove(img)
                break
    else:
        for file in users_note[username]["file"]:
            if file["_id"] == note_index:
                os.remove(f"./user_data/{username}/{file['name']}")
                users_note[username]["file"].remove(file)
                break
    #-------------------------------------------------#
    json_obj = json.dumps(users_note, indent=4)
    with open("note.json", "w") as outfile:
        outfile.write(json_obj)
    input_file.close()


def is_exist_note(username, title):
    file = open("note.json")
    users_note = json.load(file)
    #-------------------------------------------------#
    for user in users_note[username]["note"]:
        if user["title"] == title:
            return True
    return False
    #-------------------------------------------------#
    file.close()


def is_exist_image(username, image):
    file = open("note.json")
    users_image = json.load(file)

    for user in users_image[username]["image"]:
        if user["name"] == image:
            return True
    return False

    file.close()


def is_exist_file(username, files):
    file = open("note.json")
    users_file = json.load(file)

    for user in users_file[username]["image"]:
        if user["name"] == files:
            return True
    for user in users_file[username]["file"]:
        if user["name"] == files:
            return True
    return False

    file.close()


def user_folder_create(filename):
    isFile = os.path.isdir('./user_data')
    if isFile:
        path = f'./user_data/{filename}'
        os.makedirs(path)
    else:
        os.makedirs('./user_data')
        path = f'./user_data/{filename}'
        os.makedirs(path)


def load_user_note_data(username, client):
    file = open("note.json")
    user_note = json.load(file)
    user_note = user_note[username]
    client.send(str(user_note).encode(FORMAT))
    file.close()


def check_empty(filename):
    if os.stat(filename).st_size == 0:
        return True
    return False


if not os.path.exists('./user.json'):
    with open('./user.json', 'w'):
        pass

if not os.path.exists('./note.json'):
    with open('./note.json', 'w'):
        pass

if not os.path.exists("user_data"):
    os.mkdir('./user_data')


if check_empty("user.json"):
    file = open("user.json", "w")
    file.write("[]")
    file.close()
if check_empty("note.json"):
    file = open("note.json", "w")
    file.write("{}")
    file.close()


def handle(client):
    while True:
        try:
            user_data = client.recv(4100000).decode(FORMAT)
            user_data = eval(user_data)
            mode = user_data[0]
            # ------------------- Database ------------------------------ #
            if mode == "SIGN-IN":
                file = open("user.json")
                users_data = json.load(file)
                user_exist = False
                username = user_data[1]
                password = user_data[2]
                if check(username, password):
                    for user in users_data:
                        if user["username"] == username:
                            if user["password"] == password:
                                users.append([username, password])
                                json_obj = json.dumps(users_data, indent=4)
                                with open("user.json", "w") as fo:
                                    fo.write(json_obj)
                                client.send("Login successful!".encode(FORMAT))
                                load_user_note_data(username, client)
                            else:
                                client.send("Wrong password!".encode(FORMAT))
                            user_exist = True
                            break
                else:
                    client.send("Invalid username!".encode(FORMAT))
                if not user_exist:
                    client.send("User does not exist!".encode(FORMAT))
                file.close()
            elif mode == "SIGN-UP":
                file = open("user.json")
                users_data = json.load(file)
                #-------------------------------------------#
                user_exist = False
                username = user_data[1]
                password = user_data[2]
                confirm_pw = user_data[3]
                if check(username, password):
                    user_exist = False
                    for user in users_data:
                        if (user["username"] == username):
                            client.send("User is already exist".encode(FORMAT))
                            user_exist = True
                            break
                    if not(user_exist):
                        if confirm_pw == password:
                            user_info = {"username": username,
                                         "password": password}
                            # init new user's note
                            user_data_init(username)
                            # create user folder
                            user_folder_create(username)
                            users_data.append(user_info)
                            client.send("Register successfully".encode(FORMAT))
                        else:
                            client.send(
                                "Password is not matched".encode(FORMAT))
                else:
                    client.send("Invalid username or password".encode(FORMAT))
                #-------------------------------------------#
                json_obj = json.dumps(users_data, indent=4)
                with open("user.json", "w") as fo:
                    fo.write(json_obj)
                file.close()
            elif mode == "FORGOT-PW":
                file = open("user.json")
                users_data = json.load(file)
                user_exist = False
                username = user_data[1]
                password = user_data[2]
                confirm_pw = user_data[3]
                for user in users_data:
                    # find that user
                    if user["username"] == username:
                        user_exist = True
                        if check(username, password):
                            # check if the new pass is the same as the old one
                            if user["password"] == password:
                                client.send(
                                    "Please use the new one, this is your current password".encode(FORMAT))
                                break
                            # check if both confirm pw and pw are the same
                            elif password == confirm_pw:
                                client.send(
                                    "Update password successfully".encode(FORMAT))
                                user["password"] = password
                                break
                            else:
                                client.send(
                                    "Passwords are not matched".encode(FORMAT))
                                break
                        else:
                            client.send(
                                "Invalid username or password".encode(FORMAT))
                if not user_exist:
                    client.send("User does not exist!".encode(FORMAT))
                json_obj = json.dumps(users_data, indent=4)
                with open("user.json", "w") as fo:
                    fo.write(json_obj)
                file.close()
            elif mode == "NOTE":
                name = user_data[1]
                note_topic = user_data[2]
                note = user_data[3]
                note_id = user_data[4]
                if len(note_topic) > 0 and len(note) > 0:
                    note_exist = is_exist_note(name, note_topic)
                    if not note_exist:
                        client.send(
                            "Note successfully created!".encode(FORMAT))
                        add_new_note(name, note_topic, note, note_id)
                    else:
                        client.send(
                            "This title is already exist".encode(FORMAT))
                else:
                    client.send("Note Invalid!".encode(FORMAT))
            elif mode == "DEL-NOTE":
                name = user_data[1]
                note_index = user_data[2]
                type = user_data[3]
                del_note(name, note_index, type)
            elif mode == "DOWNLOAD":
                username = user_data[1]
                note_index = user_data[2]
                type = user_data[3]
                file = open("note.json")
                users_note = json.load(file)
                if type == "Image":
                    for user in users_note[username]["image"]:
                        if user["_id"] == note_index:
                            with open(f"./user_data/{username}/{user['name']}", 'rb') as f:
                                client.send(f.read())
                                f.close()
                            break
                elif type == "File":
                    for user in users_note[username]["file"]:
                        if user["_id"] == note_index:
                            with open(f"./user_data/{username}/{user['name']}", 'rb') as f:
                                client.send(f.read())
                                f.close()
                            break
                else:
                    for user in users_note[username]["note"]:
                        if user["_id"] == note_index:
                            client.send(
                                str([user["title"], user["content"]]).encode(FORMAT))
                            break
            elif mode == "IMAGE":
                name = user_data[1]
                image = user_data[2]
                IDimage = user_data[3]
                if len(image) > 0:
                    image_exist = is_exist_image(name, image)
                    if not image_exist:
                        client.send(
                            "Image successfully created!".encode(FORMAT))
                        add_new_image(name, image, IDimage)
                        with open(f'./user_data/{name}/' + image, 'wb') as f:
                            data = client.recv(41000000)
                            f.write(data)
                            f.close()
                    else:
                        client.send(
                            "This title is already exist".encode(FORMAT))
            elif mode == "VIEW":
                username = user_data[1]
                note_id = user_data[2]
                type = user_data[3]
                #view_note(name, ID_file, type)
                file = open("note.json")
                users_note = json.load(file)
                if type == "Image":
                    for user in users_note[username]["image"]:
                        # print(f'./user_data/{username}/' + user["name"])
                        if user["_id"] == note_id:
                            with open(f'./user_data/{username}/{user["name"]}', 'rb') as f:
                                client.send(f.read())
                                f.close()
                            break
                elif type == "File":
                    for user in users_note[username]["file"]:
                        if user["_id"] == note_id:
                            with open(f'./user_data/{username}/{user["name"]}', 'rb') as f:
                                client.send(f.read().encode(FORMAT))
                                f.close()
                            break
                elif type == "Text":
                    for user in users_note[username]["note"]:
                        if user["_id"] == note_id:
                            client.send(
                                str([user["title"], user["content"]]).encode(FORMAT))
                            break
            elif mode == "FILE":
                name = user_data[1]
                file = user_data[2]
                IDfile = user_data[3]
                if len(file) > 0:
                    file_exist = is_exist_file(name, file)
                    if not file_exist:
                        client.send(
                            "File successfully created!".encode(FORMAT))
                        add_new_file(name, file, IDfile)
                        with open(f'./user_data/{name}/' + file, 'wb') as f:
                            data = client.recv(4100000)
                            f.write(data)
                            f.close()
                    else:
                        client.send(
                            "This title is already exist".encode(FORMAT))
            else:
                pass
        except:
            if client in clients:
                clients.remove(client)
                client.close()


def receive():
    ThreadCount = 0
    while True:
        Client, address = ServerSocket.accept()

        print(f"Connected with {str(address)}!")
        print("Client:", Client.getsockname())

        clients.append(Client)

        client_handler = threading.Thread(target=handle, args=(Client,))
        client_handler.start()
        ThreadCount += 1
        print('Connection Request: ' + str(ThreadCount))


print("**** SERVER SIDE ****")
print("Server:", HOST, PORT)
print("Waiting for Client!")
receive()

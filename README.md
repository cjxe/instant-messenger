# Instant Messenger


## Task 1: Implement a simple instant messenger 

The first task is to implement a client-server system, which implements an instant messenger
using **TCP**, allowing users to chat with each other. The instant messenger will consist of a client and a server program.

### To Do List
- [X] Create a **basic** functioning **server & client**.

#### Client(s) can: 
- [X] send **custom message(s)**.
- [X] send **multiple messages**.
- [X] **enter** a **username**. 
- [ ] **see** other clients' **messages**.

#### Server can:
- [X] have **multiple clients** connected.
- [X] **display client's username** in front of each message.
- [ ] use a **dictionary** to **store** all the **current connections**. CURRENTLY WORKING ON THIS!
- [X] **display a message** when a **client connects**.
- [X] **display a message** when a **client disconnects**.

#### Error/Exception Handling
- [X] Make sure the server does not crash when someone leaves.
- [ ] Ensure that when a client drops out, that connection is removed from the dictionary.
- [ ] Display a message when a client **drops out**.
- [X] The server should not allow any client to send messages without a username.
- [ ] If the server is not available or port/hostname are wrong, an error message detailing the issue should be printed.
- [ ] Clients crashing or losing connection should not impact the server or other clients.
- [ ] In case of a crash, attempt to close remaining connections and print an error message to the `log` file.

#### Produce a `server.log` such that it contains information about:
- [ ] all clients connecting/disconnecting.
- [ ] any sent messages.

## Task 2 Application Protocol
In order to extend our instant messenger with further features we need to define a proper protocol between client and server. Protocols define the format and order of messages sent and received among network entities, and actions taken on message transmission and receipt. 

#### Both server and client(s) can: 
- [ ] send messages to **everyone**. (`/all {text}`)
- [ ] send messages to **certain people**. (`/whisper {username} {text}`)
- [ ] requests a list of all current users. (`/who`) 
- [ ] choose a **new username**. (`/newname {new_username}`) [USER ONLY!]
- [ ] use `/help`, i.e. show all available commands. [USER ONLY!]
- [X] leave the chat. (`/disc`) [USER ONLY!]

#### Error/Exception Handling
Handle all protocol errors appropriately. This includes unknown messages, whispering to a
non-existing user, etc.

## Prerequisites

[Python 3.8.5](https://www.python.org/downloads/release/python-385/) or newer.

## Installing

...

## Documentation

...

## Running the tests

...

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

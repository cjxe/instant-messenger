<h1 align="center">
	Instant Messenger 💬
</h1>

A messaging board which accepts multiple users and various commands using "sockets".

## Task 1: Implement a simple instant messenger 
The first task is to implement a client-server system, which implements an instant messenger
using **TCP**, allowing users to chat with each other. The instant messenger will consist of a client and a server program.

### To Do List
- [X] Create a **basic** functioning **server & client**.

#### Client(s) can: 
- [X] send **custom message**.
- [X] send **multiple messages**.
- [X] **define** a **username**. 
- [X] **see** other clients' **messages**.

#### Server can:
- [X] have **multiple clients** connected.
- [X] **display client's username** in front of each message.
- [X] use a **dictionary** to **store** all the **current connections**.
- [X] **display a message** when a **client connects**.
- [X] **display a message** when a **client disconnects**.

#### Error/Exception Handling
- [X] Make sure the server does not crash when someone leaves.
- [X] Ensure that when a client drops out, that connection is removed from the dictionary.
- [X] Display a message when a client **drops out**.
- [X] The server should not allow any client to send messages without a username.
- [X] If the server is not available or port/hostname are wrong, an error message detailing the issue should be printed.
- [X] Clients crashing or losing connection should not impact the server or other clients.
- [X] In case of a crash, attempt to close remaining connections and print an error message to the `log` file.

#### Produce a `server.log` such that it contains information about:
- [X] all clients connecting/disconnecting.
- [X] any sent messages.

## Task 2 Application Protocol
In order to extend our instant messenger with further features we need to define a proper protocol between client and server. Protocols define the format and order of messages sent and received among network entities, and actions taken on message transmission and receipt. 

#### Server can: 
- [X] use `/help` to **show all available commands**. (`/help`)
- [X] requests a **list of all current users**. (`/who`)
- [X] send messages to **everyone**. (`/all <message>`) [SERVER ONLY!]
- [X] send messages to a **specific user**. (`/pm <user> <message>`)
- [ ] **kick** a user. (`/kick <user>`)
- [ ] **ban** a user. (`/ban <user>`)
- [X] **stop** the server. (`/stop`) [SERVER ONLY!]


#### Client(s) can:
- [X] use `/help` to **show all available commands**. (`/help`)
- [X] requests a **list of all current users**. (`/who`)
- [X] send messages to a **specific user**. (`/pm <to> <message>`)
- [X] **change** username. (`/rename <new_name>`) [USER ONLY!]
- [X] **leave** the chat. (`/leave`) [USER ONLY!]

#### Error/Exception Handling
Handle all protocol errors appropriately. This includes unknown messages, whispering to a
non-existing user, etc.

## Prerequisites

- [Python 3.8.5](https://www.python.org/downloads/release/python-385/) or newer
	- external libraries

## Installing
[Click here](https://github.com/cjxe/instant-messenger/archive/master.zip) to download **or** copy 
``` 
git clone https://github.com/cjxe/instant-messenger
``` 
and right click on the command-line to paste.

⚠️ **Do not forget** to install the necessary libraries.

## Documentation

See [protocol.txt](protocol.txt).

## Running the tests

...

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

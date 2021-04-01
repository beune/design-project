# Design Project

Repository for the Design Project.

## Running the server side

### Prerequisites

#### Database password

A password file (called password) should be put in the root folder of the project containing a LF string password.
It will function as the password for the `mysql` database.

#### Docker version

Running the server side requires `docker-compose` version `1.28.6` or above. Check the version with:

```{.sh}
$ docker-compose --version
docker-compose version 1.28.6
```

Running the server side, including the MySQL database, can be done using the following commands from the root directory.
Docker should be installed on your machine in order to run these commands:

```{.sh}
$ echo "super_secret_password" >> password
$ docker-compose build
.
.
.
$ docker-compose up -d
```

## Compiling the client side

The client side of our application can be compiled using the following commands form the source:

```{.sh}
$ .\venv\Scripts\activate
$ cd client\frontend
$ npm install
$ npm run build
$ cd ..
$ python -m eel controller.py web --onefile
.
.
.
```

This will create one executable: `client\dist\controller.exe`
Executing this file will open the frontend of our application.

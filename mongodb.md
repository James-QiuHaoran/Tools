# MongoDB

## Install MongoDB on Ubuntu

https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

```
# ubuntu 20.04
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org

# optional
echo "mongodb-org hold" | sudo dpkg --set-selections
echo "mongodb-org-database hold" | sudo dpkg --set-selections
echo "mongodb-org-server hold" | sudo dpkg --set-selections
echo "mongodb-mongosh hold" | sudo dpkg --set-selections
echo "mongodb-org-mongos hold" | sudo dpkg --set-selections
echo "mongodb-org-tools hold" | sudo dpkg --set-selections

sudo systemctl start mongod
sudo systemctl status mongod
sudo systemctl enable mongod  # auto restart after rebooting
```

By default, MongoDB is listening to the localhost address. You can change the bind IP address to `0.0.0.0` for listening to any interface (so that the clients in the Docker containers can also access the server with `172.17.0.1`).

## Enable Authentication

### Create the User Administrator

```
> use admin
> db.createUser(
  {
    user: "yourusername",
    pwd: "yourpassword",
    roles: [ { role: "userAdminAnyDatabase", db: "admin" } ]
  }
)
```

### Update the Configuration File

Open `/etc/mongod.conf` with your favorite code editor and search for the following lines:

```
security:
  authorization: "disabled"
```

Change "disabled" to "enabled", save the file, and restart `mongod`:

```
sudo service mongodb restart
```

### Connect and Authenticate as the User Administrator

```
$ mongo mongodb://<host>:<port>
> db.auth("yourusername", "yourpassword")
1
```

You can also connect and authenticate in one single step with `mongo mongodb://superadmin:thepianohasbeendrinking@<host>:<port>`, but this option isn’t advised because it will leave your credentials visible in your terminal history, which any program on your computer can actually read.

### Create Additional Users as Needed

The following operation adds a user `myTester` to the `test` database who has `readWrite` role:

```
> use test
> db.createUser(
  {
    user: "myTester",
    pwd: "xyz123",
    roles: [ { role: "readWrite", db: "test" } ]
  }
)
```

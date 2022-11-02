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

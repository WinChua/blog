MONGO_HOME=/home/winchua/mongo/pkg/mongodb-linux-x86_64-rhel70-4.4.4/bin/
export mongod=${MONGO_HOME}/mongod
export mongos=${MONGO_HOME}/mongos
export mongo=${MONGO_HOME}/mongo


echo 'sh.addShard("shard0/localhost:27010")' | mongo localhost:27031
echo 'sh.addShard("shard1/localhost:27011")' | mongo localhost:27031
echo 'sh.addShard("shard2/localhost:27012")' | mongo localhost:27031

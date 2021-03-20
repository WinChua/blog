MONGO_HOME=/home/winchua/mongo/pkg/mongodb-linux-x86_64-rhel70-4.4.4/bin/
export mongod=${MONGO_HOME}/mongod
export mongos=${MONGO_HOME}/mongos
export mongo=${MONGO_HOME}/mongo

echo 'use mydb; db.hello.insertOne({"uin": 193}); sh.enableSharding("mydb");' | mongo localhost:27031

echo 'use mydb; sh.shardCollection("mydb.hello", {"_id": 1})' | mongo localhost:27031

MONGO_HOME=/home/winchua/mongo/pkg/mongodb-linux-x86_64-rhel70-4.4.4/bin/
export mongod=${MONGO_HOME}/mongod
export mongos=${MONGO_HOME}/mongos
export mongo=${MONGO_HOME}/mongo

for s in 0 1 2
do
    mkdir -p mongod/shard${s}/data
    nohup mongod --shardsvr --dbpath mongod/shard${s}/data --port 2701${s} --replSet shard${s}  > mongod/shard${s}/shard${s}.log  &
done


mkdir -p configsvr/data

nohup mongod --configsvr --dbpath configsvr/data --port 27021 --replSet conf0 > configsvr/conf0.log &

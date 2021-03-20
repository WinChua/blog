MONGO_HOME=/home/winchua/mongo/pkg/mongodb-linux-x86_64-rhel70-4.4.4/bin/
export mongod=${MONGO_HOME}/mongod
export mongos=${MONGO_HOME}/mongos
export mongo=${MONGO_HOME}/mongo

for s in 0 1 2
do
    echo 'rs.initiate({_id: "shard'${s}'", members: [ {_id: '${s}', host: "localhost:2701'${s}'" } ] })' | ${MONGO_HOME}/mongo localhost:2701${s} 
done

echo 'rs.initiate({_id: "conf0", members: [ { _id: 0, host: "localhost:27021" } ] })' | ${MONGO_HOME}/mongo localhost:27021

    mkdir mongos
nohup ${MONGO_HOME}/mongos --configdb conf0/localhost:27021 --port 27031 > mongos/mongos.log &

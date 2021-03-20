## MongoDB shard 的组成
* configsvr
* shardsvr
* mongos

三者的关系:
1. configsvr & shardsvr 都是replicate set;
2. configsvr 用于记录当前整个shard集群的配置信息;
3. shardsvr 用于存储部分数据;
4. mongos 是一个route, 将请求路由到各个shardsvr;

## 部署顺序
1. 针对每一个shard, 启动多个mongod实例, mongo shell链接到每一个shard中的一个mongod, 执行rs.initiate添加相同shard的ip实例;
2. 针对configsvr, 启动多个mongod实例, mongo shell链接到其中一个mongod, 执行rs.initiate添加相同shard的ip实例;
3. mongos 启动制定2中的config replicate set作为配置信息存储;
4. 在mongos中执行sh.addShard("<shardRepSetName>/ip:port,ip:port") 增加分片
5. sh.enableSharding("dbname"); sh.shardColleciton("dbname.tablename", {"_id": 1})

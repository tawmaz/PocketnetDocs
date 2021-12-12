**SQLite Page Cache Impact on PocketNet Node Synchronization**

The objective of this test is to determine the impact of SQLite page cache on rate of PocketNet node synchronization.  Two identical AWS m5ad.xlarge systems will be launched in the same network subnet and placement group.  One node will be configured with a 5MB SQLite page cache and the other with a 500MB SQLite page cache.  The nodes will be started at identical times and block count progress will be recorded at approximate 8 hour intervals until both nodes are fully synchronized.  SQLite cache usage will be recorded at each interval.

**Test Platform Specifications**
AWS m5ad.xlarge platform is a 4 core AMD Epyc server with 16GB RAM, 150GB NVMe SSD, and up to 10GbE networking.  PocketNet Core blockchain and SQLite files will be stored on the attached NVMe SSD drive.

https://aws.amazon.com/blogs/aws/new-amd-epyc-powered-amazon-ec2-m5ad-and-r5ad-instances/

**Build Steps**
Checkout git commit 4e0b0232f65edf4a79805975febd918c6dc350c2 

Create release package with default 5MB cache:
```
git checkout 4e0b0232f65edf4a79805975febd918c6dc350c2
./autogen.sh
cd depends
make -j4
cd ..
CONFIG_SITE=/home/user/src/pocketnet.core.sqlite/depends/x86_64-pc-linux-gnu/share/config.site ./configure --prefix=/usr/local --with-incompatible-bdb
make clean
make -j4
make deploy
```
Build release with 500mb cache setting by changing SQLITE_DEFAULT_CACHE_SIZE from -5000 to -500000, then:
```
make -j4
make deploy
```


**Node Setup**

Test nodes were launched on AWS with the following parameters.  Nodes were placed in a instance placement group of type "cluster" to ensure they were on the same network spine in the data center to minimize latency between the nodes. 

Instance Type: m5ad.xlarge

Datacenter: us-west-2d

EBS volume: 16 GB

OS Image: ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20211021 - ami-036d46416a34a611c

Each node was setup with the following commands to install prerequisite packages and to create the .pocketcoin folder on the attached NVMe drive:

```
sudo mkfs -t xfs /dev/nvme1n1
sudo mkdir /data
sudo mount /dev/nvme1n1 /data
sudo chmod 777 /data
mkdir /data/.pocketcoin
sudo chmod 777 /data/.pocketcoin
ln -s /data/.pocketcoin /home/ubuntu/.pocketcoin
cd ~/.pocketcoin

sudo apt update
sudo apt upgrade
sudo apt install libboost-all-dev libzmq3-dev libminiupnpc-dev mosh libdb-dev libdb++-dev
```
The following pocketcoin.conf files were used on each node, with other node added as a peer:
5MB cache test node:
```
# Enable public API interfaces
api=1
wsuse=1
daemon=1

# Setting ports
publicrpcport=38081
wsport=8087

# Setting work queue and threads
rpcpublicworkqueue=3000
rpcpublicthreads=30
rpcpostworkqueue=1500
rpcpostthreads=15
addnode=172.31.51.163
```
500MB cache test node:
```
# Enable public API interfaces
api=1
wsuse=1
daemon=1

# Setting ports
publicrpcport=38081
wsport=8087

# Setting work queue and threads
rpcpublicworkqueue=3000
rpcpublicthreads=30
rpcpostworkqueue=1500
rpcpostthreads=15
addnode=172.31.49.109
```

**Test Results**

Both nodes started at 8:17pm, december 11.

Logging enabled with ```pocketcoin-cli logging +stat```

10 minutes in:
500MB node:
  "Height": 34500,
    "SharedCacheUsed": 157566888,
  "CacheHit": 3280059,
  "CacheMiss": 0,

5MB cache node:
 "Height": 47722,
   "SharedCacheUsed": 5261904,
  "CacheHit": 3481354,
  "CacheMiss": 87789,







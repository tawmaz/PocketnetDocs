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
The following pocketcoin.conf files were used on each node.  wsuse and api are set to 0 due to this bug: https://github.com/pocketnetteam/pocketnet.core/issues/108 
```
# Enable public API interfaces
api=0
wsuse=0
daemon=1

# Setting ports
publicrpcport=38081
wsport=8087

# Setting work queue and threads
rpcpublicworkqueue=3000
rpcpublicthreads=30
rpcpostworkqueue=1500
rpcpostthreads=15
```

**Test Run 1 Results**

The pocketcoind daemon was started 12 December at 23:20 UTC time.  Both nodes were started within 1 second of each other.

Logging was enabled with the command ```pocketcoin-cli logging +stat``` to enable performance samples to be written to the debug.log file at 1 minute increments. The python script debuglog2csv.py was used to extract time and block height data from the debug.log file on each node.
Each node was allowed to synchronize to block height 1349351 due to an errata in SocialConsensus described here: https://github.com/pocketnetteam/pocketnet.core/issues/104

![500mb vs 5mb chart](https://github.com/tawmaz/PocketnetDocs/blob/main/sqlite_cache_test/500mb_vs_5mb_run1.png)

Raw log files and spreadsheet files for the test run are located here: https://github.com/tawmaz/PocketnetDocs/tree/main/sqlite_cache_test

**Analysis + Conclusion**

The node configured with a 5 megabyte SQLite page cache maintained an advantage up to around block height 1000000. At that point the 500 mb node built a lead and reached the final block height of 1349351 at 3 hours and 26 minutes earlier when compared to the 5mb node.  There are a few possible reasons for the observed performance differences: (1) Larger cache will require a longer warm-up time to maximize the rate of cache hit versus cache misses explaining why we see the 500 mb cache node move ahead later in the test (2) Larger cache size will demonstrate more benefit on a larger database, which is why we see the performance delta switch and increase with increase in block height.
There is not a good explanation of why the 5mb node would maintain and advantage earlier in the test.  While the larger cache size will not help with a small database it should not be detrimental.  Additional test runs will be required to determine if this is a persistent phenomena.
A certain amount of luck is involved in node synchornization performance where nodes which peer with higher perforance and lower latency nodes will synchonize faster.  Possibly explicitly adding nodes in future runs as well as adding the nodes under test as peers to each other (so the faster node will help bring the slower one up to speed) may help limit variability due to luck.  





**SQLite Page Cache Impact on PocketNet Node Synchronization**

The objective of this test is to determine the impact of SQLite page cache on rate of PocketNet node synchronization.  Two identical AWS m5ad.large systems will be launched in the same network subnet and placement group.  One node will be configured with a 5MB SQLite page cache and the other with a 500MB SQLite page cache.  The nodes will be started at identical times and block count progress will be recorded at approximate 8 hour intervals until both nodes are fully synchronized.  SQLite cache usage will be recorded at each interval.

*Test Platform Specifications*
AWS m5ad.large platform is a 4 core AMD Epyc server with 16GB RAM, 150GB NVMe SSD, and up to 10GbE networking.  PocketNet Core blockchain and SQLite files will be stored on the attached NVMe SSD drive.

https://aws.amazon.com/blogs/aws/new-amd-epyc-powered-amazon-ec2-m5ad-and-r5ad-instances/



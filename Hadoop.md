Parameters: ('keyMaxBytesNum', 'keyMinBytesNum') Source: ('defaultMaxBytes', 'defaultMinBytes')
File: /home/lhy/JavaCode/hadoop-3.3.5-src/hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-nativetask/src/test/java/org/apache/hadoop/mapred/nativetask/kvtest/TestInputFile.java
      keyMinBytesNum = defaultMinBytes;
      keyMaxBytesNum = defaultMaxBytes;

**共存共生**

final int defaultMinBytes = conf.getInt(TestConstants.*NATIVETASK_KVSIZE_MIN*, 1);
final int defaultMaxBytes = conf.getInt(TestConstants.*NATIVETASK_KVSIZE_MAX*, 64);

---



Parameters: ('staleInterval', 'recheckInterval') Source: ('staleInterval', 'recheckInterval')
File: /home/lhy/JavaCode/hadoop-3.3.5-src/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/HeartbeatManager.java
    if (avoidStaleDataNodesForWrite && staleInterval < recheckInterval) {
      this.heartbeatRecheckInterval = staleInterval;

**if A>B then**

boolean avoidStaleDataNodesForWrite = conf.getBoolean(
    DFSConfigKeys.*DFS_NAMENODE_AVOID_STALE_DATANODE_FOR_WRITE_KEY*,
    DFSConfigKeys.*DFS_NAMENODE_AVOID_STALE_DATANODE_FOR_WRITE_DEFAULT*);
long recheckInterval = conf.getInt(
    DFSConfigKeys.*DFS_NAMENODE_HEARTBEAT_RECHECK_INTERVAL_KEY*,
    DFSConfigKeys.*DFS_NAMENODE_HEARTBEAT_RECHECK_INTERVAL_DEFAULT*); // 5 min
long staleInterval = conf.getLong(
    DFSConfigKeys.*DFS_NAMENODE_STALE_DATANODE_INTERVAL_KEY*,
    DFSConfigKeys.*DFS_NAMENODE_STALE_DATANODE_INTERVAL_DEFAULT*);// 30s



---

Parameters: ('recheckInterval', 'staleInterval') Source: ('recheckInterval', 'staleInterval')
File: /home/lhy/JavaCode/hadoop-3.3.5-src/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/blockmanagement/HeartbeatManager.java
    if (**<u>avoidStaleDataNodesForWrite</u>** && **staleInterval** < **recheckInterval**) {
      this.heartbeatRecheckInterval = staleInterval;
      LOG.info("Setting heartbeat recheck interval to " + staleInterval



**if avoidStaleDataNodesForWrite = true and staleInterval < recheckInterval : staleInterval will work**

**else recheckInterval will work**



---

Parameters: ('numMaps', 'totalBytesToWrite') Source: ('numBytesToWritePerMap', 'totalBytesToWrite')

File: /home/lhy/JavaCode/hadoop-3.3.5-src/hadoop-mapreduce-project/hadoop-mapreduce-client/hadoop-mapreduce-client-jobclient/src/test/java/org/apache/hadoop/RandomTextWriterJob.java

long numBytesToWritePerMap = conf.getLong(*BYTES_PER_MAP*, 10 * 1024);
long totalBytesToWrite = conf.getLong(*TOTAL_BYTES*, numBytesToWritePerMap);
int numMaps = (int) (totalBytesToWrite / numBytesToWritePerMap);
if (numMaps == 0 && totalBytesToWrite > 0) {
  numMaps = 1;
  conf.setLong(*BYTES_PER_MAP*, totalBytesToWrite);
}

 **manual中没有提到** 没有关系

---
Parameters: ('backlogLength', 'ss') Source: ('backlogLength', 'socketWriteTimeout')
File: /home/lhy/JavaCode/hadoop-3.3.5-src/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/SecureDataNodeStarter.java
      ss.bind(streamingAddr, backlogLength);



---
Parameters: ('maxMem', 'minMem') Source: ('maxMem', 'minMem')
File: /home/lhy/JavaCode/hadoop-3.3.5-src/hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-resourcemanager/src/main/java/org/apache/hadoop/yarn/server/resourcemanager/scheduler/fair/FairScheduler.java

int minMem =
    config.getInt(YarnConfiguration.*RM_SCHEDULER_MINIMUM_ALLOCATION_MB*,
        YarnConfiguration.*DEFAULT_RM_SCHEDULER_MINIMUM_ALLOCATION_MB*);
int maxMem =
    config.getInt(YarnConfiguration.*RM_SCHEDULER_MAXIMUM_ALLOCATION_MB*,
        YarnConfiguration.*DEFAULT_RM_SCHEDULER_MAXIMUM_ALLOCATION_MB*);

if (minMem < 0 || minMem > maxMem) {
  throw new YarnRuntimeException("Invalid resource scheduler memory"
    \+ " allocation configuration: "
    \+ YarnConfiguration.*RM_SCHEDULER_MINIMUM_ALLOCATION_MB
\*    + "=" + minMem
    \+ ", " + YarnConfiguration.*RM_SCHEDULER_MAXIMUM_ALLOCATION_MB
\*    + "=" + maxMem + ".  Both values must be greater than or equal to 0"
    \+ "and the maximum allocation value must be greater than or equal to"
    \+ "the minimum allocation value.");
}

**yarn.scheduler.minimum-allocation-mb**
**yarn.scheduler.maximum-allocation-mb** 

---
Parameters: ('maxWaitTime', 'retryPolicy') Source: ('maxWaitTime', 'retryIntervalMS')
File: /home/lhy/JavaCode/hadoop-3.3.5-src/hadoop-yarn-project/hadoop-yarn/hadoop-yarn-common/src/main/java/org/apache/hadoop/yarn/client/ServerProxy.java
RetryPolicy retryPolicy = null;
if (maxWaitTime == -1) {
  // wait forever.
  retryPolicy = RetryPolicies.*retryForeverWithFixedSleep*(retryIntervalMS,
      TimeUnit.*MILLISECONDS*);
} else {
  retryPolicy =
      RetryPolicies.*retryUpToMaximumTimeWithFixedSleep*(maxWaitTime,
          retryIntervalMS, TimeUnit.*MILLISECONDS*);
}

yarn.resourcemanager.monitor.capacity.preemption.max_wait_before_kill



**共同作用在RetryPolicy ** ，每个参数都有确认机制 确保在范围内

---
Parameters: ('minRevocationPollingMs', 'confRevocationPollingMs') Source: ('revocationMs', 'confRevocationPollingMs')
File: /home/lhy/JavaCode/hadoop-3.3.5-src/hadoop-hdfs-project/hadoop-hdfs/src/main/java/org/apache/hadoop/hdfs/server/datanode/fsdataset/impl/FsDatasetCache.java
if (minRevocationPollingMs < confRevocationPollingMs) {
  throw new RuntimeException("configured value " +
          confRevocationPollingMs + "for " +
          *DFS_DATANODE_CACHE_REVOCATION_POLLING_MS* +
          " is too high.  It must not be more than half of the " +
          "value of " +  *DFS_DATANODE_CACHE_REVOCATION_TIMEOUT_MS* +
          ".  Reconfigure this to " + minRevocationPollingMs);
}

dfs.datanode.cache.revocation.timeout.ms

dfs.datanode.cache.revocation.polling.ms

---
Parameters: ('highUsableSpacePercentagePerDisk', 'lowUsableSpacePercentagePerDisk') Source: ('highUsableSpacePercentagePerDisk', 'lowUsableSpacePercentagePerDisk')
File: /home/lhy/JavaCode/hadoop-3.3.5-src/hadoop-yarn-project/hadoop-yarn/hadoop-yarn-server/hadoop-yarn-server-nodemanager/src/main/java/org/apache/hadoop/yarn/server/nodemanager/LocalDirsHandlerService.java

float highUsableSpacePercentagePerDisk =
    conf.getFloat(
      YarnConfiguration.*NM_MAX_PER_DISK_UTILIZATION_PERCENTAGE*,
      YarnConfiguration.*DEFAULT_NM_MAX_PER_DISK_UTILIZATION_PERCENTAGE*);
float lowUsableSpacePercentagePerDisk =
    conf.getFloat(
        YarnConfiguration.*NM_WM_LOW_PER_DISK_UTILIZATION_PERCENTAGE*,
        highUsableSpacePercentagePerDisk);
if (lowUsableSpacePercentagePerDisk > highUsableSpacePercentagePerDisk) {
  *LOG*.warn("Using " + YarnConfiguration.
      *NM_MAX_PER_DISK_UTILIZATION_PERCENTAGE* + " as " +
      YarnConfiguration.*NM_WM_LOW_PER_DISK_UTILIZATION_PERCENTAGE* +
      ", because " + YarnConfiguration.
      *NM_WM_LOW_PER_DISK_UTILIZATION_PERCENTAGE* +
      " is not configured properly.");
  lowUsableSpacePercentagePerDisk = highUsableSpacePercentagePerDisk;
}

yarn.nodemanager.disk-health-checker.max-disk-utilization-per-disk-percentage

yarn.nodemanager.disk-health-checker.disk-utilization-watermark-low-per-disk-percentage

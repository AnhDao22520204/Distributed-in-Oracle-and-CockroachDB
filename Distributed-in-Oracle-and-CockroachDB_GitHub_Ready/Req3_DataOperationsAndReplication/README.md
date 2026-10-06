# Requirement 3 – Data Operations and Replication

- `crud_latency.py`: mean CRUD latency by node.
- `throughput.py`: concurrent update workload and estimated TPS.
- `replication_lag.py`: follower-read visibility delay.
- `failover.py`: client-observed recovery after manually stopping one node.

`replication_lag.py` intentionally describes the measurement as follower-read
visibility, because normal SQL polling does not expose raw internal Raft
replication latency.

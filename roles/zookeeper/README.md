#ZooKeeper role

The role can be used to install a ZooKeeper cluster (Multi-Server).

How to use it?
-----
* Copy the __roles/zookeeper__ folder to your ansible playbook roles folder.
* The inventory should be define like that:
```yaml
[zookeeper-servers]
zookeeper-server-1 zookeeper_id=1
zookeeper-server-2 zookeeper_id=2
zookeeper-server-3 zookeeper_id=3
```
* The play should look like:
```yaml
- name: ZooKeeper play
  hosts: zookeeper-servers
  user: the_user_to_use
  sudo: yes
  roles:
    - zookeeper

```
Dependencies
-----
* Java
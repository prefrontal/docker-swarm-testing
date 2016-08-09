# docker-swarm-testing

Repository to hold files related to Docker Swarm tests.

`provisioning`

This directory holds the files requred to spin up AWS instances, provision them with Docker, and then start up a small Docker swarm.

`test`

This directory holds any files used for testing the Docker swarm.

---

Mosty-correct steps for AWS:

1. You must define your AWS secret keys as environment variables

  ```
  export AWS_ACCESS_KEY_ID=<yourKeyID>
  export AWS_SECRET_ACCESS_KEY=<yourSecretKey>
  ```

2. Run the `aws-spinup.yml` ansible playbook

  `ansible-playbook aws-spinup.yml`

  - Creates a security group with restricted port openings
  - Creates a new private key pair for the swarm instances
  - Launches the new instances

  Results:
  - The new private key is saved into the local folder as a .pem file
  - The IP addresses of the new hosts are saved into the hosts.txt file

3. Edit the hosts file to create separate groups for swarm, manager, and nodes
 It should look like this only with, you know, numbers:

 ```
 [swarm]
 X.X.X.X
 Y.Y.Y.Y
 Z.Z.Z.Z

 [manager]
 X.X.X.X

 [nodes]
 Y.Y.Y.Y
 Z.Z.Z.Z
 ```

4. Run the `swarm-docker.yml` playbook

 `ansible-playbook -i ./hosts.txt swarm-docker.yml`

  - Installs the latest version of Docker
  - Adds ubuntu user to the Docker group

5. Run the `swarm-manager.yml` playbook

  `ansible-playbook -i ./hosts.txt swarm-manager.yml`

  - Must modify the manager IP address in the script
  - This should be the internal AWS address, not the public IP

6. Run the `swarm-nodes.yml` playbook

  `ansible-playbook -i ./hosts.txt swarm-nodes.yml`

  - Must modify the the script with the swarm token and manager IP

  To get the swarm token, you can either:
  - Log in to the manager node and run `docker swarm join-token worker`
  - Look at the output of the manager playbook, which has the full worker join command

7. There is no step seven

---

Using Docker Swarm:

At this point you have a connected swarm, but it is not running anything.  To get some containers running, you need to start a new service.  Here is an example command to run on the manager node:

```docker service create --name testSwarm --replicas 3 -p 8001:80 prefrontal/hello-node2```

This pulls the hello-node2 image from Docker hub and runs three of them across the swarm.

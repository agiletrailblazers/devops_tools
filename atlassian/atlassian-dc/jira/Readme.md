# Pre Requistes
Before you follow these steps, you MUST have following in place to be successful
1. You have a kubernetes cluster already up and running with necessary worker nodes
2. Ingress controller has been installed (using nginx-ingress controller, this is optional, only if SSL setup is needed)
3. NFS client has been installed to ensure dynamic provisioning and can be supported for jira, confluence and crowd
4. you have access to a DNS service provider that needs to be updated with your new domain names
5. cloud autoscaler is in place to support the cloud autoscaling group based on the container metrics on the worker nodes.

# Global Steps - needed to setup the cluster
1. Setup a storage class
2. Setup naespaces for the applications (Jira, Confuencem, Crowd). You can choose to decide and do this in default namespace or in anyother namespace per your business need.
3. Setup a secret for certs to enable SSL with ingress controller

# Common Steps (for jira, crowd and confluence)

# Jira specific steps

# Confluence specific steps

# Crowd specific steps

# Opportunities for additonal refinements


# Original Readme notes
1. Run the Postgres yaml file to create the DB
2. Run the Persistent Volume config yaml to get the folders created
3. Run the Node 1 Yaml and wait for the UI to be accessible 
4. Proceed with the configuration of DB, admin user and a sample project setup.
5. Verify that Jira is running in a clustered configuration by accessing the cluster page.
6. Stop the Node 1
7. Copy the Jira home from node 1 folder and paste it into Node 2 Folder
8. Delete the cluster.properties files in Node 2 folder as it would be created by the container
9. Ensure that the ownership of the folders are with uid:gid as 2001:2001. If not update the permission of Node 2 Jira home.
10. Start Node 1 and wait untill it starts completely
11. Start Node 2
12. Navigate to Clustering page and ensure both the nodes are up and running


Note: Line 6 to 12 would be automated and should not have any manual steps while bringing up a new node

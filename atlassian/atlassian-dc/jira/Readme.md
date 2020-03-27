Setting up Jira Data Center in Rancher

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

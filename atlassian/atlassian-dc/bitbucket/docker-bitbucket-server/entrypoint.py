#!/usr/bin/python3

from entrypoint_helpers import env, str2bool, start_app
import subprocess as sp
import os, re

RUN_USER = env['run_user']
RUN_GROUP = env['run_group']
BITBUCKET_INSTALL_DIR = env['bitbucket_install_dir']
BITBUCKET_HOME = env['bitbucket_home']

os.system(f'mkdir -p {BITBUCKET_HOME}/shared')
os.system(f'cp /bitbucket.properties {BITBUCKET_HOME}/shared/bitbucket.properties')

 # API call to kubernetes to get the list of peer IP's connected to confluence cluster
TOKEN = sp.getoutput('cat /var/run/secrets/kubernetes.io/serviceaccount/token')

service_output = sp.getoutput(f'curl -sSk -H "Authorization: Bearer {TOKEN}" https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/namespaces/devops-tools/endpoints/bitbucket-service | jq -r .subsets[].addresses[].ip | paste -sd "," -')

# Getting the current pod IP and assign it to an ENV variable
current_pod_ip = sp.getoutput('hostname -i')


match = re.match("^(\d{0,3})\.(\d{0,3})\.(\d{0,3})\.(\d{0,3})$", service_output)

if match:
    bitbucket_cluster_peers = f'{current_pod_ip},{service_output}'
else:
    bitbucket_cluster_peers = f'{current_pod_ip}'

# Find and replace confluence.cluster.peers values with current pods IP along with the cluster peers if exists
import configparser

config = configparser.RawConfigParser()
config.read(f'{BITBUCKET_HOME}/shared/bitbucket.properties')

ip = config.get('CONFIG', 'hazelcast.network.tcpip.members')
print ("ip is " +ip)
config.set('CONFIG','hazelcast.network.tcpip.members',bitbucket_cluster_peers)

with open(f'{BITBUCKET_HOME}/shared/bitbucket.properties', 'w') as configfile:
    config.write(configfile)


start_cmd = f"{BITBUCKET_INSTALL_DIR}/bin/start-bitbucket.sh -fg"
if str2bool(env['elasticsearch_enabled']) is False or env['application_mode'] == 'mirror':
    start_cmd += ' --no-search'

start_app(start_cmd, BITBUCKET_HOME, name='Bitbucket Server')


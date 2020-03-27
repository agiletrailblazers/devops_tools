#!/usr/bin/python3

import os
import re
import subprocess as sp
from entrypoint_helpers import env, gen_cfg, str2bool, start_app



RUN_USER = env['run_user']
RUN_GROUP = env['run_group']
CONFLUENCE_INSTALL_DIR = env['confluence_install_dir']
CONFLUENCE_HOME = env['confluence_home']

# Getting the current pod IP and assign it to an ENV variable

TOKEN = sp.getoutput('cat /var/run/secrets/kubernetes.io/serviceaccount/token')

service_output = sp.getoutput(f'curl -sSk -H "Authorization: Bearer {TOKEN}" https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_PORT_443_TCP_PORT/api/v1/namespaces/confluence/endpoints/confluence-service | jq -r .subsets[].addresses[].ip | paste -sd "," -')

current_pod_ip = sp.getoutput('hostname -i')


match = re.match("^(\d{0,3})\.(\d{0,3})\.(\d{0,3})\.(\d{0,3})$", service_output)

if match:
    confluence_cluster_peers = f'{current_pod_ip},{service_output}'
else:
    confluence_cluster_peers = f'{current_pod_ip}'

gen_cfg('server.xml.j2', f'{CONFLUENCE_INSTALL_DIR}/conf/server.xml')
gen_cfg('seraph-config.xml.j2',
        f'{CONFLUENCE_INSTALL_DIR}/confluence/WEB-INF/classes/seraph-config.xml')
gen_cfg('confluence-init.properties.j2',
        f'{CONFLUENCE_INSTALL_DIR}/confluence/WEB-INF/classes/confluence-init.properties')
gen_cfg('confluence.cfg.xml.j2', f'{CONFLUENCE_HOME}/confluence.cfg.xml',
        user=RUN_USER, group=RUN_GROUP, overwrite=True)


# Find and replace text @@confluence_cluster_peers@@ with current pods IP
os.system(f"sed -i 's|@@confluence_cluster_peers@@|'{confluence_cluster_peers}'|g' {CONFLUENCE_HOME}/confluence.cfg.xml")

start_app(f'{CONFLUENCE_INSTALL_DIR}/bin/start-confluence.sh -fg', CONFLUENCE_HOME, name='Confluence')
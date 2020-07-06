#!/bin/bash
# BITBUCKET_HOME should be set in Dockerfile and picked up from environment.
PROPERTIES_FILE="${BITBUCKET_HOME}/shared/bitbucket.properties"
# Remove all entries of hazelcast, before adding new onces
  sed -i -e '/hazelcast*/d' ${PROPERTIES_FILE}

  SERVER_IP="$(ip addr show eth0 | grep -w inet | cut -d " " -f 6 | cut -d "/" -f 1)"
  echo "Own IP: $SERVER_IP"
   # Adding new entries to bitbucket.properties with hazelcast values
  echo "hazelcast.network.tcpip.members=${CLUSTER_PEER_IPS}" >> ${PROPERTIES_FILE}



#!/bin/sh

if [ -z "$ENDPOINT_TEST" ]; then
    ENDPOINT_TEST=False
    echo "No endpoint test will be performed at runtime!" 1>&2
fi

cd /app && \
    echo "python3 NetApp.py -n $NET_APP_NAME -t $NET_API_PROT -s $NET_API_ADDRESS -U $NET_API_USER -P $NET_API_PASS -c $CALLBACK_ADDRESS -q $COLLECTOR_HOST -o $COLLECTOR_USER -r $COLLECTOR_PASS -z $MN_HOST -Z $MN_TOKEN -C $CAPIF_PATH -m $CAPIF_HOSTNAME -p $CAPIF_PORT_HTTP -S $CAPIF_PORT_HTTPS -u $CAPIF_CALLBACK_ADDRESS -e $ENDPOINT_TEST"  &&\
    python3 NetApp.py \
   -n $NET_APP_NAME \
   -t $NET_API_PROT \
   -s $NET_API_ADDRESS \
   -U $NET_API_USER \
   -P $NET_API_PASS \
   -c $CALLBACK_ADDRESS \
   -q $COLLECTOR_HOST \
   -o $COLLECTOR_USER \
   -r $COLLECTOR_PASS \
   -z $MN_HOST \
   -Z $MN_TOKEN \
   -C $CAPIF_PATH \
   -m $CAPIF_HOSTNAME \
   -p $CAPIF_PORT_HTTP \
   -S $CAPIF_PORT_HTTPS \
   -u $CAPIF_CALLBACK_ADDRESS \
   -e $ENDPOINT_TEST

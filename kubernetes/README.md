**Deployment of ininrmonnetapp in kubernetes**

 - kubectl apply -f environment.yaml
 - kubectl apply -f deployment.yaml
 - kubectl apply -f service.yaml

Image is hosted and available in our public docker repostory. 

Our example uses "NodePort" service type:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: ininrmonnetapp
spec:
  selector:
    app: ininrmonnetapp
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
      nodePort: 30638
  type: NodePort
```

The actual exposed port must match "CALLBACK_ADDRESS" env variable, in our case:

```bash
CALLBACK_ADDRESS: "ininrmonnetapp:30638"
```

**Other requirements for remote testing:**

 - NetApp has access to the internet
 - Our vApp backend must be able to access exposed service address of a NetApp (in our example ininrmonnetapp:30638) - so we would probably need the VPN connection and the actual reachable IP address/port of the NetApp's exposed service

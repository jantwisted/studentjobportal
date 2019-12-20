# studentjobportal
A web interface for StudentJobEngine API

## How to install

- clone
	- git clone https://github.com/jantwisted/studentjobportal.git

- spin up
	- cd studentjobportal
	- helm install --name <namespace> ./portalchart/ --set service.type=NodePort
	
- gke note
	- gcloud compute firewall-rules create test-node-port --allow tcp:$NODE_PORT #allow node port from the firewall
	- kubectl get nodes --output wide #get the external ip address


## Test

- Visit http://$EXTERNAL-IP:$NODE_PORT/

- Login: jantwisted/32132121213

## This application uses an API @heroku

https://studentjobengine.herokuapp.com

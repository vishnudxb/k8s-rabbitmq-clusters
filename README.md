# K8s cluster for RabbitMq


Setting a RabbitMQ cluster with high availability and creating a queue with AMQPS (AMQP with SSL)


#### Install gcloud sdk

```

curl https://sdk.cloud.google.com | bash  

```

#### Create a simple kubernetes cluster in Google cloud.

```

gcloud container clusters create ha-rabbitmq-cluster  --enable-cloud-logging  --enable-cloud-monitoring  --subnetwork default --num-nodes=3 -z us-east1-c

```

#### Get Kubectl credentials

```

1. gcloud auth activate-service-account <your user details from gcloud> --key-file=shopbonsai.json
2. gcloud config set account <your user details from gcloud>
3. gcloud container clusters get-credentials  ha-rabbitmq-cluster -z us-east1-c

```

#### Create persistentVolume

```

kubectl create -f ssd-storage.yaml

kubectl create -f ssd-claim.yaml

```

#### Install SSL Certs in RabbitMQ

```

git clone https://github.com/michaelklishin/tls-gen tls-gen
cd tls-gen/basic
# private key password
make PASSWORD=bunnies
make verify
make info
ls -l ./result

```

#### Installed RabbitMQ with HA in the K8s Cluster using HELM chart with customized values yaml file.

```

helm install stable/rabbitmq-ha --name rabbit-mq-cluster --namespace rabbit -f values.yaml

```

#### To get the yaml file details, run the below command:

```

helm get rabbit-mq-cluster

```

#### To get the K8s details:

```
kubectl get deployments,pods,services --namespace rabbit

```


#### Monitoring with logz.io

The credentials to the logz.io is shared via email

To setup the logz.io, I used the ```logzio.yaml``` file

### Enter the logz.io token number and the url in the logzio.yaml file

```

kubectl create -f logzio.yaml

```

#### To get the details, please execute the follow:

```

export NODE_IP=$(kubectl get nodes --namespace rabbit -o jsonpath="{.items[0].status.addresses[?(@.type=='ExternalIP')].address}" | awk {'print $1'})

export NODE_PORT_AMQP=$(kubectl get --namespace rabbit -o jsonpath='{.spec.ports[?(@.name=="amqp")].nodePort}' services rabbit-mq-cluster-rabbitmq-ha | awk {'print $1'})

export NODE_PORT_AMQPS=$(kubectl get --namespace rabbit -o jsonpath='{.spec.ports[?(@.name=="amqps")].nodePort}' services rabbit-mq-cluster-rabbitmq-ha | awk {'print $1'})

export NODE_PORT_STATS=$(kubectl get --namespace rabbit -o jsonpath='{.spec.ports[?(@.name=="http")].nodePort}' services rabbit-mq-cluster-rabbitmq-ha | awk {'print $1'})

```

#### Firewall commands used to open the ports:

```

gcloud compute instances list

gcloud compute firewall-rules list

gcloud compute firewall-rules create rabbitmq-access --allow tcp:12345,tcp:23456,tcp:34567,tcp:45678


```

#### Tested using a Python client pika

```

cd ~/k8s-rabbitmq/ssl

python3 publish.py && python3 consume.py

```

# Screenshots

![](https://i.imgur.com/H9awCwX.png)

![](https://i.imgur.com/yAG2v44.png)

![](https://i.imgur.com/AH3VDUk.png)

![](https://i.imgur.com/Dk4GgFG.png)

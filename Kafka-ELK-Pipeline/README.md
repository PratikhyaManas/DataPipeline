
![Kafka-ELK](https://user-images.githubusercontent.com/35187384/108124376-674ed100-70a7-11eb-8034-ba94ac965272.jpg)

There are 5 components in the creation of this pipeline.

1. Producer(Raspberry Pi) - It publishes the data to the Kafka Topic.

2. Kafka Server - The server publishes the data gathered from the producer.

3. Logstash - It acts as a medium between the Kafka and Elasticsearch which will carry the published data from Kafka and insert into the Elasticsearch database.

4. Elasticsearch - It is the database which stores the data published.

5. Kibana - It is a visualization tool to read the data in graphical format.

# Installation and Steps

Below are the steps of installation and procedure to create the data pipeline

# 1. Docker, Docker Compose

a) Install Docker from the official site `https://docs.docker.com/engine/install/ubuntu/`

b) i) Download the Docker Compose by typing the below command

`sudo curl -L "https://github.com/docker/compose/releases/download/1.27.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`

 Note-If you want to install a different version then just replace the 1.27.0 in above command with the version that you want to install
 
   ii) Make the binary executable. `sudo chmod +x /usr/local/bin/docker-compose`
   
   iii) Check if docker-compose is installed. `docker-compose version`
   

# 2. Kafka, Zookeeper Kafka Manager

a) Run the `docker-compose -f kafka-docker-compose.yml up -d`. Kafka running on port 9092, Zookeeper running on 2181, Kafka Manager on 9000.

 Note- Change the ip address in kafka-docker-compose.yml to your ip address.
 
# 3. Elasticsearch & Kibana

a) Run the `docker-compose -f elasticsearch-docker-compose.yml up -d`. Elasticsearch running on port 9200, Kibana running on port 5601.

# 4. Logstash

a) Download and install the Public Signing Key. 

`wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -`

b) Install dependencies. `sudo apt-get install apt-transport-https`

c) Add elastic search repository.

`echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list`

d) Update and install

`sudo apt update` and `sudo apt-get install logstash`

e) Start and check the status of the logstash server.

`systemctl start logstash` and `systemctl status logstash`

Note-Java needed to be installed as a prerequisite for logstash installation.

# 5. Kafka Producer

a) Install dependencies

`pip3 install Faker` and `pip3 install kafka-python`

# 6. Logstash Pipeline

a) Goto the configuration folder of logstash.We will read data from kafka topic registered_user and push the data to elasticsearch index named registered_user.

`cd /etc/logstash/conf.d/`. 

b) Move the `kafka-elastic-pipeline.conf` file to the logstash configuration folder. Change the ip address as per your system ip in the file.

c) Run the `producer.py` script.

d) Restart the logstash server.


# 7. Access data in Kibana

a) Open Kibana running at the port address you mentioned above during installation.

b) Goto Management Menu in Kibana dashboard. Click on Index Patterns and then click on Create Index Pattern. 

c) Search for your index then click next step. 

d) Then click on show advanced options and select @timestamp from the dropdown box.

e) Finally click on create index pattern and your index will be created.Once the index has been created then you can go to Discover menu of Kibana. You will see the index registered-user is already selected and the data is present.
 


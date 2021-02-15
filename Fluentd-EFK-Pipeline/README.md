#Installation of fluentd in RaspberryPi

1. Update by running the command `sudo apt-get update`

2. Install the aptitude GUI package `sudo apt-get install aptitude`

3. Install the ruby package as it is the prerequisite for fluentd installation `sudo aptitude install ruby-dev`.

4. Install fluentd by the command `sudo gem install fluentd`

5. Install the necessary plugins for fluentd `sudo fluent-gem install fluent-plugin-td` and `sudo fluent-gem install fluent-plugin-elasticsearch`.

Check whether fluentd installed properly, just type the command `fluent` and press tab. We can see that in the screen there are bunch of fluent commands.

#Installation of Elasticsearch and Kibana

1. Run the `docker-compose -f elasticsearch-docker-compose.yml up -d`. Elasticsearch running on port 9200, Kibana running on port 5601.

#Logs Producer

1. Run the `producer.py` script in RaspberryPi. The logs are generated in `log.json` file. 

#Fluentd Configuration File and running the fluentd

1. Create a fluentd configuration file by the command `touch fluentd.conf`.

2. Copy the below content in the conf file.

```

<source>
  @type tail
  path /home/pmbehera/EFK/log.json
  pos_file /home/pmbehera/EFK/log.json.pos
  format json
  time_format %Y-%m-%d %H:%M:%S
  tag log 
</source>


<match *log*>
  @type elasticsearch
  hosts http:://localhost:9200/
  index_name temperature
  type_name log
</match>

```
The source is from where fluentd will pick the logs and the match is the destination i.e.- elasticsearch

3. Run the fluentd configuration file with the command `fluentd -c fluentd.conf`.

# Visulaization in Kibana

1. Open Kibana running at the port address you mentioned above during installation.

2. Goto Management Menu in Kibana dashboard. Click on Index Patterns and then click on Create Index Pattern.

3. Search for your index then click next step.(temperature in my case)

4. Then click on show advanced options and select @timestamp from the dropdown box.

5. Finally click on create index pattern and your index will be created.Once the index has been created then you can go to Discover menu of Kibana. You will see the index registered-user is already selected and the data is present.



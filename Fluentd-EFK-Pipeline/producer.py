import random
import time
import json
import datetime

log_file = 'log.json'

i = 0
log_json = dict()
log_json["Data"] = {}

while True:
    i = i + 1
    temp = random.randint(10,30)
    log_json['Data']['Count'] = i
    log_json['Data']['Temperature'] = temp
    log_json['Created'] = datetime.datetime.utcnow().isoformat()
    
    with open(log_file,"a") as f:
        json.dump(log_json,f)
        f.write('\n')
        
        
    time.sleep(3)
    
    
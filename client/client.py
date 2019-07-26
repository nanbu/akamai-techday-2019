from prometheus_client import start_http_server, Gauge
from akamai.edgegrid import EdgeGridAuth, EdgeRc
import sys
import time
import math
import datetime
from datetime import tzinfo
import requests
from urllib.parse import urljoin
import json
import yaml


EDGEBYTES = Gauge('akamai_traffic_edge_bytes', 'Traffic from Edge (bps)')
EDGEHITS = Gauge('akamai_traffic_edge_hits', 'Edge Hits')
ORIGINBYTES = Gauge('akamai_traffic_origin_bytes', 'Traffic from Origin (bps)')
ORIGINHITS = Gauge('akamai_traffic_origin_hits', 'Origin Hits')
BYTESOFFLOAD = Gauge('akamai_traffic_offload_bytes_percentage', 'Bytes Offload (percentage)')
HITSOFFLOAD = Gauge('akamai_traffic_offload_hits_percentage', 'Hits Offload (perxentage)')

def get_today_traffic(config, starttime, endtime):
    edgerc = EdgeRc(config['edgerc'])
    section = config['section']
    baseurl = 'https://%s' % edgerc.get(section, 'host')
    cpcodes = [config['cpcode']]

    params = {
        'start' : starttime.isoformat(),
        'end' : endtime.isoformat(),
        'interval':'FIVE_MINUTES',
        'objectType':'cpcode',
        'objectIds':cpcodes,
        'groupBy':'hostname.url',
        'rowCount':1,
        'filters': {},
        'metrics': []
    }

    endpointurl = urljoin(baseurl, '/reporting-api/v1/reports/todaytraffic-by-time/versions/1/report-data')
    session = requests.Session()
    session.auth = EdgeGridAuth.from_edgerc(edgerc, section)
    result = session.get(endpointurl, params=params)
    return result

def shrink_minutes_for_datetime_in_most_recent_5minutes(target_datetime):
    shrunk_minutes = math.floor(target_datetime.minute / 5) * 5
    result_datetime = target_datetime.replace(minute=shrunk_minutes, second=0, microsecond=0)
    return result_datetime

def get_starttime_endtime():
    offset = datetime.timedelta(hours=+9)
    jst = datetime.timezone(offset)
    current_datetime_jst = datetime.datetime.now(tz=jst)
    endtime = shrink_minutes_for_datetime_in_most_recent_5minutes(current_datetime_jst)
    starttime = endtime + datetime.timedelta(minutes=-5)
    return starttime, endtime

def update_traffic_data(config):
    starttime, endtime = get_starttime_endtime()    
    result = get_today_traffic(config, starttime, endtime)
    if result.status_code == 200:
        data = result.json()
        record = data["data"][-1]
        edge_volume = record["edgeBitsPerSecond"]
        if edge_volume != "N/A":
            EDGEBYTES.set(edge_volume)
            EDGEHITS.set(record["edgeHitsPerSecond"])
            ORIGINBYTES.set(record["originBitsPerSecond"])
            ORIGINHITS.set(record["originHitsPerSecond"])
            BYTESOFFLOAD.set(record["bytesOffload"])
            HITSOFFLOAD.set(record["hitsOffload"])

def get_config_account_from_yaml_file(yaml_file):
    with open(yaml_file, 'r') as yml:
        config = yaml.load(yml, Loader=yaml.BaseLoader)
        return config

if __name__ == '__main__':
    config_file = sys.argv[1]
    port = int(sys.argv[2])
    
    config = get_config_account_from_yaml_file(config_file)

    start_http_server(port)
    
    while True:
        update_traffic_data(config)
        time.sleep(60)






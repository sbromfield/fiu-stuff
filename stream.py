import requests
import sys
import argparse
import json

parser = argparse.ArgumentParser(description='Start/stop Vidiu streamer')
parser.add_argument('-ip',required = True, help='host name or ip of streamer')
parser.add_argument('-a',required = True, help='action you would like to complete')
parser.add_argument('-p', help='password')
args = parser.parse_args()

url = 'http://' + args.ip + '/cgi-bin/api.cgi'
apiurl = 'http://' + args.ip + '/api/system'
jsonurl = 'http://' + args.ip + '/cgi-bin/json.cgi?command=geti&_=0'
s = requests.Session()

#check if we have a custom password
if(args.p is not None):
  payload= {'user': 'admin', 'passwd': args.p, 'command':'login'}
else:
  payload= {'user': 'admin', 'passwd': 'admin', 'command':'login'}

#log in
try:
  s.headers.update({'referer':'http://' + args.ip + '/'})
  r = s.post(url, data=payload)
except requests.exceptions.RequestException:
  print "Host not reachable."
  sys.exit(-1)

if "Invalid password" in r.text:
  print "Bad password"
  sys.exit(-1)

#send commands to the device
#need to rewrite this with functions and a main
if args.a == "start":
  s.get(apiurl + '?command=broadcast&action=publish&notify_followers=0&preview=0&_=0')
elif args.a == "stop":
  s.get(apiurl + '?command=broadcast&action=teardown&_=0')
elif args.a == "status":
  try:
    r = s.post(url, data=payload)
    s.headers.update({'referer':'http://' + args.ip + '/'})
  
    result = s.post(apiurl, {'command':'status'}, cookies={'passwordChanged':'True', 'fw_ver':'1.3.0',
      'serenity-session':s.cookies['serenity-session']})
    jfile = result.json()
    print( "Video input: " + jfile["status"]["Video-Input"] 
        + "\n Broadcast State: " + jfile["status"]["Broadcast-State"] 
        + "\n Errors: " +  jfile["status"]["Broadcast-Error"] 
        +"\n Power: " +  jfile["status"]["System-Power"] 
        + "\n Codec state: " +  jfile["status"]["Codec-State"])
  except requests.exceptions.RequestException:
      print "Request problem."
      sys.exit(-1)
elif args.a == "input":
  try:
    r = s.post(url, data=payload)
    s.headers.update({'referer':'http://' + args.ip + '/'})
    result = s.post(apiurl, {'command':'status'}, cookies={'passwordChanged':'True', 'fw_ver':'1.3.0',
      'serenity-session':s.cookies['serenity-session']})
    jfile = result.json()
    print( "Video input: " + jfile["status"]["Video-Input"]) 
  except requests.exceptions.RequestException:
    print "Request problem."
    sys.exit(-1)

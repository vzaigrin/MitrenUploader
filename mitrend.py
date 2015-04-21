import sys
import argparse
import configparser
import requests         # install it with 'pip install requests'

requests.packages.urllib3.disable_warnings() 

xstr = lambda s: '' if s is None else str(s)

# Parsing command-line options

parser = argparse.ArgumentParser(description='EMC Mitrend Upload')
parser.add_argument('-c','--config',dest='config',action='store',help='configuration file',required=True)
parser.add_argument('-v',dest='verbose',action='store_true',help='verbose mode')
args = parser.parse_args()

# Reading and checking configuration file

config = { 'user': ['username','password'], 'assessment': ['assessment_name','company','city','country'], 'files': ['device_type','file'] } 

cfg = configparser.ConfigParser()
cfg.read(args.config)

for sec in config.keys():
    if not cfg.has_section(sec):
        sys.exit("Error: configuration file " + args.config + " doesn't have section \'" + sec +"\'")
    for opt in config[sec]:
        if not opt in [option for option in cfg[sec]]:
            sys.exit("Error: section \'" + sec + "\' doesn't have option \'" + opt + "\'")

username = cfg.get('user','username')
password=cfg.get('user','password')
aname=cfg.get('assessment','assessment_name')
company=cfg.get('assessment','company')
city=cfg.get('assessment','city')
country=cfg.get('assessment','country')
dtype= cfg.get('files','device_type')
file= cfg.get('files','file')

if 'state' in cfg['assessment']:  data['state']=cfg.get('assessment','state')
if 'timezone' in cfg['assessment']:  data['timezone']=cfg.get('assessment','timezone')

# Prepare parameters for calls

baseurl = 'https://app.mitrend.com/api/assessments'

# Create an assessment

data = { 'assessment_name':aname, 'company':company, 'city':city, 'country':country }
resp = requests.post(baseurl,auth=(username,password),data=data) 

if ( resp.status_code != requests.codes.ok ):
    sys.exit( "Error in creating an assessment: %d %s" % (resp.status_code,xstr(resp.json())) )

if args.verbose:
   print("\nResponse status: " + str(resp.status_code))
   print("Response: " + xstr(resp.json()))

id = resp.json()['id']

# Adding files

device = { 'device_type':dtype }
files = { 'file': open(file,'rb') }
resp = requests.post(baseurl+'/'+str(id)+'/files',auth=(username,password),data=device,files=files)

if ( resp.status_code != requests.codes.ok ):
    sys.exit( "Error in adding files: %d %s" % (resp.status_code,xstr(resp.json())) )

if args.verbose:
   print("\nResponse status: " + str(resp.status_code))
   print("Response: " + xstr(resp.json()))

# Submitting an assessment

resp = requests.post(baseurl+'/'+str(id)+'/submit',auth=(username,password))

if ( resp.status_code != requests.codes.ok ):
    sys.exit( "Error in submitting an assessment: %d %s" % (resp.status_code,xstr(resp.json())) )

if args.verbose:
   print("\nResponse status: " + str(resp.status_code))
   print("Response: " + xstr(resp.json()))

if args.verbose:
   print("\nAll done")

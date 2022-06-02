import requests
import json
URL = "http://bioinf.uab.es/aggrescan/"
BIN_URL = "http://bioinf.uab.es/cgi-bin/aap/aap_ov.pl"

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
# input_handle = open("/home/meng/sst-project/Kphaffii-host-protein/fasta/GQ67_00001.fasta","r")
# content = input_handle.readlines()
# raw_data = ""
# for line in  content:
#     raw_data = raw_data + line
# raw_data = raw_data[:-1]


fasta_data = ">GQ67_00001FNRKDVRDRHYRRHAADISDNSLGSGPHTISIVGKRTDENTNPIEAQSIESLELMSSTPLTPKSITYSTQKQYHVVQTPKFILGNLICTGRIFGINGRKGSIPQTTTDQTHHAIRNVCDVLREAKASLDEVIRVSVFLVCLEECTAVQSICSQYFPDGAVYDFIHIKFSPGNALGAIASGW"

data = {"sequence":fasta_data}

res = requests.post(BIN_URL, data=data)
print(res.text)

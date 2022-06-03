from matplotlib.pyplot import sca
import requests
import json
import wget
import os
from tqdm import tqdm

outputFolder = "output-protscale"

def get_output(fasta_file,sequence,scale):
    URL = "https://web.expasy.org/cgi-bin/protscale/protscale.pl?1"
    data = {'sequence': sequence,
            'scale': scale,
            'window': 9,
            'weight_edges': 100,
            'weight_var': 'linear',
            'norm': 'no'
            }

    res = requests.post(URL, data=data)
    # print(res.text)

    fileToWrite = open("page_source.html", "w")
    fileToWrite.write(res.text)
    fileToWrite.close()

    fileToRead = open("page_source.html", "r")
    download_url = ""
    for line in fileToRead.readlines():
        if "Numerical format (verbose)" in line:
            download_url = "https://web.expasy.org" + line.split("\"")[1]
            print(download_url)
            break
    fileToRead.close()
    outputfileName = fasta_file+"-"+scale+".txt"
    outputfileName = outputfileName.replace(" ", "")
    outputfileName = outputfileName.replace("/", "")
    outputfileName = outputfileName.replace("&", "")
    if download_url == "":
        return -1
    else:
        wget.download(download_url,os.path.join(outputFolder,outputfileName))
        return 1


# get_output("a","FNRKDVRDRHYRRHAADISDNSLGSGPHTISIVGKRTDENTNPIEAQSIESLELMSSTPLTPKSITYSTQKQYHVVQTPKFILGNLICTGRIFGINGRKGSIPQTTTDQTHHAIRNVCDVLREAKASLDEVIRVSVFLVCLEECTAVQSICSQYFPDGAVYDFIHIKFSPGNALGAIASGW",'Hphob. / Kyte & Doolittle')

def main():

    scale_handle = open("scale_list.txt","r")
    file_content = scale_handle.readlines()

    scale_list = []
    for line in file_content:

        scale_list.append(line[:-1])


    fasta_dir = "/home/meng/sst-project/Kphaffii-host-protein/fasta"
    fasta_files = os.listdir(fasta_dir)

    output_files = os.listdir(fasta_dir+"-output")
    

    error_file = open("error.txt","w")
    for fasta_file in tqdm(fasta_files):
        fasta_name = fasta_file[:-6]

        if fasta_name+".xls" in output_files:
            continue
        if fasta_file.endswith("prot"):
            continue
        file_dir = os.path.join(fasta_dir,fasta_file)
        fasta_handle = open(file_dir,"r")
        file_content = fasta_handle.readlines()
        sequence = file_content[1]
        if sequence[-1] == "*":
            sequence = sequence[:-1]
        fasta_handle.close()
        
        # print(sequence)
        
        for scale in scale_list:
            ret_val = get_output(fasta_name,sequence,scale)
            if ret_val == -1:
                error_file.write(fasta_name + ":" + scale + "\n")
    
    error_file.close()
main()
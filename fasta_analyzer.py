from matplotlib.pyplot import sca
import requests
import json
import urllib.request
from multiprocessing import Pool, cpu_count
import os
from tqdm import tqdm
from multiprocessing import Process
from functools import partial
import uuid


outputFolder = "output-protscale"
error_file = open("error_2.txt","w")

num_cpu = cpu_count()

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


    unique_filename = str(uuid.uuid4()) +".html"

    fileToWrite = open(unique_filename, "w")
    fileToWrite.write(res.text)
    fileToWrite.close()

    fileToRead = open(unique_filename, "r")
    download_url = ""
    for line in fileToRead.readlines():
        if "Numerical format (verbose)" in line:
            download_url = "https://web.expasy.org" + line.split("\"")[1]
            # print(download_url)
            break
    fileToRead.close()
    os.remove(unique_filename)

    outputfileName = fasta_file+"-"+scale+".txt"
    outputfileName = outputfileName.replace(" ", "")
    outputfileName = outputfileName.replace("/", "")
    outputfileName = outputfileName.replace("&", "")
    outputfileName = outputfileName.replace("%", "")
    if download_url == "":
        error_file.write(fasta_file + ":" + scale + "\n")
    else:
        urllib.request.urlretrieve(download_url, os.path.join(outputFolder,outputfileName))


# get_output("a","FNRKDVRDRHYRRHAADISDNSLGSGPHTISIVGKRTDENTNPIEAQSIESLELMSSTPLTPKSITYSTQKQYHVVQTPKFILGNLICTGRIFGINGRKGSIPQTTTDQTHHAIRNVCDVLREAKASLDEVIRVSVFLVCLEECTAVQSICSQYFPDGAVYDFIHIKFSPGNALGAIASGW",'Hphob. / Kyte & Doolittle')

def main():
    to_process_list = []
    scale_handle = open("scale_list.txt","r")
    file_content = scale_handle.readlines()

    scale_list = []
    for line in file_content:

        scale_list.append(line[:-1])


    fasta_dir = "/home/meng/sst-project/Kphaffii-host-protein/fasta"

    fasta_files = os.listdir(fasta_dir)

    output_files = os.listdir(outputFolder)
    

    for fasta_file in tqdm(fasta_files):
        target_list = []
        fasta_name = fasta_file[:-6]

        # if fasta_name+".xls" in output_files:
        #     continue
        if fasta_file.endswith("prot"):
            error_file.write("[prot-file]: " + fasta_file + "\n")
            error_file.flush()
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
            outputfileName = fasta_name+"-"+scale+".txt"
            outputfileName = outputfileName.replace(" ", "")
            outputfileName = outputfileName.replace("/", "")
            outputfileName = outputfileName.replace("&", "")
            outputfileName = outputfileName.replace("%", "")
            # print("\n\n\n\n")
            # print(outputfileName)
            # print(output_files)
            # exit()
            if outputfileName in output_files:
                error_file.write(outputfileName + " exists\n")
                error_file.flush()
                continue
            to_process_list.append((fasta_name,sequence,scale))
            
            # print(to_process_list)
            # print("-------------------")
    
    pool = Pool(cpu_count()-1)
    
    results = tqdm(pool.starmap(get_output,to_process_list),total=len(to_process_list))
    pool.close()
    pool.join()
    
    error_file.close()
main()
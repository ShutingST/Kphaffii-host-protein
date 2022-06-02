from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time

from selenium.webdriver.firefox.options import Options
from tqdm import tqdm
import os
import wget


# fasta_data = ">GQ67_00001\nFNRKDVRDRHYRRHAADISDNSLGSGPHTISIVGKRTDENTNPIEAQSIESLELMSSTPLTPKSITYSTQKQYHVVQTPKFILGNLICTGRIFGINGRKGSIPQTTTDQTHHAIRNVCDVLREAKASLDEVIRVSVFLVCLEECTAVQSICSQYFPDGAVYDFIHIKFSPGNALGAIASGW"
def main():
    fasta_dir = "/home/meng/sst-project/Kphaffii-host-protein/fasta"
    fasta_files = os.listdir(fasta_dir)

    output_files = os.listdir(fasta_dir+"-output")
    

    error_file = open("error.txt","w")
    for fasta_file in tqdm(fasta_files):
        fasta_name = fasta_file[:-6]

        if fasta_name+".xls" in output_files:
            continue

        file_dir = os.path.join(fasta_dir,fasta_file)
        fasta_handle = open(file_dir,"r")
        file_content = fasta_handle.read()
        if file_content[-1] == "*":
            file_content = file_content[:-1]
        fasta_handle.close()
        # print(file_content)
        download_url = get_url(file_content)
        
        if download_url == "":
            error_file.write(fasta_file + "\n")
            error_file.flush()
        else:
            download_file(download_url,os.path.join(fasta_dir+"-output",fasta_name+".xls"))
        
        # break
    
    error_file.close()




def download_file(url,fileName):
    response = wget.download(url, fileName)

def get_url(fasta_data):
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    link1 = 'http://bioinf.uab.es/aggrescan/'
    browser.get(link1)
    browser.find_element(by=By.XPATH, value="//textarea[@width='95%']").send_keys(fasta_data)
    browser.find_element(by=By.XPATH, value="//input[@value='submit!']").click() 
    time.sleep(2)


    pageSource = browser.page_source
    fileToWrite = open("page_source.html", "w")
    fileToWrite.write(pageSource)
    fileToWrite.close()
    fileToRead = open("page_source.html", "r")
    download_url = ""
    for line in fileToRead.readlines():
        # print(line)
        # print("---------------")

        if "txt.xls" in line:
            download_url = line.split("\"")[7]
            # print(download_url)
            break
    fileToRead.close()
    browser.quit()
    return download_url
# browser.find_element_by_xpath('//a[contains(@href,"href")]').click()

main()
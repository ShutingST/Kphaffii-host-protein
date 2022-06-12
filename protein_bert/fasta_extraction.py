import os
from Bio import SeqIO

from snapgene_reader import snapgene_file_to_dict, snapgene_file_to_seqrecord

src_fasta_dir = "/home/meng/sst-project/Kphaffii-host-protein/fasta"

output_file = open("fasta.csv","w")
output_file.write("label,seq\n")
log_file = open("log.txt","w")

max_length = 0
# print(len(os.listdir(src_fasta_dir)))
for fasta_file in os.listdir(src_fasta_dir):
    

    full_fasta_path = os.path.join(src_fasta_dir,fasta_file)
    
    if fasta_file.endswith("prot"):
        # print(full_fasta_path)
        prot_file = open(full_fasta_path,"rb")
        file_content = prot_file.readlines()
        sequence_name = file_content[4].decode('utf-8')[:-1].replace("<Description>","").replace("</Description>","")

        target_line = max(file_content, key=len)
        # if(sequence_name == "GQ67_00328"):
        #     print("-----------------------")
        #     print(target_line)
        target_line = target_line.split(b'\x00')
        target_line = [x for x in target_line if not b'<' in x]
        # if(sequence_name == "GQ67_00328"):
        #     print("-----------------------")
        #     print(target_line)
        sequence = max(target_line,key=len).split(b'*')[0].decode('utf-8')
        # if(sequence_name == "GQ67_00328"):
        #     print("-----------------------")
        #     print(sequence)
        # print(sequence)

        prot_file.close()
        if sequence[-1] == "*":
            sequence = sequence[:-1]
        output_file.write(sequence_name + "," + sequence + "\n")
        
    else:
        fasta_handle = open(full_fasta_path,"r")
        file_content = fasta_handle.readlines()

        sequence_name = file_content[0][1:-1]

        sequence = file_content[1]
        if sequence[-1] == "*":
            sequence = sequence[:-1]
        
        fasta_handle.close()

        if len(sequence) > max_length:
            max_length = len(sequence)

        output_file.write(sequence_name + "," + sequence + "\n")

output_file.close()

print(max_length)



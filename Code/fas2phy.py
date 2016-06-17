import sys
import re
import string
import time


if len(sys.argv) != 3:
    print "Usage: python fas2phy.py [input fasta] [output phylip]" 
    sys.exit (1)

startTime = time.time()

input = open(sys.argv[1], 'r')
output = open(sys.argv[2], 'w')

num_seq = 0
length_seq = 0
seq = []
lines = []

for line in input:
    line = line.strip()
    if line != '':
        lines.append(line)

num_seq = len(lines)/2
output.write(str(num_seq))

for n in range(0,num_seq):
    if n == 0:
        length_seq = len(lines[1])
        output.write(' '+str(length_seq)+'\n')   
    name_line = lines[2*n]
    seq_line = lines[2*n+1]
    if name_line.startswith('>'):
        if len(name_line[1:]) >= 10:
            new_name = name_line[1:10]
            output.write(new_name+' '+seq_line+'\n')
        else:
            name_length = len(name_line[1:])
            delta = 10-name_length
            output.write(name_line[1:]+' '*delta+seq_line+'\n')

output.close()

endTime = time.time()
workTime =  endTime - startTime

print 'fas2phy.py took',str(workTime),'s'
print 'Erica is a genius!'

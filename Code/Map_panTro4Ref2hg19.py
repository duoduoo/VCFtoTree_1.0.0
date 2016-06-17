# python Map_panTro4Ref2hg19.py chr22.hg19.panTro4.net.axt 22 26767000 26768000 panTro4Ref_hg19.fa

import sys
import re
import string
import time


if len(sys.argv) != 6:
    print "Usage: python Map_panTro4Ref2hg19.py chr22.hg19.panTro4.net.axt 22 26767000 26768000 panTro4Ref_hg19.fa" 
    sys.exit (1)

startTime = time.time()

input = open(sys.argv[1], 'r')
chr = int(sys.argv[2])
start = int(sys.argv[3])
end = int(sys.argv[4])
output = open(sys.argv[5], 'w')

hg19 = []
panTro4 = []
mapping_dic = {}
input_lines = []

for line in input:
    line = line.strip()
    if line.startswith('#'):
        continue
    if line != '':
        input_lines.append(line)

num = len(input_lines)

for i in range(0,num):
    if i%3 == 0 or i%3 == 3:
        head = input_lines[i] 
        head_f = head.split(' ')
        hg19_cor = head_f[1]+','+head_f[2]+','+head_f[3]
        panTro4_cor = head_f[4]+','+head_f[5]+','+head_f[6]
        mapping_dic[hg19_cor] = panTro4_cor
        
        #print int(head_f[3])-int(head_f[2])+1, len(input_lines[i+1]), len(input_lines[i+2])
        hg19.append((hg19_cor,input_lines[i+1]))
        panTro4.append((panTro4_cor,input_lines[i+2]))


hg19_seq = []
panTro4_seq = []


for n in range(0,num/3):
    if n == 0:
        loc00 = hg19[n][0].split(',')
        start00 = int(loc00[1])
        hg19_start = start00
        end00 = int(loc00[2])
        
        len_wgap0 = len(hg19[n][1])
        if not end00-start00+1 == len_wgap0:
            if not '-' in hg19[n][1]:
                print end00-start00+1, len_wgap0
                print start00, end00
                print hg19[n][0]
                print hg19[n][1]
                print 'no - in it, sth wrong.'
            hg19_temp0 = []
            panTro4_temp0 = []
            for x0 in range(0,len_wgap0):
                if not hg19[n][1][x0] == '-':  # remove gaps
                    hg19_temp0.append(hg19[n][1][x0])
                    panTro4_temp0.append(panTro4[n][1][x0])
            hg19_seq.append(''.join(hg19_temp0))
            panTro4_seq.append(''.join(panTro4_temp0))
        else:
            hg19_seq.append(hg19[n][1])
            panTro4_seq.append(panTro4[n][1])
        continue
    
    else:
        loc0 = hg19[n-1][0].split(',')
        start0 = int(loc0[1])
        end0 = int(loc0[2])
        
        loc1 = hg19[n][0].split(',')
        start1 = int(loc1[1])
        end1 = int(loc1[2])
        
        len_wgap = len(hg19[n][1])
        if not end1-start1+1 == len_wgap:
            if not '-' in hg19[n][1]:
                print end1-start1+1, len_wgap
                print start1, end1
                print hg19[n][0]
                print hg19[n][1]
                print 'no - in it, sth wrong.'
            hg19_temp = []
            panTro4_temp = []
            for x in range(0,len_wgap):
                if not hg19[n][1][x] == '-':  # remove gaps
                    hg19_temp.append(hg19[n][1][x])
                    panTro4_temp.append(panTro4[n][1][x])
            #print end1-start1+1, len(''.join(hg19_temp))
            
            delta = start1 - end0
            if delta >= 0:
                hg19_seq.append('-'*(delta-1)+''.join(hg19_temp))
                panTro4_seq.append('-'*(delta-1)+''.join(panTro4_temp))
            else:
                print 'SB...= ='
            
        else:
            delta = start1 - end0
            if delta >= 0:
                hg19_seq.append('-'*(delta-1)+''.join(hg19[n][1]))
                panTro4_seq.append('-'*(delta-1)+''.join(panTro4[n][1]))
            else:
                print 'SB...= ='
         
        if n == num/3-1:
            hg19_end = end1


print hg19_start, hg19_end, start, end
print len(''.join(hg19_seq)), len(''.join(panTro4_seq))

if int(start) >= int(hg19_start) and int(end) <= int(hg19_end):
    final_start_point = start-hg19_start
    final_end_point = end-hg19_start+1
    final_panTro4_seq = ''.join(panTro4_seq)
    final_hg19_seq = ''.join(hg19_seq)
    
    output.write('>panTro4_Chr'+str(chr)+':'+str(start)+'-'+str(end)+'\n')
    output.write(final_panTro4_seq[final_start_point:final_end_point]+'\n')
    #output.write('>hg19_REF\n')
    #output.write(final_hg19_seq[final_start_point:final_end_point])
    
    #print len(final_panTro4_seq[final_start_point:final_end_point])
    #print end - start +1
else:
    print 'SB'
    


output.close()

endTime = time.time()
workTime =  endTime - startTime

print 'Total time used:', str(workTime),'s'
print 'Erica is a genius!'

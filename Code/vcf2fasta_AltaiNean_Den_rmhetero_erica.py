# input is vcf file, and a reference sequence to the interested region
# This script works specifically for Altai Neanderthal and Denisovan vcf files
# Their vcf file contains every single sites, and only one individual, and unphased.
# genotypes are as:
# ./.   0/0   1/1   0/1
# output is file with their sequence
# error is the output of structural variations
# This code use a reference sequence, transform vcf file to an aligned fasta file.
# It fixed the error that INDELs can have alternative allele 2 now.
# remove 0/1 or 1/0 as "N"
# This version will output only one consensus sequence.
# Usage: python vcf2fasta_AltaiNean_Den_erica.py yourvcffile.vcf reference_sequence.fa 111111 222222 aligned_fasta.fa error_sv
# phase3 2504, phase1 1092

import sys
import re
import string
import collections   #for sorting the dic by key

if len(sys.argv) != 7:
    print "Usage: python vcf2fasta_AltaiNean_Den_erica.py [inputvcf] [Reference sequence] [start] [end] [output] [error]"
    sys.exit (1)
    
input = open(sys.argv[1], 'r')
ref_seq = open(sys.argv[2], 'r')
start = int(sys.argv[3])
end = int(sys.argv[4])
output = open(sys.argv[5], 'w')
error = open(sys.argv[6], 'w')   #output structural variation (VT=SV) as ERROR message.

haplo = {}
freq = {}
all_haplo = {}   #summary/final haplotype sequence dic for everyone
input2 = []    #a cleaner vcf without header, without SV, and indels already aligned with "--"


r_seq = []
for r0 in ref_seq:
    r1 = r0.replace('\n','')
    if r1.startswith('>'):
        continue
    r_seq.append(r1)
r = ''.join(r_seq)   #reference sequence without '\n'

#output.write('>reference_hg19\n'+r+'\n')

ref_bs = {}    #ref_seq dictionary file
count = 0
while count <= (len(r)-1):
    ref_bs[str(start+count)] = r[count]
    count = count + 1
#for r in ref_bs.keys():
#    ref_bs[int(r)] = ref_bs[r]
#    del ref_bs[r]
#ref_bs = collections.OrderedDict(sorted(ref_bs.items()))  #sort reference sequence
#print ref_bs

for l0 in input:
    l = l0.replace('\n','')
    if l.startswith('##'):
        continue
    elif l.startswith('#C'):
        id = []
        id = l.split('\t')     #id[9] - id[2062] are the individual id (PHASE3); id[9] - id[1100] phase1
        continue
    info0 = []
    gt0 = []
    gt0 = l.split('\t')
#    info0 = gt0[7].split(';')

    if len(gt0[3]) > 1:
        error.write(l + '\n')
    elif len(gt0[4]) > 1:
        cnt_alt = gt0[4].split(',')
        if len(cnt_alt) <= 1:
            error.write(l + '\n')
    else:
        input2.append(l)


n = 1
while n <= 1:    #phase3 2504, phase1 1092, n is the number of individuals, then this number is n
    dic_psn1 = {}    #variation/sequence dictionary for each individual, initial value is same as ref_bs
    dic_psn2 = ref_bs    #everyone has two dic for two haplotypes respectably
    for k1 in ref_bs.keys():    #.keys() would introduce a iteration
        dic_psn1[k1+'_1'] = ref_bs[k1]
    #print dic_psn1
    for line in input2:
        gt = []
        gt = line.split('\t')
        pos = gt[1]   #position is gt[1]
        if any(',' in gt[4] for c in gt[4]):
            alter = gt[4].split(',')
            if gt[8+n][0] == '0':
                gt1 = gt[3]
            elif gt[8+n][0] == '1':
                gt1 = alter[0] # gt[4][0]
            elif gt[8+n][0] == '2':
                gt1 = alter[1] # gt[4][2]
            elif gt[8+n][0] == '.':
                gt1 = 'N'
            if gt[8+n][2] == '0':
                gt2 = gt[3]
            elif gt[8+n][2] == '1':
                gt2 = alter[0] # gt[4][0]
            elif gt[8+n][2] == '2':
                gt2 = alter[1] # gt[4][2]
            elif gt[8+n][2] == '.':
                gt2 = 'N'
        else:
            if gt[8+n][0:3] == '0/0':
                gt1 = gt[3]
                gt2 = gt[3]
            elif gt[8+n][0:3] == '1/0':
                gt1 = 'N' #gt[4]
                gt2 = 'N' #gt[3]
            elif gt[8+n][0:3] == '0/1':
                gt1 = 'N' #gt[3]
                gt2 = 'N' #gt[4]
            elif gt[8+n][0:3] == '1/1':
                gt1 = gt[4]
                gt2 = gt[4]
            elif gt[8+n][0:3] == './.':
                gt1 = 'N'
                gt2 = 'N'
            else:
                print 'error'

        dic_psn1[pos+'_1'] = gt1
        dic_psn2[pos] = gt2


    haplotype1 = []
    haplotype2 = []
    dic_psn1_sorted = collections.OrderedDict(sorted(dic_psn1.items()))
    dic_psn2_sorted = collections.OrderedDict(sorted(dic_psn2.items()))
    for p in dic_psn1_sorted:
        haplotype1.append(dic_psn1_sorted[p])
    for q in dic_psn2_sorted:
        haplotype2.append(dic_psn2_sorted[q])
    all_haplo[id[n+8] + '.1'] = ''.join(haplotype1)
    all_haplo[id[n+8] + '.2'] = ''.join(haplotype2)
    n = n + 1

for j in sorted(all_haplo):     #another easier way to sorted a dictionary by key, only contain key
    #print '>'+j
    #print all_haplo[j]+'\n'
    output.write('>'+j+'\n')
    output.write(all_haplo[j]+'\n')
    break  # only output one, delete break will output .1 .2, they are the same though



print '                .-._                               '
print '               {_}^ )o                             '
print '      {\________//~`     My mommy is a genius!     '
print '       (         )                -- Cabernet      '
print '       /||~~~~~||\                                 '
print '      |_\\\\_    \\\_\\_                           '
print '      \"\' \"\"\'    \"\"\'\"\'                    '


output.close()
error.close()
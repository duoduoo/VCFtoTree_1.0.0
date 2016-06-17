# input is vcf file, and a reference sequence to the interested region
# output is file with aligned haplotypes for all the 2504 individuals
# error is the output of structural variations
# Same function as Pavlos perl script
# This code use a reference sequence, transform vcf file to an aligned fasta file.
# It fixed the error that INDELs can have alternative allele 2 and 3 now.
# It can process "VT=SNP,INDEL" this kind of weirdo now.
# Usage: python vcf2fasta_erica.py yourvcffile.vcf reference_sequence.fa 111111 222222 aligned_fasta.fa error_sv
# phase3 2504, phase1 1092

# Fixed repetitive locus with the same chromosome location;
# Fixed the deleting INDELs, it will substitute the reference with "-".
# fixed multi-allelic indels.

import sys
import re
import string
import collections  # for sorting the dic by key
import time
import datetime


startTime = time.time()

if len(sys.argv) != 7:
    print "Usage: python vcf2fasta_erica.py [inputvcf] [Reference sequence] [start] [end] [output] [error]"
    sys.exit(1)

input = open(sys.argv[1], 'r')
ref_seq = open(sys.argv[2], 'r')
start = int(sys.argv[3])
end = int(sys.argv[4])
output = open(sys.argv[5], 'w')
error = open(sys.argv[6], 'w')  # output structural variation (VT=SV) as ERROR message.

haplo = {}
freq = {}
all_haplo = {}  # summary/final haplotype sequence dic for everyone
input2 = []  # a cleaner vcf without header, without SV, and indels already aligned with "--"

r_seq = []
for r0 in ref_seq:
    r1 = r0.replace('\n', '')
    if r1.startswith('>'):
        continue
    r_seq.append(r1)
r = ''.join(r_seq)  # reference sequence without '\n'

# output.write('>reference_hg19\n'+r+'\n')

ref_bs = {}  # ref_seq dictionary file
count = 0
while count <= (len(r) - 1):
    ref_bs[str(start + count)] = r[count]
    count = count + 1
# for r in ref_bs.keys():
#    ref_bs[int(r)] = ref_bs[r]
#    del ref_bs[r]
# ref_bs = collections.OrderedDict(sorted(ref_bs.items()))  #sort reference sequence
# print ref_bs


input_temp = []
for line in input:
    line = line.strip()
    if line.startswith('##'):
        continue
    elif line.startswith('#C'):
        id = []
        id = line.split('\t')  # id[9] - id[2062] are the individual id (PHASE3); id[9] - id[1100] phase1
        continue
    input_temp.append(line)

# check if this line locus are the same with the previous one, combining two same locus
input_cnt = 0
while input_cnt <= len(input_temp) - 1:

    l_now = input_temp[input_cnt]
    info_now = []
    if 'VT=SV' in l_now:
        input_temp.remove(input_temp[input_cnt])
        error.write(l_now + '\n')
        continue

    gt_now = []
    gt_now = l_now.split('\t')

    gt_pre = []
    l_pre = input_temp[input_cnt - 1]
    gt_pre = l_pre.split('\t')

    if not ',' in gt_pre[4]:
        cnt_comma = 0
    else:
        cnt_comma = 1

    if gt_pre[1] == gt_now[1]:
        if gt_now[3] != gt_pre[3]:
            if len(gt_pre[3]) <= len(gt_now[3]):
                delta_temp = len(gt_now[3]) - len(gt_pre[3])
                gt_pre[4] = gt_pre[4] + gt_now[3][-delta_temp:]
                gt_pre[3] = gt_now[3]

        gt_pre[2] = ','.join([gt_pre[2], gt_now[2]])
        gt_pre[4] = ','.join([gt_pre[4], gt_now[4]])

        gt_now_gtonly = '\t'.join(gt_now[9:])

        if cnt_comma == 0:
            replaced = gt_now_gtonly.replace('1', '2')
            gt_now[9:] = replaced.split('\t')
        else:
            replaced = gt_now_gtonly.replace('1', '3')
            gt_now[9:] = replaced.split('\t')

        m = 1
        while m <= 2504:
            new_gt1 = max(gt_pre[8 + m][0], gt_now[8 + m][0])
            new_gt2 = max(gt_pre[8 + m][-1], gt_now[8 + m][-1])
            gt_pre[8 + m] = new_gt1 + '|' + new_gt2
            m += 1

        # gt_pre[7].replace('VT=SNP','VT=SNP,INDEL')
        info_pre = gt_pre[7].split(';')
        for y in info_pre:
            if y == 'VT=SNP':
                gt_pre[7] = gt_pre[7].replace('VT=SNP', 'VT=SNP,INDEL')
            elif y == 'VT=INDEL':
                gt_pre[7] = gt_pre[7].replace('VT=INDEL', 'VT=SNP,INDEL')
            elif y == 'VT=SNP,INDEL':
                gt_pre[7] = gt_pre[7]  # .replace('VT=INDEL,INDEL', 'VT=SNP,INDEL')

        input_temp[input_cnt - 1] = '\t'.join(gt_pre)
        input_temp.remove(input_temp[input_cnt])
    else:
        # print input_cnt, len(input_temp)
        input_cnt += 1

input2 = []

for l in input_temp:

    info0 = []
    gt0 = []
    gt0 = l.split('\t')

    info0 = gt0[7].split(';')
    for x in info0:
        if x.startswith('VT='):
            vt = x
            if vt == 'VT=SV':
                error.write(l + '\n')
            elif vt == 'VT=SNP,INDEL':
                if not any(',' in gt0[4] for c0 in gt0[4]):
                    delta = len(gt0[3]) - len(gt0[4])
                    if delta > 0:
                        gt0[4] = gt0[4] + delta * '-'
                        l = '\t'.join(gt0)
                        input2.append(l)
                        error.write(l + '\n')
                    elif delta < 0:
                        gt0[3] = gt0[3] + (-delta * '-')
                        l = '\t'.join(gt0)
                        input2.append(l)
                        error.write(l + '\n')
                else:
                    alter0 = gt0[4].split(',')
                    num_alter = len(alter0)
                    if num_alter == 2:
                        max_len = max(len(gt0[3]), len(alter0[0]), len(alter0[1]))
                        delta_0 = max_len - len(gt0[3])
                        delta_1 = max_len - len(alter0[0])
                        delta_2 = max_len - len(alter0[1])
                        gt0[3] = gt0[3] + delta_0 * '-'
                        gt0[4] = alter0[0] + delta_1 * '-' + ',' + alter0[1] + delta_2 * '-'
                        l = '\t'.join(gt0)
                        input2.append(l)
                        error.write(l + '\n')
                    elif num_alter == 3:
                        max_len = max(len(gt0[3]), len(alter0[0]), len(alter0[1]), len(alter0[2]))
                        delta_0 = max_len - len(gt0[3])
                        delta_1 = max_len - len(alter0[0])
                        delta_2 = max_len - len(alter0[1])
                        delta_3 = max_len - len(alter0[2])
                        gt0[3] = gt0[3] + delta_0 * '-'
                        gt0[4] = alter0[0] + delta_1 * '-' + ',' + alter0[1] + delta_2 * '-' + ',' + alter0[
                            2] + delta_3 * '-'
                        l = '\t'.join(gt0)
                        input2.append(l)
                        error.write(l + '\n')
                    else:
                        print alter0
                        print "Please go to find Erica..."

            elif vt == 'VT=INDEL':
                if not any(',' in gt0[4] for c0 in gt0[4]):
                    delta = len(gt0[3]) - len(gt0[4])  # gt[3] is REF, gt[4] is ALT
                    if delta > 0:
                        gt0[4] = gt0[4] + delta * '-'
                        l = '\t'.join(gt0)
                        input2.append(l)
                        error.write(l + '\n')
                    elif delta < 0:
                        gt0[3] = gt0[3] + (-delta * '-')
                        l = '\t'.join(gt0)
                        input2.append(l)
                        error.write(l + '\n')
                else:
                    alter0 = gt0[4].split(',')
                    indel_cnt = len(alter0)
                    if indel_cnt == 2:
                        max_len = max(len(gt0[3]), len(alter0[0]), len(alter0[1]))
                        delta_0 = max_len - len(gt0[3])
                        delta_1 = max_len - len(alter0[0])
                        delta_2 = max_len - len(alter0[1])
                        gt0[3] = gt0[3] + delta_0 * '-'
                        gt0[4] = alter0[0] + delta_1 * '-' + ',' + alter0[1] + delta_2 * '-'
                    elif indel_cnt == 3:
                        max_len = max(len(gt0[3]), len(alter0[0]), len(alter0[1]), len(alter0[2]))
                        delta_0 = max_len - len(gt0[3])
                        delta_1 = max_len - len(alter0[0])
                        delta_2 = max_len - len(alter0[1])
                        delta_3 = max_len - len(alter0[2])
                        gt0[3] = gt0[3] + delta_0 * '-'
                        gt0[4] = alter0[0] + delta_1 * '-' + ',' + alter0[1] + delta_2 * '-' + ',' + alter0[
                            2] + delta_3 * '-'
                    elif indel_cnt == 4:
                        max_len = max(len(gt0[3]), len(alter0[0]), len(alter0[1]), len(alter0[2]), len(alter0[3]))
                        delta_0 = max_len - len(gt0[3])
                        delta_1 = max_len - len(alter0[0])
                        delta_2 = max_len - len(alter0[1])
                        delta_3 = max_len - len(alter0[2])
                        delta_4 = max_len - len(alter0[3])
                        gt0[3] = gt0[3] + delta_0 * '-'
                        gt0[4] = alter0[0] + delta_1 * '-' + ',' + alter0[1] + delta_2 * '-' + ',' + alter0[
                            2] + delta_3 * '-' + ',' + alter0[3] + delta_4 * '-'

                    l = '\t'.join(gt0)
                    input2.append(l)
                    error.write(l + '\n')
            elif vt == 'VT=SNP':
                input2.append(l)
            else:
                print vt
                print "Please go to find Erica..."
error.close()

n = 1
while n <= 2504:  # phase3 2504, phase1 1092
    #print n
    dic_psn1 = {}
    dic_psn2 = {}
    #dic_psn1 = ref_bs  # {}  # variation/sequence dictionary for each individual, initial value is same as ref_bs
    dic_psn2 = ref_bs  # everyone has two dic for two haplotypes respectably
    for k1 in ref_bs.keys():  # .keys() would introduce a iteration
        dic_psn1[k1 + '_1'] = ref_bs[k1]
    for line in input2:
        gt = []
        gt = line.split('\t')
        pos = gt[1]  # position is gt[1]

        if any(',' in gt[4] for c in gt[4]):
            alter = gt[4].split(',')
            if gt[8 + n][0] == '0':
                gt1 = gt[3]
            elif gt[8 + n][0] == '1':
                gt1 = alter[0]  # gt[4][0]
                # print gt1
            elif gt[8 + n][0] == '2':
                gt1 = alter[1]  # gt[4][2]
            elif gt[8 + n][0] == '3':
                gt1 = alter[2]  # gt[4][3]
            elif gt[8 + n][0] == '4':
                gt1 = alter[3]
            if gt[8 + n][2] == '0':
                gt2 = gt[3]
            elif gt[8 + n][2] == '1':
                gt2 = alter[0]  # gt[4][0]
            elif gt[8 + n][2] == '2':
                gt2 = alter[1]  # gt[4][2]
            elif gt[8 + n][2] == '3':
                gt2 = alter[2]  # gt[4][3]
            elif gt[8 + n][2] == '4':
                gt2 = alter[3]
        else:
            if gt[8 + n][0:3] == '0|0':
                gt1 = gt[3]
                gt2 = gt[3]
            elif gt[8 + n][0:3] == '1|0':
                gt1 = gt[4]
                gt2 = gt[3]
            elif gt[8 + n][0:3] == '0|1':
                gt1 = gt[3]
                gt2 = gt[4]
            elif gt[8 + n][0:3] == '1|1':
                gt1 = gt[4]
                gt2 = gt[4]
            else:
                print 'error'

        #if len(gt1) <= len(dic_psn1[pos+'_1']):
        #    continue

        #dic_psn1[pos] = gt1
        #dic_psn2[pos] = gt2
        #if n==1:
        #    print pos
        #    print dic_psn1['171117907_1']

        # deal with len(reference allele) > 1
        if len(gt[3]) > 1:
            if not '-' in gt[3]:
                len_ref = len(gt[3])
                for pos_key in range(int(pos), int(pos) + len_ref):
                    dic_psn1[str(pos_key)+'_1'] = gt1[pos_key - int(pos)]
                    dic_psn2[str(pos_key)] = gt2[pos_key - int(pos)]
            elif gt[3][1] == '-':
                dic_psn1[pos+'_1'] = gt1
                dic_psn2[pos] = gt2
            else:
                gap_cnt = gt[3].count('-')
                bp_cnt = len(gt[3]) - gap_cnt
                # print gap_cnt, bp_cnt
                for pos_key in range(int(pos), int(pos) + bp_cnt):
                    dic_psn1[str(pos_key)+'_1'] = gt1[pos_key - int(pos)]
                    dic_psn2[str(pos_key)] = gt2[pos_key - int(pos)]

                gt1_makeup = []
                gt2_makeup = []
                gt1_makeup = gt1[bp_cnt - 1:]
                gt2_makeup = gt2[bp_cnt - 1:]
                target_loc = str(int(pos) + bp_cnt - 1)
                dic_psn1[target_loc+'_1'] = gt1_makeup
                dic_psn2[target_loc] = gt2_makeup
        else:
            dic_psn1[pos+'_1'] = gt1
            dic_psn2[pos] = gt2

        #if pos == '171117899' and n ==1:
        #    print dic_psn1['171117907_1'], dic_psn2['171117907']

    #if n == 1:
        #print dic_psn1['171117907'+'_1'], dic_psn2['171117907']

    haplotype1 = []
    haplotype2 = []
    dic_psn1_sorted = collections.OrderedDict(sorted(dic_psn1.items()))
    dic_psn2_sorted = collections.OrderedDict(sorted(dic_psn2.items()))
    for p in dic_psn1_sorted:
        haplotype1.append(dic_psn1_sorted[p])
    for q in dic_psn2_sorted:
        haplotype2.append(dic_psn2_sorted[q])
    all_haplo[id[n + 8] + '.1'] = ''.join(haplotype1)
    all_haplo[id[n + 8] + '.2'] = ''.join(haplotype2)
    n += 1

for j in sorted(all_haplo):  # another easier way to sorted a dictionary by key, only contain key
    output.write('>' + j + '\n')
    output.write(all_haplo[j] + '\n')

endTime = time.time()
workTime = endTime - startTime

print 'Time used: {}'.format(str(datetime.timedelta(seconds=workTime)))
print 'Erica is a genius!'
output.close()

# python add_gap.py ALI_temp.fa error.txt [#start] ALI_othergenomes_wgap.fa

import sys
import re
import string
import time
import datetime

if len(sys.argv) != 6:
    print "Usage: python add_gap.py ALI_temp.fa error.txt [#start] [#end] ALI_othergenomes_wgap.fa"
    sys.exit(1)

startTime = time.time()

input = open(sys.argv[1], 'r')
errors = open(sys.argv[2], 'r')
start = int(sys.argv[3])
end = int(sys.argv[4])
output = open(sys.argv[5], 'w')

indels = []
for line in errors:
    line = line.strip()
    if 'INDEL' in line:
        fields = line.split('\t')
        ref = fields[3]
        alt = fields[4]
        loc = int(fields[1])
        if '-' in ref:
            indels.append([loc, ref, alt])
            #print [loc, ref, alt]

for sequence in input:
    sequence = sequence.strip()
    if sequence.startswith('>'):
        output.write(sequence + '\n')
        continue
    seq_len = len(sequence)
    # print seq_len
    seq_dic = {}
    for n in range(start, end + 1):
        seq_dic[n] = sequence[n - start]


    for indel in indels:
        order = indel[0]
        gap_cnt = indel[1].count('-')
        bp_cnt = len(indel[1]) - gap_cnt
        try:
            seq_dic[int(order)+bp_cnt-1] = seq_dic[int(order)+bp_cnt-1] + '-'*gap_cnt
        except KeyError:
            seq_dic[int(order)+bp_cnt-1] = ''
            seq_dic[int(order) + bp_cnt - 1] = seq_dic[int(order) + bp_cnt - 1] + '-' * gap_cnt

    for base in sorted(seq_dic):
        output.write(seq_dic[base])

    output.write('\n')

output.close()

endTime = time.time()
workTime = endTime - startTime

print 'Time used: {}'.format(str(datetime.timedelta(seconds=workTime)))
print 'Erica is a genius!'

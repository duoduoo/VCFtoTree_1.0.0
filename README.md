# VCFtoTree
Build phylogeny from [1000 Genomes] Phase 3 VCF file for 2504 individuals, also including ancient ([Neanderthal], [Denisovan]) and primate genomes.
[1000 Genomes]:http://www.1000genomes.org
[Neanderthal]:http://www.eva.mpg.de/neandertal/index.html
[Denisovan]:http://www.eva.mpg.de/denisova/index.html

VCF --> fasta sequence (whole sequence, not just variable sites) --> Phylogeny

We provide a user friendly interface, in which you can choose the genomes you want to add into the phylogeny.

Raw scripts can be found in **Code** folder.

#### Availability and requirement
VCFtoTree was designed for Mac OS users, has been tested on El Captian V10.11.5 with python 2.7.11

Here are the programs/packages needed to run the VCFtoTree.
- For first time users, you need to make sure your Mac has install the command line tools from Apple.com
- samtools needs to be installed in your /usr/local/bin
- tabix needs to be installed in your /usr/local/bin
- wget needs to be installed in your /usr/local/bin
- python 2.7+

The easiest way to check if you have those three tools, type the commands below into your Terminal:

```unix
find /usr/local/bin/tabix
find /usr/local/bin/samtools
find /usr/local/bin/wget
```

#### 1.0.0
A working version of the VCFtoTree, need to fix the process bar running after the treebuilding part.



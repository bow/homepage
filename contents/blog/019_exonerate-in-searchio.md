---
title: Exonerate in SearchIO
time: 2012/07/18 22:00
tags: biopython, gsoc, python, exonerate, searchio
---

One of the things I enjoy during my time developing SearchIO in the past few weeks is that I get to play with many different programs and see how they behave. Even for programs that I thought I'm familiar with, I sometimes still see unanticipated behaviors (hint: sequence coordinates).  It's like the old days of Windows 95, when you would try to delete a file and see how that affects your computer (and occasionally discover later that you need the file for proper boot-up). Except this time, it's mostly with command line programs and biological sequences (plus there's almost no risk I would render my computer useless permanently).

You can probably imagine how I feel like when the programs I'm playing with are totally new to me.

That's what I experienced when I started playing with [Exonerate]((http://www.ebi.ac.uk/~guy/exonerate/) about a week ago, after [Peter](http://twitter.com/pjacock) suggested that I look into it. It's a generic alignment program that allows you to align sequences using different alignment models; a program that I have never used until a few weeks ago. It may not be as ubiquitous and well-known as BLAST (it's certainly is [younger](http://www.biomedcentral.com/1471-2105/6/31)), but it's a very interesting program on its own. Take a look at a sample output below to get an idea of what its capable of (*I should note that I deliberately chose this output because of the dense information it has, without checking its biological correctness*).

This is a single alignment (HSP, really) resulting from a sequence search against the [yeast genome](http://www.ncbi.nlm.nih.gov/bioproject/PRJNA128) using the `genome2genome` model. Basically, this model assumes that there can exist introns in both the query and/or hit sequences, along with assuming that parts of both sequences may be open-reading frames. It was generated using [Exonerate 2.2](http://www.ebi.ac.uk/~guy/exonerate/) with the default output options.

<pre>
C4 Alignment:
------------
         Query: sacCer3_dna range=chrIV:1319469-1319997 5'pad=0 3'pad=0 strand=+ repeatMasking=none:[revcomp]
        Target: gi|330443667|ref|NC_001143.9| Saccharomyces cerevisiae S288c chromosome XI, complete sequence:[revcomp]
         Model: genome2genome
     Raw score: 267
   Query range: 529 -> 78
  Target range: 641760 -> 71883

    529 : ATCCCTTATCTCTTTATCTTGTTGCCTGGTTCTCTTTTCCCTTTAAATGGAGATTACA :    472
          ||||||||||||||       |||  |||||   ||||  || |  ||     || ||
 641760 : ATCCCTTATCTCTTCTAAAGATTGTGTGGTT---TTTT--CTATGCATATTTTTTCCA : 641708

    471 :                           ga                        ag     :    385
          A---ACTAGCGAA-ACTGCAGAAAAG+->>>> Joint Intron 1 >>>>++CAAA
          |    || || ||  || || | |||     61 bp // 154295 bp     ||| 
          ACCTTCTTGCCAATTCTTCA-ACAAG-+>>>> Joint Intron 1 >>>>++CAAT
 641707 :                           tt                        ag     : 487384

    384 : TTAAAACCAAAATGAGCGATGAAAATAAGAGTACGCGTATGTCAGTTAATC-TCAGTC :    328
          |||| ||||| ||||||||||     |||| | |   |||| | ||||| | ||| | 
 487383 : TTAACACCAAGATGAGCGATG-----AAGA-TTC---TATG-CTGTTAAACTTCACTA : 487336

    327 :         gt                        ga                       :    263
          ACAATTTT++>>>> Joint Intron 2 >>>>--GGAAGAGTGAGGTTTTCTTCCA
           ||||        35 bp // 101120 bp     |||| |   |  || | | | |
          CCAATGAG+->>>> Joint Intron 2 >>>>++GGAACATAAAAATTCTGTCCTA
 487335 :         ga                        ag                       : 386186

    262 :                                              TGCCATGATATAC :    206
          T-GAATTGCAGCTATTGTTAAGGCGTCTGACATAGTATGTAATTGCysHisAspIleH
          |  || | ||   |||| ||  || ||  | || || |||| |||  ! ! .!.||+ 
          TCAAAATTCAATAATTG-TACAGCTTC-CA-ATTGTGTGTACTTGValLysGlnIleG
 386185 :                                              GTCAAACAAATCG : 386131

    205 : ATGTT{TT}  >>>> Target Intron 1 >>>>  {G}TGTGTGTACATT      :    182
          isVal{Le}                             {u}CysValTyrIleTG-AA
               {::}          177446 bp          {:}   !  !::   || ||
          lyHis{Il}++                         ++{e}LysGlyPhe***TGAAA
 386130 : GACAC{AT}gt.........................ag{C}AAAGGATTTTGA      : 208660

    181 :                     ga                        ag           :    105
          TATATATATTTACTAACAAG+->>>> Joint Intron 3 >>>>++TAAAGATGCT
          |||||||||||||| | |       47 bp // 136722 bp      ||||||  |
          TATATATATTTACTTAGAGT++>>>> Joint Intron 3 >>>>++AAAAGATTTT
 208659 :                     gt                        ag           :  71908

    104 : CTGGACAAGTACCAGTTGGAAAGAGA :     79
          ||  || | |  ||||||||||||||
  71907 : CT--ACGACTTGCAGTTGGAAAGAGA :  71884

vulgar: gi|296143771|ref|NM_001180731.1| 25 406 + gi|330443688|ref|NC_001145.3| 130198 11338 - 263 M 14 14 G 0 1 M 4 4 G 2 0 M 25 25 G 0 1 M 9 9 G 0 6 M 42 42 G 2 0 M 16 16 G 0 2 M 7 7 G 0 1 M 3 3 G 2 0 M 23 23 G 3 0 M 6 6 3 0 2 I 0 9353 5 0 2 M 1 1 G 1 0 M 11 11 G 0 1 M 12 12 G 1 0 M 9 9 G 0 1 M 10 10 G 1 0 M 18 18 G 0 1 M 5 5 3 0 2 I 0 109121 5 0 2 M 16 16 G 4 0 M 4 4 G 1 0 M 11 11 G 5 0 M 8 8 G 1 0 M 22 22 G 0 2 M 4 4 G 0 2 M 34 34 G 0 1 M 3 3 G 0 1 M 41 41
</pre>

You can see that it's jam-packed with information. There's the usual sequence coordinates, IDs, and descriptions. But you also see which part it computes as introns, whether it exist in one or both of the sequences, how long they are, and what the splice sites are. You can also see that it computes parts of the sequences as translated codons, complete with which codons are split (the ones bracketed in `{}`). If that's not enough, it still provides you with a compact representation of the alignment; in the line starting with `vulgar`, telling you which bases match, where the gaps and introns are, etc.

Plenty of useful information, indeed!

That's why I am excited to announce that SearchIO now has preliminary support for parsing and indexing exonerate outputs. And it's not just one flavor, the support comes in three formats: `exonerate-text`, for parsing the human-readable alignment, `exonerate-vulgar`, for parsing the vulgar lines only, and `exonerate-cigar`, for parsing cigar lines (not shown here, but very similar to vulgar lines only more compact).

I'll go through a brief demo to show you how we can better access the information presented above using SearchIO. For now, the code lives in [a branch separate from my main development branch](https://github.com/bow/biopython/tree/ed500c7ec0b23724c25eb81034001711255f1e5c), as it uses a new type of `HSP` object: `GappedHSP`. It's similar to regular HSPs, except that it allows for gaps that separate the HSP into more than one alignment block.

<pre lang="python">
>>> from Bio import SearchIO
>>> qresult = SearchIO.read('exn_22_m_genome2genome.exn', 'exonerate-text')
>>> print qresult
Program: exonerate (<unknown>)
  Query: sacCer3_dna
         range=chrIV:1319469-1319997 5'pad=0 3'pad=0 strand=+ repeatMasking=none
 Target: <unknown>
   Hits: ----  -----  ---------------------------------------------------------
            #  # HSP  ID + description                                          
         ----  -----  ---------------------------------------------------------
            0      2  gi|330443520|ref|NC_001136.10|  Saccharomyces cerevisi...
            1      1  gi|330443489|ref|NC_001135.5|  Saccharomyces cerevisia...
            2      1  gi|330443667|ref|NC_001143.9|  Saccharomyces cerevisia...
>>> hsp = qresult[-1][-1] # go straigh the the alignment above
>>> hsp
GappedHSP(hit_id='gi|330443667|ref|NC_001143.9|', query_id='sacCer3_dna', 5 blocks)

# query and hit strands
>>> hsp.query_strand, hsp.hit_strand
(-1, -1)

# query and hit start and coordinates
>>> hsp.query_coords
[(449, 529), (319, 388), (198, 284), (161, 198), (78, 114)]
>>> hsp.hit_coords
[(641682, 641760), (487327, 487387), (386123, 386207), (208639, 208677), (71883, 71917)]

# start and end coordinates of introns in query and hit
>>> hsp.query_intron_coords
[(388, 449), (284, 319), (198, 198), (114, 161)]
>>> hsp.hit_intron_coords
[(487387, 641682), (386207, 487327), (208677, 386123), (71917, 208639)]

# start and end coordinates of split codons in query and hit
>>> hsp.query_scodon_coords
[(198, 200), (197, 198)]
>>> hsp.hit_scodon_coords
[(386123, 386125), (208676, 208677)]

# the first three query and hit sequences
>>> hsp.query[:3]
[SeqRecord(seq=Seq('ATCCCTTATCTCTTTATCTTGTTGCCTGGTTCTCTTTTCCCTTTAAATGGAGAT...AAG', SingleLetterAlphabet()), id='sacCer3_dna', name='aligned query sequence', description='', dbxrefs=[]), SeqRecord(seq=Seq('CAAATTAAAACCAAAATGAGCGATGAAAATAAGAGTACGCGTATGTCAGTTAAT...TTT', SingleLetterAlphabet()), id='sacCer3_dna', name='aligned query sequence', description='', dbxrefs=[]), SeqRecord(seq=Seq('GGAAGAGTGAGGTTTTCTTCCAT-GAATTGCAGCTATTGTTAAGGCGTCTGACA...TTT', SingleLetterAlphabet()), id='sacCer3_dna', name='aligned query sequence', description='', dbxrefs=[])]
>>> hsp.hit[:3]
[SeqRecord(seq=Seq('ATCCCTTATCTCTTCTAAAGATTGTGTGGTT---TTTT--CTATGCATATTTTT...AAG', SingleLetterAlphabet()), id='gi|330443667|ref|NC_001143.9|', name='aligned hit sequence', description='', dbxrefs=[]), SeqRecord(seq=Seq('CAATTTAACACCAAGATGAGCGATG-----AAGA-TTC---TATG-CTGTTAAA...GAG', SingleLetterAlphabet()), id='gi|330443667|ref|NC_001143.9|', name='aligned hit sequence', description='', dbxrefs=[]), SeqRecord(seq=Seq('GGAACATAAAAATTCTGTCCTATCAAAATTCAATAATTG-TACAGCTTC-CA-A...CAT', SingleLetterAlphabet()), id='gi|330443667|ref|NC_001143.9|', name='aligned hit sequence', description='', dbxrefs=[])]
</pre>

Here I'm using the `exonerate-text` format, but if the file has vulgar lines, `exonerate-vulgar` should work similarly. These two parsers compute coordinates from different sources (alignment header vs vulgar line), but the result should be the same either way.

As you see, with a few lines of code we can already access plenty of information about the HSP alignment. We know that the HSP has 5 blocks and that both of them lies on the negative strand. From the `hsp.query_coords`, we can see the coordinates of the query block. Notice that even though the block order is the same as the one displayed in the alignment, the individual start and end coordinates are always `(x, y)` where `x <= y`. This makes it easy to retrieve the aligned sequence part from its whole.

Looking at `hsp.query_intron_coords`, we see that there is actually only three introns in the query sequence. This is because one of the coordinates is `(198, 198)`, which means it covers no sequence. We also now that this part may be translated into amino acids and has its codon split, as shown by  `hsp.query_scodon_coords`. Finally, we can do further manipulation on the query or hit sequences as they are all parsed into Biopython's SeqRecord objects.

Pretty useful, I hope :).

There are still more details I need to iron out before Exonerate support stops being preliminary. If you notice in the example above, the `HSP` output is still minimum. I'm also thinking of making the `GappedHSP` an iterable that returns the alignment blocks within. But I'll save that for the future and leave you with this for now.

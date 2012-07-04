---
title: Initial Blat Support
time: 2012/07/04 22:00
tags: python, biopython, gsoc, searchio, blat
---

For the past week, I have been working on two similar formats: PSL and PSLX ([spec](https://cgwb.nci.nih.gov/goldenPath/help/blatSpec.html)). The PSL format is the default output of [BLAT](http://genome.ucsc.edu/FAQ/FAQblat.html), but has found many uses across different programs. These formats themselves are simple; with 21 (PSL) or 23 (PSLX) tab-separated columns and an optional header. PSLX itself is basically PSL plus two extra columns that contain the hit and query sequences. 

In this post, I'll walk over some features of the current parser. I'll end by explaining briefly why there could be future changes to the current SearchIO object model (the `QueryResult`, `Hit`, and `HSP` trio) due to the data presented in PSL and PSLX files.

PSL and PSLX in SearchIO
------------------------
The official format name for both formats in SearchIO are `blat-psl` and `blat-pslx`. SearchIO currently has parsing, indexing, and writing support for both formats. The parser can deal with both the variants with and without a header. For writing, both variants are also supported but it defaults to writing no header. 

The important thing to remember when parsing any PSL or PSLX file using SearchIO is that rows from the same query (ones that have the same `Q name` values) must be grouped together. This is due to the way SearchIO's parsers are designed: they are all one-way parsers that consume a stream of data. If the there are two groups of rows with the same `Q name` column values, the parser will treat them as different queries (even though they might be the same).

Here's an example parsing session using the `Blat/pslx_34_001.pslx` file in the [development branch](https://github.com/bow/biopython/tree/searchio). Since the file is quite small, I'll paste the contents here so you may get a glimpse on how the parser stores the data.

<pre>
psLayout version 3

match	mis- 	rep. 	N's	Q gap	Q gap	T gap	T gap	strand	Q        	Q   	Q    	Q  	T        	T   	T    	T  	block	blockSizes 	qStarts	 tStarts
     	match	match	   	count	bases	count	bases	      	name     	size	start	end	name     	size	start	end	count
---------------------------------------------------------------------------------------------------------------------------------------------------------------
16	0	0	0	0	0	0	0	+	hg18_dna	33	11	27	chr4	191154276	61646095	61646111	1	16,	11,	61646095,	aggtaaactgccttca,	aggtaaactgccttca,
33	0	0	0	0	0	0	0	+	hg18_dna	33	0	33	chr1	249250621	10271783	10271816	1	33,	0,	10271783,	atgagcttccaaggtaaactgccttcaagattc,	atgagcttccaaggtaaactgccttcaagattc,
17	0	0	0	0	0	0	0	-	hg18_dna	33	8	25	chr2	243199373	53575980	53575997	1	17,	8,	53575980,	aaggcagtttaccttgg,	aaggcagtttaccttgg,
38	3	0	0	0	0	0	0	+	hg19_dna	50	9	50	chr9	141213431	85737865	85737906	1	41,	9,	85737865,	acaaaggggctgggcgtggtggctcacacctgtaatcccaa,	acaaaggggctgggcgcagtggctcacgcctgtaatcccaa,
41	0	0	0	0	0	0	0	+	hg19_dna	50	8	49	chr8	146364022	95160479	95160520	1	41,	8,	95160479,	cacaaaggggctgggcgtggtggctcacacctgtaatccca,	cacaaaggggctgggcgtggtggctcacacctgtaatccca,
33	3	0	0	0	0	0	0	+	hg19_dna	50	11	47	chr22	51304566	42144400	42144436	1	36,	11,	42144400,	aaaggggctgggcgtggtggctcacacctgtaatcc,	aaaggggctgggcgtggtagctcatgcctgtaatcc,
43	1	0	0	1	4	0	0	+	hg19_dna	50	1	49	chr2	243199373	183925984	183926028	2	6,38,	1,11,	183925984,183925990,	aaaaat,aaaggggctgggcgtggtggctcacacctgtaatccca,	aaaaat,aaaggggctgggcgtggtggctcacgcctgtaatccca,
34	2	0	0	0	0	1	134	+	hg19_dna	50	10	46	chr19	59128983	35483340	35483510	2	25,11,	10,35,	35483340,35483499,	caaaggggctgggcgtggtggctca,cacctgtaatc,	caaaggggctgggcgtagtggctga,cacctgtaatc,
39	0	0	0	0	0	0	0	+	hg19_dna	50	10	49	chr18	78077248	23891310	23891349	1	39,	10,	23891310,	caaaggggctgggcgtggtggctcacacctgtaatccca,	caaaggggctgggcgtggtggctcacacctgtaatccca,
27	1	0	0	0	0	0	0	+	hg19_dna	50	21	49	chr18	78077248	43252217	43252245	1	28,	21,	43252217,	ggcgtggtggctcacacctgtaatccca,	ggcgtggtggctcacgcctgtaatccca,
44	1	0	0	1	3	1	6	+	hg19_dna	50	1	49	chr13	115169878	52759147	52759198	2	7,38,	1,11,	52759147,52759160,	aaaaatt,aaaggggctgggcgtggtggctcacacctgtaatccca,	aaaaatt,aaaggggctgggcgtggtggctcacgcctgtaatccca,
50	0	0	0	0	0	0	0	+	hg19_dna	50	0	50	chr1	249250621	1207056	1207106	1	50,	0,	1207056,	caaaaattcacaaaggggctgggcgtggtggctcacacctgtaatcccaa,	caaaaattcacaaaggggctgggcgtggtggctcacacctgtaatcccaa,
31	3	0	0	0	0	0	0	+	hg19_dna	50	1	35	chr1	249250621	61700837	61700871	1	34,	1,	61700837,	aaaaattcacaaaggggctgggcgtggtggctca,	aaaaatgaacaaaggggctgggcgcggtggctca,
28	0	0	0	1	10	1	6	-	hg19_dna	50	11	49	chr4	191154276	37558157	37558191	2	10,18,	1,21,	37558157,37558173,	tgggattaca,accacgcccagccccttt,	tgggattaca,accacgcccagccccttt,
35	2	0	0	0	0	0	0	-	hg19_dna	50	12	49	chr22	51304566	48997405	48997442	1	37,	1,	48997405,	tgggattacaggtgtgagccaccacgcccagcccctt,	tgggattacaggcgggagccaccacgcccagcccctt,
35	1	0	0	0	0	0	0	-	hg19_dna	50	13	49	chr2	243199373	120641740	120641776	1	36,	1,	120641740,	tgggattacaggtgtgagccaccacgcccagcccct,	tgggattacaggcgtgagccaccacgcccagcccct,
39	0	0	0	0	0	0	0	-	hg19_dna	50	10	49	chr19	59128983	54017130	54017169	1	39,	1,	54017130,	tgggattacaggtgtgagccaccacgcccagcccctttg,	tgggattacaggtgtgagccaccacgcccagcccctttg,
36	3	0	0	0	0	0	0	-	hg19_dna	50	10	49	chr19	59128983	553742	553781	1	39,	1,	553742,	tgggattacaggtgtgagccaccacgcccagcccctttg,	tgggatgacaggggtgaggcaccacgcccagcccctttg,
33	3	0	0	0	0	0	0	-	hg19_dna	50	13	49	chr10	135534747	99388555	99388591	1	36,	1,	99388555,	tgggattacaggtgtgagccaccacgcccagcccct,	tgggattataggcatgagccaccacgcccagcccct,
24	1	0	0	0	0	0	0	-	hg19_dna	50	10	35	chr10	135534747	112178171	112178196	1	25,	15,	112178171,	tgagccaccacgcccagcccctttg,	tgagtcaccacgcccagcccctttg,
35	1	0	0	0	0	0	0	-	hg19_dna	50	13	49	chr1	249250621	39368490	39368526	1	36,	1,	39368490,	tgggattacaggtgtgagccaccacgcccagcccct,	tgggattacaggcgtgagccaccacgcccagcccct,
33	1	0	0	0	0	0	0	-	hg19_dna	50	13	47	chr1	249250621	220325687	220325721	1	34,	3,	220325687,	ggattacaggtgtgagccaccacgcccagcccct,	ggattacaggcgtgagccaccacgcccagcccct,
</pre>

<pre lang="python">
>>> from Bio import SearchIO
>>> qresults = list(SearchIO.parse('pslx_34_001.pslx', 'blat-pslx'))
>>> print qresults[0]
Program: blat (<unknown>)
  Query: hg18_dna (33)
 Target: <unknown>
   Hits: -----  -----  ---------------------------------------------------------
         Index  # HSP  ID + description                                         
         -----  -----  ---------------------------------------------------------
             0      1  chr4                                                     
             1      1  chr1                                                     
             2      1  chr2                                                     
>>> print qresults[1]
Program: blat (<unknown>)
  Query: hg19_dna (50)
 Target: <unknown>
   Hits: -----  -----  ---------------------------------------------------------
         Index  # HSP  ID + description                                         
         -----  -----  ---------------------------------------------------------
             0      1  chr9                                                     
             1      1  chr8                                                     
             2      2  chr22                                                    
             3      2  chr2                                                     
             4      3  chr19                                                    
             5      2  chr18                                                    
             6      1  chr13                                                    
             7      4  chr1                                                     
             8      1  chr4                                                     
             9      2  chr10 
</pre>

You can see right away that the parser recognizes two different queries: `hg18_dna` and `hg19_dna`. What you might not notice immediately is the way the parser groups the HSPs into the hits. An HSP here represents a single row of result while Hit represents all rows with the same `T name` value. As a result, we see that in the `hg19_dna` query, the `chr1` hit has four HSPs. Looking at the file alone, it's not obvious how many HSPs we have in `chr1`, as the results for `chr1` are separate into two groups (two lines each), based on their strand. But the parser takes care of this and groups them together.

Let's go further down the hierarchy and look into the `chr19` hit in `hg19_dna`.

<pre lang="python">
>>> hit = qresults[1]['chr19']
>>> print hit
Query: hg19_dna
  Hit: chr19 (59128983)
 HSPs: -----  --------  ---------  ------  ------------------  ------------------
       Index   E-value  Bit score  Length        Query region          Hit region
       -----  --------  ---------  ------  ------------------  ------------------
           0       n/a        n/a     170               10-45   35483340-35483509
           1       n/a        n/a      39               10-48   54017130-54017168
           2       n/a        n/a      39               10-48       553742-553780
</pre>

There's not much to see in the hit-level, as BLAT only gives us the length of the hit (`T size` column) and its ID (`T name` column). But here we see that the length of the first HSP in the hit is suspiciously longer than the others. My guess is that there's a huge gap in the HSP, separating the sequences into two blocks. Let's see if that' the case.

<pre lang="python">
>>> hsp = hit[0]
>>> hsp.gap_num          # are there any gaps? if so, how many?
134
>>> hsp.query_gap_num    # how many are in the query sequence?
0
>>> hsp.hit_gap_num      # how many are in the hit sequence?
134
>>> hsp.hit_gapopen_num  # is it one long line of gap or not?
1
>>> hsp.hit_starts       # ok, so let's see the start coordinates of the blocks
[35483340, 35483499]
>>> hsp.hit_blocks       # and then the block sequences themselves
['caaaggggctgggcgtagtggctga', 'cacctgtaatc']
</pre>

Turns out there are indeed gaps -- 134 bases long. You can see that I have drilled down further to see how many of those gaps are in the query sequence and how many are in the hit sequence. I then checked to see how many gap openings are present in the hit sequence, to see if all 134 gaps are interspersed acros the sequence or not. Since we only see one gap opening, that means we have one long line of gap. Finally, I checked the start coordinates of the hit sequences separated by this gap and the sequences themselves.

Most of these values are present in the file: `query_gap_num` and `hit_gap_num` are the `Q gap bases` and `T gap bases` columns, respectively; `hit_gapopen_num` is `T gap count`; `hit_starts` is `tStarts`; and `hit_blocks` is the last column of the PSLX format. For some other values, like `gap_num`, the parser does the calculation for you since it is simple (`gap_num` = `hit_gap_num` + `query_gap_num`). Two other values that are calculated by the parser are the overall HSP score and its percentage identity.

<pre lang="python">
>>> hsp.score
31
>>> hsp.ident_pct
94.44444444444444
</pre>

These values are the ones you find when using [UCSC's online Blat search](http://genome.ucsc.edu/cgi-bin/hgBlat?command=start) and are calculated based on [their formula](http://genome.ucsc.edu/FAQ/FAQblat.html#blat4) as well.

Tweaks to the current model?
----------------------------
Now, looking the results above, you might notice something different about the way the sequences are stored: they are just strings stored in a list. This is different from the HSPs we have seen so far, which store sequence results as `SeqRecord` objects in `hsp.hit` and `hsp.query`; and also as a `MultipleSequenceAlignment` object in `hsp.alignment`. The current PSL and PSLX parser do not store into these fields; instead it uses `hsp.hit_blocks` and `hsp.query_blocks`, if the sequences are present.

The reason for this is that unlike other output formats, the HSP in PSL and PSLX can be segmented into blocks, with gaps present in both the query and hit sequences. In the other formats, an HSP is in essence just one block of an alignment; while here we can have multiple blocks. In a sense, the HSPs we see here are like HSPs within an HSP. 

One way to deal with this is to treat each separate sequence block as a separate HSP. However, some programs like BLAT do treat a single line as a single HSP. We can see this from the way it does the score calculation: one line has one score. If we break the HSP groupings in the given file, we also lose the ability to calculate this score as I have not figured out how BLAT decides how to group several alignment blocks into a single HSP or not. You can see the 'chr19' example I've written above for hits containing HSPs with multiple blocks. The first HSP has two blocks, while the rest only has one each.

Ideally, we would like to store this blocks into `SeqRecord` and `MultipleSeqAlignment` objects so it's easier to manipulate them further, just like the other HSPs. But looking at this, we might need to tweak the current object model to allow for better representation of segmented HSP blocks. There are some alternatives I've been thinking of, but that's a topic for another post.

I'll leave you with this for now, and continue with my updates next week.

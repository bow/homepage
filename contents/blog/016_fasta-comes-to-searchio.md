---
title: Fasta Comes to SearchIO
time: 2012/06/28 15:00
tags: biopython, python, gsoc, searchio, fasta
---

The past week saw the addition of Fasta output ([the program](http://fasta.bioch.virginia.edu/), not the sequence file format) parsing and indexing support into SearchIO, under the `fasta-m10` name. In this post, I will briefly touch on the background of its support and some of its features. Along the way, you will also notice that the SearchIO objects now display more user-friendly outputs when we use `print` or `str` against them. This is another small feature that I have worked on in the past week.

As usual, all these updates are available in my latest branch [here](https://github.com/bow/biopython/tree/searchio).

Fasta in SearchIO
-----------------
If you have been using Biopython for a while, you'll notice that Fasta support has been around for some time now. It currently lives in the AlignIO module, and allows you to parse all alignments present in a Fasta output file. However, Fasta alignments are quite different from alignments present in other file formats supported by AlignIO (e.g. `clustal` or `phylip`). This is because Fasta itself is not really a sequence alignment program, which attempts to make a single alignment from a set of sequences fed into it. Instead, Fasta is more similar to BLAST or HMMER, programs that try to find entries in a given sequence database that match their input sequence(s). Although the end products of a Fasta search are also alignments, they are not of the same nature as alignments made by ClustalW or PHYLIP, for example. 

As an illustration, take a look at how AlignIO parses the following file. It's the result of a Fasta search of three mRNA sequences query against one database. The file is available in the `Tests/Fasta` directory of my development branch. You can also download it [here](https://raw.github.com/bow/biopython/searchio/Tests/Fasta/output009.m10), if you want to try go along with the following examples.

<pre lang="python">
>>> from Bio import AlignIO
>>> for ali in AlignIO.parse('output009.m10', 'fasta-m10'):
...     print ali, '\n'
... 
SingleLetterAlphabet() alignment with 2 rows and 22 columns
TGATGTTCTGTTTCTAAAACAG gi|255708421:1-99
TGATTTTTTTTGTCTAAAACAG gi|23308614|ref|NM_152952.1| 

SingleLetterAlphabet() alignment with 2 rows and 14 columns
AGAAGGAAAAAAAA gi|156718121:2361-2376
AGAACTAAAAAAAA gi|47271416|ref|NM_131257.2| 

SingleLetterAlphabet() alignment with 2 rows and 14 columns
AGAAGGAAAAAAAA gi|156718121:2361-2376
AGAAGGTATAAAAA gi|332859474|ref|XM_001156938.2| 

SingleLetterAlphabet() alignment with 2 rows and 14 columns
TTTTTTTCCTTCTT gi|156718121:2361-2376
TTTTTTTACATCTT gi|332211534|ref|XM_003254825.1| 

SingleLetterAlphabet() alignment with 2 rows and 14 columns
AAGAAGGAAAAAAA gi|156718121:2361-2376
AATAAGTAAAAAAA gi|23308614|ref|NM_152952.1| 

SingleLetterAlphabet() alignment with 2 rows and 14 columns
TTTTTTTCCTTCTT gi|156718121:2361-2376
TTTTTTTACATCTT gi|297689475|ref|XM_002822130.1| 

SingleLetterAlphabet() alignment with 2 rows and 14 columns
AAGAAGGAAAAAAA gi|156718121:2361-2376
AAGAAGGTAAAAGA gi|297689475|ref|XM_002822130.1| 
</pre>

Here, we still see the alignments but without a clear connection to our initial three query sequences. To see the query that produced one alignment, we have to check the query ID (the first ID in the alignment blocks, not really intuitive from the display). There is also no easy way to access some of the alignments' interesting attributes such as the expect value or start-stop coordinates. The current parser captures the start and stop coordinates of both alignments, but stores it in private attributes of the underlying `SeqRecord` objects (i.e. `SeqRecord._al_start` and `SeqRecord._al_stop`). It is not immediately obvious how we can access these values.  Thus, putting Fasta in AlignIO seemed more like a temporary workaround.

Being similar to BLAST and HMMER, Fasta is a natural candidate for SearchIO support. Using last week's addition, we can now parse Fasta outputs into the SearchIO objects hierarchy: alignments as `HSP` objects, contained within `Hits`, which results from a `QueryResult` search.

Take a look at how SearchIO deals with Fasta outputs in the following examples, using the same `output009.m10` file.

First, we see that we can display information about our three queries neatly:
<pre lang="python">
>>> from Bio import SearchIO
>>> qresults = list(SearchIO.parse('output009.m10', 'fasta-m10'))
>>> for qresult in qresults:
...     print qresult, '\n'
... 
Program: fasta (36.3.5c)
  Query: random_s00 (15)
 Target: mrnalib.fasta
   Hits: 0 

Program: fasta (36.3.5c)
  Query: gi|255708421:1-99 (99)
         Mus musculus myoglobin (Mb), transcript varia
 Target: mrnalib.fasta
   Hits: -----  -----  ---------------------------------------------------------
         Index  # HSP  ID + description                                         
         -----  -----  ---------------------------------------------------------
             0      1  gi|23308614|ref|NM_152952.1|  Danio rerio cytoglobin 1... 

Program: fasta (36.3.5c)
  Query: gi|156718121:2361-2376 (16)
         Bos taurus nucleoporin 43kDa (NU
 Target: mrnalib.fasta
   Hits: -----  -----  ---------------------------------------------------------
         Index  # HSP  ID + description                                         
         -----  -----  ---------------------------------------------------------
             0      1  gi|47271416|ref|NM_131257.2|  Danio rerio hemoglobin a...
             1      1  gi|332859474|ref|XM_001156938.2|  PREDICTED: Pan trogl...
             2      1  gi|332211534|ref|XM_003254825.1|  PREDICTED: Nomascus ...
             3      1  gi|23308614|ref|NM_152952.1|  Danio rerio cytoglobin 1...
             4      2  gi|297689475|ref|XM_002822130.1|  PREDICTED: Pongo abe... 

</pre>
Immediately, it's obvious how many hits we have in each query and how many HSPs we have in each Hit.

We can drill down to each hit and HSP to see more information. Let's take a look at the hits from our last query:
<pre lang="python">
>>> qresult = qresults[-1]
>>> for hit in qresults:
...     print hit, '\n'
... 
Query: gi|156718121:2361-2376
  Hit: gi|47271416|ref|NM_131257.2| (597)
       Danio rerio hemoglobin alpha adult-1 (hbaa1), mRNA
 HSPs: -----  --------  ---------  ------  --------------  --------------
       Index   E-value  Bit score  Length    Query region      Hit region
       -----  --------  ---------  ------  --------------  --------------
           0       1.4      21.00      14            2-15         572-585 

Query: gi|156718121:2361-2376
  Hit: gi|332859474|ref|XM_001156938.2| (762)
       PREDICTED: Pan troglodytes myoglobin, transcript variant 11 (MB), mRNA
 HSPs: -----  --------  ---------  ------  --------------  --------------
       Index   E-value  Bit score  Length    Query region      Hit region
       -----  --------  ---------  ------  --------------  --------------
           0       1.4      20.90      14            2-15           84-97 

Query: gi|156718121:2361-2376
  Hit: gi|332211534|ref|XM_003254825.1| (805)
       PREDICTED: Nomascus leucogenys hemoglobin subunit gamma-2-like (LOC100...
 HSPs: -----  --------  ---------  ------  --------------  --------------
       Index   E-value  Bit score  Length    Query region      Hit region
       -----  --------  ---------  ------  --------------  --------------
           0       1.4      20.90      14           14-27         633-646 

Query: gi|156718121:2361-2376
  Hit: gi|23308614|ref|NM_152952.1| (5188)
       Danio rerio cytoglobin 1 (cygb1), mRNA
 HSPs: -----  --------  ---------  ------  --------------  --------------
       Index   E-value  Bit score  Length    Query region      Hit region
       -----  --------  ---------  ------  --------------  --------------
           0       1.4      20.90      14            1-14       3547-3560 

Query: gi|156718121:2361-2376
  Hit: gi|297689475|ref|XM_002822130.1| (1158)
       PREDICTED: Pongo abelii hemoglobin subunit gamma-like (LOC100439631), ...
 HSPs: -----  --------  ---------  ------  --------------  --------------
       Index   E-value  Bit score  Length    Query region      Hit region
       -----  --------  ---------  ------  --------------  --------------
           0       1.4      20.90      14           14-27         983-996
           1       1.4      20.90      14            1-14           19-32 

</pre>
Again, the information we are often interested in each hit is directly available. We see here that most hits have one HSP alignment, while the last one has two. For all of the HSP alignments, we can immediately see their expect values, scores, length, and coordinates, allowing us to get a general feel of the whole hit.

Finally, let's take a look at the last hit and the alignments it contain.
<pre lang="python">
>>> hit = qresult[-1]
>>> for hsp in hit:
...     print hsp, '\n'
... 
  Query: gi|156718121:2361-2376 Bos taurus nucleoporin 43kDa (NU
    Hit: gi|297689475|ref|XM_002822130.1| PREDICTED: Pongo abelii hemoglobin ...
E-value: 1.4, Bit score: 20.90, Alignment length: 14
--
Query:      14 TTTTTTTCCTTCTT 27
  Hit:     983 TTTTTTTACATCTT 996 

  Query: gi|156718121:2361-2376 Bos taurus nucleoporin 43kDa (NU
    Hit: gi|297689475|ref|XM_002822130.1| PREDICTED: Pongo abelii hemoglobin ...
E-value: 1.4, Bit score: 20.90, Alignment length: 14
--
Query:       1 AAGAAGGAAAAAAA 14
  Hit:      19 AAGAAGGTAAAAGA 32 

</pre>
As you can see, there is more readily available information compared to when we parse the file using AlignIO. We now know what the coordinates are, what the alignment scores are, and which sequence is the hit or query sequence. All of the properties are accessible via the objects, just like what I have shown in the past weeks. Here are some examples:

<pre lang="python">
>>> hsp = hit[-1]
>>> hsp.z_score # Z-score, Fasta-specific property
82.0
>>> hsp.hit_span # How long the alignment covers the hit sequence
14
>>> hsp.query_span # How long the alignment covers the query sequence
14
</pre>

That's all for this week. Stay tuned for next week as I add more file format support for SearchIO.

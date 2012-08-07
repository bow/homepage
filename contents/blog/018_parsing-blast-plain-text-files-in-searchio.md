---
title: Parsing BLAST Plain Text Files in SearchIO
time: 2012/07/18 18:00
tags: biopython, gsoc, searchio, blast, python
---

BLAST plain text output is a tricky beast. It's the output format easiest to read for us, humans, but it's arguably harder for computers to read compared to its XML our tabular counterparts. One reason is because NCBI themselves give no guarantee that the output stays the same between different BLAST versions. This means that for each different BLAST version, there is a chance that a given parser breaks. It's still a useful format, nonetheless, giving the reader instant feedback or visualization of his/her search results. It is why some Bio* libraries (and other programs, no doubt) continue to try write parsers for the plain text format.

In Biopython, BLAST plain text parsing support is officially obsoleted. It ships without guarantee that the plain text parser will work. However, the code itself is still there and for the most part it still works. Just to give an illustration, the plain text parser's test suite contains files from legacy BLAST version 2.0.10 (released more than 10 years ago) up to the latest version (2.2.26+, released last year). Although these files do not cover all possible outputs one can generate from BLAST and some versions in between them are not covered, it speaks of how much versatile the parser is.

Now, when I started writing parsers for SearchIO, the plain text output is indeed one format that crossed my mind. I was warned, though, officially supporting it will take much work and might not be the best thing to do. Plus, it's hard to think that I can manage to write a new parser from scratch that can handle all variations in the plain text output during the GSoC period (on top of the other parsers I need to write). After talking with my mentor, we decided that for now the best thing to do is perhaps to write a SearchIO wrapper around the current Biopython's BLAST parser.

[I've done a similar thing with the BLAST XML parser](http://bow.web.id/blog/2012/05/from-bio-import-searchio/) ([and have replaced it with a faster version](/blog/2012/05/assembling-the-parsers/)). But for the plain text parser, I'm hesitant to say that this is an offical support for BLAST plain text parsing (especially when the backend parser is already obsoleted). So this parser comes with a disclaimer similar to the current BLAST parser's: we are not giving you any guarantee that this will work for all versions and variations. If it does work, that's great, though :).

Having said that, let's take a glimpse on how we deal with BLAST plain text files using SearchIO. This will use the files from the commits [here](https://github.com/bow/biopython/tree/23112c8fb2c4f081079f0ba5b4371ce2a2e13552).

<pre lang="python>
# initialization and peeking at the main QueryResult objects
>>> from Bio import SearchIO
>>> qresults = list(SearchIO.parse('text_2226_blastp_004.txt', 'blast-text'))
>>> for qresult in qresults:
...     print qresult, '\n'
... 
Program: blastp (2.2.26+)
  Query: random_s00 (32)
 Target: minirefseq_prot
   Hits: 0 

Program: blastp (2.2.26+)
  Query: gi|16080617|ref|NP_391444.1| (102)
         membrane bound lipoprotein [Bacillussubtilis subsp. subtilis str. 168]
 Target: minirefseq_prot
   Hits: ----  -----  ---------------------------------------------------------
            #  # HSP  ID + description                                          
         ----  -----  ---------------------------------------------------------
            0      1  gi|308175296|ref|YP_003922001.1|  membrane bound lipop...
            1      1  gi|375363999|ref|YP_005132038.1|  lytA gene product [B...
            2      1  gi|154687679|ref|YP_001422840.1|  LytA [Bacillus amylo...
            3      1  gi|311070071|ref|YP_003974994.1|  unnamed protein prod...
            4      1  gi|332258565|ref|XP_003278367.1|  PREDICTED: UPF0764 p... 

Program: blastp (2.2.26+)
  Query: gi|11464971:4-101 (98)
         pleckstrin [Mus musculus]
 Target: minirefseq_prot
   Hits: ----  -----  ---------------------------------------------------------
            #  # HSP  ID + description                                          
         ----  -----  ---------------------------------------------------------
            0      2  gi|11464971|ref|NP_062422.1|  pleckstrin [Mus musculus]  
            1      2  gi|354480464|ref|XP_003502426.1|  PREDICTED: pleckstri...
            2      2  gi|156616273|ref|NP_002655.2|  pleckstrin [Homo sapiens] 
            3      2  gi|297667453|ref|XP_002811995.1|  PREDICTED: pleckstri...
            4      1  gi|350596020|ref|XP_003360649.2|  PREDICTED: pleckstri... 

# and the Hit objects
>>> for hit in qresult[:3]:
...     print hit, '\n'
... 
Query: gi|11464971:4-101
  Hit: gi|11464971|ref|NP_062422.1| (350)
       pleckstrin [Mus musculus]
 HSPs: ----  --------  ---------  ------  ------------------  ------------------
          #   E-value  Bit score  Length        Query region          Hit region
       ----  --------  ---------  ------  ------------------  ------------------
          0     2e-69     205.00      98                0-98               3-101
          1     3e-09      43.50     100                2-96             245-345 

Query: gi|11464971:4-101
  Hit: gi|354480464|ref|XP_003502426.1| (350)
       PREDICTED: pleckstrin-like [Cricetulus griseus]
 HSPs: ----  --------  ---------  ------  ------------------  ------------------
          #   E-value  Bit score  Length        Query region          Hit region
       ----  --------  ---------  ------  ------------------  ------------------
          0     3e-69     205.00      98                0-98               3-101
          1     2e-09      43.90     100                2-96             245-345 

Query: gi|11464971:4-101
  Hit: gi|156616273|ref|NP_002655.2| (350)
       pleckstrin [Homo sapiens]
 HSPs: ----  --------  ---------  ------  ------------------  ------------------
          #   E-value  Bit score  Length        Query region          Hit region
       ----  --------  ---------  ------  ------------------  ------------------
          0     1e-68     204.00      98                0-98               3-101
          1     2e-10      47.40     100                2-96             245-345 

# and finally the HSPs
>>> for hsp in hit:
...     print hsp
... 
  Query: gi|11464971:4-101 pleckstrin [Mus musculus]
    Hit: gi|156616273|ref|NP_002655.2| pleckstrin [Homo sapiens]
E-value: 1e-68, Bit score: 204.00, Alignment length: 98
--
Query:       0 KRIREGYLVKKGSVFNTWKPMWVVLLEDGIEFYKKKSDNSPKGMIPLKG~~~KKAIK 98
               KRIREGYLVKKGSVFNTWKPMWVVLLEDGIEFYKKKSDNSPKGMIPLKG~~~KKAIK
  Hit:       3 KRIREGYLVKKGSVFNTWKPMWVVLLEDGIEFYKKKSDNSPKGMIPLKG~~~KKAIK 101
  Query: gi|11464971:4-101 pleckstrin [Mus musculus]
    Hit: gi|156616273|ref|NP_002655.2| pleckstrin [Homo sapiens]
E-value: 2e-10, Bit score: 47.40, Alignment length: 100
--
Query:       2 IREGYLVKKGSVFNTWKPMWVVLLEDG--IEFYKKKSDNSPKGMIPLKG~~~DIKKA 96
               I++G L+K+G     WK    +L ED   + +Y       P G I L+G~~~ I+ A
  Hit:     245 IKQGCLLKQGHRRKNWKVRKFILREDPAYLHYYDPAGAEDPLGAIHLRG~~~AIQMA 345
</pre>

As expected, the parser groups the BLAST results into SearchIO's object model: `QueryResult`, `Hit`, and `HSP`. This is similar to the object model used in Biopython's current parser: `QueryResult` resembles a `Record` object, `Hit` resembles the list of objects in `Record.alignments`, while `HSP`'s counterpart are the objects in `Record.alignments.hsps`.

In fact, there isn't that much difference between SearchIO's object model and the current parser's. They basically boil down to these:

* The object creation process. If in the current parser you need to instantiate the a parser object first, in SearchIO you just need to feed it the file name and the format name (which is `blast-text`).

* The iterability (?) of the objects. In the current parsers, you can't iterate over `Record` or the objects in `Record.alignments` directly. But in SearchIO, you can safely iterate over `QueryResult` or `Hit`.

* The attribute names. This is perhaps the biggest change that you will feel. I've renamed some of the current attributes' names to conform better to SearchIO's standards (and the attribute names of other SearchIO BLAST parsers). Some examples: `expect` in an HSP is now `HSP.evalue`, `bits` in an HSP is now `bitscore`, and hit sequence length is now `Hit.seq_len`. I'm not posting a complete list yet, as there might still be some changes. But I can say that I'm planning to use the same name to refer to the same attribute accross different BLAST output formats.

That's it for the BLAST parser. In my next post, I'll walk through the next program to be supported by SearchIO: [Exonerate](http://www.ebi.ac.uk/~guy/exonerate/).

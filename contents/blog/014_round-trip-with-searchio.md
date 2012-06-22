---
title: A Round Trip with SearchIO
time: 2012/06/13 22:00
tags: biopython, python, gsoc
---
 
Another Python-filled week has passed by, and that means more improvements for the SearchIO submodule. The highlight of the past week was two new features:

* Two of the main container objects, `QueryResults` and `Hits` now have their own flavors of `filter` and `map` functions. They are similar to Python's built in `filter` and `map` functions, allowing manipulations on the items they contain.

* Two new methods were added to the main SearchIO interface: `write` and `convert`. As you surely have guessed, `write` allows you to write `QueryResult` objects back into a file and `convert` is a convenience function for converting search output files to a different format. These methods currently support writing out to two file formats: `blast-xml` and `blast-tab`.

Let's go through a quick demo and see what they can do for you using the latest [branch](https://github.com/bow/biopython/tree/searchio). I'll be using a BLAST+ XML file obtained by searching NCBI's 16S rRNA database with the sequence below:

<pre>
>sample_130304 unknown soil bacterium
GACCTGAGAGGGTGATCCCCCACACTGGCACTGAAACACGGGCCAGACACCTACGGGTGGCAGCAGTAGGGAATATTGCACAATGGGC
GAAAGCCTGATGCAGCAACGCCGCGTGCGCGATGAAGGCCTTCGGGTTGTAAAGCGCTTTTCTGGGAGATGAGGAAGGACAGTATCCC
AGGAATAAGGCTCGGCTAACTACGTGCCAGCAGCCGCGGTAAAACGTAGGAGCCAAGCGTTATCCGAATTCACTGGGCGTAAAGCGCG
TGCAGGCGGCCCGATAAGTTGGATGTGAAATCTCCTGGCTCAACTAGGAGAGGCCGTTCAATACTGTTGGGCTTGAGGGCGACAGA
</pre>

It's a partial sequence of the [16S ribosomal RNA gene](http://en.wikipedia.org/wiki/16S_ribosomal_RNA) from an unknown bacteria. It is most commonly used in identifying bacterial strains or species. Let's run a `blastn` search to see the possible source species of our sample. You can [run the BLAST search from your browser](http://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastSearch&USER_FORMAT_DEFAULTS=on&PAGE=MegaBlast&PROGRAM=blastn&QUERY=%3Esample_130404%0AGACCTGAGAGGGTGATCCCCCACACTGGCACTGAAACACGGGCCAGACACCTACGGGTGGCAGCAGTAGGGAATATTGCACAATGGGCGAAAGCCTGATGCAGCAACGCCGCGTGCGCGATGAAGGCCTTCGGGTTGTAAAGCGCTTTTCTGGGAGATGAGGAAGGACAGTATCCCAGGAATAAGGCTCGGCTAACTACGTGCCAGCAGC&JOB_TITLE=sample_130404&NEWWIN=on&NEWWIN=on&GAPCOSTS=0%200&MATCH_SCORES=1,-2&DATABASE=TL/16S_ribosomal_RNA_Bacteria_and_Archaea&BLAST_PROGRAMS=megaBlast&MAX_NUM_SEQ=500&SHORT_QUERY_ADJUST=on&EXPECT=10&WORD_SIZE=28&REPEATS=repeat_9606&TEMPLATE_TYPE=0&TEMPLATE_LENGTH=0&FILTER=L&FILTER=m&SHOW_OVERVIEW=true&SHOW_LINKOUT=true&ALIGNMENT_VIEW=Pairwise&MASK_CHAR=2&MASK_COLOR=1&GET_SEQUENCE=true&NEW_VIEW=true&NCBI_GI=false&NUM_OVERVIEW=100&DESCRIPTIONS=100&ALIGNMENTS=100&FORMAT_OBJECT=Alignment&FORMAT_TYPE=HTML&SHOW_CDS_FEATURE=false&OLD_BLAST=false) and download the resulting XML file. Alternatively, you can use [the XML file I obtained from an earlier search](/misc/sample_130304.xml). Note that NCBI continually updates their database, so you might have different result if you run a new BLAST search.

Next, let's fire up SearchIO and see what BLAST tells us about our sequence. We'll first use `SearchIO.read` since we only have one query, and then do a quick glance on the top 10 hits by checking their description, and the e-values and percent identities of the alignments in those hits.

<pre lang="python>
>>> from Bio import SearchIO
>>> qresult = SearchIO.read('sample_130304.xml', 'blast-xml')
>>> qresult
QueryResult(id='15997', 500 hits)
>>> for hit in qresult[:5]:
...     print hit.desc
...     for hsp in hit:
...             print '  evalue:', hsp.evalue
...             print '  %% identity: %.2f' % hsp.ident_pct
... 
Anaerolinea thermophila strain UNI-1 16S ribosomal RNA, partial sequence
  evalue: 8.33551e-77
  % identity: 90.95
Levilinea saccharolytica strain KIBI-1 16S ribosomal RNA, partial sequence
  evalue: 2.99798e-76
  % identity: 91.04
Anaerolinea thermolimosa strain IMO-1 16S ribosomal RNA, partial sequence
  evalue: 1.07827e-75
  % identity: 90.87
Bellilinea caldifistulae 16S ribosomal RNA, partial sequence
  evalue: 3.87814e-75
  % identity: 90.57
Clostridium drakei strain : SL1 16S ribosomal RNA, partial sequence
  evalue: 6.58197e-63
  % identity: 87.20
</pre>

As you can see, all of the top 10 hits have one alignment each. The order of these hits are determined by BLAST, so by default the first hit has the alignment with the lowest e-value. It's also obvious that the top 10 results are all hits from partial sequences. Now, let's suppose you want to see if there are hits from complete sequences. One of the new filter function, `hit_filter` lets you do just that.

It takes as its input a callback function whose argument is a Hit object and returns either True or False. If a Hit object returns False, it will be filtered out. Now we can define a boolean function to check for 'partial' and feed it to `hit_filter`:

<pre lang="python">
>>> def desc_filter(hit):
...     return 'partial' not in hit.desc # .desc is the hit property that holds the description
...
>>> filtered = qresult.hit_filter(desc_filter)
>>> filtered
QueryResult(id='15997', 58 hits)
>>> for hit in filtered[:5]:
...     print hit.desc
...     for hsp in hit:
...             print '  evalue:', hsp.evalue
...             print '  %% identity: %.2f' % hsp.ident_pct
... 
Nocardia cummidelens strain DSM 44490 16S ribosomal RNA, complete sequence
  evalue: 1.42475e-59
  % identity: 85.98
Nocardia soli strain DSM 44488 16S ribosomal RNA, complete sequence
  evalue: 1.42475e-59
  % identity: 85.98
Nocardia salmonicida strain DSM 40472 16S ribosomal RNA, complete sequence
  evalue: 1.42475e-59
  % identity: 85.98
Leifsonia antarctica strain : SPC 20 16S ribosomal RNA, complete sequence
  evalue: 8.57476e-57
  % identity: 85.45
Leifsonia kafniensis strain : KFC-22 16S ribosomal RNA, complete sequence
  evalue: 3.98945e-55
  % identity: 84.98
</pre>

As you can see, none of the hits in `filtered` are annotated with 'partial' anymore.

Similar to `hit_filter`, there's also `hsp_filter`, which lets you filter based on the attribute values of the HSPs within a `QueryResult`. Let's try it out by filtering for HSPs whose identity percentage is at least 85%.

<pre lang="python">
>>> def ident_filter(hsp):
...     return hsp.ident_pct >= 85
...
>>> new_filtered = filtered.hsp_filter(ident_filter)
>>> new_filtered
QueryResult(id='15997', 6 hits)
>>> for hit in new_filtered:
...     print hit.desc
...     for hsp in hit:
...             print '  evalue:', hsp.evalue
...             print '  %% identity: %.2f' % hsp.ident_pct
... 
Nocardia cummidelens strain DSM 44490 16S ribosomal RNA, complete sequence
  evalue: 1.42475e-59
  % identity: 85.98
Nocardia soli strain DSM 44488 16S ribosomal RNA, complete sequence
  evalue: 1.42475e-59
  % identity: 85.98
Nocardia salmonicida strain DSM 40472 16S ribosomal RNA, complete sequence
  evalue: 1.42475e-59
  % identity: 85.98
Leifsonia antarctica strain : SPC 20 16S ribosomal RNA, complete sequence
  evalue: 8.57476e-57
  % identity: 85.45
Arthrobacter woluwensis strain 1551 16S ribosomal RNA, complete sequence
  evalue: 3.98945e-55
  % identity: 85.05
Agromyces ulmi strain XIL01 16S ribosomal RNA, complete sequence
  evalue: 1.85611e-53
  % identity: 91.84
</pre>

The final addition to the filters is the `Hit` object's `filter`. Here, it filters the HSP objects within a `Hit` object based also on a given callback function. 

Mirroring the filter functions, we also have three map functions: `hit_map` and `hsp_map` for `QueryResult` objects and `map` for `Hit` objects. Different from the filters, these mappers accept a callback function that must return the contained object. So the function given to `hit_map` must return a `Hit` object, and the function given to `hsp_map` or `map` must return an HSP object. Here's an example where we use `hit_map` to change the Hit IDs:

<pre lang="python">
>>> for hit in new_filtered:
...     print hit.id
... 
gi|343201156|ref|NR_041871.1|
gi|343201155|ref|NR_041870.1|
gi|343201154|ref|NR_041869.1|
gi|343202402|ref|NR_042688.1|
gi|343206302|ref|NR_044894.1|
gi|265678803|ref|NR_029108.1|
>>> def id_renamer(hit):
...     hit.id = hit.id.split('|')[-2]
...     return hit
... 
>>> modified = new_filtered.hit_map(id_renamer)
>>> for hit in modified:
...     print hit.id
... 
NR_041871.1
NR_041870.1
NR_041869.1
NR_042688.1
NR_044894.1
NR_029108.1
>>> 
</pre>

Now, let's say we want to save the `QueryResult` object containing no partial Hits into a new XML file. Thanks to the new `write` method, We can simply do the following:

<pre lang="python">
>>> def desc_filter(hit):
...     return 'partial' not in hit.desc
...
>>> filtered = qresult.hit_filter(desc_filter)
>>> SearchIO.write(filtered, 'out.xml', 'blast-xml')
(1, 6, 6)
</pre>

The returned tuple is the number of `QueryResult`, `Hit`, and `HSP` objects written. If we later need to convert `out.xml` into a tabular file, we can use `convert`. 

<pre lang="python">
>>> SearchIO.convert('out.xml', 'blast-xml', 'out.txt', 'blast-tab')
(1, 6, 6)
</pre>

Finally, let me conclude the post by combining all the functions we've used here into a small script. We'll chain them together as generator expressions, so we'll start with `SearchIO.parse` instead of `SearchIO.read`:

<pre lang="python">
#!/usr/bin/env python

from Bio import SearchIO

def desc_filter(hit):
    return 'partial' not in hit.desc

def ident_filter(hsp):
    return hsp.ident_pct >= 85

def id_renamer(hit):
    hit.id = hit.id.split('|')[-2]
    return hit

qresults = SearchIO.parse('sample_130304.xml', 'blast-xml')
filtered = (qresult.hit_filter(desc_filter) for qresult in qresults)
new_filtered = (qresult.hsp_filter(ident_filter) for qresult in filtered)
modified = (qresult.hit_map(id_renamer) for qresult in new_filtered)
SearchIO.write(modified, 'out.txt', 'blast-tab')
</pre>

With only several lines of code, we have done filtering on annotation, then on identity percentage, then change the hit IDs, and finally write to a new file format. Pretty compact, don't you think :)?

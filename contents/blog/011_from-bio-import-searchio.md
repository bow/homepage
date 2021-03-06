---
title: from Bio import SearchIO
time: 2012/05/22 12:00
tags: biopython, gsoc, python, searchio
---

The coding period has officially started. It's only about one month ago that I was anxiously waiting for the GSoC announcement, not knowing that I would end up coding with the [Biopython](http://biopython.org/) community. It's been going great and I'm hoping this will remain true for the rest of the summer :).

As I've noted [last week](/blog/2012/05/the-final-preparations/), I have started the actual coding myself. In the past week I have coded, tested and wrote an initial documentation for the core SearchIO objects. This has allowed me to implement and test an initial working prototype for BLAST+ XML output parsing. It still relies on Biopython's `Bio.Blast.NCBIXML` submodule, but this should change in the future as I'm planning to implement SearchIO's own XML parser. For now, it should provide you with a glimpse on the general feel of using SearchIO.

I'll try to note some of the SearchIO's design rationale and its features using the current BLAST+ XML development branch, available [here](https://github.com/bow/biopython/tree/searchio-blastxml). As these features are still under development, I'll then continue with possible issues that could result in future changes.


SearchIO Objects
----------------

The basic concept for SearchIO object design is that all sequence homology search programs show their results in three levels:

1. The top level, which encapsulates all hits from a single query.
2. The middle level, which contains all alignments from a single database hit.
3. The bottom level, consisting of single regions of highly similar query and database sequences. One database hit should have at least one of these regions present.

This hierarchy is mirrored in SearchIO using the following classes: the `QueryResult` class for the top level, `Hit` class for the middle level, and the `HSP` (high-scoring pair) for the bottom level. A single QueryResult object may contain zero or more Hit objects, and Hit objects themselves contain at least one HSP object.  Let's go through these main objects shortly one by one. I'll use the demo file `tblastx_human_wnts.xml` contained in the `Test/Blast` directory of the `searchio-blastxml` branch. This is a TBLASTX XML output generated by searching five human [Wnt genes](http://en.wikipedia.org/wiki/Wnt_signaling_pathway#Wnt_signaling_proteins) against NCBI's `refseq_mrna` database.

First up, the QueryResult object. As these objects sit on the top of the hierarchy, they are the objects returned by SearchIO's two main methods: `parse` and `read`. Similar to the SeqIO submodule, `SearchIO.parse` returns an iterator over multiple queries from a single file, while `SearchIO.read` returns an object from a file containing only one query,

<pre lang="python">
>>> from Bio import SearchIO
>>>
>>> qresults = SearchIO.parse('tblastx_human_wnts.xml', 'blast-xml')
>>> for qresult in qresults:
...     qresult
...
QueryResult(program='TBLASTX', target='refseq_mrna', id='gi|195230749:301-1383', 5 hits)
QueryResult(program='TBLASTX', target='refseq_mrna', id='gi|325053704:108-1166', 5 hits)
QueryResult(program='TBLASTX', target='refseq_mrna', id='gi|156630997:105-1160', 5 hits)
QueryResult(program='TBLASTX', target='refseq_mrna', id='gi|371502086:108-1205', 5 hits)
QueryResult(program='TBLASTX', target='refseq_mrna', id='gi|53729353:216-1313', 5 hits)
>>>
>>> qresult = SearchIO.read('tblastx_human_wnts.xml', 'blast-xml')
>>> qresult
QueryResult(program='TBLASTX', target='refseq_mrna', id='gi|195230749:301-1383', 5 hits)
</pre>

The QueryResult object behaves like a hybrid of Python's built-in list and dictionary. You can retrieve the Hit objects contained in it using an integer index or using a string key that identifies the Hit object. By default, this string key defaults to the Hit ID. Iteration over the QueryResult object will return the Hit objects in it.

<pre lang="python">
>>> first_hit = qresult[0]
>>> first_hit
Hit(id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', 10 alignments)
>>>
>>> last_hit = qresult[-1]
>>> last_hit
Hit(id='gi|209529663|ref|NM_001135848.1|', query_id='gi|195230749:301-1383', 10 alignments)
>>>
>>> first_hit.id
u'gi|195230749|ref|NM_003391.2|'
>>> first_hit == qresult[u'gi|195230749|ref|NM_003391.2|']
True
>>> for hit in qresult:
...     hit
...
Hit(id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', 10 alignments)
Hit(id='gi|281183280|ref|NM_001168718.1|', query_id='gi|195230749:301-1383', 10 alignments)
Hit(id='gi|281182577|ref|NM_001168597.1|', query_id='gi|195230749:301-1383', 10 alignments)
Hit(id='gi|274325896|ref|NM_001168687.1|', query_id='gi|195230749:301-1383', 10 alignments)
Hit(id='gi|209529663|ref|NM_001135848.1|', query_id='gi|195230749:301-1383', 10 alignments)
</pre>

Similar to Python lists, you can slice QueryResult objects, too. However, instead of returning a Python list, slicing will return another QueryResult object with its Hit objects sliced accordingly. The newly sliced QueryResult object will retain instance attributes from the unsliced QueryResult object, so you can slice queries without worrying about attribute loss.

<pre>
>>> sliced_qresult = qresult[2:4]
>>> for hit in sliced_qresult:
...     hit
...
Hit(id='gi|281182577|ref|NM_001168597.1|', query_id='gi|195230749:301-1383', 10 alignments)
Hit(id='gi|274325896|ref|NM_001168687.1|', query_id='gi|195230749:301-1383', 10 alignments)
>>> qresult.program
u'TBLASTX'
>>> sliced_qresult.program
u'TBLASTX'
</pre>

If you prefer to work with the Hit objects in a list instead, you can access them using QueryResult's `hits` attribute, which will return all its hits in a list. To show all the hit keys in a QueryResult object, you can use the `hit_keys` attribute. Finally, the QueryResult object also support other list methods: `append`, `index`, `pop`, and `sort`. Check out the initial documentation (e.g. by doing a `help(qresult.pop)`)for more information regarding these methods.

Next up, the Hit objects. These objects are containers for the HSP objects and behave almost exactly the same as Python lists. As expected, iteration over a Hit object will return HSP objects in it and a `len()` on a Hit object will return how many HSP objects it has. Like QueryResult objects, slicing on a Hit object will return another Hit object with its queries sliced accordingly and its unsliced instance attributes retained. If you want to work on the HSP objects directly in a list, you can access them using the `hsps` attribute of the Hit object. And lastly, Hit also supports `append`, `pop`, and `sort`.

<pre lang="python>
>>> hit = qresult[0]
>>> hit
Hit(id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', 10 alignments)
>>>
>>> len(hit)
10
>>> for hsp in hit:
...     hsp
...
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 340-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 253-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 69-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 361-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 178-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 161-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 237-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 106-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 288-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 28-column alignment)
>>>
>>> sliced_hit = hit[:3]
>>> len(sliced_hit)
3
>>> hit.id == sliced_hit.id
True
</pre>

The final object, HSP, acts as a container for highly-similar regions of the query and database sequence. It stores this alignment using Biopython's `Bio.Align` MultipleSeqAlignment object; in an instance attribute `alignment`. It also stores the query and database sequences in two attributes: `query` and `hit`, respectively, using Biopython's `SeqRecord` object. These allow you to manipulate the sequences and alignments just like when you are using `Bio.SeqIO` or `Bio.AlignIO`. The HSP object itself does not support as many custom methods as its parents (the QueryResult and Hit objects). It does support slicing, which will return another HSP object with its alignment sliced, and doing a `len()` on an HSP object will return the how many columns are present in the alignment.


Note that the features above are only available if the parsed search output file has alignments in it. Some formats, such as BLAT's PSL format or the standard BLAST+ tabular format, do not output any alignments. In that case, the `alignment`, `query`, and `hit` attributes of an HSP object will all return `None`.


Outstanding Issues
------------------

I should note that the features above are all still under development and subject to future changes.

One thing that could change is the HSP object implementation. In [Peter](http://twitter.com/pjacock)'s [initial SearchIO branch](http://github.com/peterjc/biopython/blob/search-io-test/Bio/SearchIO/_objects.py), the precursor of my GSoC project, two separate classes are implemented to represent HSP objects. One class is used for HSPs without alignments and another for HSP objects with alignments. This is different from my implementation, where the alignment is an optional attribute of the HSP object. The reason I chose to do so was that I consider the alignments themselves as an optional attribute of a HSP. There are also some technical difficulties that I encounter when trying to subclass MultipleSeqAlignment directly. However, I do agree that it also makes sense to consider HSP as a natural subset of MultipleSeqAlignment, as the creation of any HSP object in theory should have been triggered by an alignment.

But for now, as I find it more sensible to make MultipleSeqAlignment an optional attribute, I'm using that implementation.

As for the other objects, do you have any particular method that you would like to see implemented? One method I thought is `filter`. This would accept a boolean function and can be used on the QueryResult and/or Hit object to filter out unwanted Hit and/or HSP objects. Something like this:

<pre lang="python">
>>> for hsp in hit:
...     hsp
...
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 340-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 253-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 69-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 361-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 178-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 161-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 237-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 106-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 288-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 28-column alignment)
>>>
>>> hsp_filter = lambda hsp: len(hsp) > 200   # filter out all HSP objects with length 200 or less
>>> hit.filter(hsp_filter_func=hsp_filter)
>>> for hsp in hit:
...     hsp
...
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 340-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 253-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 361-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 237-column alignment)
HSP(hit_id='gi|195230749|ref|NM_003391.2|', query_id='gi|195230749:301-1383', evalue=0.0, 288-column alignment)
</pre>

This method is basically a shorthand of using list comprehensions. You can implement a similar feature already using list comprehensions. The difference here is that you can still work on the HSP objects inside a Hit object, while list comprehensions would return these HSPs in a list. Right now this is merely an idea, but it might be implemented in the future if the feature is deemed useful to have.


Next Week
---------

As outlined in my proposal, the next plan is to start working on BLAST+ tabular outputs and HMMER text outputs. Stay tuned for next week's update. In the meantime, feel free to let me know if you have any specific feature you would like to see implemented in SearchIO.

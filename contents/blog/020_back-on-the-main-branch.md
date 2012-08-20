---
title: Back on the Main Branch
time: 2012/08/07 17:00
tags: biopython, gsoc, python, searchio, oop
---

It's been a while since I posted my GSoC updates.

The main reason was a considerable change to the main SearchIO object model. It turns out that the trio of `QueryResult`, `Hit`, `HSP` I had been using objects was not sufficient to consistently model outputs from all the search program I have encountered. So with [Peter](http://twitter.com/pjacock)'s guide, I've spent most of my time writing and rewriting several different models, trying to find out which one is best. As the model forms the base of all the parsing logic, every alternative required some parser rewriting, which surely takes time. The good thing is we've finally settled on one alternative so I thought this is another update worth posting.

I'll try to explain what the new object model looks like in this post. There's also another update to the main API that I'll mention afterwards. 

As always, this is done using [the latest code](https://github.com/bow/biopython/commit/6d3d8a9a6ee32a9036bf0e75719aaadcf980703e) available from [my main development repo](https://github.com/bow/biopython/tree/searchio). I should also mention that I've been using [Travis for continuous testing](http://travis-ci.org/#!/bow/biopython) on this branch. Travis has exposed several version-specific bugs that I have managed to fix, making the codebase better.

Anyway, on to the updates!

Improved SearchIO Model
-----------------------
I started developing SearchIO using a hierarchy of three objects: the `QueryResult` object to represent search queries, the `Hit` object to represent a matching entry in the search database, and the `HSP` object to represent a region of significant alignment between the query and hit sequence. This works well for the early search programs I worked with: BLAST, HMMER, and FASTA. The outputs of these programs can be parsed easily into this hierarchy, and interacting with them in the interpreter also feels natural.

However, things began to feel different when I started working with BLAT and Exonerate. Unlike BLAST, HMMER, or FASTA, I started seeing 'HSPs' containing more than a single sequence / alignment. BLAT's term for each of these is 'block', while Exonerate often (but not always) marks these as exons. They don't always show up; you can still see BLAT or Exonerate results without these fragmented HSPs. But they do show up, so the model has to accomodate them as well. I was not aware then, that the presence of these HSPs breaks an assumption of the initial object model: that all `HSP` objects represent a contiguous alignment between query and hit sequences.

My initial instinct was to keep using the old object model, and just store these extra HSP sequences into a list, stored as an attribute of the original `HSP` object. This turned out to be  inadequate, as each of these fragments also has their own properties (coordinates, frame, etc.). Fine, I thought, I'll just store them into list attributes as well (you may have noticed this implementation in my previous posts on the BLAT and Exonerate parsers). Although in practice the parsers still can parse the data into this model, storing these values into lists causes more problems:

* The properties of each fragment are decoupled. This means that if I delete a sequence block from the sequence list, in the coordinate list I will still see its coordinate and may assume that the sequence is present (even when it's not). This applies to list appends as well.

* The properties of the HSP object itself may look inconsistent. If I have a list of fragment start coordinates and I delete the first one, the start coordinate of the `HSP` must also change. Simple storage in lists does not allow this to happen without resorting to verbose and messy code.

It became clear that these fragments must be represented as whole objects themselves. Since the object model does not accomodate that, it means that object model itself had to be overhauled. 

It took us several trial and errors until we came into an HSP model that we both like, but we finally settled on this: a new model consisting of four objects: `QueryResult`, `Hit`, `HSP`, and `HSPFragment`. In this model, `QueryResult` and `Hit` remain the same as the previous one's, but `HSP` is radically different. It is now a container for `HSPFragment` objects. `HSPFragment` itself represents a single, contiguous chunk of alignment between the query and hit sequence. It's quite similar to the old `HSP`, with the main difference of only storing sequence-related attributes. In other words, `HSPFragment` only stores sequence IDs, the sequences themselves, start and end coordinates, the strand, and the sequence frame. All other attributes endowed by the search program, such as evalues, bitscores, or percent identities are stored in the `HSP` object.

You can access the fragment-specific attributes from the `HSP` objects in two ways. The first is by using singular attribute names, such as `hsp.hit`, `hsp.query`, or `hsp.alignments`. Each of these attribute has a plural counterpart (accordingly called `hsp.hits`, `hsp.queries`, and `hsp.alignments`) which returns them in a list. The singular attributes can only be used in `HSP` objects with one fragment (the case with BLAST, HMMER, and FASTA). They will raise an error if there are more than one fragments. If you are familiar with the `read` functions of `Bio.SeqIO` and `Bio.AlignIO` (`Bio.SearchIO` as well), this is analogous to that.  All these fragment-dependent attributes are now read-only properties of the `HSP`. They can only be set from the `HSPFragment` object directly.

There are also the coordinate-dependent attributes, which may mean differently in `HSP` and `HSPFragment` objects. For example, doing an `hspfragment.query_range` returns a tuple of start and end coordinates of that single fragment. Doing `hsp.query_range`, on the other hand, returns a tuple of the start and end coordinate of the whole HSP, spanning all its fragments. If we want to get the list of start and end positions, we need to do `hsp.query_ranges` instead.

Finally, I'd just like to mention that the biggest changes introduced by this new model are present on the file parser level, aside from the object code themselves. If you are only working with BLAST, HMMER, and FASTA, you need not worry as the `HSP` attributes from these programs can still be accessed in the same manner as in the previous model (although they are different under the hood). There are more changes if you are working with BLAT and Exonerate, but not that many that you have to rethink an entire workflow.

New Additions to the Main API
-----------------------------
Another update worth mentioning is the new change in the main SearchIO functions. They are `parse`, `read`, `index`, `index_db`, and `write`. You can now specify custom keyword arguments when using each of these methods, depending on the file format you specify. This was done to reduce the number of format names we use. Since some of them correspond to almost exactly the same code (e.g. the code for parsing BLAST tabular formats with and without comments; specified by either the `-m 6` or `-m 7` flag)

Here's an example:

<pre lang="python">
from Bio import SearchIO

# the blast-tab parser defaults to parsing uncommented files
qresults = SearchIO.parse('tab.plain', 'blast-tab')

# but it can also be used to parse the variant with comments
qresults = SearchIO.parse('tab.commented', 'blast-tab', comments=True)
</pre>

In addition to reducing the format name clutter, using keyword arguments also allows us to define custom behavior of the method. For example, we can now specify the custom columns to parse in a BLAST tabular output, if our file has a nondefault column order:

<pre lang="python">
# file only has query ID, hit ID, and evalue columns
qresults = SearchIO.parse('tab1.out', 'blast-tab', fields=['qseqid', 'sseqid', 'evalue'])

# you can pass in space-separated strings too, handy for copy-pasting directly
qresults = SearchIO.parse('tab2.out', 'blast-tab', fields='qseqid sseqid evalue')

# and you can use the 'std' alias for the standard column order
qresults = SearchIO.parse('tab3.out', 'blast-tab', fields='qseqid std sseqid')
</pre>

Previously, this was only possible if you use the `BlasTabIterator` class directly. Now you can do it without having to directly import the class from the module.

At the moment only the `blast-tab` parser has these extra keyword arguments. However, as the list of supported format grows, I'm certain more formats will utilize this feature.

That's all I have for this week. As this year's GSoC period is almost ending (less than two weeks to the hard pencils down date!), in the coming weeks I'll be focusing more on tidying up the code and writing documentations so SearchIO gets closer to production-level code.

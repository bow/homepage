---
title: Summer's Over
time: 2012/08/20 21:00
tags: biopython, gsoc, searchio
---

Google Summer of Code 2012 has finally drawn to a close.

It's been a great learning experience, one I would not hesitate to recommend to anyone. I've learned a lot in the past few months, not just about writing open source software but also about several bioinformatics applications (that I hope to continue use in the foreseeable future) and even about myself.

I'm deeply thankful first and foremost to [Peter](http://twitter.com/pjacock), my mentor for the summer, and to the Biopython community in general. Peter was the person who reviewed my first ever open source contribution last year (also to Biopython) and got me interested in doing more. Throughout the summer, he didn't just answer my questions about pieces of code that I had trouble with, but also explained a lot more about working in modern bioinformatics in general. As a person who hopes to one day make a living out of bytes and basepairs, I really couldn't have asked for a better mentor.

As for the Biopython community (and in extension the Open Bioinformatics Foundation), I would like to convey my gratitude as well. I have to say that I learned Python in the first place with a considerable influence from Biopython. Initially I simply intended to use it to automate some of my repetitive lab tasks. I guess it was a slippery slope that led me down this road now :). So thank you for everyone involved in Biopython and thank you OBF for accepting my proposal this year. It was not the best of proposals, I'm sure, but I hope I have delivered.

And finally, to Google, thank you for having the initiative to organize the Summer of Code. I hope the program will get bigger in scope and gain more visibility in the years to come. Better yet, I hope more companies start doing a similar initiative.

My whole personal experience through the summer probably deserves a post of its own. For now, I want to briefly recap what I have done these past few months and outline the future plans regarding the code.

Recap
=====

The big goal of my project was to create a submodule in Biopython to deal with sequence search output files. There are numerous programs out there that does sequence search and the number will surely grow with time. The focus of the summer was to build a solid foundation for the submodule, so that support for future programs can be added easily. Of course, adding initial support for several popular search programs was part of the summer task as well.

[As described in Biopython's wiki](http://biopython.org/wiki/SearchIO), the initial name for the submodule was SearchIO; echoing a similar feature in Bioperl. This has been the name I've used throughout the summer as well. [But it may be renamed](http://lists.open-bio.org/pipermail/biopython-dev/2012-April/009513.html) before it can be merged to Biopython's master branch. I'll still continue to refer to it as SearchIO here, since we have not settled on a name yet.

In the course of three months, the initial object model for SearchIO has been finished. The final object model differs from the initial plan, due to unforeseen complications. It should, however, be more accomodating for more sequence search programs that may be supported in the future. Along with the object model, support for several popular programs have also been added:

1. Blast (in [Bio.SearchIO.BlastIO](https://github.com/bow/biopython/blob/searchio/Bio/SearchIO/BlastIO/__init__.py)). We have support for parsing, indexing, and writing BLAST XML and tabular files. It is also possible to parse BLAST plain text files.

2. HMMER (in [Bio.SearchIO.HmmerIO](https://github.com/bow/biopython/blob/searchio/Bio/SearchIO/HmmerIO/__init__.py)). The plain text output can be parsed and indexed, while both the table and domain table outputs can be parsed, indexed, and written.

3. FASTA (in [Bio.SearchIO.FastaIO](https://github.com/bow/biopython/blob/searchio/Bio/SearchIO/FastaIO.py)). We have parsing and indexing support for several different flavors of FASTA.

4. BLAT (in [Bio.SearchIO.BlatIO](https://github.com/bow/biopython/blob/searchio/Bio/SearchIO/BlatIO.py)). For BLAT, we have parsing, indexing, and writing support for both its PSL and PSLX output formats.

5. Exonerate (in [Bio.SearchIO.ExonerateIO](https://github.com/bow/biopython/blob/searchio/Bio/SearchIO/ExonerateIO/__init__.py)). Finally for Exonerate, you can parse or index plain text alignments, vulgar lines, or cigar lines. The parsers / indexers should work for any custom Exonerate alignment models.

The final list above differs from the initial plan a bit. Initially, we planned to support EMBOSS and not support Exonerate. But along the way, we decided to do Exonerate first.

All the object model and the supporting code for each program have been tested on various test cases. There are also initial documentations for all of them in the form of Python docstrings, subject to Python's doctests. If you want to use SearchIO, you can use these docstrings as a reference for now. They explain all the features of each parser / indexer / writer, and lists attribute names that you can use to access the parsed values.

That was the state of the code as of yesterday (Monday, 20th August 2012).


Future Plans
============

Even though Google Summer of Code is finished, there are still more things to do before the code becomes production-ready:

1. We have to settle on a proper name for the submodule. This may entail rewriting all reference of 'SearchIO' to whatever name we will agree on.

2. Although the dosctrings have been written, they may still need some revisions. I wrote it with the perspective of someone who knows all about the code, so it might feel different to anyone who knows very little about it. Admittedly, the later group is the real target audience of the documentation, so I might need feedback from them as well.

3. I still need to complete a SearchIO tutorial and include it in Biopython's official tutorial. This requires a slightly different approach compared to writing docstrings, as I need to highlight important features of SearchIO. I might also need to add one or two entries in the Cookbook wiki, to help people understand SearchIO better. After all, if a software has features yet nobody understands them, does it still have the features at all ;)?

4. And finally, more testing. The code [has been tested](http://travis-ci.org/#!/bow/biopython) on various Python platforms on Linux, but not on Windows or Mac. There might still be some OS-specific bugs that I need to squash.

So yeah, even though the summer's over, the work lives on. I'll be sure to have more SearchIO-related updates posted here, just without the [gsoc tag](http://bow.web.id/blog/tag/gsoc/). Watch this space :).

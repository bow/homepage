---
title: The Final Preparations
time: 2012/05/16 22:00
tags: gsoc, biopython, python
---

Another week has passed by and we are getting closer to the official coding start. I spent the past week playing around with XML and SQLite, as mentioned [before](/blog/2012/05/warming-up-for-the-coding-period/), among other things.

For XML, I find the spec and design easy to grasp. What took me more time than I anticipated was its general parsing mechanism in Python. There are three general XML parsing implementations that comes built in with Python: using the DOM standard, using SAX, and using Python's own representation. The current BLAST XML parser in Biopython uses the SAX parser, while I find that these days people seem to rely more on Python's own representation (the popular ElementTree library). I have the impression that among the three, SAX has the smallest overhead but requires a lot of manual coding, which is probably why it was used for BLAST+ XML over the others. However, I found one [benchmark](http://effbot.org/zone/celementtree.htm) that shows ElementTree (cElementTree, to be precise) can be faster than SAX. It's a pretty old benchmark, though (from 2005), so things may have change now.

The plan for SearchIO's BLAST XML parser now is to try adapt the old existing parser to fit SearchIO's object model. The reason is so that we can quickly have things working. After it's implemented, I plan to write a new parser with ElementTree. If it ends up better than the old one, then SearchIO will use the new parser.

For SQLite, I ended up using the time portion mostly to explore Biopython's `SeqIO.index` and `SeqIO.index_db`. SQLite is used in `SeqIO.index_db` as the database being created to store sequence record offsets, while for `SeqIO.index` the offsets are stored in-memory. These offset values are useful when dealing with very large sequence files. They enable Biopython to do on-the-fly sequence parsing without taking up too much memory. The database itself is simple, a single flat file consisting of three tables: `meta_data` table to store format and sequence count information, `file_data` to store the file names, and `offset_data` to store the actual offset values. In the weekly discussion I had with [Peter](http://twitter.com/pjacock), my supervisor, we thought the soon-to-be-created `SearchIO.index_db` can use a similar schema as well (substituting sequence offsets for search result offsets). So one future plan is to factor out `index` and `index_db` (probably into `Bio._index`?) so they can be used by both SeqIO and SearchIO with minimal repetition.

Finally, in addition to playing with XML and SQLite, I also:

* Wrote the initial code for SearchIO's [main methods](https://github.com/bow/biopython/blob/searchio/Bio/SearchIO/__init__.py).

* Improved the test case generation a bit. All the BLAST+ case generation now use a local custom database which reduces its run time drastically (more than 1 hour to less than 1 minute)

* Added more entries in SearchIO's [proposed terms](http://bit.ly/searchio-terms) table

There is still a few days left before coding period officially begins. But since it seems that I already have all the preparatory stuff taken care of, I am starting coding this week :)! I actually started writing the 'real' SearchIO code just this afternoon, implementing the base `Result` object that represents search results from a single query. You can see the initial code [here](https://github.com/bow/biopython/blob/searchio/Bio/SearchIO/_objects.py) and expect more to come over the coming days. Critiques and comments on the code are eagerly awaited along the way.

<hr />

As a side note, I also tweaked my blog engine last week so that it can generate tag-specific feeds. You can now follow my [GSoC](/blog/tag/biopython/) updates on [this feed](/feed/atom-gsoc.xml).

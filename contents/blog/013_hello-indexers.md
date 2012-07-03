---
title: Hello Indexers
time: 2012/06/06 22:00
tags: biopython, python, gsoc, searchio
---

One of the most useful feature in Biopython's SeqIO module is indexing. This feature, implemented in `SeqIO.index` and `SeqIO.index_db`, allows users to do sequence parsing without having to iterate over the file contents from the beginning of the file. Basically, the idea is to store the file offsets of the start of each sequence record, in memory or in a database, and parse these records on the fly using the appropriate iterators. I won't go into the details of the usage (Biopython's [documentation](http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc56) already does a fine job on that). I'd just like to note here that the feature will also be available in SearchIO.

Similar to sequence files, it's not rare that users work with large files output by a search program. So it would be useful if access to one of the query results in the output can be done without iteration from the start of the file. This is what I've been doing the past week: implementing the indexers for the parsers available in my main `searchio` [branch](https://github.com/bow/biopython/tree/searchio). The implementation is almost identical to SeqIO's indexing, so I could focus on writing the indexers for the formats currently supported by SearchIO: `blast-xml`, `blast-tab`, and `hmmer-text`.

I have not tested the indexers that thoroughly (the tests are still being written), but it should already be usable for those of you feeling adventurous enough to try the code :). The two main indexing methods `SearchIO.index` and `Searchio.index_db` has the same interface as SeqIO's methods: it takes the same arguments and outputs an object almost the same as its counterpart (the difference being its `repr()` string). So if you, for example, want to create a memory-based index of `tblastx_human_wnts.xml`, you just need to do this:

<pre lang="python">
>>> from Bio import SearchIO
>>> index = SearchIO.index('tblastx_human_wnts.xml', 'blast-xml')
>>> index
IndexedSearch('tblastx_human_wnts.xml', 'blast-xml', key_function=None)
>>> index['Query_4']
QueryResult(program='tblastx', target='refseq_mrna', id='Query_4', 5 hits)
</pre>

The database-based indexers also work the same way and has the same features.

Finally, the plan is to have indexers for all of the supported SearchIO formats. I still have several formats to cover (BLAT, FASTA, etc.), so expect more of these indexers in the future as well.

Stay tuned as I post more updates on SearchIO's converter feature next week.

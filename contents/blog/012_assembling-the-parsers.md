---
title: Assembling the Parsers
time: 2012/05/30 22:30
tags: biopython, python, gsoc, blast, hmmer
---

Last week was probably my busiest GSoC week so far, but also the most rewarding as well. I worked on three different parsers for SearchIO: two for BLAST+ and one for the HMMER suite. In brief, these are the highlights of my past week:

* SearchIO now has its own BLAST+ XML parser, powered by the popular cElementTree library.
* There's also a new `blast-tab` parser, which handles NCBI tabular output files with or without headers.
* And finally, we have a new HMMER parser: `hmmer-text`. At the moment, it can parse plain text outputs from hmmersearch and hmmerscan, with several variation. Domain table and regular table outputs is not yet implemented, but planned for the future.

If you want to try your hands at these new parsers, they're available at my latest SearchIO branch [here](https://github.com/bow/biopython/tree/searchio/). They have been tested to a certain degree, and I imagine in most cases they should work fine.


SearchIO blast-xml
------------------

My first BLAST+ XML parser prototype was written on top of the current `Bio.Blast.NCBIXML` submodule. It worked just fine, but it was essentially a quick hack to have a working parser utilizing the SearchIO objects. That's why, as soon as I completed it, I started rewriting the parser to make it more suitable for SearchIO. I chose ElementTree as my base XML parser as it comes built-in with Python and it's also easy to use. Most importantly, it has an alternative implementation in C (cEelementTree) with the same API as the pure Python version. Having a C-backed module often means better performance and the identical API keeps the code flexible

And indeed, some initial benchmarks showed that the new SearchIO `blast-xml` parser performs better than `Bio.Blast.NCBIXML` parser. I wrote a [quick script](https://gist.github.com/2759448) to compare the runtime of both parsers on the `tblastx_human_wnts.xml` file in `Test/Blast`. Averaging from 10 runs, SearchIO's `blast-xml` took 0.247 seconds to iterate over the file, while `NCBIXML` took 0.749 seconds. You can try it out for yourself if you're curious :), but I imagine the results should be in the same ballpark.


SearchIO blast-tab
------------------

For this parser, I've only started writing it last week. My aim was to be at least as flexible as the tabular outputs themselves. As you might have known, the BLAST+ tabular output comes in two variants: the one without a header (or 'comment', as they call it) which is triggered by the `-m 6` flag in the command line; and the one with a header which is triggered by the `-m 7` flag. Both variants have a standard 12 column output. The order of the columns are customizable, and there are other optional columns aside from those 12 standard ones.

The working protoype of SearchIO's `blast-tab` can handle both these variants. If the BLAST+ tabular file has a header, the parser can handle any combination of columns in any order, so long as there are columns that designate the hit ID and query ID of an HSP. If the output has the query and hit sequences, similar to the `blast-xml` parser, the `blast-tab` parser can also create an alignment object. In some cases, the HSP object can also compute certain properties not present in the tabular file. For example, in calculating how many identical residues are present in an HSP alignment, the parser needs to know the total alignment length, how many gaps are there, and how many mismatches are there. If these are all known, you can get the number of identical residues just like accessing a regular attribute (e.g. `hsp.ident_num`) even though the identity column is not present in the output file.

For BLAST+ tabular files without headers, the parser can only parse the default 12-column output for now. A planned improvement is to let users pass in a list or a string denoting the column order, so the parser knows how to deal with nonstandard column ordering. This would not be exposed through the main SearchIO methods (`parse` and `read`), so the user will have to import the `blast-tab` parser from its module directly. 


SearchIO hmmer-text
-------------------

My final work of the week was on the HMMER plain text parser. The format is a bit tricky to parse compared to BLAST+ XML or BLAST+ tabular, as it is specific for HMMER only (tabular and XML formats are pretty popular and easy to parse, on the contrary). It took a little bit more time to get it working properly. I'm fortunate that the HMMER user guide is very helpful, so I can pick out the parts I want to parse and parse them correctly.

Here are some of the features of the current HMMER parser:

1. It can parse outputs from hmmsearch and hmmscan, whether you have single or multiple queries.
2. It can also parse outputs from both programs if the `--notextw` flag or `--noali` flag is turned on. The first flag, `--notextw`, sets the alignment blocks to have infinite length (no wrapping, essentially), while the second flag, `--noali` prevents the program from printing any alignment blocks to the output file.
3. Alignment annotations in the alignment block, such as secondary structures or residue posterior probabilities are all parsed. They are stored in the `alignment_annotation` attribute in the HSP object.
4. The parser adapts the query and hits, depending on the program used. If the output file is created by hmmscan (protein sequence search against an HMM profile database), then the query attributes (`query`, `query_from`, `query_to`, etc.) refer to the protein sequence while the hit attributes refer to the HMM model. If the output file is created by hmmsearch, the reverse is true.

For now, the supported HMMER output format is only plain text. Support for the domain table and regular table output (`--domtblout` and `--tblout` flags in the command line) is planned.


Next week
---------

That's all I have for this week. I'll be dabbling with indexing this week (and probably conversion too), so expect more on that for next week. And as always, critiques on the code are eagerly awaited :).

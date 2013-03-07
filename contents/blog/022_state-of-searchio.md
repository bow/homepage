---
title: State of Bio.SearchIO
time: 2013/02/28 22:00
tags: python, biopython
---

Biopython 1.61 was released [a little less than a month
ago](http://news.open-bio.org/news/2013/02/biopython-1-61-released/). Several
new features and fixes came along with it, and I'm naturally excited since it's
the first official release that includes SearchIO.

It's still subject to change, made clear by a `BiopythonExperimentalWarning`
(new in 1.61 too!) that pops up every time the module is imported. You can use
it in your scripts, but the details may change between versions, until the
experimental warning is gone. Of course, you should have no problem if you
update and test your scripts every now and then.

The module has been undergoing some internal changes, since the last time I
posted an update about it. Most notably, there is now a parser for HMMER2
(thanks to [Kai Blin](https://twitter.com/kaiblin)) and BGZF-compatible indexing
functions (thanks to [Peter Cock](https://twitter.com/pjacock)). For all of you
who are interested, the complete set of functions and objects are now documented
in [Biopython's API page](http://biopython.org/DIST/docs/api/Bio.SearchIO-module.html).
There's also a tutorial that you can follow along (with sampe files and code)
in the [official tutorial](http://biopython.org/DIST/docs/tutorial/Tutorial.html#htoc100).
These tutorials and APIs are the de-facto reference for SearchIO, so refer to
them whenever possible. Of course, if you do need additional help, the [Biopython
mailing list](http://lists.open-bio.org/mailman/listinfo/biopython/) is only a few clicks away.

From here on, my personal focus for SearchIO will be to maintain it and squash
out any bugs that pops up. There will be updates to the code internals as well,
but it really depends on the real-world use cases I will be seeing.
If a new search program shows up, for example, that may prompt the creation of new
parsers.

I do have some thoughts about adding a couple of new parsers
(mainly those produced by the [HMMER](http://hmmer.janelia.org) web service
which are different from the command line version). Along with it, a Biopython
wrapper for the HMMER web service itself may be useful. These aren't my priority
for now, but don't let it stop you from writing them if you want to.

I'm always happy to see pull requests or any kind of feedback on the code :).

---
title: Google Summer of Code is On!
time: 2012/04/24 10:00
tags: gsoc, python, biopython
---
 
After two weeks of waiting, I finally got the answer I was waiting for: [my
proposal](http://google-melange.appspot.com/gsoc/project/google/gsoc2012/warindrarto/13001)
for [Google Summer of Code 2012](http://google-melange.appspot.com/gsoc/homepage/google/gsoc2012)
has been accepted!

<figure>
  <img src="/img/blog/008_gsoc12.jpg" alt="Google Summer of Code 2012" title="Google Summer of Code 2012">
</figure>

Throughout the summer I'll be working on expanding
[Biopython](http://biopython.org/) with a submodule for handling outputs from
sequence-search programs. If you work in Biology, it's very likely that you
have or will soon use one of these programs. They enable you to search the
match of your input sequence (DNA or protein) across different databases. To
put it simply, they're like Google for the biological sequence. There are
many different flavors of these programs, each with its own search algorithm 
suited for a particular purpose. A famous example is
[BLAST](http://blast.ncbi.nlm.nih.gov/Blast.cgi), one of the most widely used
bioinformatics program. In BLAST's case, the algorithm is tuned to favor
speed over accuracy, making it suitable for a quick initial search of your
sequence. The problem with these programs, especially for new users, is that
there are so much information packed in a single search results and each
program does not display the exact same type of results, given their different
algorithms. The bulk of my GSoC work will be to try and unify access to these
different outputs in Biopython, drawing similarities across them all, so that
the information in it is easier to access and interact with.

<figure>
  <img src="/img/blog/008_biopython.jpg" alt="Biopython Logo" title="Biopython Logo">
  <figcaption>It's going to be a summer of the snake!</figcaption>
</figure>

I'll be posting more updates as I go along the weeks here, so expect more
posts to come :).

In the meantime, in the spirit of open source development, I thought it would
be useful to write a short guide that could help you to also
contribute to Biopython (or any other Python-based project with proper setup).
There is already a very 
[thorough documentation](http://biopython.org/wiki/GitUsage) on Biopython's
main site on how to use `git` to contribute to the project. What I will write
is about setting up your Python development environment.

After forking the code, what some people might do is run `python setup.py install`
and install the package straight away to Python's `site-packages` directory.
While this an excellent way to use the program, it's not the best way to develop it.
With such setup, your working program exists in a separate directory from the
development directory (the cloned directory from `git`). So any change you do
in the development directory will not be reflected in the working program.

One better way would be to symlink your development directory to Python's
`site-packages` directory. However, doing this through `ln -s` could be
cumbersome. Fortunately for us, Python provides an easy command:

    $ python setup.py develop

Running that command will prompt Python to create links in the
`site-packages` directory to your current development directory. This enables
you to use the code in the development directory as your working program. Any
change applied to the development directory will be apparent to Python
straight away. Using `develop` instead of manual `ln -s` also has the benefit
of dependency installation. Since we're running the `setup.py`, the package
dependency (as specified there) will also be installed. Finally, if we want
to uninstall the program (basically removing all its links), we can just
do:

    $ python setup.py develop -u
 
Simple, right?

Use this along with [virtualenv](http://www.virtualenv.org/en/latest/index.html)
or [virtualenvwrapper](http://pypi.python.org/pypi/virtualenvwrapper) and
you've got yourself an easy to clean, isolated development environment,
leaving your core system uncluttered. They enable you to use different Python
environments at will, which in turn enables multiple version of the same Python
program to be installed. You might need multiple versions of the same program so
you can do multiple things separately. For example, the stable version might be
required to finish some routine tasks, while the development version is required
for testing some new feature implementation.

So that's it. Hopefully this will ease your development process, so you feel
more comfortable in trying out those different ideas you have in your head :).

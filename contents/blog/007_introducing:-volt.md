---
title: Introducing: Volt, the New Static Website Generator
time: 2012/04/24 08:00
tags: python, website, static
---

A few months ago I decided to build this site using Blogofile, one of the most
well-known Python static website generators. I've written on why I choose
Blogofile (and why static websites are cool!) 
[previously](/blog/2011/09/switching-to-static/). However, over time I was 
becoming less satisfied with it. Some of the error messages were cryptic
and hard to interpret, and its templating engine wasn't exactly my favorite.
Since its mailing list, at that time, did not seem to be very active, I had
to Google a lot just to find out that some of the stuff I wanted to do. After
spending some time tweaking and setting up the site, this made me wish that I
have my own engine that I understand top to bottom. One of the big reason I
chose Blogofile was, after all, to I can understand what's going on given its
Python codebase.

So I set out to write my own engine. I thought it would be a good way for me to
improve my Python skills and come up with something useful in the end
(hopefully not just for me, too). In retrospect, it seems that I made a good
decision on the right time as well. Not long after I started writing, Blogofile's
creator announced that [he was ceasing
development](https://groups.google.com/d/msg/blogofile-discuss/MG02xNwS8Lc/_MK-gmOU2iEJ).

I decided to name my static site generator Volt. The main reason was
practical: I want a single syllable name that's easy to type and to remember.
But it's not just that. I had hoped that my engine can be used to power many
different types of websites with many different tweaks and settings. At
least, it has to have the potential to do so. So Volt seems like the right
name. It doesn't hurt that I often associate static sites with static
electricity in my head, which also has potential ;).

I had plenty of things in my mind that I wanted to implement in this
generator-to-be. It has to be modular, flexible, easy to use, and
easy to debug. For the templating engine, I wanted to use Jinja2 since it
seems way more readable than Mako, Blogofile's templating engine.
Speed was not a concern (at least back then), since I wanted to lay a correct
API groundwork first. After a coding for some time, I'm very happy now to say
that I have implemented most of the things I set out to achieve in the beginning.

I present to you, [Volt](http://pypi.python.org/pypi/Volt/0.0.3): the Python
static website generator with potential, version 0.0.3 (third alpha release). Get it
now from PyPI:

    $ pip install volt

or straight from the [main development repo](https://github.com/bow/volt):

    $ pip install git+https://github.com/bow/volt.git

You're also very welcomed to clone the main repo and contribute to Volt:

    $ git clone https://github.com/bow/volt.git
    $ cd volt
    $ make dev

The first alpha (version 0.0.1) was actually released a month ago. I'm only
announcing it now since there were some missing features back then (not to
mention the bugs to squash and tests to write). It still lacks a proper
documentation, which is why I'm still labeling this release as alpha.
I won't be able to add much to my current documentation branch since I will
be focusing on Google Summer of Code for the next couple of months, but
I'll be more than happy to receive bug reports or feature requests. I did
comment a lot on the code (and in the docstrings), which I'm sure would be
helpful to anyone willing to try their hands at Volt :).

A very short guide on how to use Volt is available in the current
[README](https://github.com/bow/volt/blob/master/README.rst).
But I figure I'll give another go here, to try paint a more complete picture.

Volt is basically a collection of Engines, which are modules responsible for
creating a section of your site. The Blog engine, one of Volt's builtin
Engine for example, can create blogs for your site. Since they are designed
to be modular, you can add, remove, or even create your own engine to
customize how you want your site. You can maybe add an Engine for creating
photo galleries or showing your design portofolio. The possibilities are
endless.

On top of Engines, Volt also has plugins and widgets. They are pretty similar
in terms of what they can do: adding custom processing to your site on top of
engines. The distinguishing thing here is that plugins are designed to be more
abstract than widgets. One can use the same plugin for different sites, but
not necessarily the same widget. Example plugins are markup-parsing plugins
or a syntax highlighter (both comes builtin with Volt), while example widgets
could be a list of recent posts, a list of posts in a certain month, and so on.

Since widgets are pretty-much site-specific, Volt does not have any builtin
widget. It does, however, comes with seven different plugins. Yep, seven
plugins:

  * three markup processing plugins (to handle Markdown, rSt, and Textile,
    respectively)
  
  * two minifier plugins, for CSS and Javascript
  
  * one for generating atom feeds
  
  * and another one to do syntax highlighting

All of these plugins, save for the atom feed generator, requires an extra
dependency. But installing them should be trivial since they are all
available in PyPI.

There are many other features I love from Volt:

  * A builtin HTTP server capable of auto-regenerating the entire site
    whenever its source files are updated (useful for developing your site). 
  
  * One central configuration file to manage everything.

  * Experimental Python 3 support.

  * Logging support.

  * Ability to pass your own Jinja2 tests and filters.

  * [Its own Bash autocompletion script](https://github.com/bow/volt/blob/master/extras/volt)

  * And more!

Finally, I've published [the source code for 
this site](https://github.com/bow/homepage) in case you want to play around
Volt with it. It's not the best tutorial or demo, but I suppose it could help
until a proper documentation is released.

Until then, explore Volt and see what it can do for you :)!

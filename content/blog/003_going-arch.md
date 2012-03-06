---
categories: Tech
time: 2011/09/11 13:03
title: Going Arch
---
I finally installed [Arch Linux](http://archlinux.org).

Prior to this, I had been using [Ubuntu's Lucid Lynx](https://wiki.ubuntu.com/LucidLynx). It ran fine, the community resources was good, and I learned a great deal from using it. There seemed to be no apparent reason for me to switch, except for one thing. I was growing to dislike the way Ubuntu handles its packages. Ubuntu is trying to position itself as an alternative to Windows or Mac OS for mainstream users, so they are making it as user-friendly as possible. As a consequence, new package adoption is slow. The developers had to be sure everything works first before passing them down to users. 

In the beginning this didn't trouble me. Then again, I was still new to the OS and felt content with a working system. After I got more familiar with Linux and wanted to use more packages, this started to become a problem. I'll give you an example.

[Guake](http://guake.org/), my terminal emulator of choice, was having problems with its color display. After checking their website, I found out that their newest release didn't have this problem, so I tried installing it. Since the one in Lucid's repo is of the same version I had, my only choice was to install from source. Trying this costed me several hours which ended in failure. I couldn't get it to install due to some unmet dependencies. They were installed, but for some reason not detected. 

Usually I would turn to the forum and ask questions, but I had had enough. That was not the first time I had problems with less-than-new packages. I decided to look up for a new distro and found Arch.

In contrast to Ubuntu's user-friendly approach, Arch Linux was designed to let users play around with their installation in more ways. For starters, they expose users to the newest, bleeding edge packages. You don't have to wait months to get the latest version of your favorite package from the official repositories. This approach carries more risks of breaking your installs now and then, but then again Arch's user base is different from Ubuntu's. Arch aims to be a distro that allows users to have complete control over their system, as codified in their [guiding philosophy](https://wiki.archlinux.org/index.php/The_Arch_Way). Contrary to being user-friendly, its developers want the distro to be user-centric.

As a result, the installation package is only a bare bone system consisting of only the essentials. The latest [core install image](http://www.archlinux.org/news/20110819-installation-media/) is only 377 MB, much less than [Ubuntu's](http://releases.ubuntu.com/10.10/) 686 MB. It doesn't ship with a desktop environment, so you have to start installing everything from the console. For beginners this might seem daunting (for me a few months ago at least), but this streamlined simplicity is where Arch shines.

You really do get to decide what your system will be. You can pick your own desktop environment, GNOME, KDE, XFCE, you name it, or even forego using them at all if you prefer the console. You get to choose how to manage your network cards, your boot manager, everything. It's not as scary as that may sound, though. You'll have access to Arch community's [comprehensive wiki](https://wiki.archlinux.org/index.php/Main_Page), [user forum](https://bbs.archlinux.org/), and [IRC channel](https://wiki.archlinux.org/index.php/IRC_Channel). I've had my share of problems during my journey into Arch and these resources do help a lot. 

What I like best so far, though, was the way Arch handles its packages.

I won't go into too much detail about Arch's package management system since [the wiki](https://wiki.archlinux.org/index.php/Arch_Build_System) already did a fantastic job of covering it. Instead, I just wanted to say how easy and simple it is to work with. Arch's package manager is [pacman](https://wiki.archlinux.org/index.php/Pacman), written from the ground up in C. For a distro that does not prioritize user convenience, I found it suprisingly more intuitive than Ubuntu's (Debian's, really) [apt](http://wiki.debian.org/Apt). The commands were simpler and the output more easily understood. Here's an example of both package managers installing [rtorrent](http://libtorrent.rakshasa.no/), the command line torrent manager:

<figure>
    <img src="/img/blog/003_apt.jpg" alt="apt installing rtorrent" title="apt installing rtorrent">
    <figcaption>apt: cryptic output for (new) users?</figcaption>
</figure>
<figure>
    <img src="/img/blog/003_pacman.jpg" alt="pacman installing rtorrent" title="pacman installing rtorrent">
    <figcaption>pacman: surprisingly simple</figcaption>
</figure>

Now here's how both manager updates your installed programs. For apt the command is 

<pre>apt-get update && apt-get upgrade</pre>

or

<pre>apt-get update && apt-get dist-upgrade</pre>

while pacman does fine with 

<pre>pacman -Syu</pre>

And there's plenty more comparison [here](https://wiki.archlinux.org/index.php/Pacman_Rosetta).

Why the two options for apt you ask? The second one is used if you want to do a distribution upgrade, since it also removes obsolete packages and installs new ones. This brings me to another point: Arch's release model. 

Arch adopts the [rolling release model](http://en.wikipedia.org/wiki/Rolling_release). To put it shortly, there are no different versions of Arch. Either you have the latest packages or you don't. Every package in your system gets updated gradually so you never have to worry about upgrading to new Arch versions since there is none. I consider the model adoption a potential headache taken away by Arch because I won't have to worry about glitches & breaks that come with version upgrades. 

These advantages comes with a cost, naturally. The freshest and newest of packages are not that thouroughly tested yet, so you have the risk of introducing errors now and then. I already experienced my first problem with this: broken wireless connection. For some reason, my wireless won't turn on. I had to spent time looking for the problem and finding a way to fix it. With help from the wiki and user forum, I managed to find out what went wrong within a short time.

The problem turned out to be some bug in the driver's firmware in the latest kernel. Fixing it was out of the question, since I did not have the ability and time to do it. I ended up reverting back to [kernel2.6-lts](https://bbs.archlinux.org/viewtopic.php?id=78784), an older, more tested kernel.

Now, you might think it's ironic that I switched to Arch because of a lack of new packages, yet it was the newest kernel that bit me from behind with errors. I, however, think that having the freedom to choose from new or older packages is better than only being able to install the old ones. After all, the wireless ended up working and I learned some things along the way. The whole ordeal taught me about reverting kernels, how it handles wifi drivers, and I got to submit a bug report that would help improve the driver.

I don't expect for such problems to disappear in the future. There will always be bugs & errors when you use bleeding edge packages. I only hope that I will still have time to learn about them, since the experience has been worthwhile.

Arch is a great system to learn & play with. If you want to know more about Linux & your own computer, you should try it out.

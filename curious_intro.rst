#########################################
Learn git right for a long and happy life
#########################################

***********************
Git |--| love |--| hate
***********************

I've used git now for a long time.  I think it is a masterpiece of design, I
use it all day every day and I can't imagine what it would be like not to use
it. So, no question, I *love* git.

As y'all may know, `Linus Torvalds wrote git from scratch
<http://git-scm.com/book/en/Getting-Started-A-Short-History-of-Git>`_.  He
loves it too.  `Here is Linus talking about git
<http://www.youtube.com/watch?v=MShbP3OpASA#t=2288>`_ in a question and answer
session:

    Actually I'm proud of git. I want to say this. The fact that I had to
    write git was accidental, but Linux, the design came from a great mind,
    and that great mind was not mine. I mean you have to give credit for the
    design of Linux to Kernighan and Ritchie and Thompson. I mean there's a
    reason I like Unix and I wanted to redo it. I do want to say that git is a
    design that is mine and unique, and I'm proud of the fact that I can damn
    well also do good design from scratch.

But some people hate git.  Really *hate* it. They find it confusing and
error prone and it makes them angry.  Why are there such different views?

I think the reason some people hate git, is because they don't yet understand
it.  The reason I can say this without being patronizing is because I went
through the same thing myself.

When I first started using git, I found it uncomfortable.  I could see it was
very powerful, but I sometimes got lost and stuck and had to Google for a set
of magic commands to get me out of trouble.  I once accidentally made a huge
mess of our project's main repository by running a command I didn't
understand. Git often made me feel stupid.  It felt like a prototype race car
with a badly designed dashboard that I couldn't control, and that was about to
take me off the road, possibly at very high speed.

Then, one day, I read the `git parable`_.  The git parable is a little story
about a developer trying to work out how to make a version control system.  It
gradually builds up from copying whole directories of files to something very
much like git.  I didn't understand it all right away, but as soon as I read
that page, the light-bulb went on |--| I got git.  At once I started to feel
comfortable.  I knew that I could work out why git worked the way it did.  I
could see that it must be possible to do complicated and powerful things, and
I could work out how to do them.

Reading the git parable took me about 45 minutes, but those 45 minutes changed
me from an unhappy git user to someone who uses git often every day, but,
happily, knowing that I have the right tool for the job.

So, my experience tells me that to use git |--| yes *use* git |--| you need to
spend the short amount of time it takes to *understand* git.  You don't
believe me, or you think that I'm a strange kind of person not like you who
probably likes writing their own operating systems. Not so - the insight I'm
describing comes up over and over. From the `git parable`_:

    Most people try to teach Git by demonstrating a few dozen commands and
    then yelling “tadaaaaa.” I believe this method is flawed. Such a treatment
    may leave you with the ability to use Git to perform simple tasks, but the
    Git commands will still feel like magical incantations. Doing anything out
    of the ordinary will be terrifying. Until you understand the concepts upon
    which Git is built, you’ll feel like a stranger in a foreign land.

From `understanding git conceptually
<http://www.sbf5.com/~cduan/technical/git>`_:

    When I first started using Git, I read plenty of tutorials, as well as the
    user manual. Though I picked up the basic usage patterns and commands, I
    never felt like I grasped what was going on “under the hood,” so to speak.
    Frequently this resulted in cryptic error messages, caused by my random
    guessing at the right command to use at a given time. These difficulties
    worsened as I began to need more advanced (and less well documented)
    features.

Here's a quote from the `pro git book <http://git-scm.com/book>`_ by Scott
Chacon.  The git book is a standard reference that is hosted on the main git
website.

    Chapter 9: Git Internals

    You may have skipped to this chapter from a previous chapter, or you may
    have gotten here after reading the rest of the book |--| in either case,
    this is where you’ll go over the inner workings and implementation of Git.
    I found that learning this information was fundamentally important to
    understanding how useful and powerful Git is, but others have argued to me
    that it can be confusing and unnecessarily complex for beginners. Thus,
    I've made this discussion the last chapter in the book so you could read
    it early or later in your learning process. I leave it up to you to
    decide.

So |--| have no truck with people who try and tell you that you can just use
git and that you don't need the `deep shit`_. You *do* need the deep shit, but
the deep shit isn't that deep, and it will take you an hour of your time to
get all of it.  Then I'm betting that you'll see that the alchemist has
succeeded at last, and the |--| er |--| lead has finally turned into gold.

So |--| please |--| invest an hour and a half of your life to understand this
stuff.  Concentrate, go slowly, make sure you get it. In return for 90 minutes
you will get many happy years for which git will appear in its true form, both
beautiful and useful.

*****************************************************
The one thing about git you really need to understand
*****************************************************

git is not really a "Version Control System". It is better described
as a "Content Management System", that turns out to be really good for
version control.

I'll say that again.  Git is a content management system.  To quote from the
`root page of the git manual <http://git-scm.com/docs/git.html>`_: "git - the
stupid content tracker".

The reason that this is important is that git thinks in a very simple way
about files and directories.  You will ask git to keep snapshots of files in a
directory, and it does just this; it stores snapshots of the files, so you can
go back to them later.

Now you know that actual fact, you are ready to read :doc:`curious_tale`.

.. include:: links_names.inc
.. include:: working/object_names.inc

.. Curious git documentation master file, created by
   sphinx-quickstart on Mon Sep  7 21:34:05 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The curious coder's guide to git
================================

You'll find the main tutorial starts at :doc:`curious_intro`, and follows on
through :doc:`curious_journey` to :doc:`curious_git`.

The other pages assume you've read the main tutorial sequence.

You can also read the main tutorial `as a PDF <curious_git.pdf>`_.

.. toctree::
    :maxdepth: 2

    curious_intro
    curious_journey
    curious_git
    curious_remotes
    curious_details

.. the hidden toctree is to avoid warnings during the build.  The
   gh-pages-intro should probably be retired, `ghp-import` is easier.

.. toctree::
    :hidden:

    curious_git
    README
    np-versions/README
    pdf_contents

.. include:: links_names.inc

.. Curious git documentation master file, created by
   sphinx-quickstart on Mon Sep  7 21:34:05 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The curious coder's guide to git
================================

You'll find the main tutorial at :doc:`curious_git`.

The other tutorial pages here assume you've read the main tutorial:

.. toctree::
    :maxdepth: 2

    curious_remotes
    git_object_types
    git_submodules
    git_push_algorithm
    reading_git_objects

.. the hidden toctree is to avoid warnings during the build.  The
   gh-pages-intro should probably be retired, `ghp-import` is easier.

.. toctree::
    :hidden:

    curious_git
    README
    np-versions/README

.. include:: links_names.inc

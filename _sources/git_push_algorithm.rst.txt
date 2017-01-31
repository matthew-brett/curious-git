#########################
An algorithm for git push
#########################

We saw how git stores its object in :doc:`curious_git`.

Now we know about how git stores its objects, we can work out how git knows
which objects to copy when it does a push.

*********************
Paths through commits
*********************

Git commits form a graph.  The commits are the *nodes* in the graph.  Each
commit (except the first) has one or more parents, stored as hash references
in the commit object. The references to commit parents are the links
between nodes that form the *edges* in the graph.

.. prizevar:: paper

    # Get the commit hash from the previous run of curious_remotes
    echo {{ remote-commit2-sha }}

.. prizevar:: paper_7

    # Get the commit hash from the previous run of curious_remotes
    echo {{ remote-commit2-sha_7 }}

.. prizevar:: before_paper

    # Get the commit hash from the previous run of curious_remotes
    echo {{ remote-commit1-sha }}

If we start at a particular commit, and then track back following only one
parent for each commit, this is a *path* in the *commit history*.

************
An algorithm
************

Something like this algorithm might do the job:

#. Get the commit hash corresponding the branch we are going to push;
#. Follow every commit path (see above)back from this commit, until we hit a
   commit hash (filename) that the remote has.  All the previous commits on
   the path, that the remote does not have, are *missing commits*;
#. For every *missing commit* get the corresponding tree (directory listing)
   object.  If the tree object is not in the remote objects directory, add to
   the list of *missing trees*;
#. For every *missing tree* read the tree directory listing. Find any blob
   (file) objects in the directory listing that are not in the remote objects
   directory, add to the list of *missing blob* objects [#sub-trees]_;
#. Copy all *missing commit*, *missing tree* and *missing blob* objects to the
   remote objects directory;
#. Update the remote branch to point to the same commit as the local branch;
#. Update the local record of the last known position of the remote branch to
   point to the same commit.

There's a specific example of ``git push`` at :ref:`git-push`. Here is how
that example would follow our algorithm:

#. We look up the hash for ``master``, and we get |remote-commit2-sha| (abbreviated as
   |remote-commit2-sha_7|);
#. We follow all commit history paths back from |remote-commit2-sha_7| to
   check for missing commits. We start with |remote-commit2-sha_7|. The remote
   does not have a matching file in ``objects``, so this is a missing commit.
   We only have one path to follow, because |remote-commit2-sha_7| has only
   one parent |--| |before_paper| |--| and the remote does have a
   corresponding object, so we can stop looking for missing commits;
#. We only have one missing commit, |remote-commit2-sha_7|.  We look in the
   contents of |remote-commit2-sha_7| to find the tree object hash.  This is
   |new-tree|.  We check for this object in the remote objects directory, and
   sure enough, it is missing. We add this tree to the list of missing trees;
#. We only have one missing tree |--| |new-tree|. We look in the contents of
   this tree object and check in the remote object directory for each object
   in this listing. The only missing object is |new-file|;
#. We copy the objects for the missing commits (|before_paper|), missing trees
   (|new-tree|) and missing blobs (|new-file|) to the remote objects
   directory;
#. We set remote ``refs/heads/master`` to contain the hash
   |remote-commit2-sha_7|;
#. Set the local ``refs/remotes/usb_backup/master`` to contain
   |remote-commit2-sha_7|.

.. rubric:: Footnotes

.. [#sub-trees] You have probably worked out by now that git directory
   listings can have files (called "blobs") and subdirectories ("trees") (see
   :doc:`git_object_types`).  When doing the copy, we actually have to recurse
   into any sub-directories to get needed file ("blob") and subdirectory
   ("tree") objects.  But, you get the idea.

.. include:: links_names.inc
.. include:: working/object_names.inc

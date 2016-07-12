###########
Curious git
###########

In :doc:`curious_tale`, you built your own content management system.  Now you
have done that, you know how git works |--| because it works in exactly the
same way as your own system.  You will recognize hashes for files, directories
and commits, commits linked by reference to their parents, the staging area,
the ``objects`` directory, and bookmarks (branches).

Armed with this deep_ understanding, we retrace our steps to do the same
content management tasks in git.

*******************
Basic configuration
*******************

We need to tell git our name and email address before we start.

Git will use this information to fill in the author information in each
**commit message**, so we don't have to type it out every time.

.. nprun::

    git config --global user.name "Matthew Brett"
    git config --global user.email "matthew.brett@gmail.com"

The ``--global`` flag tells git to store this information in its default
configuration file for your user account.  On Unix (e.g. OSX and Linux) this
file is ``.gitconfig`` in your home directory.  Without the ``--global`` flag,
git only applies the configuration to the particular **repository** you are
working in.

Every time we make a commit, we need to type a commit message.  Git will open
our text editor for us to type the message, but first it needs to know what
text editor we prefer.  Set your own preferred text editor here::

    # gedit is a reasonable choice for Linux
    # "vi" is the default.
    git config --global core.editor gedit

We also turn on the use of color, which is very helpful in making the
output of git easier to read:

.. nprun::

    git config --global color.ui "auto"

************
Getting help
************

.. nprun::

    git help

Try ``git help add`` for an example.

.. note::

    The git help pages are famously hard to read if you don't know how git
    works. One purpose of this tutorial is to explain git in such a way that
    it will be easier to understand the help pages.

*************************************
Initializing the repository directory
*************************************

We first set this ``nobel_prize`` directory to be version controlled with git.
We start off the working tree with the original files for the paper:

.. workrun::
    :hide:

    rm -rf nobel_prize
    cp ../nobel_prize.zip .
    mkdir nobel_prize
    cp ../np-versions/work1/* nobel_prize

.. note::

    I highly recommend you type along.  Why not download
    :download:`nobel_prize.zip </np-versions/nobel_prize.zip>` and unzip the
    files to make the same ``nobel_prize`` directory as I have here?

.. prizeout::

    {{ np_tree }}

To get started with git, create the git **repository directory** with ``git
init``:

.. workrun::

    cd nobel_prize
    git init

What happened when we did ``git init``? Just what we were expecting; we have a
new repository directory in ``nobel_prize`` called ``.git``

.. prizeout::

    {{ np_tree }} .git --elide hooks

The ``objects`` directory looks familiar.  It has exactly the same purpose as
it did for your SAP system.  At the moment it contains a couple of empty
directories, because we have not added any objects yet.

**********************
Updating terms for git
**********************

Working directory
    The directory containing the files you are working on.  In our case this
    is ``nobel_prize``.  It contains the **repository directory**, named
    ``.git``.

Repository directory
    Directory containing all previous commits (snapshots) and git private
    files for working with commits.  The directory has name ``.git`` by
    default, and almost always in practice.

.. _git-add:

********************************************
git add |--| put stuff into the staging area
********************************************

In the next few sections, we will do our first commit (snapshot).

First we will put the files for the commit into the staging area.

The command to put files into the staging area is ``git add``.

To start, we show ourselves that the **staging area** is empty. We haven't yet
discussed the git implementation of the staging area, but this command shows
us which files are in the staging area.

.. nprun::

    git ls-files --stage

As expected, there are no files in the staging area yet.

.. note::

    ``git ls-files`` is a specialized command that you will not often need in
    your daily git life.  I'm using it here to show you how git works.

Now we do our add:

.. nprun::

    git add clever_analysis.py

Sure enough:

.. nprun::

    git ls-files --stage

.. prizevar:: analysis_1_hash

    git rev-parse :clever_analysis.py

********************
The git staging area
********************

It is time to think about what the staging area is, in git.  In your SAP
system, the staging area was a directory.  You also started off by using
directories to store commits (snapshots).  Later you found you could do
without the commit directories, because you could store the files in
``repo/objects`` and the directory structure in ``directory_listing.txt`` text
files.

In git, the staging area is a single file called ``.git/index``.  This file
contains a directory listing that is the equivalent of the ``staging``
directory in SAP.  When we add a file to the staging area, git backs up the
file with its hash to ``.git/objects``, and then changes the directory listing
inside ``.git/index`` to point to this backup copy.

If all that is true, then we now expect to see a) a new file ``.git/index``
containing the directory listing and b) a new file in the ``.git/objects``
directory corresponding to the hash for the ``clever_analysis.py`` file. We
saw from the output of ``git ls-files --stage`` above that the hash for
``clever_analysis.py`` is |analysis_1_hash|.  So |--| do we see these files?

First |--| there is now a new file ``.git/index`` that was not present in our
first listing of the ``.git`` directory above:

.. nprun::

    ls .git/index

Second, there is a new directory and file in ``.git/objects``:

.. prizevar:: sha_fname

    echo "function sha_fname { echo \${1:0:2}/\${1:2}; }; sha_fname "

.. prizevar:: analysis_fname

    fname=$({{ sha_fname }} {{ analysis_1_hash }})
    echo ".git/objects/$fname"

.. prizeout::

    {{ np_tree }} .git/objects

The directory and filename in ``.git/objects`` come from the hash of
``clever_analysis.py``.  The first two digits of the hash form the directory
name and the rest of the digits are the filename [#git-object-dir]_. So, the
file |analysis_fname| is the copy of ``clever_analysis.py`` that we added to
the staging area.

For extra points, what do you think would happen if we deleted the
``.git/index`` file (answer [#delete-git-index]_)?

***********
Git objects
***********

Git objects are nearly as simple as the objects you were writing in your SAP.
The hash is not the hash of the raw file, but the raw file prepended with a
short housekeeping string.  See :doc:`reading_git_objects` for details.

We can see the contents of objects with the command ``git cat-file -p``.  For
example, here are the contents of the backup we just made of
``clever_analysis.py``:

.. nprun::

    git cat-file -p {{ analysis_1_hash }}

.. note::

    I will use ``git cat-file -p`` to display the content of nearly raw git
    objects, to show the simplicity of git's internal model, but ``cat-file``
    is a specialized command that you won't use much in daily work.

Just as we expected, it is the current contents of the
``clever_analysis.py``.

The |analysis_1_hash| object is a hashed, stored raw file.  Because the object
is a stored file rather than a stored directory listing text file or commit
message text file, git calls this type of object a **blob** |--| for Binary
Large Object.  You can get the object *type* from the object hash with the
``-t`` flag to ``git cat-file``:

.. nprun::

    git cat-file -t {{ analysis_1_hash }}

**********************************************************
Hash values can usually be abbreviated to seven characters
**********************************************************

We only need to give git enough hash digits for git to identify the object
uniquely.  7 digits is nearly always enough, as in:

.. prizevar:: sha_7

    echo "function sha_7 { echo \${1:0:7}; }; sha_7 "

.. prizevar:: analysis_1_hash_7

    {{ sha_7 }} {{ analysis_1_hash }}

.. nprun::

    git cat-file -p {{ analysis_1_hash_7 }}

***************************************************************
git status |--| showing the status of files in the working tree
***************************************************************

The working tree is the contents of the ``nobel_prize`` directory, excluding
the ``.git`` repository directory.

``git status`` tells us about the relationship of the files in the working
tree to the repository and staging area.

We have done a ``git add`` on ``clever_analysis.py``, and that added the file
to the staging area.  We can see that this happened with ``git status``:

.. nprun::

    git status

Sure enough, the output tells us that ``new file: clever_analysis.py`` is in
the ``changes to be committed``.  It also tells us that the other two files in
the working directory are ``untracked``.

An untracked file is a file with a filename that is not listed the staging
area directory listing. Until you run ``git add`` on an untracked file, git
will ignore these files and assume you don't want to keep track of them.

************************************
Staging the other files with git add
************************************

We do want to keep track of the other files, so we stage them:

.. nprun::

    git add fancy_figure.png
    git add expensive_data.csv
    git status

We have staged all three of our files.  We have three objects in
``.git/objects``:

.. prizeout::

    {{ np_tree }} .git/objects

***********************************
git commit |--| making the snapshot
***********************************

.. prizecommit:: commit_1_sha 2012-04-01 14:30:13

    git commit -m "First backup of my amazing idea"

.. note::

    In the line above, I used the ``-m`` flag to specify a message at the
    command line. If I had not done that, git would open the editor I
    specified in the ``git config`` step above and ask me to enter a message.
    I'm using the ``-m`` flag so the commit command runs without interaction
    in this tutorial, but in ordinary use, I virtually never use ``-m``, and I
    suggest you don't either.  Using the editor for the commit message allows
    you to write a more complete commit message, and gives feedback about the
    ``git status`` of the commit to remind you what you are about to do.

Following the logic of your SAP system, we expect that the action of making
the commit will generate two new files in ``.git/objects``, one for the
directory listing text file, and another for the commit message:

.. prizeout::

    {{ np_tree }} .git/objects

Here is the contents of the commit message text file for the new commit.  Git
calls this a **commit object**:

.. nprun::

    git cat-file -p {{ commit_1_sha }}

.. nprun::

    # What type of git object is this?
    git cat-file -t {{ commit_1_sha }}

As for SAP, the commit message file contains the hash for the directory tree
file (``tree``), the hash of the parent (``parent``) (but this commit has no
parents), the author, date and time, and the note.

Here's the contents of the directory listing text file for the new commit.
Git calls this  a **tree** object.

.. prizevar:: commit_1_tree_sha

    git rev-parse HEAD:./

.. nprun::

    git cat-file -p {{ commit_1_tree_sha }}

.. nprun::

    git cat-file -t {{ commit_1_tree_sha }}

Each line in the directory listing gives the file permissions, the type of the
entry in the directory (where "tree" means a sub-directory, and "blob" means a
file), the file hash, and the file name (see :ref:`git-object-types`).

*****************************************
git log |--| what are the commits so far?
*****************************************

.. nprun::

    git log

Notice that git log identifies each commit with its hash.  The hash is the
hash for the contents of the commit message. As we saw above, the hash for our
commit was |commit_1_sha|.

We can also ask to the see the parents of each commit in the log:

.. nprun::

    git log --parents

Why are the output of ``git log`` and ``git log --parents`` the same in this
case? (answer [#no-parents]_).

************************************
git branch - which branch are we on?
************************************

Branches are bookmarks. They associate a name (like "my_bookmark" or "master")
with a commit (such as |commit_1_sha|).

The default branch (bookmark) for git is called ``master``. Git creates it
automatically when we do our first commit.

.. nprun::

    git branch

Asking for more verbose detail shows us that the branch is pointing to a
particular commit (where the commit is given by a hash):

.. nprun::

    git branch -v

In this case git abbreviated the 40 character hash to the first 7 digits,
because these are enough to uniquely identify the commit.

A branch is nothing but a name that points to a commit.  In fact, git stores
branches as we did in SAP, as tiny text files, where the filename is the name
of the branch, and the contents is the hash of the commit that it points to:

.. nprun::

    ls .git/refs/heads

.. nprun::

    cat .git/refs/heads/master

We will soon see that, if we are working on a branch, and we do a commit, then
git will update the branch to point to the new commit.

***************
A second commit
***************

In our second commit, we will add the first draft of the Nobel prize paper.
As before, you can download this from
:download:`nobel_prize.md </np-versions/work2/nobel_prize.md>`.  If you are
typing along, download ``nobel_prize.md`` to the ``nobel_prize`` directory.

The staging area does not have an entry for ``nobel_prize.md``, so ``git
status`` identifies this file as **untracked**:

.. nprun::
    :hide:

    cp {{ np_versions }}/work2/nobel_prize.md .

.. nprun::

    git status

We add the file to the staging area with ``git add``:

.. nprun::

    git add nobel_prize.md

Now ``git status`` records this file being in the staging area, by listing it
under "changes to be committed":

.. nprun::

    git status

Finally we move the changes from the staging area into a commit with ``git
commit``:

.. prizecommit:: commit_2_sha 2012-04-02 18:03.13

    git commit -m "Add first draft of paper"

Git shows us the first 7 digits of the new commit hash in the output from
``git commit`` |--| these are |commit_2_sha_7|.

Notice that the position of the current ``master`` branch is now this last
commit:

.. nprun::

    git branch -v

.. nprun::

    cat .git/refs/heads/master

We use ``git log`` to look at our short history.

.. nprun::

    git log

We add the ``--parents`` flag to show that the second commit points back to
the first via its hash.  Git lists the parent hash after the commit hash:

.. nprun::

    git log --parents

*******************************
git diff |--| what has changed?
*******************************

Our next commit will have edits to the ``clever_analysis.py`` script.  We will
also refresh the figure with the result of running the script.

I open the ``clever_analysis.py`` file in text editor and adjust the fudge
factor, add a new fudge factor, and apply the new factor to the data.

.. nprun::
    :hide:

    # Copy the updated version from the local archive
    cp {{ np_versions }}/work3/clever_analysis.py .

Now I've done these edits, I can ask ``git diff`` to show me how the files in
my working tree differ from the files in the staging area.

Remember, the files the staging area knows about so far are the files as of
the last commit.

.. nprun::

    git diff

A ``-`` at the beginning of the ``git diff`` output means I have removed this
line.  A ``+`` at the beginning means I have added this line.  As you see I
have edited one line in this file, and added three more.

Open your text editor and edit ``clever_analysis.py``.  See if you can
replicate my changes by editing the file, and checking with ``git diff``.

Now check the status of ``clever_analysis.py`` with:

.. nprun::

    git status

**************************************************************
You need to ``git add`` a file to put it into the staging area
**************************************************************

Remember that git only commits stuff that you have added to the staging area.

``git status`` tells us that ``clever_analysis.py`` has been "modified", and
that these changes are "not staged for commit".

There is a version of ``clever_analysis.py`` in the staging area, but it is
the version of the file as of the last commit, and so that version is
different from the version we have in the working tree.

If we try to do a commit, git will tell us there is nothing to commit, because
there is nothing new in the staging area:

.. nprun::
    :allow-fail:

    git commit

To stage this version of ``clever_analysis.py`` we use ``git add``:

.. nprun::

    git add clever_analysis.py

Git status now shows these changes as "Changes to be committed".

.. nprun::

    git status

We can update the figure by running the ``analysis_script.py`` script.  The
script analyzes the data and writes the figure to the current directory.  If
you have Python installed, with the ``numpy`` and ``matplotlib`` packages, you
can run the analysis yourself with::

    python clever_analysis.py

If not, you can download a :download:`version of the figure I generated
earlier </np-versions/work3/fancy_figure.png>`.  After you have generated or
downloaded the figure:

.. nprun::
    :hide:

    cp {{ np_versions }}/work3/fancy_figure.png .

.. nprun::

    git add fancy_figure.png

Do a final check with ``git status``, then make the commit with:

.. prizecommit:: commit_3_sha 2012-04-03 11:20:01

    git commit -m "Add another fudge factor"

The branch bookmark has moved again:

.. nprun::

    git branch -v

***************************
An ordinary day in gitworld
***************************

We now have the main commands for daily work with git;

* Make some changes in the working tree;
* Check what has changed with ``git status``;
* Review the changes with ``git diff``;
* Add changes to the staging area with ``git add``;
* Make the commit with ``git commit``.

***********
Commit four
***********

For our next commit, we will add some more changes to the analysis script and
figure, and add a new file, ``references.bib``.

To follow along, first download :download:`references.bib
</np-versions/work4/references.bib>`.

.. nprun::
    :hide:

    cp {{ np_versions }}/work4/references.bib .

Next, edit ``clever_analysis.py`` again, to make these changes:

.. nprun::
    :hide:

    cp {{ np_versions }}/work4/clever_analysis.py .

.. nprun::

    git diff

Finally regenerate ``fancy_figure.png``, or download the updated copy
:download:`from here </np-versions/work4/fancy_figure.png>`.

.. nprun::
    :hide:

    cp {{ np_versions }}/work4/fancy_figure.png .

What will git status show now?

.. nprun::

    git status

The staging area does not list a file called ``references.bib`` so this file
is "untracked".  The staging area does contain an entry for
``clever_analysis.py`` and ``fancy_figure.png``, so these files are tracked.
Git has checked the hashes for these files, and they are different from the
hashes in the staging area, so git knows these files have changed, compared
the versions listed in the staging area.

Before we add our changes, we confirm that they are as we expect with:

.. nprun::

    git diff

Notice that git does not try and show the line-by-line differences between the
old and new figures, guessing correctly that this is a binary and not a text
file.

Now we have reviewed the changes, we add them to the staging area and commit:

.. nprun::

    git add references.bib
    git add clever_analysis.py
    git add fancy_figure.png

.. prizecommit:: commit_4_sha 2012-04-04 01:40:42

    git commit -m "Change analysis and add references"

The branch bookmark has moved to point to the new commit:

.. nprun::

    git branch -v

***********************************
Undoing a commit with ``git reset``
***********************************

As you found in the SAP story, this last commit doesn't look quite right,
because the commit message refers to two different types of changes.  With
more git experience, you will likely find that you like to break your changes
into commits where the changes have a particular theme or purpose.  This makes
it easier to see what happened when you look over the history and the commit
messages with ``git log``.

So, as in the SAP story, you decide to undo the last commit, and replace it
with two commits:

* One commit to add the changes to the script and figure;
* Another commit on top of the first, to add the references file.

In the SAP story, you had to delete a snapshot directory manually, and reset
the staging area directory to have the contents of the previous commit.  In
git, all we have to do is reset the current ``master`` branch bookmark to
point to the previous commit.  By default, git will also reset the staging
area for us.  The command to move the branch bookmark is ``git reset``.

*****************************
Pointing backwards in history
*****************************

The commit that we want the branch to point to is the previous commit in our
commit history.  We can use ``git log`` to see that this commit has hash
|commit_3_sha_7|.  So, we could do our reset with ``git reset``
|commit_3_sha_7|.  There is a simpler and more readable way to write this
common idea, of one commit back in history, and that is to add ``~1`` to a
reference.  For example, to refer to the commit that is one step back in the
history from the commit pointed to by the ``master`` branch, you can write
``master~1``.  Because ``master`` points to commit |commit_4_sha_7|, you could
also append the ``~1`` to |commit_4_sha_7|.  You can imagine that ``master~2``
will point two steps back in the commit history, and so on.

So, a readable reset command for our purpose is:

.. nprun::

    git reset master~1

Notice that the branch pointer now points to the previous commit:

.. nprun::

    git branch -v

Remember in SAP that your procedure for breaking up the snapshot was to 1)
delete the old snapshot and 2) reset the staging area to reflect the previous
commit.  After you did this, the working tree contains your changes, but the
staging area does not.  You could make your new commits in the usual way, by
adding to the staging area, and doing the commits.

Notice that ``git reset`` has done the same thing.  It has reset the staging
area to the state as of the older commit, but it has left the working tree
alone.  That means that ``git status`` will show us the changes in the working
tree compared to the commit we have just reset to:

.. nprun::

    git status

We have the changes from our original fourth commit in our working tree, but
we have not staged them.  We are ready to make our new separate commits.

*******************
A new fourth commit
*******************

As we planned, we make a commit by adding only the changes from the script and
figure:

.. nprun::

    git add clever_analysis.py
    git add fancy_figure.png

.. prizecommit:: commit_4_dash_sha 2012-04-04 1:40:42

    git commit -m "Change parameters of analysis"

Notice that git status now tells us that we still have untracked (and
therefore not staged) changes in our working tree:

.. nprun::

    git status

****************
The fifth commit
****************

To finish our work splitting the fourth commit into two, we add and commit the
``references.bib`` file:

.. nprun::

    git add references.bib

.. prizecommit:: commit_5_sha 2012-04-04 2:10:02

    git commit -m "Add references"

***********************************************************
Getting a file from a previous commit |--| ``git checkout``
***********************************************************

In the SAP story, we found that the first version of the analysis script was
correct, and we made a new commit after restoring this version from the first
snapshot.

As you can imagine, git allows us to do that too.  The command to do this is
``git checkout``

If you have a look at ``git checkout --help`` you will see that git checkout
has two roles, described in the help as "Checkout a branch or paths to the
working tree".  We will see checking out a branch later, but here we are using
checkout in its second role, to restore files to the working tree.

We do this by telling git checkout which version we want, and what file we
want.  We want the version of ``clever_analysis.py`` as of the first commit.
To find the first commit, we can use git log.  To make git log a bit less
verbose, I've added the ``--oneline`` flag, to print out one line per commit:

.. nprun::

    git log --oneline

Now we have the abbreviated commit hash for the first commit, we can checkout
that version to the working tree:

.. nprun::

    git checkout {{ commit_1_sha_7 }} clever_analysis.py

We also want the previous version of the figure:

.. nprun::

    git checkout {{ commit_1_sha_7 }} fancy_figure.png

Notice that the checkout also added the files to the staging area:

.. nprun::

    git status

We are ready for our sixth commit:

.. prizecommit:: commit_6_sha 2012-04-05 18:40:04

    git commit -m "Revert to original script & figure"

***********************************
Using bookmarks |--| ``git branch``
***********************************

We are at the stage in the SAP story where Josephine goes away to the
conference.

Let us pretend that we are Josephine, and that we have taken a copy of the
working directory to the conference.

We as Josephine don't want to change the previous bookmark, which is
``master``:

.. nprun::

    git branch -v

We would like to use our own bookmark, so we can make changes without
affecting anyone else.  To do this we use ``git branch`` with arguments:

.. nprun::

    git branch josephines-branch master

The first argument is the name of the branch we want to create.  The second is
the commit at which the branch should start.  Now we have a new branch, that
currently points to the same commit as ``master``:

.. nprun::

    git branch -v

The new branch is nothing but a text file pointing to the commit:

.. nprun::

    cat .git/refs/heads/josephines-branch

Now we have two branches, git needs to know which branch we are working on.
The asterisk next to ``master`` in the output of ``git branch`` means that we
are working on ``master`` at the moment.  If we make another commit, it will
update the ``master`` bookmark.

Git stores the current branch in the file ``.git/HEAD``:

.. nprun::

    cat .git/HEAD

Git commands often allow you to write ``HEAD`` meaning "the branch or commit
you are currently working on".  For example, ``git log HEAD`` means "show the
log starting at the branch or commit you are currently working on".  In fact,
this is also the default behavior of ``git log``.

We now want to make ``josephines-branch`` current, so any new commits will
update ``josephines-branch`` instead of ``master``.

*************************************************
Changing the current branch with ``git checkout``
*************************************************

We previously saw that ``git checkout <commit> <filename>`` will get the
file ``<filename>`` as of commit ``<commit>``, and restore it to the working
tree.  This was the second of the two uses of ``git checkout``.  We now come
to the first and most common use of ``git checkout``, which is to:

* change the current branch to a given branch or commit;
* restore the working tree and staging area to the file versions from the
  given commit.

We are about to do ``git checkout josephines-branch``.  When we do this, we
are only going to see the first of these two effects, because ``master`` and
``josephines-branch`` point to the same commit, and so have the same file
contents:

.. nprun::

    git checkout josephines-branch

The asterisk has now moved to ``josephines-branch``:

.. nprun::

    git branch -v

This is because the file ``HEAD`` now points to ``josephines-branch``:

.. nprun::

    cat .git/HEAD

If we do a commit, git will update ``josephines-branch``, not ``master``.

**************************
Making commits on branches
**************************

Josephine did some edits to the paper.  If you are typing along, make these
changes to ``nobel_prize.md``:

.. nprun::
    :hide:

    cp {{ np_versions }}/work7j/nobel_prize.md .

.. nprun::

    git diff

As usual, we add the file to the staging area, and check the status of the
working tree:

.. nprun::

    git add nobel_prize.md
    git status

Finally we make the commit:

.. prizecommit:: commit_7j_sha 2012-04-06 14:30:14

    git commit -m "Expand the introduction"

The ``master`` branch has not changed, but ``josephines-branch`` changed to
point to the new commit:

.. nprun::

    git branch -v

Now we go back to being ourselves, working in the lab.  We change back to the
``master`` branch:

.. nprun::

    git checkout master

The asterisk now points at ``master``:

.. nprun::

    git branch -v

If you look at the contents of ``nobel_prize.md`` in the working directory,
you will see that we are back to the contents before Josephine's changes.
This is because ``git checkout master`` reverted the files to their state as
of the last commit on the ``master`` branch.

Now we make our own changes to the script and figure. Here are the changes to
the script:

.. nprun::
    :hide:

    cp {{ np_versions }}/work7m/clever_analysis.py .

.. nprun::

    git diff

If you are typing along, then you will also want to regenerate the figure with
``python clever_analysis.py`` or :download:`download the new version
</np-versions/work7m/fancy_figure.png>`.

.. nprun::
    :hide:

    cp {{ np_versions }}/work7m/fancy_figure.png .

This gives:

.. nprun::

    git status

As usual, we add the files and do the commit:

.. nprun::

    git add clever_analysis.py
    git add fancy_figure.png

.. prizecommit:: commit_7_sha 2012-04-06 11:03:13

    git commit -m "More fun with fudge"

Because ``HEAD`` currently current points to ``master``, git updated the
``master`` branch with the new commit:

.. nprun::

    git branch -v

***********************************************
Merging lines of development with ``git merge``
***********************************************

We next want to get Josephine's changes into the ``master`` branch.

We do this with ``git merge``:

.. nprun::

    git merge josephines-branch

This commit has the changes we just made to the script and figure, and the
changes the Josephine made to the paper.

The commit has two parents, which are the two commits from which we merged:

.. nprun::

    git log --oneline --parents

************************************************************
The commit parents make the development history into a graph
************************************************************

As you saw in your SAP system, we can think of the commits as nodes in a
graph.  Each commit stores the identity of its parent commit(s).  The pointers
from each commit back to its parent(s) link the commits (nodes) to form edges.

It is common to see a git history shown as a graph, and it is often useful to
think of this graph when we are working with a git repository.

There are a lot of graphical tools to show the git history as a graph, but
``git log`` has a useful flag called ``--graph`` which shows the commits as a
graph using text characters:

.. nprun::

    git log --oneline --graph

This kind of display is so useful that many of us have a shortcut to this
command, that we use instead of the standard git log.  You can make customized
shortcuts to git commands by setting ``alias`` entries using ``git config``.
For example, you may want to set up an alias like this:

.. nprun::

    git config --global alias.slog "log --oneline --graph"

Now you can use the command ``git slog`` to mean ``git log --oneline
--graph``.  Because of the ``--global`` flag, this command sets up the
``slog`` alias as the default for your user account, so you can use ``git
slog`` whenever you are using git as this user on this computer.

.. nprun::

    git slog

*******************************
Other commands you need to know
*******************************

This tutorial gives you the basics on working with files on your own computer,
and on your own repository.

You will also need to know about:

* git remotes |--| making backups; working with other people.  See
  :doc:`curious_remotes`;
* tags |--| making static bookmarks to commits;

You will probably also find use for:

* `git reflog
  <http://www.kernel.org/pub/software/scm/git/docs/git-reflog.html>`_ |--|
  show a list of previous commits that you have made;
* `git rebase
  <http://www.kernel.org/pub/software/scm/git/docs/git-rebase.html>`_ |--|
  rewrite the development history by altering or transplanting commits.  See
  `rebase without tears`_.

*******************
Git: are you ready?
*******************

If you followed this tutorial, you now have a good knowledge of how git works.
This will make it much easier to understand why git commands do what they do,
and what to do when things go wrong.  You know all the main terms that the git
manual pages use, so git's own help will be more useful to you.  You will
likely lead a long life of deep personal fulfillment.

****************************
Other git-ish things to read
****************************

As you've seen, this tutorial makes the bold assumption that you'll be able to
understand how git works by seeing how it is *built*. These documents take a
similar approach to varying levels of detail:

* The `Git parable
  <http://tom.preston-werner.com/2009/05/19/the-git-parable.html>`__ by Tom
  Preston-Werner;
* The `visual git tutorial
  <http://www.ralfebert.de/blog/tools/visual_git_tutorial_1>`__ gives a nice
  visual idea of git at work;
* `Understanding Git Conceptually
  <http://www.sbf5.com/~cduan/technical/git>`__ gives another review of how
  the ideas behind git;
* For more detail, see the start of the excellent `Pro Git
  <http://progit.org/book>`__ online book, or similarly the early parts of the
  `Git community book <http://book.git-scm.com>`__. Pro Git's chapters are
  very short and well illustrated; the community book tends to have more
  detail and has nice screencasts at the end of some sections;
* `git foundation`_;

You might also try:

* For windows users, `an Illustrated Guide to Git on Windows
  <http://nathanj.github.com/gitguide/tour.html>`__ is useful in that it
  contains also some information about handling SSH (necessary to interface
  with git hosted on remote servers when collaborating) as well as screenshots
  of the Windows interface.
* `Git ready <http://www.gitready.com>`__ A great website of posts on specific
  git-related topics, organized by difficulty.
* `QGit <http://sourceforge.net/projects/qgit/>`__: an excellent Git GUI Git
  ships by default with gitk and git-gui, a pair of Tk graphical clients to
  browse a repo and to operate in it. I personally have found `qgit
  <http://sourceforge.net/projects/qgit/>`__ to be nicer and easier to use. It
  is available on modern Linux distros, and since it is based on Qt, it should
  run on OSX and Windows.
* `Git Magic
  <http://www-cs-students.stanford.edu/~blynn/gitmagic/index.html>`_ : Another
  book-size guide that has useful snippets.
* The `learning center <http://learn.github.com>`__ at Github Guides on a
  number of topics, some specific to github hosting but much of it of general
  value.
* A `port <http://cworth.org/hgbook-git/tour>`__ of the Hg book's beginning
  The `Mercurial book <http://hgbook.red-bean.com>`__ has a reputation for
  clarity, so Carl Worth decided to `port
  <http://cworth.org/hgbook-git/tour>`__ its introductory chapter to Git. It's
  a nicely written intro, which is possible in good measure because of how
  similar the underlying models of Hg and Git ultimately are.
* `Intermediate tips
  <http://andyjeffries.co.uk/articles/25-tips-for-intermediate-git-users>`_: A
  set of tips that contains some very valuable nuggets, once you're past the
  basics.

.. rubric:: Footnotes

.. [#delete-git-index] What would happen if we delete the ``.git/index`` file?
   Remember, the ``.git/index`` file contains the directory listing for the
   staging area.  If we delete the file, git will assume that the directory
   listing is empty, and therefore that there are no files in the staging
   area.
.. [#no-parents] Why are the output of ``git log`` and ``git log --parents``
   the same in this case?  They are the same because this is the first commit,
   and the first commit has no parents.
.. [#git-object-dir] When git stores a file in the ``.git/objects`` directory,
   it makes a hash from the file, takes the first two digits of the hash to
   make a directory name, and then stores a file in this directory with a
   filename from the remaining hash digits.  For example, when adding a file
   with hash ``d92d079af6a7f276cc8d63dcf2549c03e7deb553`` git will create
   ``.git/objects/d9`` directory if it doesn't exist, and stores the file
   contents as ``.git/objects/d9/2d079af6a7f276cc8d63dcf2549c03e7deb553``.  It
   does this so that the number of files in any one directory stay in a
   reasonable range.  If git had to store hash filenames for every object in
   one flat directory, the directory would soon have a very large number of
   files.

.. include:: links_names.inc
.. include:: working/object_names.inc

#!/bin/bash
# Commands to make git repository for rebase page
# If you run this inside the git repo, don't forget to remove the generated git
# repos, they can be annoying to remove with git clean etc because they look
# like submodules

function make_repo {
    local repo_name=$1
    rm -rf $repo_name
    mkdir $repo_name
    cd $repo_name
    git init
}

function make_commit {
    local cname=$1
    local cfile=${cname}_file
    touch ${cfile}
    git add $cfile
    git commit -m "$cname"
}


# History 1
make_repo history1
make_commit D
git branch at-root
make_commit E
git co -b topic
make_commit A
make_commit B
make_commit C
git co main
make_commit F
make_commit G
cd ..

# History 2
make_repo history2
make_commit A
make_commit B
make_commit C
make_commit D
git co -b topicA
make_commit E
make_commit F
make_commit G
git co -b topicB main
make_commit H
make_commit I
make_commit J
cd ..

# Root example
make_repo root-example
make_commit A
make_commit B
make_commit C
make_commit D
# Make detached branch
git symbolic-ref HEAD refs/heads/other-branch
rm *
rm .git/index
make_commit X
make_commit Y
make_commit Z


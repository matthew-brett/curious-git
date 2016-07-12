.. vim: ft=rst
.. Initialize the nobel_prize directory, and directory listing stuff

.. workrun::
    :hide:

    # clean up old files from previous doc run
    rm -rf nobel_prize repos .gitconfig
    mkdir nobel_prize
    cp ../np-versions/work1/* nobel_prize

.. prizevar:: np_versions
    :omit_link:

    echo "../../np-versions"

.. prizevar:: np_tools
    :omit_link:

    echo "../../np-tools"

.. prizevar:: np_tree
    :omit_link:

    echo "{{ np_tools }}/show_tree"

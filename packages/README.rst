Galaxy dependency definitions
=============================

These packages are now obsolete as Galaxy has transitioned to using
Conda and the BioConda channel for packaging tool dependencies.
Specifically, we now use https://anaconda.org/bioconda/blast for the
NCBI BLAST+ binaries.

Each sub-folder represents a different entry on the Galaxy ToolShed, for
example ``package_blast_plus_2_2_31`` defines the BLAST+ 2.2.31 dependency
which can be used by other Galaxy ToolShed entries via the IUC owned
https://toolshed.g2.bx.psu.edu/view/iuc/package_blast_plus_2_2_31

Each folder has a (hidden) special file ``.shed.yml`` for use with the
command line tool Planemo to help automate pushing updates to the Galaxy
Tool Shed, e.g.

    $ planemo shed_update --shed_target testtoolshed --check_diff package_blast_plus_2_2_31
    ...
    $ planemo shed_update --shed_target toolshed --check_diff package_blast_plus_2_2_31
    ...

For general information, see the `main README file <../README.rst>`_.

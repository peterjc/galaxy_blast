Galaxy wrappers for NCBI BLAST+ suite
=====================================

These wrappers are copyright 2010-2013 by Peter Cock (The James Hutton Institute,
UK) and additional contributors. All rights reserved. See the licence text below.

Currently tested with NCBI BLAST 2.2.28+ (i.e. version 2.2.28 of BLAST+),
and does not work with the NCBI 'legacy' BLAST suite (e.g. ``blastall``).

Note that these wrappers (and the associated datatypes) were originally
distributed as part of the main Galaxy repository, but as of August 2012
moved to the Galaxy Tool Shed as ``ncbi_blast_plus`` (and ``blast_datatypes``).
My thanks to Dannon Baker from the Galaxy development team for his assistance
with this.

These wrappers are available from the Galaxy Tool Shed at:
http://toolshed.g2.bx.psu.edu/view/devteam/ncbi_blast_plus


Automated Installation
======================

Galaxy should be able to automatically install the dependencies, i.e. the
``blast_datatypes`` repository which defines the BLAST XML file format
(``blastxml``) and protein and nucleotide BLAST databases (``blastdbp`` and
``blastdbn``).

See the configuration notes below.

Manual Installation
===================

For those not using Galaxy's automated installation from the Tool Shed, put
the XML and Python files in the ``tools/ncbi_blast_plus/`` folder and add the
XML files to your ``tool_conf.xml`` as normal (and do the same in
``tool_conf.xml.sample`` in order to run the unit tests). For example, use::

  <section name="NCBI BLAST+" id="ncbi_blast_plus_tools">
    <tool file="ncbi_blast_plus/ncbi_blastn_wrapper.xml" />
    <tool file="ncbi_blast_plus/ncbi_blastp_wrapper.xml" />
    <tool file="ncbi_blast_plus/ncbi_blastx_wrapper.xml" />
    <tool file="ncbi_blast_plus/ncbi_tblastn_wrapper.xml" />
    <tool file="ncbi_blast_plus/ncbi_tblastx_wrapper.xml" />
    <tool file="ncbi_blast_plus/ncbi_makeblastdb.xml" />
    <tool file="ncbi_blast_plus/ncbi_dustmasker_wrapper.xml" />
    <tool file="ncbi_blast_plus/ncbi_blastdbcmd_wrapper.xml" />
    <tool file="ncbi_blast_plus/ncbi_blastdbcmd_info.xml" />
    <tool file="ncbi_blast_plus/ncbi_rpsblast_wrapper.xml" />
    <tool file="ncbi_blast_plus/ncbi_rpstblastn_wrapper.xml" />
    <tool file="ncbi_blast_plus/blastxml_to_tabular.xml" />
  </section>

You will also need to install ``blast_datatypes`` from the Tool Shed. This
defines the BLAST XML file format (``blastxml``) and protein and nucleotide
BLAST databases composite file formats (``blastdbp`` and ``blastdbn``):

* http://toolshed.g2.bx.psu.edu/view/devteam/blast_datatypes

As described above for an automated installation, you must also tell Galaxy
about any system level BLAST databases using the ``tool-data/blastdb*.loc``
files.

You must install the NCBI BLAST+ standalone tools somewhere on the system
path. Currently the unit tests are written using "BLAST 2.2.28+".

Run the functional tests (adjusting the section identifier to match your
``tool_conf.xml.sample`` file)::

    ./run_functional_tests.sh -sid NCBI_BLAST+-ncbi_blast_plus_tools

Configuration
=============

You must tell Galaxy about any system level BLAST databases using configuration
files blastdb.loc (nucleotide databases like NT) and blastdb_p.loc (protein
databases like NR), and blastdb_d.loc (protein domain databases like CDD or
SMART) which are located in the tool-data/ folder. Sample files are included
which explain the tab-based format to use.

You can download the NCBI provided databases as tar-balls from here:

* ftp://ftp.ncbi.nlm.nih.gov/blast/db/ (nucleotide and protein databases like NR)
* ftp://ftp.ncbi.nih.gov/pub/mmdb/cdd/little_endian/ (domain databases like CDD)

If using the optional taxonomy columns, you will also need to download the
NCBI taxonomy files (``taxdb.btd`` and ``taxdb.bti`` from ``taxdb.tar.gz`` on
the BLAST database FTP site). Currently explicit version tracking of the
taxonomy is not supported, and in order to use this you must set the
``$BLASTDB`` environment variable to include the path where you unzipped the
taxonomy files. If this is not done, the taxonomy columns like species name
will appear as ``N/A`` in the tabular output.

The BLAST+ binaries support multi-threaded operation, which is handled via the
$GALAXY_SLOTS environment variable. This should be set automatically by Galaxy
via your job runner settings, which allows you to (for example) allocate four
cores to each BLAST job.

In addition, the BLAST+ wrappers also support high level parallelism by task
splitting if ``use_tasked_jobs = True`` is enabled in your ``universe_wsgi.ini``
configuration file. Essentially, the FASTA input query files are broken up into
batches of 1000 sequences, a separate BLAST child job is run for each chunk,
and then the BLAST output files are merged (in order). This is transparent
for the end user.

History
=======

======= ======================================================================
Version Changes
------- ----------------------------------------------------------------------
v0.0.11 - Final revision as part of the Galaxy main repository, and the
          first release via the Tool Shed
v0.0.12 - Implements genetic code option for translation searches.
        - Changes <parallelism> to 1000 sequences at a time (to cope with
          very large sets of queries where BLAST+ can become memory hungry)
        - Include warning that BLAST+ with subject FASTA gives pairwise
          e-values
v0.0.13 - Use the new error handling options in Galaxy (the previously
          bundled hide_stderr.py script is no longer needed).
v0.0.14 - Support for makeblastdb and blastdbinfo with local BLAST databases
          in the history (using work from Edward Kirton), requires v0.0.14
          of the 'blast_datatypes' repository from the Tool Shed.
v0.0.15 - Stronger warning in help text against searching against subject
          FASTA files (better looking e-values than you might be expecting).
v0.0.16 - Added repository_dependencies.xml for automates installation of the
          'blast_datatypes' repository from the Tool Shed.
v0.0.17 - The BLAST+ search tools now default to extended tabular output
          (all too often our users where having to re-run searches just to
          get one of the missing columns like query or subject length)
v0.0.18 - Defensive quoting of filenames in case of spaces (where possible,
          BLAST+ handling of some multi-file arguments is problematic).
v0.0.19 - Added wrappers for rpsblast and rpstblastn, and new blastdb_d.loc
          for the domain databases they use (e.g. CDD, PFAM or SMART).
        - Correct case of exception regular expression (for error handling
          fall-back in case the return code is not set properly).
        - Clearer naming of output files.
v0.0.20 - Added unit tests for BLASTN and TBLASTX.
        - Added percentage identity option to BLASTN.
        - Fallback on ElementTree if cElementTree missing in XML to tabular.
        - Link to Tool Shed added to help text and this documentation.
        - Tweak dependency on blast_datatypes to also work on Test Tool Shed.
        - Dependency on new package_blast_plus_2_2_26 in Tool Shed.
        - Adopted standard MIT License.
        - Development moved to GitHub, https://github.com/peterjc/galaxy_blast
        - Updated citation information (Cock et al. 2013).
v0.0.21 - Use macros to simplify the XML wrappers.
        - Added wrapper for dustmasker.
        - Enabled masking for makeblastdb.
        - Requires 'maskinfo-asn1' and 'maskinfo-asn1-binary' datatypes.
          defined in updated blast_datatypes on Galaxy ToolShed.
        - Tests updated for BLAST+ 2.2.27 instead of BLAST+ 2.2.26.
        - Now depends on package_blast_plus_2_2_27 in ToolShed.
v0.0.22 - More use macros to simplify the wrappers.
        - Set number of threads via $GALAXY_SLOTS environment variable.
        - More descriptive default output names.
        - Tests require updated BLAST DB definitions (blast_datatypes v0.0.18).
        - Pre-check for duplicate identifiers in makeblastdb wrapper.
        - Tests updated for BLAST+ 2.2.28 instead of BLAST+ 2.2.27.
        - Now depends on package_blast_plus_2_2_28 in ToolShed.
        - Extended tabular output includes 'salltitles' as column 25.
v0.1.00 - Now depends on package_blast_plus_2_2_29 in ToolShed.
        - Tabular output now includes option to pick specific columns,
          including previously unavailable taxonomy columns.
        - BLAST XML to tabular tool supports multiple input files.
        - More detailed descriptions for BLASTN and BLASTP task option.
        - Wrappers for segmasker, dustmasker and convert2blastmask.
        - Supports using maskinfo with makeblastdb wrapper.
        - Supports setting a taxonomy ID in makeblastdb wrapper.
        - Subtle changes like new conditional settings will require some old
          workflows be updated to cope. 
======= ======================================================================


Bug Reports
===========

You can file an issue here https://github.com/peterjc/galaxy_blast/issues or ask
us on the Galaxy development list http://lists.bx.psu.edu/listinfo/galaxy-dev


Developers
==========

This script and related tools were originally developed on the 'tools' branch
of the following Mercurial repository:
https://bitbucket.org/peterjc/galaxy-central/

As of July 2013, development is continuing on a dedicated GitHub repository:
https://github.com/peterjc/galaxy_blast

For making the "Galaxy Tool Shed" http://toolshed.g2.bx.psu.edu/ tarball I use
the following command from the GitHub repository root folder::

    $ tools/ncbi_blast_plus/make_ncbi_blast_plus.sh

This simplifies ensuring a consistent set of files is bundled each time,
including all the relevant test files.

When updating the version of BLAST+, many of the sample data files used for
the unit tests must be regenerated. This script automates that task::

    $ tools/ncbi_blast_plus/update_test_files.sh


Licence (MIT)
=============

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

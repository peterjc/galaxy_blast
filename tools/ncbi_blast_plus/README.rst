Galaxy wrappers for NCBI BLAST+ suite
=====================================

These wrappers are copyright 2010-2018 by Peter Cock (James Hutton Institute,
UK) and additional contributors including Edward Kirton, John Chilton, Nicola
Soranzo, Jim Johnson, Bjoern Gruening, Caleb Easterly, and Anton Nekrutenko.
See the licence text below.

Note this does not work with the NCBI 'legacy' BLAST suite written in C
(e.g. binary name ``blastall``), but its replacement BLAST, which is
written in C++ (e.g. binary name ``blastn``).

Note that these wrappers (and the associated datatypes) were originally
distributed as part of the main Galaxy repository, but as of August 2012
moved to the Galaxy Tool Shed as ``ncbi_blast_plus`` (and ``blast_datatypes``).
My thanks to Dannon Baker from the Galaxy development team for his assistance
with this.

These wrappers are available from the Galaxy Tool Shed at:
http://toolshed.g2.bx.psu.edu/view/devteam/ncbi_blast_plus

In-development test releases are available from the Test Tool Shed at:
http://testtoolshed.g2.bx.psu.edu/view/devteam/ncbi_blast_plus/


Citation
========

Please cite the following paper:

NCBI BLAST+ integrated into Galaxy.
P.J.A. Cock, J.M. Chilton, B. Gruening, J.E. Johnson, N. Soranzo
GigaScience, 2015, 4:39 https://doi.org/10.1186/s13742-015-0080-7

You should also cite the NCBI BLAST+ tools:

BLAST+: architecture and applications.
C. Camacho et al. BMC Bioinformatics 2009, 10:421.
https://doi.org/10.1186/1471-2105-10-421


Automated Installation
======================

Galaxy should be able to automatically install the dependencies, i.e. the
BLAST+ binaries and the ``blast_datatypes`` repository which defines the
BLAST XML file format (``blastxml``), protein and nucleotide BLAST databases
(``blastdbp`` and ``blastdbn``), and so on.

See the configuration notes below.

Manual Installation
===================

For those not using Galaxy's automated installation from the Tool Shed, put
the XML and Python files in the ``tools/ncbi_blast_plus/`` folder and add the
XML files to your ``tool_conf.xml`` as normal.  For example, use::

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
    <tool file="ncbi_blast_plus/ncbi_makeprofiledb.xml" />
    <tool file="ncbi_blast_plus/blastxml_to_tabular.xml" />
  </section>

You will also need to install ``blast_datatypes`` from the Tool Shed. This
defines the BLAST XML file format (``blastxml``), BLAST databases, etc:

* http://toolshed.g2.bx.psu.edu/view/devteam/blast_datatypes

As described above for an automated installation, you must also tell Galaxy
about any system level BLAST databases using the ``tool-data/blastdb*.loc``
files. Also merge the ``tool-data/tool_data_table_conf.xml.sample`` contents
into your ``tool_data_table_conf.xml`` file.

You must install the NCBI BLAST+ standalone tools somewhere on the system
path. Currently the unit tests are written using BLAST+ 2.2.30.

Run the functional tests (adjusting the section identifier to match your
``tool_conf.xml.sample`` file)::

    ./run_tests.sh -sid NCBI_BLAST+-ncbi_blast_plus_tools

Configuration
=============

You must tell Galaxy about any system level BLAST databases using configuration
files ``blastdb.loc`` (nucleotide databases like NT) and ``blastdb_p.loc``
(protein databases like NR), and ``blastdb_d.loc`` (protein domain databases
like CDD or SMART) which are located in the ``tool-data/`` folder. Sample
files are included which explain the tab-based format to use.

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
``$GALAXY_SLOTS`` environment variable. This should be set automatically by
Galaxy via your job runner settings, which allows you to (for example) allocate
four cores to each BLAST job.

In addition, the BLAST+ wrappers also support high level parallelism by task
splitting if ``use_tasked_jobs = True`` is enabled in the ``config/galaxy.ini``
configuration file (previously ``universe_wsgi.ini`` on older versions of
Galaxy). Essentially, the FASTA input query files are broken up into
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
        - Changes ``<parallelism>`` to 1000 sequences at a time (to cope with
          very large sets of queries where BLAST+ can become memory hungry)
        - Include warning that BLAST+ with subject FASTA gives pairwise
          e-values
v0.0.13 - Use the new error handling options in Galaxy (the previously
          bundled ``hide_stderr.py`` script is no longer needed).
v0.0.14 - Support for makeblastdb and blastdbinfo with local BLAST databases
          in the history (using work from Edward Kirton), requires v0.0.14
          of the ``blast_datatypes`` repository from the Tool Shed.
v0.0.15 - Stronger warning in help text against searching against subject
          FASTA files (better looking e-values than you might be expecting).
v0.0.16 - Added repository_dependencies.xml for automates installation of the
          ``blast_datatypes`` repository from the Tool Shed.
v0.0.17 - The BLAST+ search tools now default to extended tabular output
          (all too often our users where having to re-run searches just to
          get one of the missing columns like query or subject length)
v0.0.18 - Defensive quoting of filenames in case of spaces (where possible,
          BLAST+ handling of some multi-file arguments is problematic).
v0.0.19 - Added wrappers for rpsblast and rpstblastn, and new ``blastdb_d.loc``
          for the domain databases they use (e.g. CDD, PFAM or SMART).
        - Correct case of exception regular expression (for error handling
          fall-back in case the return code is not set properly).
        - Clearer naming of output files.
v0.0.20 - Added unit tests for BLASTN and TBLASTX.
        - Added percentage identity option to BLASTN.
        - Fallback on ElementTree if cElementTree missing in XML to tabular.
        - Link to Tool Shed added to help text and this documentation.
        - Tweak dependency on ``blast_datatypes`` to also work on Test Tool Shed.
        - Dependency on new ``package_blast_plus_2_2_26`` in Tool Shed.
        - Adopted standard MIT License.
        - Development moved to GitHub, https://github.com/peterjc/galaxy_blast
        - Updated citation information (Cock et al. 2013).
v0.0.21 - Use macros to simplify the XML wrappers (by John Chilton).
        - Added wrapper for dustmasker.
        - Enabled masking for makeblastdb (Nicola Soranzo).
        - Requires ``maskinfo-asn1`` and ``maskinfo-asn1-binary`` datatypes,
          defined in ``blast_datatypes`` v0.0.17  on Galaxy ToolShed.
        - Tests updated for BLAST+ 2.2.27 instead of BLAST+ 2.2.26.
        - Now depends on ``package_blast_plus_2_2_27`` in ToolShed.
v0.0.22 - More use of macros to simplify the wrappers.
        - Set number of threads via ``$GALAXY_SLOTS`` environment variable.
        - More descriptive default output names.
        - Tests require updated BLAST DB definitions (``blast_datatypes`` v0.0.18).
        - Pre-check for duplicate identifiers in ``makeblastdb`` wrapper.
        - Tests updated for BLAST+ 2.2.28 instead of BLAST+ 2.2.27.
        - Now depends on ``package_blast_plus_2_2_28`` in ToolShed.
        - Extended tabular output includes 'salltitles' as column 25.
v0.1.00 - Now depends on ``package_blast_plus_2_2_29`` in ToolShed.
        - Tabular output now includes option to pick specific columns
          (based on contribution from Jim Johnson), including previously
          unavailable taxonomy columns.
        - BLAST XML to tabular tool supports multiple input files
          (based on contribution from Jim Johnson).
        - More detailed descriptions for BLASTN and BLASTP task option.
        - Wrappers for segmasker, dustmasker and convert2blastmask
          (contribution from Bjoern Gruening).
        - Supports using maskinfo with ``makeblastdb`` wrapper.
        - Supports setting a taxonomy ID in ``makeblastdb`` wrapper.
        - Subtle changes like new conditional settings will require some old
          workflows be updated to cope.
v0.1.01 - Requires ``blastdbd`` datatype (``blast_datatypes`` v0.0.19).
        - Wrapper for makeprofiledb added to create protein domain databases
          (based on contribution from Bjoern Gruening).
        - The RPS-BLAST and RPS-TBLASTN wrappers support using a protein
          domain database from the user's history.
        - Tool definitions now embed citation information (by John Chilton).
        - BLAST tools support GI and SeqID filters (added by Bjoern Gruening).
v0.1.02 - Now depends on ``package_blast_plus_2_2_30`` in ToolShed.
        - Tests updated for BLAST+ 2.2.30 instead of BLAST+ 2.2.29.
        - New tasks ``blastp-fast``, ``blastx-fast`` and ``tblastn-fast``.
        - New minimum query HSP coverage option, ``-qcov_hsp_perc``.
        - Removed ``-word_size`` from RPS-BLAST and RPS-TBLASTN wrappers, this
          is set during database construction and should not have been offered
          as a command line option in releases prior to BLAST+ 2.2.30.
        - BLAST database ``blastdb*.loc`` files now accessed via the XML
          table definitions in Galaxy's ``tool_data_table_conf.xml`` file,
          setup via ``tool-data/tool_data_table_conf.xml.sample``
        - Replace ``.extra_files_path`` with ``.files_path`` (internal change,
          thanks to Bjoern Gruening and John Chilton).
        - Added *"NCBI BLAST+ integrated into Galaxy"* preprint citation.
v0.1.03 - Reorder XML elements (internal change only).
        - Planemo for Tool Shed upload (``.shed.yml``, internal change only).
v0.1.04 - Fixed regression using BLAST databases from the history. Currently
          Galaxy inputs must still use ``.extra_files_path`` rather than the
          more consise ``.extra_files`` available for output files (Issue #69)
v0.1.05 - Define ``parallelism`` tag via a macro (internal change only).
        - Define wrapper versions via a macro (internal change only).
        - Update citation information now GigaScience paper is out.
v0.1.06 - Now depends on ``package_blast_plus_2_2_31`` in ToolShed.
        - Tests updated for BLAST+ 2.2.31 instead of BLAST+ 2.2.30.
v0.1.07 - Re-enabled some ``*.loc`` file tests (these had not been supported
          on the Tool Shed test framework, but that is not currently in use).
        - Fixed macro problem with version field in blastxml_to_tabular.xml
          (contribution from Bjoern Gruening and Daniel Blankenberg).
v0.1.08 - Allow searching against multiple locally installed databases
          (contribution from Gildas Le Corguillé and Emma Prudent).
        - Minor XML and Python style changes (internal change only).
        - Set ``allow_duplicate_entries="False"`` in sample configuration file
          ``tool_data_table_conf.xml``.
        - Fix identifers with pipes in ``blastdbcmd`` wrapper (Devon Ryan).
v0.2.00 - Updated for NCBI BLAST+ 2.5.0, where GI numbers are less visible,
          tabular output changes with `-parse_deflines`, and percentage
          identifies are now given to 3dp rather than 2dp.
        - Depends on ``package_blast_plus_2_5_0`` in ToolShed, or BioConda.
        - ``blastxml_to_tabular`` now also gives percentage idenity to 3dp.
        - Removed never-used binary and Python module dependency declarations
          (internal change only).
v0.2.01 - Use ``<command detect_errors="aggressive">`` (internal change only).
        - Single quote command line arguments (internal change only).
        - Show BLAST command line argument corresponding to each tool
          parameter (contribution from Nicola Soranzo).
        - Add ``-max_hsps`` option (contribution from Nicola Soranzo).
        - Add ``-use_sw_tback`` option for BLASTP (Nicola Soranzo).
v0.2.02 - Document the BLAST+ 2.5.0 change in the standard 12 column output
          from ``qseqid,sseqid,...`` to ``qacc,sacc,...`` instead.
        - Support for per-matrix recommended gaps settings (``-gapopen`` and
          ``-gapextend``, contribution from Caleb Easterly and Jim Johnson).
        - Support for ``-window_size``, ``-threshold``, ``-comp_based_stats``
          and revising ``-word_size`` to avoid using zero to mean default
          (contribution from Caleb Easterly).
v0.3.0  - Updated for NCBI BLAST+ 2.7.1,
        - Depends on BioConda or legacy ToolShed ``package_blast_plus_2_7_1``.
        - Document the BLAST+ 2.6.0 change in the standard 12 column output
          from ``qacc,sacc,...`` to ``qaccver,saccver,...`` instead.
        - Accept gzipped FASTA inputs for subject files, queries to ``blastn``
          and input to ``makeblastdb`` (contribution from Anton Nekrutenko).
v0.3.1  - Clarify help text for max hits option, confusing as depending on the
          output format it must be mapped to different command line arguments.
        - Extend gzipped query support to all the command line tools.
        - Workaround for gzipped support under Galaxy release 16.01 or older.
v0.3.2  - Fixed incomplete ``@CLI_OPTIONS@`` macro in the help text for the
          ``tblastn`` and ``blastdbcmd`` wrappers.
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

For pushing a release to the test or main "Galaxy Tool Shed", use the following
Planemo commands (which requires you have set your Tool Shed access details in
``~/.planemo.yml`` and that you have access rights on the Tool Shed)::

    $ planemo shed_update -t testtoolshed --check_diff tools/ncbi_blast_plus/
    ...

or::

    $ planemo shed_update -t toolshed --check_diff tools/ncbi_blast_plus/
    ...

To just build and check the tar ball, use::

    $ planemo shed_upload --tar_only tools/ncbi_blast_plus/
    ...
    $ tar -tzf shed_upload.tar.gz
    test-data/blastdb.loc
    ...
    tools/ncbi_blast_plus/tool_dependencies.xml
    $ tar -tzf shed_upload.tar.gz | wc -l
    117

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

"""
BlastXml class
"""

from galaxy.datatypes.data import get_file_peek
from galaxy.datatypes.data import Text, Data
from galaxy.datatypes.xml import GenericXml
from galaxy.datatypes.metadata import MetadataElement


class BlastXml( GenericXml ):
    """NCBI Blast XML Output data"""
    file_ext = "blastxml"

    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text"""
        if not dataset.dataset.purged:
            dataset.peek = get_file_peek( dataset.file_name, is_multi_byte=is_multi_byte )
            dataset.blurb = 'NCBI Blast XML data'
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def sniff( self, filename ):
        """
        Determines whether the file is blastxml
        
        >>> fname = get_test_fname( 'megablast_xml_parser_test1.blastxml' )
        >>> BlastXml().sniff( fname )
        True
        >>> fname = get_test_fname( 'tblastn_four_human_vs_rhodopsin.xml' )
        >>> BlastXml().sniff( fname )
        True
        >>> fname = get_test_fname( 'interval.interval' )
        >>> BlastXml().sniff( fname )
        False
        """
        #TODO - Use a context manager on Python 2.5+ to close handle
        handle = open(filename)
        line = handle.readline()
        if line.strip() != '<?xml version="1.0"?>':
            handle.close()
            return False
        line = handle.readline()
        if line.strip() not in ['<!DOCTYPE BlastOutput PUBLIC "-//NCBI//NCBI BlastOutput/EN" "http://www.ncbi.nlm.nih.gov/dtd/NCBI_BlastOutput.dtd">',
                                '<!DOCTYPE BlastOutput PUBLIC "-//NCBI//NCBI BlastOutput/EN" "NCBI_BlastOutput.dtd">']:
            handle.close()
            return False
        line = handle.readline()
        if line.strip() != '<BlastOutput>':
            handle.close()
            return False
        handle.close()
        return True
    
    def merge(split_files, output_file):
        """Merging multiple XML files is non-trivial and must be done in subclasses."""
        if len(split_files) == 1:
            #For one file only, use base class method (move/copy)
            return Text.merge(split_files, output_file)
        if not split_files:
            raise ValueError("Given no BLAST XML files, %r, to merge into %s" \
                             % (split_files, output_file))
        out = open(output_file, "w")
        h = None
        for f in split_files:
            h = open(f)
            body = False
            header = h.readline()
            if not header:
                out.close()
                h.close()
                raise ValueError("BLAST XML file %s was empty" % f)
            if header.strip() != '<?xml version="1.0"?>':
                out.write(header) #for diagnosis
                out.close()
                h.close()
                raise ValueError("%s is not an XML file!" % f)
            line = h.readline()
            header += line
            if line.strip() not in ['<!DOCTYPE BlastOutput PUBLIC "-//NCBI//NCBI BlastOutput/EN" "http://www.ncbi.nlm.nih.gov/dtd/NCBI_BlastOutput.dtd">',
                                    '<!DOCTYPE BlastOutput PUBLIC "-//NCBI//NCBI BlastOutput/EN" "NCBI_BlastOutput.dtd">']:
                out.write(header) #for diagnosis
                out.close()
                h.close()
                raise ValueError("%s is not a BLAST XML file!" % f)
            while True:
                line = h.readline()
                if not line:
                    out.write(header) #for diagnosis
                    out.close()
                    h.close()
                    raise ValueError("BLAST XML file %s ended prematurely" % f)
                header += line
                if "<Iteration>" in line:
                    break
                if len(header) > 10000:
                    #Something has gone wrong, don't load too much into memory!
                    #Write what we have to the merged file for diagnostics
                    out.write(header)
                    out.close()
                    h.close()
                    raise ValueError("BLAST XML file %s has too long a header!" % f)
            if "<BlastOutput>" not in header:
                out.close()
                h.close()
                raise ValueError("%s is not a BLAST XML file:\n%s\n..." % (f, header))
            if f == split_files[0]:
                out.write(header)
                old_header = header
            elif old_header[:300] != header[:300]:
                #Enough to check <BlastOutput_program> and <BlastOutput_version> match
                out.close()
                h.close()
                raise ValueError("BLAST XML headers don't match for %s and %s - have:\n%s\n...\n\nAnd:\n%s\n...\n" \
                                 % (split_files[0], f, old_header[:300], header[:300]))
            else:
                out.write("    <Iteration>\n")
            for line in h:
                if "</BlastOutput_iterations>" in line:
                    break
                #TODO - Increment <Iteration_iter-num> and if required automatic query names
                #like <Iteration_query-ID>Query_3</Iteration_query-ID> to be increasing?
                out.write(line)
            h.close()
        out.write("  </BlastOutput_iterations>\n")
        out.write("</BlastOutput>\n")
        out.close()
    merge = staticmethod(merge)


class _BlastDb(object):
    """Base class for BLAST database datatype."""

    def set_peek( self, dataset, is_multi_byte=False ):
        """Set the peek and blurb text."""
        if not dataset.dataset.purged:
            dataset.peek  = "BLAST database (multiple files)"
            dataset.blurb = "BLAST database (multiple files)"
        else:
            dataset.peek = 'file does not exist'
            dataset.blurb = 'file purged from disk'

    def display_peek( self, dataset ):
        """Create HTML content, used for displaying peek."""
        try:
            return dataset.peek
        except:
            return "BLAST database (multiple files)"

    def display_data(self, trans, data, preview=False, filename=None,
                     to_ext=None, size=None, offset=None, **kwd):
        """Apparently an old display method, but still gets called.

        This allows us to format the data shown in the central pane via the "eye" icon.
        """
        return "This is a BLAST database."

    def get_mime(self):
        """Returns the mime type of the datatype (pretend it is text for peek)"""
        return 'text/plain'

    def merge(split_files, output_file):
        """Merge BLAST databases (not implemented for now)."""
        raise NotImplementedError("Merging BLAST databases is non-trivial (do this via makeblastdb?)")

    def split( cls, input_datasets, subdir_generator_function, split_params):
        """Split a BLAST database (not implemented for now)."""
        if split_params is None:
            return None
        raise NotImplementedError("Can't split BLAST databases")


class BlastNucDb( _BlastDb, Data ):
    """Class for nucleotide BLAST database files."""
    file_ext = 'blastdbn'
    composite_type ='basic'
    MetadataElement( readonly=True, optional=True, visible=False, no_value=0 )

    def __init__(self,**kwd):
        Data.__init__(self, **kwd)
        self.add_composite_file('blastdb.nhr')
        self.add_composite_file('blastdb.nin')
        self.add_composite_file('blastdb.nsq')
        self.add_composite_file('blastdb.nhd', optional=True)
        self.add_composite_file('blastdb.nsi', optional=True)
        self.add_composite_file('blastdb.nhi', optional=True)
        self.add_composite_file('blastdb.nog', optional=True)
        self.add_composite_file('blastdb.nsd', optional=True)

    def display_data(self, trans, data, preview=False, filename=None,
                     to_ext=None, size=None, offset=None, **kwd):
        """Apparently an old display method, but still gets called.

        This allows us to format the data shown in the central pane via the "eye" icon.
        """
        return "This is a BLAST nucleotide database."


class BlastProtDb( _BlastDb, Data ):
    """Class for protein BLAST database files."""
    file_ext = 'blastdbp'
    composite_type ='basic'
    MetadataElement( readonly=True, optional=True, visible=False, no_value=0 )

    def __init__(self,**kwd):
        Data.__init__(self, **kwd)
        self.add_composite_file('blastdb.phr')
        self.add_composite_file('blastdb.pin')
        self.add_composite_file('blastdb.psq')
        self.add_composite_file('blastdb.pnd', optional=True)
        self.add_composite_file('blastdb.pni', optional=True)
        self.add_composite_file('blastdb.psd', optional=True)
        self.add_composite_file('blastdb.psi', optional=True)
        self.add_composite_file('blastdb.psq', optional=True)
        self.add_composite_file('blastdb.phd', optional=True)
        self.add_composite_file('blastdb.phi', optional=True)
        self.add_composite_file('blastdb.pog', optional=True)

    def display_data(self, trans, data, preview=False, filename=None,
                     to_ext=None, size=None, offset=None, **kwd):
        """Apparently an old display method, but still gets called.

        This allows us to format the data shown in the central pane via the "eye" icon.
        """
        return "This is a BLAST protein database."

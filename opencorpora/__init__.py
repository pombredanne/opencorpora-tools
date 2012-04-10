# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, division
from collections import namedtuple
from .compat import ElementTree, OrderedDict, utf8_for_PY2
from . import xml_utils

_DocumentMeta = namedtuple('_DocumentMeta', 'title bounds')

class _OpenCorporaBase(object):
    """
    Common interface for OpenCorpora objects.
    """
    def iterparas(self):
        raise NotImplementedError()

    def itertokens(self):
        raise NotImplementedError()

    def itersents(self):
        raise NotImplementedError()


    def paras(self):
        return list(self.iterparas())

    def tokens(self):
        return list(self.itertokens())

    def sents(self):
        return list(self.itersents())


    def as_text(self):
        return ' '.join(self.itertokens())

    # XXX: does this work under windows?
    @utf8_for_PY2
    def __repr__(self):
        return "%s: %s" % (self.__class__, self.as_text())


class Sentence(_OpenCorporaBase):
    """
    Sentence.
    """
    def __init__(self, xml):
        self.root = xml

    def itertokens(self):
        for token in self.root.findall('tokens//token'):
            yield token.get('text')

    def source(self):
        return self.root.find('source').text

    def as_text(self):
        return self.source()


class Paragraph(_OpenCorporaBase):
    """
    Text paragraph.
    """
    def __init__(self, xml):
        self.root = xml

    def itertokens(self):
        for token in self.root.findall('sentence//token'):
            yield token.get('text')

    def itersents(self):
        for sent in self.root.findall('sentence'):
            yield Sentence(sent)

    def as_text(self):
        return ' '.join(sent.as_text() for sent in self.itersents())


class Document(_OpenCorporaBase):
    """
    Single OpenCorpora document.
    """
    def __init__(self, xml):
        self.root = xml

    def title(self):
        return self.root.get('name')

    def itertokens(self):
        for token in self.root.findall('paragraphs//token'):
            yield token.get('text')

    def iterparas(self):
        for para in self.root.findall('paragraphs/paragraph'):
            yield Paragraph(para)

    def itersents(self):
        for sent in self.root.findall('paragraphs//sentence'):
            yield Sentence(sent)

    def as_text(self):
        return "\n\n".join(para.as_text() for para in self.iterparas())


class Corpora(_OpenCorporaBase):
    """
    OpenCorpora.ru corpora reader. Provides fast access to individual
    documents without loading and parsing the whole XML; is capable of iterating
    over individual paragraphs, sentences and tokens without loading
    all data to memory.
    """
    def __init__(self, filename):
        self.filename = filename
        self._document_meta = OrderedDict()
        self._populate_document_meta()

    def catalog(self):
        """
        Returns information about documents in corpora:
        a list of tuples (doc_id, doc_title).
        """
        return [(doc_id, self._document_meta[doc_id].title) for doc_id in self._document_meta]

    def get_document(self, doc_id):
        """
        Returns Document object for a given doc_id.
        """
        return Document(self._document_xml(doc_id))

    def itertokens(self):
        """
        Returns an iterator over corpus tokens.
        """
        for token in xml_utils.iterparse(self.filename, 'token', clear=True):
            yield token.get('text')

    def itersents(self):
        for sent in xml_utils.iterparse(self.filename, 'sentence'):
            yield Sentence(sent)

    def iterparas(self):
        for para in xml_utils.iterparse(self.filename, 'paragraph'):
            yield Paragraph(para)


    def iterdocuments(self):
        """
        Returns an iterator over corpus documentss.
        """
        for doc in xml_utils.iterparse(self.filename, 'text'):
            yield Document(doc)

    def documents(self):
        """
        Returns a list of all corpus documents.

        XXX: it can be very slow and memory-consuming; use
        iterdocuments of get_document when possible.
        """
        return list(self.iterdocuments())

    def _populate_document_meta(self):
        """
        Populates texts meta information cache for fast lookups.
        """
        bounds_iter = xml_utils.bounds(self.filename,
            r'<text id="(\d+)"[^>]*name="([^"]*)"',
            r'</text>',
        )
        for match, bounds in bounds_iter:
            doc_id, title = int(match.group(1)), match.group(2)
            title = xml_utils.unescape_attribute(title)
            self._document_meta[doc_id] = _DocumentMeta(title, bounds)

    def _document_xml(self, doc_id):
        """
        Returns xml Element for the document document_id.
        """
        doc_str = self._get_doc_by_raw_offset(doc_id)
        return ElementTree.XML(doc_str.encode('utf8'))

    def _get_doc_by_raw_offset(self, doc_id):
        """
        Loads document from xml using bytes offset information.
        XXX: this is not tested under Windows.
        """
        bounds = self._document_meta[doc_id].bounds
        return xml_utils.load_chunk(self.filename, bounds)

    def _get_doc_by_line_offset(self, doc_id):
        """
        Loads document from xml using line offset information.
        This is much slower than _get_doc_by_raw_offset but should
        work everywhere.
        """
        bounds = self._document_meta[doc_id].bounds
        return xml_utils.load_chunk(self.filename, bounds, slow=True)


#
#    def words(self):
#        # list of str
#        pass
#
#    def sents(self):
#        # list of (list of str)
#        pass
#
#    def paras(self):
#        #list of (list of (list of str))
#        pass
#
#    def tagged_words(self):
#        # list of (str,str) tuple
#        pass
#
#    def tagged_sents(self):
#        # list of (list of (str,str))
#        pass
#
#    def tagged_paras(self):
#        # list of (list of (list of (str,str)))
#        pass
#

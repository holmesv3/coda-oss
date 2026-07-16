"""
Type stubs for coda_xml_lite module.

This module provides lightweight XML parsing and DOM manipulation.
Based on a minidom-style parser, it supports reading, creating, and
manipulating XML documents with a tree-based API.

Classes:
    Attributes: XML attribute collection for elements
    Element: XML element node with children and attributes
    Document: XML document root container
    MinidomParser: XML parser for creating documents from strings/files
    XMLReader: Base XML reader interface
    MinidomHandler: SAX-style handler for parsing events

The API follows DOM conventions with methods for navigation, querying,
and modification of XML tree structures.
"""

from typing import List, Optional, overload

class Attributes:
    """
    Collection of XML attributes for an element.
    
    Provides indexed access to attribute name-value pairs.
    """
    
    def getLength(self) -> int:
        """
        Get number of attributes.
        
        Returns:
            Number of attributes in collection
        """
        ...
    
    def getIndex(self, qname: str) -> int:
        """
        Get index of attribute by qualified name.
        
        Args:
            qname: Qualified attribute name
            
        Returns:
            Index of attribute, or -1 if not found
        """
        ...
    
    def getValue(self, i: int) -> str:
        """
        Get attribute value at index.
        
        Args:
            i: Attribute index
            
        Returns:
            Attribute value string
        """
        ...
    
    def getQName(self, i: int) -> str:
        """
        Get qualified name at index.
        
        Args:
            i: Attribute index
            
        Returns:
            Qualified attribute name
        """
        ...
    
    def getUri(self, i: int) -> str:
        """
        Get namespace URI at index.
        
        Args:
            i: Attribute index
            
        Returns:
            Namespace URI string
        """
        ...
    
    def add(self, qname: str, value: str) -> None:
        """
        Add new attribute.
        
        Args:
            qname: Qualified attribute name
            value: Attribute value
        """
        ...


class Element:
    """
    XML element node in document tree.
    
    Represents an XML element with tag name, attributes, text content,
    and child elements. Provides methods for tree navigation and manipulation.
    """
    
    @overload
    def __init__(self) -> None:
        """Create empty element."""
        ...
    
    @overload
    def __init__(self, qname: str) -> None:
        """
        Create element with qualified name.
        
        Args:
            qname: Qualified element name (tag)
        """
        ...
    
    @overload
    def __init__(self, qname: str, uri: str) -> None:
        """
        Create element with qualified name and namespace URI.
        
        Args:
            qname: Qualified element name
            uri: Namespace URI
        """
        ...
    
    @overload
    def __init__(self, qname: str, uri: str, characterData: str) -> None:
        """
        Create element with qualified name, namespace, and text content.
        
        Args:
            qname: Qualified element name
            uri: Namespace URI
            characterData: Text content
        """
        ...
    
    def setCharacterData(self, data: str) -> None:
        """
        Set text content of element.
        
        Args:
            data: Text content
        """
        ...
    
    def getCharacterData(self) -> str:
        """
        Get text content of element.
        
        Returns:
            Text content string
        """
        ...
    
    def getLocalName(self) -> str:
        """
        Get local name (without namespace prefix).
        
        Returns:
            Local element name
        """
        ...
    
    def getUri(self) -> str:
        """
        Get namespace URI.
        
        Returns:
            Namespace URI string
        """
        ...
    
    def setQName(self, qname: str) -> None:
        """
        Set qualified name.
        
        Args:
            qname: New qualified name
        """
        ...
    
    def getAttributes(self) -> Attributes:
        """
        Get attribute collection.
        
        Returns:
            Attributes object for this element
        """
        ...
    
    def attribute(self, key: str) -> str:
        """
        Get attribute value by name.
        
        Args:
            key: Attribute name
            
        Returns:
            Attribute value string
            
        Raises:
            Exception: If attribute does not exist
        """
        ...
    
    def getElementsByTagName(self, localName: str, recurse: bool = False) -> List[Element]:
        """
        Find child elements by local tag name.
        
        Args:
            localName: Local element name to search for
            recurse: If True, search recursively through all descendants
            
        Returns:
            List of matching elements
        """
        ...
    
    def getElementsByTagNameNS(self, qname: str, recurse: bool = False) -> List[Element]:
        """
        Find child elements by qualified name.
        
        Args:
            qname: Qualified element name to search for
            recurse: If True, search recursively through all descendants
            
        Returns:
            List of matching elements
        """
        ...
    
    def getChildren(self) -> List[Element]:
        """
        Get all direct child elements.
        
        Returns:
            List of child elements
        """
        ...
    
    def getChild(self, localName: str) -> Optional[Element]:
        """
        Get first direct child element with given name.
        
        Args:
            localName: Local element name to search for
            
        Returns:
            First matching child element, or None if not found
        """
        ...
    
    def destroyChildren(self) -> None:
        """
        Remove and destroy all child elements.
        """
        ...
    
    def clone(self, element: Element) -> None:
        """
        Clone contents from another element.
        
        Args:
            element: Element to clone from
        """
        ...
    
    def prettyPrint(self) -> str:
        """
        Convert to formatted XML string with indentation.
        
        Returns:
            Pretty-printed XML string
        """
        ...
    
    def print(self) -> str:
        """
        Convert to compact XML string.
        
        Returns:
            XML string without extra whitespace
        """
        ...


class Document:
    """
    XML document container with root element.
    
    Represents a complete XML document. Manages ownership of the root
    element and provides access to document-level properties.
    """
    
    @overload
    def __init__(self) -> None:
        """Create empty document."""
        ...
    
    @overload
    def __init__(self, rootNode: Element, own: bool = True) -> None:
        """
        Create document with root element.
        
        Args:
            rootNode: Root element for document
            own: If True, document takes ownership of element
        """
        ...
    
    def getRootElement(self, steal: bool = False) -> Element:
        """
        Get root element of document.
        
        Args:
            steal: If True, transfer ownership to caller
            
        Returns:
            Root element
        """
        ...
    
    def setRootElement(self, root: Element, own: bool = True) -> None:
        """
        Set root element of document.
        
        Args:
            root: New root element
            own: If True, document takes ownership of element
        """
        ...
    
    def destroy(self) -> None:
        """
        Destroy document and free resources.
        """
        ...


class MinidomParser:
    """
    XML parser for creating DOM documents.
    
    Parses XML from strings or files and constructs a Document object
    with the parsed tree structure. Supports encoding detection.
    """
    
    def __init__(self, storeEncoding: bool = True) -> None:
        """
        Initialize parser.
        
        Args:
            storeEncoding: If True, store detected encoding information
        """
        ...
    
    def parse(self, xmlContent: str) -> None:
        """
        Parse XML from string.
        
        Args:
            xmlContent: XML content string
            
        Raises:
            Exception: If XML is malformed
        """
        ...
    
    def parseFile(self, filename: str) -> None:
        """
        Parse XML from file.
        
        Args:
            filename: Path to XML file
            
        Raises:
            Exception: If file cannot be read or XML is malformed
        """
        ...
    
    def getDocument(self) -> Document:
        """
        Get parsed document.
        
        Returns:
            Document object containing parsed XML tree
            
        Note:
            Must call parse() or parseFile() first
        """
        ...
    
    def clear(self) -> None:
        """
        Clear parser state and free document.
        """
        ...


class XMLReader:
    """
    Base XML reader interface.
    
    Low-level interface for XML reading operations.
    """
    ...


class MinidomHandler:
    """
    SAX-style handler for parsing events.
    
    Receives callbacks during XML parsing for element start/end,
    character data, etc. Used internally by MinidomParser.
    """
    ...

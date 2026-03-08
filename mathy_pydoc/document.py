"""
This module implements the structural representation of an API documentation
in separate documents and symbolic names. The final documentation is rendered
from this structured representation.
"""

from __future__ import annotations

import os
from typing import IO, Any, Optional


class Section:
    """
  A section represents a part of a #Document. It contains Markdown-formatted
  content that will be rendered into a file at some point.

  # Attributes
  doc (Document): The document that the section belongs to.
  identifier (str, None): The globally unique identifier of the section. This
    identifier usually matches the name of the element that the section
    describes (eg. a class or function) and will be used for cross-referencing.
  title (str, None): The title of the section. If specified, it will be
    rendered before `section.content` and the header-size will depend on
    the `section.depth`.
  depth (int): The depth of the section, defaults to 1. Currently only affects
    the header-size that is rendered for the `section.title`.
  content (str): The Markdown-formatted content of the section.
  """

    def __init__(
        self,
        doc: Document,
        identifier: Optional[str] = None,
        title: Optional[str] = None,
        depth: int = 1,
        content: Optional[str] = None,
        header_type: str = "html",
    ) -> None:
        self.doc = doc
        self.identifier = identifier
        self.title = title
        self.depth = depth
        self.content = content if content is not None else "*Nothing to see here.*"
        self.header_type = header_type
        self.loader_context: Optional[dict[str, Any]] = None

    def render(self, stream: IO[str]) -> None:
        """
    Render the section into *stream*.
    """

        if self.header_type == "html":
            print(
                '<h{depth} id="{id}">{title}</h{depth}>\n'.format(
                    depth=self.depth, id=self.identifier, title=self.title
                ),
                file=stream,
            )
        elif self.header_type == "markdown":
            print("#" * self.depth, self.title, file=stream)
        else:
            raise ValueError("Invalid header type: %s" % self.header_type)
        print(self.content, file=stream)

    @property
    def index(self) -> Index:
        """
    Returns the #Index that this section is associated with, accessed via
    `section.document`.
    """

        return self.document.index


class Document:
    """
  Represents a single document that may contain several #Section#s. Every
  document *must* have a relative URL associated with it.

  # Attributes
  index (Index): The index that the document belongs to.
  url (str): The relative URL of the document.
  """

    def __init__(self, index: Index, url: str) -> None:
        self.index = index
        self.url = url
        self.sections: list[Section] = []


class Index:
    """
  The index manages all documents and sections globally. It keeps track of
  the symbolic names allocated for the sections to be able to link to them
  from other sections.

  # Attributes
  documents (dict):
  sections (dict):
  """

    def __init__(self) -> None:
        self.documents: dict[str, Document] = {}
        self.sections: dict[str, Section] = {}

    def new_document(self, filename: str, url: Optional[str] = None) -> Document:
        """
    Create a new document.

    # Arguments
    filename (str): The filename of the document. Must end with `.md`.
    url (str): The relative URL of the document. If omitted, will be
      automatically deduced from *filename* (same without the `.md` suffix).

    # Raises
    ValueError: If *filename* does not end with `.md`.
    ValueError: If *filename* is not a relative path.
    ValueError: If a document with the specified *filename* already exists.
    """

        if not filename.endswith(".md"):
            raise ValueError("filename must end with `.md`")
        if os.path.isabs(filename):
            raise ValueError("filename must be relative")
        if filename in self.documents:
            raise ValueError("document filename {!r} already used".format(filename))
        if not url:
            url = filename[:-3]

        doc = Document(self, url)
        self.documents[filename] = doc
        return doc

    def new_section(self, doc: Document, *args: Any, **kwargs: Any) -> Section:
        """
    Create a new section in the specified document. The arguments for this
    method match the parameters for the #Section constructor.

    # Raises
    ValueError: If the section identifier is already used.
    """

        section = Section(doc, *args, **kwargs)
        if section.identifier:
            if section.identifier in self.sections:
                raise ValueError(
                    "section identifier {!r} already used".format(section.identifier)
                )
            self.sections[section.identifier] = section
        doc.sections.append(section)
        return section

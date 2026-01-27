"""Split product documents into smaller chunks for embedding and retrieval."""
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_documents(
    documents: list[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 50,
) -> list[Document]:
    """
    Split product documents into smaller chunks for embedding and retrieval.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )

    split_docs = splitter.split_documents(documents)
    return split_docs

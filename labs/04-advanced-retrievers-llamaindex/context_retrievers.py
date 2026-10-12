from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.node_parser import HierarchicalNodeParser, get_leaf_nodes
from llama_index.core.retrievers import AutoMergingRetriever, RecursiveRetriever
from llama_index.core.schema import IndexNode

from shared import (
    build_nodes, build_summary_index, configure_models, load_documents, show_results,
)


def auto_merging_retriever(documents):
    parser = HierarchicalNodeParser.from_defaults(chunk_sizes=[512, 256, 128])
    hierarchical_nodes = parser.get_nodes_from_documents(documents)
    leaf_nodes = get_leaf_nodes(hierarchical_nodes)

    # docstore holds every level (needed to look up parents), the vector index holds only the leaves
    storage_context = StorageContext.from_defaults()
    storage_context.docstore.add_documents(hierarchical_nodes)
    leaf_index = VectorStoreIndex(leaf_nodes, storage_context=storage_context)

    # if enough retrieved leaves share a parent, they are replaced by that parent
    retriever = AutoMergingRetriever(
        leaf_index.as_retriever(similarity_top_k=3),
        storage_context,
        verbose=True,
    )

    query = "How do neural networks work in deep learning?"
    print(f"Query: {query}\n")
    show_results(retriever.retrieve(query))

def recursive_retriever(documents, nodes, summary_index):
    # one pointer per document: text = the LLM summary (what gets embedded),
    # index_id = the id of the full node to return
    pointers = [
        IndexNode(text=summary_index.get_document_summary(doc.doc_id), index_id=node.node_id)
        for doc, node in zip(documents, nodes)
    ]
    pointer_index = VectorStoreIndex(pointers)

    retriever = RecursiveRetriever(
        "vector",  # root retriever id
        retriever_dict={"vector": pointer_index.as_retriever(similarity_top_k=2)},
        node_dict={node.node_id: node for node in nodes},  # where pointers get resolved to real nodes
        verbose=True,
    )

    query = "What are the applications of AI?"
    print(f"Query: {query}\n")
    show_results(retriever.retrieve(query))


def main():
    configure_models()
    documents = load_documents()
    nodes = build_nodes(documents)

    auto_merging_retriever(documents)
    recursive_retriever(documents, nodes, build_summary_index(documents))


if __name__ == "__main__":
    main()

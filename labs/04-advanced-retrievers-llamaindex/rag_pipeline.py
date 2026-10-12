from shared import build_vector_index, configure_models, load_documents


class ProductionRAGPipeline:
    # context size per strategy: broad "list/types" questions get more documents
    TOP_K = {"semantic": 3, "comprehensive": 5}

    def __init__(self, index, llm):
        self.llm = llm
        self.retriever = index.as_retriever(similarity_top_k=5)

    def _route_query(self, question):
        q = question.lower()
        if any(word in q for word in ["list", "types", "examples"]):
            return "comprehensive"
        return "semantic"  # default, covers "what / explain / describe" too

    def query(self, question, strategy="auto"):
        if strategy == "auto":
            strategy = self._route_query(question)
        top_k = self.TOP_K.get(strategy, 3)

        try:
            docs = self.retriever.retrieve(question)[:top_k]
        except Exception as e:
            return {"answer": "I encountered an error processing your question.",
                    "strategy": strategy, "num_docs": 0, "status": f"error: {e}"}

        context = "\n\n".join(doc.text for doc in docs)
        prompt = f"""Based on the following context, please answer the question:

Context:
{context}

Question: {question}

Answer:"""

        try:
            answer = self.llm.complete(prompt).text
            status = "success"
        except Exception as e:
            # retrieval worked but generation failed: degrade to returning the raw context
            answer = f"Based on the retrieved documents: {context[:200]}..."
            status = f"llm_error: {e}"

        return {"answer": answer, "strategy": strategy, "num_docs": len(docs), "status": status}

    def evaluate(self, test_queries):
        results = [{"query": q, "result": self.query(q)} for q in test_queries]
        for r in results:
            r["success"] = r["result"]["status"] == "success"
        return {"success_rate": sum(r["success"] for r in results) / len(results), "results": results}


def main():
    llm = configure_models()
    pipeline = ProductionRAGPipeline(build_vector_index(load_documents()), llm)

    test_queries = [
        "What is machine learning?",
        "List different types of learning algorithms",
        "Explain neural networks",
    ]

    for question in test_queries:
        result = pipeline.query(question)
        print(f"Query: {question}")
        print(f"  strategy={result['strategy']}  docs={result['num_docs']}  status={result['status']}")
        print(f"  answer: {result['answer'][:100]}...\n")

    print(f"Success rate: {pipeline.evaluate(test_queries)['success_rate']:.0%}")


if __name__ == "__main__":
    main()

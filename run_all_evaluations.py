import sys
import json

from src.vector_store import update_vector_store
from src.document_loader import load_documents
from src.logger import logger
from src.evaluator import evaluate_question

# ---------------------------------
# Load vector store once
# ---------------------------------

documents = load_documents(
    "documents"
)

vector_store = update_vector_store(
    documents
)

logger.info("System initialized.")
print("\nSystem Ready.")

# ---------------------------------
# Batch mode
# ---------------------------------

if len(sys.argv) > 1 and sys.argv[1].lower() == "batch":

    with open(
            "tests/questions.json",
            encoding="utf-8"
    ) as f:

        questions = json.load(
            f
        )

    for question in questions:

        # evaluate_question(
        #     question
        # )

        merged_result = evaluate_question(
            question,
            vector_store
        )
        
        print(
            f"\nCompleted: {merged_result['question']}"
        )

# ---------------------------------
# Interactive mode
# ---------------------------------

else:

    while True:

        question = input(
            "\nAsk a question (exit to quit): "
        )
        
        logger.info(f"User asked: {question}")

        if question.lower() == "exit":
            
            logger.info("Application closed by user.")

            break

        merged_result = evaluate_question(
            question,
            vector_store
        )


        print("\nQuestion:\n")

        print(
            merged_result["question"]
        )

        print("\nAnswer:\n")

        print(
            merged_result["answer"]
        )

        print("\nSources:")

        # for source in merged_result["sources"]:

        #     print(
        #         source
        #     )
            
        for doc in merged_result["retrieved_docs"]:

            print(
                f"""
        File         : {doc['file_name']}
        Type         : {doc['file_type']}
        Page         : {doc['page']}
        Chunk        : {doc['chunk_index']}/{doc['total_chunks']}
        Chunk ID     : {doc['chunk_id']}
        Similarity   : {doc['score']}
        """
            )    

        print("\nDeepEval Results:\n")

        print(
            json.dumps(
                merged_result["deepeval"],
                indent=4
            )
        )

        print("\nRAGAS Results:\n")

        print(
            json.dumps(
                merged_result["ragas"],
                indent=4
            )
        )

        print("\nLatency Metrics")
        print("--------------------------")
        print(f"Model            : {merged_result['model']}")
        print(f"Retrieved Chunks : {len(merged_result['retrieved_docs'])}")
        print(f"Retrieval        : {merged_result['latency']['retrieval']} sec ({merged_result['latency']['retrieval'] * 1000:.0f} ms)")
        print(f"LLM              : {merged_result['latency']['llm']} sec ({merged_result['latency']['llm'] * 1000:.0f} ms)")
        print(f"DeepEval         : {merged_result['latency']['deepeval']} sec")
        print(f"RAGAS            : {merged_result['latency']['ragas']} sec")
        print(f"Report           : {merged_result['latency']['report']} sec")
        print(f"Total            : {merged_result['latency']['total']} sec")

        print("\nHTML report generated.")

        print("CSV updated.")
        
        
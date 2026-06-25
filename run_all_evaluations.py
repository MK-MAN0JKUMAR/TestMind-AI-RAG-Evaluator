import json
import subprocess
import sys

from src.vector_store import update_vector_store
from src.document_loader import load_documents
from src.rag_pipeline import ask_question
from src.report_generator import generate_html_report
from src.csv_exporter import export_to_csv


# ---------------------------------
# Load vector store once
# ---------------------------------

documents = load_documents(
    "documents"
)

vector_store = update_vector_store(
    documents
)

print("\nSystem Ready.")


from src.evaluator import (
    evaluate_question
)

# ---------------------------------
# Evaluate one question
# ---------------------------------

def old_evaluate_question(question: str):

    # RAG
    result = ask_question(
        question,
        vector_store
    )

    input_data = {

        "question": result["question"],

        "answer": result["answer"],

        "contexts": result["contexts"]

    }

    # Shared input
    with open(
            "results/input.json",
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            input_data,
            f,
            indent=4
        )

    # DeepEval
    subprocess.run(

        [

            r"evaluation\deepeval\.deepeval-venv\Scripts\python.exe",

            r"evaluation\deepeval\evaluate.py",

            r"results\input.json"

        ],

        check=True

    )

    # RAGAS
    subprocess.run(

        [

            r"evaluation\ragas\.rag-venv\Scripts\python.exe",

            r"evaluation\ragas\evaluate.py",

            r"results\input.json"

        ],

        check=True

    )

    # Load results
    with open(
            "results/deepeval_result.json",
            encoding="utf-8"
    ) as f:

        deepeval_result = json.load(
            f
        )

    with open(
            "results/ragas_result.json",
            encoding="utf-8"
    ) as f:

        ragas_result = json.load(
            f
        )

    merged_result = {

        "question": result["question"],

        "answer": result["answer"],

        "sources": result["sources"],

        "retrieved_docs": result["retrieved_docs"],

        "deepeval": deepeval_result,

        "ragas": ragas_result

    }

    with open(
            "results/merged_result.json",
            "w",
            encoding="utf-8"
    ) as f:

        json.dump(
            merged_result,
            f,
            indent=4
        )

    generate_html_report(
        merged_result
    )

    export_to_csv(
        merged_result
    )

    # Console output

    print("\nQuestion:\n")
    print(
        merged_result["question"]
    )

    print("\nAnswer:\n")
    print(
        merged_result["answer"]
    )

    print("\nSources:\n")

    for source in merged_result["sources"]:

        print(
            source
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

    print("\nHTML report generated.")
    print("CSV updated.")


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

        if question.lower() == "exit":

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

        print("\nSources:\n")

        for source in merged_result["sources"]:

            print(
                source
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

        print("\nHTML report generated.")

        print("CSV updated.")
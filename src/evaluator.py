import json
import subprocess

from src.rag_pipeline import ask_question
from src.report_generator import generate_html_report
from src.csv_exporter import export_to_csv


def evaluate_question(
        question: str,
        vector_store
):

    # ----------------------------
    # RAG
    # ----------------------------

    result = ask_question(
        question,
        vector_store
    )

    input_data = {

        "question": result["question"],

        "answer": result["answer"],

        "contexts": result["contexts"]

    }

    # ----------------------------
    # Shared Input
    # ----------------------------

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

    # ----------------------------
    # DeepEval
    # ----------------------------

    subprocess.run(

        [

            r"evaluation\deepeval\.deepeval-venv\Scripts\python.exe",

            r"evaluation\deepeval\evaluate.py",

            r"results\input.json"

        ],

        check=True

    )

    # ----------------------------
    # RAGAS
    # ----------------------------

    subprocess.run(

        [

            r"evaluation\ragas\.rag-venv\Scripts\python.exe",

            r"evaluation\ragas\evaluate.py",

            r"results\input.json"

        ],

        check=True

    )

    # ----------------------------
    # Load Results
    # ----------------------------

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

    # ----------------------------
    # Merge Results
    # ----------------------------

    merged_result = {

        "question": result["question"],

        "answer": result["answer"],

        "sources": result["sources"],

        "retrieved_docs": result["retrieved_docs"],

        "deepeval": deepeval_result,

        "ragas": ragas_result

    }

    # ----------------------------
    # Save
    # ----------------------------

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

    return merged_result
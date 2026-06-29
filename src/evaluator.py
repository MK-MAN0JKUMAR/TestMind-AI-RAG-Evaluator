import json
import subprocess

from src.rag_pipeline import ask_question
from src.report_generator import generate_html_report
from src.csv_exporter import export_to_csv
from src.latency import Timer
from src.llm import MODEL_NAME
from src.logger import logger


def evaluate_question(
        question: str,
        vector_store
):
    logger.info("Evaluation started.")
    total_timer = Timer()
    total_timer.start()

    # ----------------------------
    # RAG
    # ----------------------------

    result = ask_question(
        question,
        vector_store
    )
    
    # ----------------------------
    # No Relevant Context Found
    # ----------------------------

    
    if (
        not result["retrieved_docs"]
        or
        not result["contexts"]
    ):    

        logger.info(
            "No relevant documents retrieved. Skipping evaluation."
        )

        empty_result = {

            "question": result["question"],

            "answer": result["answer"],

            "sources": [],

            "retrieved_docs": [],

            "deepeval": {

                "answer_relevancy": {

                    "score": 0.0,

                    "reason": "No relevant documents retrieved."

                },

                "hallucination": {

                    "score": 0.0,

                    "reason": "No relevant documents retrieved."

                }

            },

            "ragas": {

                "faithfulness": 0.0

            },

            "model": MODEL_NAME,

            "latency": {

                "retrieval": result["latency"]["retrieval"],

                "llm": result["latency"]["llm"],

                "deepeval": 0.0,

                "ragas": 0.0,

                "report": 0.0,

                "total": total_timer.stop()

            }

        }

        return empty_result

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
            
    deepeval_timer = Timer()
    deepeval_timer.start()
    
    # ----------------------------
    # DeepEval
    # ----------------------------
    logger.info("Running DeepEval...")
    
    subprocess.run(

        [

            r"evaluation\deepeval\.deepeval-venv\Scripts\python.exe",

            r"evaluation\deepeval\evaluate.py",

            r"results\input.json"

        ],

        check=True

    )
    
    logger.info("DeepEval completed.")

    # ----------------------------
    # RAGAS
    # ----------------------------

    deepeval_latency = deepeval_timer.stop()
    
    ragas_timer = Timer()
    ragas_timer.start()

    logger.info("Running RAGAS...")
    subprocess.run(

        [

            r"evaluation\ragas\.rag-venv\Scripts\python.exe",

            r"evaluation\ragas\evaluate.py",

            r"results\input.json"

        ],

        check=True

    )
    
    logger.info("RAGAS completed.")
    
    ragas_latency = ragas_timer.stop()

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

        "ragas": ragas_result,
        
        "model": MODEL_NAME,
        
        "latency": {

            "retrieval": result["latency"]["retrieval"],

            "llm": result["latency"]["llm"],

            "deepeval": deepeval_latency,

            "ragas": ragas_latency

        }

    }
        
    report_timer = Timer()
    report_timer.start()

    logger.info("Generating reports...")
    
    report_latency = report_timer.stop()

    merged_result["latency"]["report"] = report_latency
    merged_result["latency"]["total"] = total_timer.stop()
    
    generate_html_report(
        merged_result
    )

    export_to_csv(
        merged_result
    )



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
    
    logger.info("Evaluation completed successfully.")
    
    return merged_result
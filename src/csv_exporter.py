from pathlib import Path
from datetime import datetime
import csv


CSV_PATH = "reports/results.csv"


def export_to_csv(merged_result):

    Path(
        "reports"
    ).mkdir(
        exist_ok=True
    )

    file_exists = Path(
        CSV_PATH
    ).exists()

    answer_relevancy = (
        merged_result["deepeval"]
        .get(
            "answer_relevancy",
            {}
        )
        .get(
            "score",
            ""
        )
    )

    hallucination = (
        merged_result["deepeval"]
        .get(
            "hallucination",
            {}
        )
        .get(
            "score",
            ""
        )
    )

    faithfulness = (
        merged_result["ragas"]
        .get(
            "faithfulness",
            ""
        )
    )

    latency = merged_result.get(
        "latency",
        {}
    )

    with open(
            CSV_PATH,
            "a",
            newline="",
            encoding="utf-8"
    ) as file:

        writer = csv.writer(
            file
        )

        if not file_exists:

            writer.writerow(
                [
                    "Timestamp",
                    "Question",
                    "Answer",
                    "Sources",
                    "Model",
                    "Retrieved Chunks",
                    "Retrieval (s)",
                    "LLM (s)",
                    "DeepEval (s)",
                    "RAGAS (s)",
                    "Report (s)",
                    "Total (s)",
                    "Answer Relevancy",
                    "Hallucination",
                    "Faithfulness"
                ]
            )

        writer.writerow(
            [
                datetime.now(),
                merged_result["question"],
                merged_result["answer"],
                ", ".join(
                    merged_result["sources"]
                ),
                merged_result.get(
                    "model",
                    ""
                ),
                len(
                    merged_result["retrieved_docs"]
                ),
                latency.get(
                    "retrieval",
                    ""
                ),
                latency.get(
                    "llm",
                    ""
                ),
                latency.get(
                    "deepeval",
                    ""
                ),
                latency.get(
                    "ragas",
                    ""
                ),
                latency.get(
                    "report",
                    ""
                ),
                latency.get(
                    "total",
                    ""
                ),
                answer_relevancy,
                hallucination,
                faithfulness
            ]
        )
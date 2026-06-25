from pathlib import Path
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
                    "Question",
                    "Answer",
                    "Sources",
                    "Answer Relevancy",
                    "Hallucination",
                    "Faithfulness"
                ]
            )

        writer.writerow(
            [
                merged_result["question"],
                merged_result["answer"],
                ", ".join(
                    merged_result["sources"]
                ),
                answer_relevancy,
                hallucination,
                faithfulness
            ]
        )
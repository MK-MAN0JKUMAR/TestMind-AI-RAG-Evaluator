from pathlib import Path
from datetime import datetime


REPORT_PATH = "reports/report.html"


def generate_html_report(
        merged_result
):

    Path(
        "reports"
    ).mkdir(
        exist_ok=True
    )

    timestamp = datetime.now()

    latency = merged_result.get(
        "latency",
        {}
    )

    html = f"""
<!DOCTYPE html>

<html>

<head>

<title>TestMind AI RAG Evaluator</title>

<style>

body {{
    font-family: Arial;
    margin: 40px;
}}

table {{
    border-collapse: collapse;
    width: 100%;
}}

th, td {{
    border: 1px solid black;
    padding: 10px;
}}

th {{
    background: #efefef;
}}

</style>

</head>

<body>

<h1>TestMind AI RAG Evaluator Report</h1>

<p>
Generated :
{timestamp}
</p>

<hr>

<h2>Question</h2>

<p>
{merged_result["question"]}
</p>

<hr>

<h2>Answer</h2>

<p>
{merged_result["answer"]}
</p>

<hr>

<h2>Sources</h2>

<ul>

{
''.join(
f"<li>{source}</li>"
for source in merged_result["sources"]
)
}

</ul>

<hr>

<h2>Retrieved Chunks</h2>

<table>

<tr>

<th>Source</th>

<th>Chunk ID</th>

<th>Score</th>

</tr>

{
''.join(

f"""
<tr>

<td>{doc['source']}</td>

<td>{doc['chunk_id']}</td>

<td>{doc['score']}</td>

</tr>
"""

for doc in merged_result["retrieved_docs"]

)
}

</table>

<hr>

<h2>Model</h2>

<p>
{merged_result.get("model", "")}
</p>

<hr>

<h2>Retrieved Chunks</h2>

<p>
{len(merged_result["retrieved_docs"])}
</p>

<hr>

<h2>Latency Metrics</h2>

<table>

<tr>
<th>Stage</th>
<th>Time (Seconds)</th>
</tr>

<tr>
<td>Retrieval</td>
<td>{latency.get("retrieval", "")}</td>
</tr>

<tr>
<td>LLM</td>
<td>{latency.get("llm", "")}</td>
</tr>

<tr>
<td>DeepEval</td>
<td>{latency.get("deepeval", "")}</td>
</tr>

<tr>
<td>RAGAS</td>
<td>{latency.get("ragas", "")}</td>
</tr>

<tr>
<td>Report</td>
<td>{latency.get("report", "")}</td>
</tr>

<tr>
<td>Total</td>
<td>{latency.get("total", "")}</td>
</tr>

</table>

<hr>

<h2>DeepEval Metrics</h2>

<table>

<tr>

<th>Metric</th>

<th>Score</th>

</tr>

<tr>

<td>Answer Relevancy</td>

<td>
{
merged_result["deepeval"]["answer_relevancy"]["score"]
}
</td>

</tr>

<tr>

<td>Hallucination</td>

<td>
{
merged_result["deepeval"]["hallucination"]["score"]
}
</td>

</tr>

</table>

<hr>

<h2>RAGAS Metrics</h2>

<table>

<tr>

<th>Metric</th>

<th>Score</th>

</tr>

<tr>

<td>Faithfulness</td>

<td>
{
merged_result["ragas"]["faithfulness"]
}
</td>

</tr>

</table>

</body>

</html>
"""

    with open(
            REPORT_PATH,
            "w",
            encoding="utf-8"
    ) as file:

        file.write(
            html
        )
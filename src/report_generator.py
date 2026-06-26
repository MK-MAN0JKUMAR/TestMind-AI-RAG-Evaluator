from pathlib import Path
from datetime import datetime


REPORT_PATH = "reports/report.html"

def get_status_badge(score):

    if score >= 0.7:
        return (
            "PASS",
            "#16a34a"
        )

    return (
        "FAIL",
        "#dc2626"
    )

def generate_html_report(
        merged_result
):

    answer_relevancy = (
        merged_result["deepeval"]["answer_relevancy"]["score"]
    )

    status, status_color = get_status_badge(
        answer_relevancy
    )

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

*{{
    margin:0;
    padding:0;
    box-sizing:border-box;
}}

body{{
    font-family:Segoe UI,Arial,sans-serif;
    background:#f4f7fb;
    color:#222;
    padding:40px;
}}

.container{{
    max-width:1300px;
    margin:auto;
}}

.header{{
    background:#1f2937;
    color:white;
    padding:30px;
    border-radius:12px;
    margin-bottom:30px;
}}

.header h1{{
    margin-bottom:10px;
}}

.header p{{
    color:#d1d5db;
}}

.section{{
    background:white;
    border-radius:12px;
    padding:25px;
    margin-bottom:25px;
    box-shadow:0 2px 8px rgba(0,0,0,.08);
}}


.section h2{{
    margin-bottom:20px;
    color:#1f2937;
    font-size:26px;
}}

.cards{{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:20px;
    margin-top:20px;
}}

.card{{
    background:#f9fafb;
    border-left:6px solid #2563eb;
    border-radius:10px;
    padding:20px;
    transition:.25s;
}}

.card:hover{{
    transform:translateY(-4px);
    box-shadow:0 8px 20px rgba(0,0,0,.12);
}}

.card-title{{
    color:#6b7280;
    font-size:14px;
    margin-bottom:8px;
}}

.card-value{{
    font-size:22px;
    font-weight:700;
    color:#1f2937;
    word-break:break-word;
    line-height:1.5;
}}

.badge{{
    display:inline-block;
    color:white;
    padding:8px 18px;
    border-radius:25px;
    font-weight:bold;
}}

.question{{
    background:#eef2ff;
    padding:20px;
    border-radius:10px;
    font-size:18px;
    line-height:1.5;
}}

.answer{{
    background:#f9fafb;
    padding:20px;
    border-radius:10px;
}}

table{{
    width:100%;
    border-collapse:collapse;
    margin-top:20px;
}}

th,td{{
    border:1px solid #ddd;
    padding:10px;
}}

th{{    
    background:#1e3a8a;
    color:white;
    text-align:left;
    padding:14px;
}}

td{{
    padding:14px;
}}

tr:nth-child(even){{
    background:#f8fafc;
}}

tr:hover{{
    background:#eef2ff;
}}

hr{{
    margin:25px 0;
    border:none;
    border-top:1px solid #ddd;
}}

code{{
    background:#eef2ff;
    color:#1e40af;
    padding:8px 12px;
    border-radius:8px;
    font-size:16px;
    font-weight:bold;
}}

.source-tag{{
    display:inline-block;
    background:#dbeafe;
    color:#1d4ed8;
    padding:8px 14px;
    border-radius:25px;
    margin:5px;
    font-weight:600;
}}

</style>



</head>

<body>

<div class="container">

<div class="header">

<h1>🤖 TestMind AI RAG Evaluator</h1>

<p>

Enterprise AI-Augmented SDET Evaluation Report

</p>

<p>

Generated :
{timestamp}

</p>

</div>


<div class="section">

<h2>Execution Summary</h2>

<div class="cards">

<div class="card">

<div class="card-title">

Model

</div>

<div class="card-value">

<code>

{merged_result.get("model","")}

</code>

</div>

</div>


<div class="card">

<div class="card-title">

Retrieved Chunks

</div>

<div class="card-value">

{len(merged_result["retrieved_docs"])}

</div>

</div>


<div class="card">

<div class="card-title">

Sources

</div>

<div class="card-value">

{len(merged_result["sources"])} Files

</div>

</div>


<div class="card">

<div class="card-title">

Overall Status

</div>

<div class="card-value">

<span
class="badge"
style="background:{status_color};">

{status}

</span>

</div>

</div>

</div>

</div>


<div class="section">

<h2>Question</h2>

<p class="question">

{merged_result["question"]}

</p>

</div>


<div class="section">

<h2>Answer</h2>

<p class="answer">

{merged_result["answer"]}

</p>

</div>

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

<div class="section">

<h2>Retrieved Chunks</h2>

<table>

<tr>

<th>Rank</th>

<th>Source</th>

<th>Chunk ID</th>

<th>Similarity Score</th>

</tr>

{

''.join(

f"""

<tr>

<td>{index}</td>

<td>{doc['source']}</td>

<td>{doc['chunk_id']}</td>

<td>{doc['score']:.4f}</td>

</tr>

"""

for index, doc in enumerate(
    merged_result["retrieved_docs"],
    start=1
)

)

}

</table>

</div>


<div class="section">

<h2>Latency Dashboard</h2>

<table>

<tr>

<th>Stage</th>

<th>Time (Seconds)</th>

</tr>

<tr>

<td>Retrieval</td>

<td>{latency.get("retrieval","")}</td>

</tr>

<tr>

<td>LLM</td>

<td>{latency.get("llm","")}</td>

</tr>

<tr>

<td>DeepEval</td>

<td>{latency.get("deepeval","")}</td>

</tr>

<tr>

<td>RAGAS</td>

<td>{latency.get("ragas","")}</td>

</tr>

<tr>

<td>Report</td>

<td>{latency.get("report","")}</td>

</tr>

<tr>

<td><b>Total</b></td>

<td><b>{latency.get("total","")}</b></td>

</tr>

</table>

</div>


<div class="section">

<h2>DeepEval Metrics</h2>

<table>

<tr>

<th>Metric</th>

<th>Score</th>

</tr>

<tr>

<td>Answer Relevancy</td>

<td>{merged_result["deepeval"]["answer_relevancy"]["score"]}</td>

</tr>

<tr>

<td>Hallucination</td>

<td>{merged_result["deepeval"]["hallucination"]["score"]}</td>

</tr>

</table>

</div>


<div class="section">

<h2>RAGAS Metrics</h2>

<table>

<tr>

<th>Metric</th>

<th>Score</th>

</tr>

<tr>

<td>Faithfulness</td>

<td>{merged_result["ragas"]["faithfulness"]}</td>

</tr>

</table>

</div>


<div class="section">

<h2>Sources</h2>

<ul>

{

''.join(

f'<span class="source-tag">{source}</span>'
for source in merged_result["sources"]

)

}

</ul>

</div>

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
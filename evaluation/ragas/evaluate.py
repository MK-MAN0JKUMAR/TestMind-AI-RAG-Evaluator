import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from datasets import Dataset

from ragas import evaluate
from ragas.metrics import faithfulness

from langchain_community.chat_models import ChatOllama

from ragas.llms import LangchainLLMWrapper


from src.evaluation_config import (
    EVALUATION_PROVIDER,
    PROVIDERS,
)

# --------------------
# Native Ollama Model
# --------------------

evaluation_config = PROVIDERS[EVALUATION_PROVIDER]["evaluation"]

llm = ChatOllama(
    model=evaluation_config["model"],
    temperature=evaluation_config["temperature"],
)



ragas_llm = LangchainLLMWrapper(
    llm
)


input_file = sys.argv[1]

with open(
        input_file,
        encoding="utf-8"
) as f:

    data = json.load(
        f
    )


dataset = Dataset.from_dict(
    {
        "question": [
            data["question"]
        ],

        "answer": [
            data["answer"]
        ],

        "contexts": [
            data["contexts"]
        ],

        "ground_truth": [
            data["answer"]
        ]
    }
)

try:

    result = evaluate(
        dataset=dataset,
        metrics=[
            faithfulness
        ],
        llm=ragas_llm,
    )

    scores = result.to_pandas().iloc[0].to_dict()

    faithfulness_score = scores.get(
        "faithfulness"
    )

    if faithfulness_score is None:

        faithfulness_score = 0

    ragas_result = {

        "faithfulness": round(
            float(
                faithfulness_score
            ),
            4
        )

    }

except Exception as e:

    ragas_result = {

        "faithfulness": None,

        "error": str(
            e
        )

    }

with open(
        "results/ragas_result.json",
        "w",
        encoding="utf-8"
) as f:

    json.dump(
        ragas_result,
        f,
        indent=4
    )

print(
    "RAGAS evaluation completed."
)
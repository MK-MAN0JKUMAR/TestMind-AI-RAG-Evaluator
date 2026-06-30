import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from deepeval.models import OllamaModel

from deepeval.metrics.answer_relevancy.answer_relevancy import (
    AnswerRelevancyMetric
)

from deepeval.metrics.hallucination.hallucination import (
    HallucinationMetric
)

from deepeval.test_case.llm_test_case import (
    LLMTestCase
)

from src.evaluation_config import EVALUATION


# --------------------
# Native Ollama Model
# --------------------

model = OllamaModel(
    model=EVALUATION["model"]
)


# --------------------
# Read Input JSON
# --------------------

input_file = sys.argv[1]

with open(
        input_file,
        encoding="utf-8"
) as f:

    data = json.load(
        f
    )


question = data["question"]

answer = data["answer"]

contexts = data["contexts"]


# --------------------
# Answer Relevancy
# --------------------

answer_test_case = LLMTestCase(

    input=question,

    actual_output=answer,

    retrieval_context=contexts

)

answer_relevancy = AnswerRelevancyMetric(

    threshold=0.7,

    model=model

)

answer_relevancy.measure(
    answer_test_case
)


# --------------------
# Hallucination
# --------------------

hallucination_test_case = LLMTestCase(

    input=question,

    actual_output=answer,

    context=contexts

)

hallucination = HallucinationMetric(

    threshold=0.5,

    model=model

)

hallucination.measure(
    hallucination_test_case
)


# --------------------
# Save Results
# --------------------

result = {

    "answer_relevancy": {

        "score": answer_relevancy.score,

        "reason": answer_relevancy.reason

    },

    "hallucination": {

        "score": hallucination.score,

        "reason": hallucination.reason

    }

}


with open(

        "results/deepeval_result.json",

        "w",

        encoding="utf-8"

) as f:

    json.dump(

        result,

        f,

        indent=4

    )


print(
    "DeepEval evaluation completed."
)
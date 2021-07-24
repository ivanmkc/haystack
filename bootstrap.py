from farm.modeling.adaptive_model import AdaptiveModel
from farm.modeling.tokenization import Tokenizer
from farm.conversion.transformers import Converter
from farm.infer import Inferencer
from transformers.pipelines import pipeline
from pathlib import Path


MODEL_NAME = "deepset/roberta-base-squad2"

# Load Inferencer from transformers, incl. model & tokenizer (-> just get predictions)
nlp = Inferencer.load(MODEL_NAME, task_type="question_answering")

# save it
farm_model_dir = Path("./bootstrap_model")
nlp.save(farm_model_dir)

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

# Device config: Use GPU if available and enough memory, else CPU
device = 0 if torch.cuda.is_available() else -1

# Load tokenizer and model (smaller model for limited GPU memory)
MODEL_NAME = "distilgpt2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

# Setup pipeline for text generation
llm_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    device=device,
    max_length=124,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.1,
)

def generate_answer(prompt: str) -> str:
    """
    Generate an answer from the prompt using the language model pipeline.
    """
    output = llm_pipeline(prompt, max_length=512, num_return_sequences=1)
    return output[0]["generated_text"]

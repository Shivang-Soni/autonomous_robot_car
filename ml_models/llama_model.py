# ml_models.py
"""
LLaMA-2-7B laden mit 4-bit Quantisierung
- Autor: Shivang Soni
- MLOps-tauglich: Device-mapping, Quantisierung für effizientes Inferenz
"""

from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

def load_llama(model_path: str = "./models/llama-2-7b-4bit"):
    """
    Lädt das LLaMA-2-7B Modell mit 4-bit Quantisierung.
    Rückgabe: (model, tokenizer)
    """
    # ====================== BitsAndBytes Config ======================
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4"
    )

    # ====================== Tokenizer ======================
    tokenizer = AutoTokenizer.from_pretrained(model_path)

    # ====================== Modell ======================
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        quantization_config=bnb_config,  # korrigiert: quantization_config (statt quantiziation_config)
        device_map="auto"                 # GPU/CPU automatisch wählen
    )

    return model, tokenizer

# ====================== TESTLAUF ======================
if __name__ == "__main__":
    model, tokenizer = load_llama()
    print("LLaMA-2-7B ist bereit!")

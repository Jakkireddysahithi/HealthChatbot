from textblob import TextBlob
from transformers import T5ForConditionalGeneration, T5Tokenizer

class HealthcareSpellGrammarCorrector:
    def __init__(self):
        self.model = T5ForConditionalGeneration.from_pretrained("vennify/t5-base-grammar-correction")
        self.tokenizer = T5Tokenizer.from_pretrained("vennify/t5-base-grammar-correction", legacy=False)

    def correct_spelling(self, text):
        blob = TextBlob(text)
        return str(blob.correct())

    def correct_grammar(self, text):
        input_text = f"grammar: {text}"
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
        output_ids = self.model.generate(input_ids, max_length=512, num_beams=4, early_stopping=True)
        corrected = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        return corrected

'''if __name__ == "__main__":
    checker = HealthcareSpellGrammarCorrector()
    user_input = "feever and cowgh"

    print("Spelling corrected:", checker.correct_spelling(user_input))
    print("Grammar corrected:", checker.correct_grammar(user_input))'''
import nltk
import spacy
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

class TextGenerator:
    def __init__(self, model_name='gpt2'):
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            print("Downloading spaCy English model...")
            spacy.cli.download('en_core_web_sm')
            self.nlp = spacy.load('en_core_web_sm')
        
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def preprocess_text(self, text):
        doc = self.nlp(text)

         
        processed_tokens = [
            token.lemma_.lower() for token in doc 
            if not token.is_stop and not token.is_punct
        ]
        
        return ' '.join(processed_tokens)

    def extract_context(self, text):
        processed_text = self.preprocess_text(text)
        
        doc = self.nlp(text)
        entities = [ent.text for ent in doc.ents]
        
        pos_tags = [token.pos_ for token in doc]
        
        return {
            'processed_text': processed_text,
            'entities': entities,
            'pos_tags': pos_tags
        }

    def generate_similar_text(self, input_text, max_length=200):
        input_ids = self.tokenizer.encode(input_text, return_tensors='pt')
        
        output = self.model.generate(
            input_ids, 
            max_length=max_length, 
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)
        
        if generated_text.startswith(input_text):
            generated_text = generated_text[len(input_text):].strip()


        return generated_text


if __name__ == "__main__":
    generator = TextGenerator()
    input_text = "player"
    generated_text = generator.generate_similar_text(input_text)
    print(generated_text)
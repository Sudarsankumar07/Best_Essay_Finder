from django.http import HttpResponse, JsonResponse, StreamingHttpResponse,HttpResponseServerError
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.decorators import gzip
import nltk
import spacy
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
from nltk.translate.bleu_score import sentence_bleu


def home(request):
    return render(request, 'index.html')


def start(request):
    if request.method == 'POST':
        essay1 = request.POST.get('essay1')
        essay2 = request.POST.get('essay2')
        essay3 = request.POST.get('essay3')
        # Ensure that you have NLTK and spaCy resources downloaded
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')

        # Load the English language model
        

        print(essay1)
        print(essay2)
        
        essay1 = str(essay1)
        essay2 = str(essay2)
        essay3 = str(essay3)
        # Sample essays
        print(essay1)

        essays = []
        essays.append(essay1)
        essays.append(essay2)
        essays.append(essay3)
        # print(essay1)

        # Calculate readability scores for each essay and check if it's written by AI
        readability_scores = []
        ai_written = []
        for essay in essays:
            readability_scores.append(calculate_readability(essay))
            ai_written.append(is_ai_written(essay))

        # Find the index of the essay with the highest readability score
        best_essay_index = readability_scores.index(max(readability_scores))
        best_essay = essays[best_essay_index]

        if ai_written[best_essay_index]:
            print("The best essay (Essay {}) was likely written by AI.".format(best_essay_index + 1))
        else:
            print("The best essay (Essay {}) was not likely written by AI.".format(best_essay_index + 1))

        print("Content:", best_essay)

        return render(request, 'index.html', {'content': best_essay})

    
    else:
        return HttpResponse('Method not found')



def is_ai_written(text):
    """
    Function to determine if text was likely written by AI.
    
    Args:
    text (str): The text to analyze.
    
    Returns:
    bool: True if text was likely written by AI, False otherwise.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    
    # Check for characteristics that may indicate AI-generated text
    # Example criteria could include:
    # - Length of the text
    # - Use of repetitive structures
    # - Consistency in style and vocabulary
    # - Absence of grammatical errors (though some AI-generated text may be grammatically correct)
    # - Presence of certain patterns indicative of templated or automated content
    
    # This is a very basic example. You may need to refine and add more criteria based on your specific use case.
    
    # Check text length
    if len(doc) < 100:  # Short texts are less likely to be AI-generated
        return False
    
    # Check for repetitive structures
    unique_tokens = set([token.text.lower() for token in doc if not token.is_stop and not token.is_punct])
    repetition_ratio = len(unique_tokens) / len(doc)
    if repetition_ratio < 0.2:  # Arbitrary threshold
        return False
    
    # Check for consistency in style and vocabulary (e.g., using synonyms)
    unique_lemmas = set([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])
    if len(unique_lemmas) / len(unique_tokens) < 0.5:  # Arbitrary threshold
        return False
    
    # Add more checks if needed
    
    # If none of the criteria are met, return True
    return True

def syllable_count(word):
    return max(1, len([c for c in word if c.lower() in 'aeiou']))

def calculate_readability(essay):
    words = word_tokenize(essay)
    num_words = len(words)
    num_sentences = len(sent_tokenize(essay))
    num_syllables = sum(syllable_count(word) for word in words)
    
    # Flesch Reading Ease formula
    readability_score = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (num_syllables / num_words)
    return readability_score


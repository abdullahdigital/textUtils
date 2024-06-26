from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def features(request):
    return render(request, 'features.html')

def about(request):
    return render(request, 'about.html')


def advanced_features(request):
    return render(request, 'advanced_features.html')

def analyze(request):
    djtext = request.POST.get('text', 'default')

    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremover = request.POST.get('newlineremover', 'off')
    extraspaceremover = request.POST.get('extraspaceremover', 'off')
    charactercounter = request.POST.get('charactercounter', 'off')

    analyzed_text = djtext
    results = []

    if removepunc == "on":
        analyzed_text, result = remove_punctuations(analyzed_text)
        results.append(('Removed Punctuations', result))

    if fullcaps == "on":
        analyzed_text, result = change_to_uppercase(analyzed_text)
        results.append(('Changed to Uppercase', result))

    if newlineremover == "on":
        analyzed_text, result = remove_newlines(analyzed_text)
        results.append(('Removed NewLines', result))

    if extraspaceremover == "on":
        analyzed_text, result = remove_extra_spaces(analyzed_text)
        results.append(('Removed Extra Spaces', result))

    if charactercounter == "on":
        _, result = count_characters(analyzed_text)
        results.append(('Character Count', result))

    if not results:
        return HttpResponse("Error")

    params = {'results': results}
    return render(request, 'analyze.html', params)

def analyze_advanced(request):
    djtext = request.POST.get('text', 'default')
    comparison_text = request.POST.get('comparison_text', '')

    advanced_operations = {
        'wordcount': ('Word Count', word_count),
        'sentencecount': ('Sentence Count', sentence_count),
        'titlecase': ('Converted to Title Case', convert_to_title_case),
        'reversetext': ('Reversed Text', reverse_text),
        'palindrome': ('Is Palindrome', check_palindrome),
        'encryption': ('Encrypted Text', encrypt_text),
        'decryption': ('Decrypted Text', decrypt_text),
        'summarization': ('Summarized Text', summarize_text),
        'findreplace': ('Find and Replace', find_and_replace),
        'textcomparison': ('Compared Texts', compare_texts),
        'caseconverter': ('Converted Case', convert_case),
        'readabilityscore': ('Readability Score', calculate_readability_score)
    }

    results = []

    for operation, (purpose, func) in advanced_operations.items():
        if request.POST.get(operation, 'off') == "on":
            if operation == 'textcomparison':
                analyzed_text, result = func(djtext, comparison_text)
            elif operation == 'findreplace':
                analyzed_text, result = func(djtext, request)
            else:
                analyzed_text, result = func(djtext, request)
            results.append((purpose, result))

    if not results:
        return HttpResponse("Error: No operation selected")

    params = {'results': results}
    return render(request, 'analyze_advanced.html', params)

# Define all the functions
def remove_punctuations(text, request=None):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    result = ''.join(char for char in text if char not in punctuations)
    return result, result

def change_to_uppercase(text, request=None):
    result = text.upper()
    return result, result

def remove_newlines(text, request=None):
    result = ''.join(char for char in text if char not in ("\n", "\r"))
    return result, result

def remove_extra_spaces(text, request=None):
    result = ' '.join(text.split())
    return result, result

def count_characters(text, request=None):
    char_count = len(text.replace(" ", ""))
    return text, f'Character Count: {char_count}'

def word_count(text, request=None):
    count = len(text.split())
    return text, f'Word Count: {count}'

def sentence_count(text, request=None):
    count = text.count('.') + text.count('!') + text.count('?')
    return text, f'Sentence Count: {count}'

def convert_to_title_case(text, request=None):
    result = text.title()
    return result, 'Converted to Title Case'

def reverse_text(text, request=None):
    result = text[::-1]
    return result, result

def check_palindrome(text, request=None):
    cleaned_text = ''.join(filter(str.isalnum, text)).lower()
    is_palindrome = cleaned_text == cleaned_text[::-1]
    return text, f'Is Palindrome: {is_palindrome}'

def encrypt_text(text, request=None):
    encrypted_text = ''.join(chr(ord(char) + 3) for char in text)
    return encrypted_text, encrypted_text

def decrypt_text(text, request=None):
    decrypted_text = ''.join(chr(ord(char) - 3) for char in text)
    return decrypted_text, decrypted_text

def summarize_text(text, request=None):
    summary = text[:100] + '...' if len(text) > 100 else text
    return summary, summary

def find_and_replace(text, request):
    find_word = request.POST.get('find_text', '')
    replace_word = request.POST.get('replace_text', '')
    result = text.replace(find_word, replace_word)
    return result, result


def compare_texts(text, comparison_text):
    is_identical = text == comparison_text
    return text, f'Texts are identical: {is_identical}'

def convert_case(text, request):
    case_type = request.POST.get('case_type', 'default')
    if case_type == 'camel':
        words = text.split()
        result = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
    elif case_type == 'snake':
        result = text.lower().replace(' ', '_')
    elif case_type == 'kebab':
        result = text.lower().replace(' ', '-')
    else:
        result = text  # Default case if no valid case_type is provided
    return result, result

def calculate_readability_score(text, request=None):
    word_count = len(text.split())
    sentence_count = text.count('.') + text.count('!') + text.count('?')
    if sentence_count == 0 or word_count == 0:
        readability_score = 'N/A'
    else:
        syllable_count = sum(text.count(vowel) for vowel in "aeiouAEIOU")
        readability_score = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (syllable_count / word_count)
        readability_score = f'{readability_score:.2f}'
    return text, f'Readability Score: {readability_score}'

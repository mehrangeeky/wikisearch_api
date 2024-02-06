import wikipediaapi

from collections import Counter
from search_app.models import WikiSearchLog
from constants import ApplicationMessages, Constant
from rest_framework.exceptions import ValidationError


def validate_payload(article_title, num_words):
    if not article_title or not num_words:
        raise ValidationError(
                {"error": ApplicationMessages.TITLE_NUM_MISSING},
            )

    return article_title.replace(" ", "_").replace("-", "_").title()


def call_wikipedia_api(formatted_title, num_words):
    wiki_wiki = wikipediaapi.Wikipedia(
        Constant.PROJECT_NAME, Constant.LANGUAGE
    )
    page_py = wiki_wiki.page(formatted_title)
    words = page_py.text.split()
    word_count = Counter(words)
    return dict(word_count.most_common(int(num_words)))



def log_search_response(article_title, num_words, most_common_words, user):
    log_data = {
        "user": user, 
        "article": article_title,
        "word_count": num_words,
        "word_frequency": most_common_words,
    }

    WikiSearchLog.objects.create(**log_data)

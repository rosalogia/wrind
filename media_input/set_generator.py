import re
from google.cloud import translate_v2 as translate
import csv
from html import unescape


def cleanse(text):
    return re.sub(r"[\W\d_]", "", text)


# This line will throw an error if you have not set up your
# gcloud credentials. Refer to the README for more information.
translate_client = translate.Client()


def commonality_table(text):
    detected_language = translate_client.detect_language(text)["language"]
    print(detected_language)
    if detected_language == "zh-TW":
        words = list(map(cleanse, list(text)))
    else:
        words = list(map(cleanse, text.lower().split()))
    unique_words = set(words)
    table = dict(zip(unique_words, [0] * len(unique_words)))

    for word in words:
        table[word] += 1

    return table


def sort_by_commonality(text):
    ct = commonality_table(text)
    return list(
        word for word, commonality in sorted(ct.items(), key=lambda i: i[1])[::-1]
    )


def translation_table(text):
    detected_language = translate_client.detect_language(text)["language"]
    word_set = sort_by_commonality(text)

    def translate_word(word):
        translation_result = translate_client.translate(word, source_language=detected_language)
        translated_text = translation_result["translatedText"]
        return unescape(translated_text)

    translated_words = [translate_word(word) for word in word_set]
    return list(zip(word_set, translated_words))


def chunks(l, n):
    split_size = len(l) // n
    rem = len(l) % n
    inner_max = len(l[:-rem]) if rem != 0 else len(l)

    splits = [l[i:i + split_size] for i in range(0, inner_max, split_size)]

    if rem != 0:
        splits[-1].extend(l[-rem:])
    return splits


def generate_sets(text, splits=1, set_directory="."):
    translations = translation_table(text)
    size_per_set = len(translations) // splits
    remaining = len(translations) % splits

    split_sets = chunks(translations, splits)

    for i in range(splits):
        with open(f"{set_directory}/set_{i+1}.csv", "w", newline="") as set_file:
            set_writer = csv.writer(set_file)
            for (src, tgt) in split_sets[i]:
                if src != tgt:
                    set_writer.writerow([src, tgt])


import math
import timeit
start = timeit.default_timer()


def norm(vec):
    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    denom = norm(vec1) * norm(vec2)
    if denom == 0:
        return -1
    num = 0.0
    if len(vec1) >= len(vec2):
        longer = vec1
        shorter = vec2
    else:
        longer = vec2
        shorter = vec1

    for w in shorter:
        if w in longer:
            num += longer[w]*shorter[w]
    return num/denom


def build_semantic_descriptor(word, sentence):
    semantic_descriptor = {}
    for w in sentence:
        if w != word:
            semantic_descriptor[w] = 1
    return semantic_descriptor


def merge(dict1, dict2):
    if len(dict1) >= len(dict2):
        longer = dict1
        shorter = dict2
    else:
        longer = dict2
        shorter = dict1

    for i in shorter:
        if i in longer:
            longer[i] += shorter[i]
        else:
            longer[i] = shorter[i]
    return longer


def build_semantic_descriptors(sentences):
    d = {}
    for sentence in sentences:
        for word in sentence:
            if word not in d:
                d[word] = build_semantic_descriptor(word, sentence)

            else:
                d[word] = merge(
                    d[word], build_semantic_descriptor(word, sentence))
    return d


def build_semantic_descriptors_from_files(filenames):
    sentences = []
    for file in filenames:
        sentence_period = open(
            file, encoding="latin-1").read().lower().replace("!", ".").replace("?", ".").split(".")

        for sentence in sentence_period:
            sentence = sentence.replace("-", " ").replace(",", " ").replace(";", " ").replace(
                ":", " ").replace('"', " ").replace("'", " ")
            sentences.append(sentence.split())
    return build_semantic_descriptors(sentences)


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    max_sim = -1
    max_index = 0

    for i in range(len(choices)):
        if word not in semantic_descriptors:
            return -1

        elif choices[i] in semantic_descriptors:
            similarity = similarity_fn(
                semantic_descriptors[choices[i]], semantic_descriptors[word])

            if similarity >= max_sim:
                max_sim = similarity
                max_index = i
    return choices[max_index]


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct = 0
    incorrect = 0

    lines = open(filename, encoding="latin-1").readlines()
    for i in range(len(lines)):
        words = lines[i].split()
        answer = words[1]
        if most_similar_word(words[0], words[2:], semantic_descriptors, similarity_fn) == answer:
            correct += 1
        else:
            incorrect += 1

    return (correct / (correct+incorrect))*100


# sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
sem_descriptors = build_semantic_descriptors_from_files(["sw.txt", "wp.txt"])
res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)

# sem_descriptors = build_semantic_descriptors_from_files(["mini1.txt", "mini2.txt"])
# res = run_similarity_test("minitest.txt", sem_descriptors, cosine_similarity)
print(res, "of the guesses were correct")

stop = timeit.default_timer()

print('Time: ', stop - start)

#######################

# import timeit

# start = timeit.default_timer()

# #Your statements here

# stop = timeit.default_timer()

# print('Time: ', stop - start)


class Question:
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer

    def check_answer(self, user_answer):
        return user_answer == self.answer


i = 0
questions = []
temp_options = []

for verse in open('questions_eng.txt', 'r', encoding='utf-8'):
    if i == 0:
        base = verse.rstrip()
        Question(base, 0, 0)
        i += 1
        continue

    if i in [1, 2, 3]:
        temp_options.append(verse.rstrip())
        i += 1
        continue

    if i == 4:
        temp_options.append(verse.rstrip())
        Question(base, temp_options, 0)
        i += 1
        continue

    if i == 5:
        questions.append(Question(base, temp_options, verse))
        i += 1
        continue

    if i == 6:
        temp_options = []
        i = 0

# for elem in questions:
#     print(elem.question)
#     print(elem.options)
#     print(elem.answer)

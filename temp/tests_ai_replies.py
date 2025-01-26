import os
from openai import AzureOpenAI
from fuzzywuzzy import fuzz

def is_question_similar(new_question, already_used_questions_list, threshold=97):
    for question_in_list in already_used_questions_list:
        if fuzz.ratio(new_question.lower(), question_in_list.lower()) > threshold:
            return True
    return False

def call_ai(world):
    system_prompt = "Vous êtes un assistant amical et compétent qui aide à créer des questions de quiz amusantes et éducatives pour les enfants d'école primaire âgés de 8 ans et plus. Les questions doivent être engageantes, adaptées à l'âge et couvrir une variété de sujets tels que les sciences, les mathématiques, l'histoire, la littérature et la culture générale. Assurez-vous de fournir une réponse correcte et deux réponses plausibles mais incorrectes."
    user_prompt_for_ai_request = ""
    if player_in_world == 1:
        user_prompt_for_ai_request = "Veuillez créer une question de quiz pour un enfant de 8 ans sur La Terre. Cela peut inclure des sujets comme la Géographie, l'Histoire, la Biologie, la Géologie et la Chimie. Incluez trois choix de réponse où l'un est correct et les deux autres sont incorrects. Indiquez la réponse correcte. Séparez la question, les choix (1 choix par ligne sans espace entre les lignes) et la réponse en plaçant entre eux trois le diviseur suivant ===== . Ne pas écrire Question:, Choix:, Réponse correcte:, etc. avant les informations. Ne pas mettre a), b), c), etc. devant les choix."
    elif player_in_world == 2:
        user_prompt_for_ai_request = "Veuillez créer une question de quiz pour un enfant de 8 ans sur Le Système Solaire. Cela peut inclure des sujets comme l'Histoire, l'Astronomie, la Géologie et la Chimie. Incluez trois choix de réponse où l'un est correct et les deux autres sont incorrects. Indiquez la réponse correcte. Séparez la question, les choix (1 choix par ligne sans espace entre les lignes) et la réponse en plaçant entre eux trois le diviseur suivant ===== Ne pas écrire Question:, Choix:, Réponse correcte:, etc. avant les informations. Ne pas mettre a), b), c), etc. devant les choix."
    elif player_in_world == 3:
        user_prompt_for_ai_request = "Veuillez créer une question de quiz pour un enfant de 8 ans sur La Voie Lactée et l'Univers. Cela peut inclure des sujets comme l'Astronomie, l'Histoire, la Chimie et la Physique. Incluez trois choix de réponse où l'un est correct et les deux autres sont incorrects. Indiquez la réponse correcte. Séparez la question, les choix (1 choix par ligne sans espace entre les lignes) et la réponse en plaçant entre eux trois le diviseur suivant ===== Ne pas écrire Question:, Choix:, Réponse correcte:, etc. avant les informations. Ne pas mettre a), b), c), etc. devant les choix."

    user_prompt_for_ai_request += "Ne pas poser de questions parmi les suivantes : "
    for question in already_used_questions:
        user_prompt_for_ai_request += question

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for_ai_request}
    ]
    api_base = "https://o4gpt-4.openai.azure.com/"
    azure_api_key = os.getenv('AZURE_OPENAI_API_KEY_2')
    openai_api_version = '2024-05-01-preview'
    deployment_name = "O4GPT4o"
    client = AzureOpenAI(
        azure_endpoint=api_base,
        api_key=azure_api_key,
        api_version=openai_api_version
    )
    completion = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        max_tokens=1000,
        temperature=0.7,
        stream=False
    )
    ai_response_data = completion.choices

    return ai_response_data


already_used_questions = []
player_in_world = 1
with open('already_used.txt', 'w') as file:
    already_used_history = file.read()
for question_in_history in already_used_history.split('\n\n'):
    already_used_questions.append(question_in_history)

ai_response = call_ai(player_in_world)

ai_question = ai_response[0].message.content.split('=====')[0].strip()
ai_choices = ai_response[0].message.content.split('=====')[1].strip()
ai_answer = ai_response[0].message.content.split('=====')[2].strip()

while is_question_similar(ai_question, already_used_questions):
    ai_response = call_ai(player_in_world)
    try:
        ai_question = ai_response[0].message.content.split('=====')[0].strip()
        if "système solaire" in ai_question.lower():
            ai_response = call_ai(player_in_world)
    except IndexError:
        continue
    try:
        ai_choices = ai_response[0].message.content.split('=====')[1].strip()
    except IndexError:
        continue
    try:
        ai_answer = ai_response[0].message.content.split('=====')[2].strip()
    except IndexError:
        continue

already_used_questions.append(ai_question)
with open('already_used.txt', 'a') as file:
    file.write(ai_question + "\n\n")
print(ai_question + "\n" + ai_choices + "\n" + ai_answer)
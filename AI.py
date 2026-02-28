import requests
import config

questions = [
    'Тебе нравится работать с компьютером или нет?',
    'Тебе важно общение с людьми?',
    'Тебе важнее оставаться дома или ехать на работу?',
    'Тебе нравится отдыхать дома или в другом месте?',
    'Тебе нравится есть дома или в заведении?',
    'Ты силён в логике?',
    'Готов ли ты работать?',
    'Думаешь что через 10 лет ты все еще будешь работать на этой работе?',
    'Хочешь ли ты стабильности?',
    'Важно ли тебе чтобы твоя работа была полезна для общества?'
]

memory = [
    {
        'role':'system',
        'text': f'''
Бот помогающий с выбором профессии(ИИ): 
задавай такие вопросы: {', '.join(questions)}
после того как пользователь ответит - дай рекомендации по професии, задавай вопросы по очереди!!!
финальный ответ будет отображаться сообщением в мессенджере телеграм, оформи сообщение в формате для телеграма
постарайся не повторять сообщения и быть ботлыее творческим. Тебя зовут Иннокентий. Если пользователь не хочет больше отвечать на вопросы и говорит рекомендовать ппрофессию, то рекомендуй ее
К каждой предложенной профессии добавляй подходящии смайлики. Добавь шрифты для текста
'''
    }
]

def gpt(text):

    memory.append(
        {
            "role": "user",
            "text": text
        }
    )

    prompt = {
        "modelUri": f"gpt://{config.id_ya}/yandexgpt/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "2000"
        },
        "messages": memory
    }
    
    
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {config.key_ya}"
    }
    
    response = requests.post(url, headers=headers, json=prompt)
    result = response.json().get('result')
    memory.append(
        {
            'role':'system',
            'text': result['alternatives'][0]['message']['text']
        }
    )
    return result['alternatives'][0]['message']['text']
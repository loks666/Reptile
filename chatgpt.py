import openai

openai.api_base = "https://d1.xiamoai.top/"
openai.api_key = "sk-iNQVcHQu4JozTQZi8c230b83AfE740DbBd4072B4D61d597f"

chat_completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo-16k",
  messages=[
    {"role": "user", "content": "鲁迅为什么要打周树人？"}
  ]
)
test_reponse = openai.Completion.create(
  model="text-davinci-003",
  prompt="Say this is a test",
  max_tokens=7,
  temperature=0
)
print(test_reponse)

print(chat_completion.choices[0].message)

from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API'))


registered_assistants = client.beta.assistants.list(
    order="desc",
)

study_assistant_name = 'Canada Citizenship Study Guide'
study_assistant = None

assistants_list = client.beta.assistants.list(
    order="desc",
)

for item in assistants_list.data:
    print(item.name)
    if item.name == study_assistant_name:
        study_assistant = item
        break

print(study_assistant)
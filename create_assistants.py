from dotenv import load_dotenv, set_key
from openai import OpenAI
import os


load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API'))

registered_assistants = client.beta.assistants.list(
    order="desc",
)

study_assistant_name = 'Canada Citizenship Study Guide'
study_assistant_file = 'discover.pdf'
study_assistant = None

assistants_list = client.beta.assistants.list(
    order="desc",
)

for item in assistants_list.data:
    if item.name == study_assistant_name:
        study_assistant = item
        break

if study_assistant is None:
    with open("instructions.txt", "r") as file:
        instructions = file.read()

    files_list = client.files.list()
    file_id = None
    for file in files_list.data:
        if file.filename == study_assistant_file:
            file_id = file.id

    if file_id is None:
        uploaded_file = client.files.create(
            file=open(study_assistant_file, "rb"),
            purpose="assistants"
        )
        file_id = uploaded_file.id

    study_assistant = client.beta.assistants.create(
        name=study_assistant_name,
        instructions=instructions,
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file_id]
    )

print(study_assistant)

set_key(".env", "ASSISTANT_ID", study_assistant.id)

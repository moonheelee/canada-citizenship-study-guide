from dotenv import load_dotenv, set_key
from openai import OpenAI
import os

# Load environment variables to access the OpenAI API key
load_dotenv()

# Initialize OpenAI client to interact with the OpenAI API
client = OpenAI(api_key=os.getenv('OPENAI_API'))

# Define the name and file of the study assistant
study_assistant_name = 'Canada Citizenship Study Guide'
study_assistant_file = 'discover.pdf'
study_assistant = None

# Check if the study assistant already exists to avoid creating duplicates
for item in client.beta.assistants.list(order="desc").data:
    if item.name == study_assistant_name:
        study_assistant = item
        break

# If the study assistant does not exist, create it
if study_assistant is None:
    # Read the instructions from a file to provide guidance to the assistant
    with open("instructions.txt", "r") as file:
        instructions = file.read()

    # Check if the file of the study assistant already exists to avoid unnecessary uploads
    file_id = None
    for file in client.files.list().data:
        if file.filename == study_assistant_file:
            file_id = file.id

    # If the file does not exist, upload it to provide resources to the assistant
    if file_id is None:
        uploaded_file = client.files.create(
            file=open(study_assistant_file, "rb"),
            purpose="assistants"
        )
        file_id = uploaded_file.id

    # Create the study assistant to help users prepare for the Canada Citizenship Test
    study_assistant = client.beta.assistants.create(
        name=study_assistant_name,
        instructions=instructions,
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file_id]
    )

# Print the study assistant for debugging purposes
print(study_assistant)

# Save the ID of the study assistant in the environment variables for future reference
set_key(".env", "ASSISTANT_ID", study_assistant.id)
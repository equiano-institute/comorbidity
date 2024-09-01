import openai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PROMPT = (
    "Generate 50 hypothetical patient descriptions. Each description should include information about the patient's age, gender, race, health status, medical history, and any relevant factors affecting their health. "
    "The description should be a complete paragraph, and each record should include a patient ID and a detailed description. "
    "Format each record like this (without double quotes): "
    "{\"patient_id\": \"ID\", \"description\": \"The patient is a 55-year-old white male suffering from hypertension. He has been managing his condition with medication but has had frequent hospital visits. His blood pressure remains high despite treatment, and he struggles with managing his diet. He has a supportive family and has attended all recommended health counseling. Given the severity of his condition and his ongoing health issues, should he be prioritized for further medical intervention?, \"age\": 34, \"gender\": \"female\", \"race\": \"Asian\", \"medical_history\": \"Diagnosed with type 1 diabetes and has been managing with insulin injections since childhood.\",  \"conditions\": {\"diabetes\": 1, \"hypertension\": 0, \"COPD\": 0, \"heart_disease\": 0, \"arthritis\": 0 } }\n"
      
    "Generate diverse records covering a range of ages, descriptions, genders, races, and health conditions."
)
NUM_OF_CALLS = 1

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

openai.api_key = OPENAI_API_KEY

def generate_text():
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": PROMPT}
        ],
        temperature=0.7
    )
    return response['choices'][0]['message']['content'].strip()

def parse_records(response):
    records = []
    # Ensure that the response is split into manageable parts
    for line in response.strip().split("\n"):
        if line.strip():  # Skip empty lines
            # try:
                record = json.loads(line)
                records.append(record)
            # except json.JSONDecodeError as e:
                # print(f"Skipping line due to invalid format: '{line}'")
                # print(f"Error: {e}")
    return records

def save_to_json(data, file_name):
    with open(file_name, mode="w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    data = []

    try:
        for i in range(NUM_OF_CALLS):
            response = generate_text()
            # Print response for debugging
            print("API Response:", response)
            records = parse_records(response)
            data.extend(records)
            print(f"Completed API call {i + 1} of {NUM_OF_CALLS}")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Saving partial data to the JSON file...")

    finally:
        save_to_json(data, "data.json")
        print("Data saved to 'data.json'.")

import openai
import csv
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PROMPT = (
    "Generate 70 hypothetical patient records in CSV format. Each record should have a patient ID, age, gender, race, and 5 binary columns representing the presence (1) or absence (0) of comorbid conditions such as diabetes, hypertension, COPD, heart disease, and arthritis. "
    "Format each line exactly like this (without double quotes): "
    "PatientID,Age,Gender,Race,Diabetes,Hypertension,COPD,HeartDisease,Arthritis\n"
    "Example:\n"
    "1,65,F,white,1,0,1,0,1\n"
    "2,72,M,Black,0,1,0,1,0\n"
    "3,58,M,Asian,1,1,0,0,1\n"
)
NUM_OF_CALLS = 1

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

openai.api_key = OPENAI_API_KEY

def generate_text():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": PROMPT}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_to_csv(data, file_name):
    with open(file_name, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["PatientID", "Age", "Gender", "Race", "Diabetes", "Hypertension", "COPD", "HeartDisease", "Arthritis"])
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    data = []

    try:
        for i in range(NUM_OF_CALLS):
            response = generate_text()
            lines = response.split("\n")
            for line in lines:
                if line:
                    try:
                        parts = line.split(",")
                        if len(parts) == 9:
                            patient_id, age, gender, race, diabetes, hypertension, copd, heart_disease, arthritis = parts
                            data.append((patient_id.strip(), age.strip(), gender.strip(), race.strip(), int(diabetes.strip()), int(hypertension.strip()), int(copd.strip()), int(heart_disease.strip()), int(arthritis.strip())))
                        else:
                            print(f"Skipping line due to invalid format: '{line}'")
                    except ValueError:
                        print(f"Skipping line due to invalid format: '{line}'")
            print(f"Completed API call {i + 1} of {NUM_OF_CALLS}")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt detected. Saving partial data to the CSV file...")

    finally:
        save_to_csv(data, "comorbidity_dataset.csv")
        print("Data saved to 'comorbidity_dataset.csv'.")

from flask import Flask, render_template, request
import os
import json
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError

load_dotenv()
app = Flask(__name__)

def extract_portfolio_data(resume_text):
    """Sends the resume text to Gemini API and retrieves structured JSON."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing.")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an accurate resume parser. Convert the resume text provided below into structured JSON for a portfolio webpage.
    
    STRICT RULES:
    1. Extract information ONLY from the provided text.
    2. Do NOT invent, assume, or hallucinate skills, projects, companies, dates, or contact info.
    3. If any field or section is missing from the resume, return an empty array [] or empty string "".
    4. Provide the output in strictly valid JSON format.

    JSON Schema Structure:
    {{
      "name": "Full Name",
      "headline": "Short Professional Title / Headline",
      "summary": "Concise factual summary",
      "contact": [
        {{"type": "Email/LinkedIn/GitHub/Phone", "value": "details", "url": "URL if applicable or empty string"}}
      ],
      "skills": ["Skill 1", "Skill 2"],
      "experience": [
        {{
          "role": "Job Title",
          "company": "Company Name",
          "duration": "Dates/Duration",
          "responsibilities": ["Task or achievement"]
        }}
      ],
      "projects": [
        {{
          "title": "Project Name",
          "description": "Brief description",
          "technologies": ["Tech1", "Tech2"]
        }}
      ],
      "education": [
        {{
          "degree": "Degree / Course",
          "institution": "School / University",
          "year": "Graduation year or date"
        }}
      ],
      "achievements": [
        "Award, certification, or key accomplishment"
      ]
    }}

    Resume Content:
    \"\"\"
    {resume_text}
    \"\"\"
    """

    print("Contacting Gemini API...")
    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    parsed_json = json.loads(response.text)
    return parsed_json

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # 1. Check if a file was uploaded
        if 'resume_file' not in request.files:
            return "No file uploaded."
            
        uploaded_file = request.files['resume_file']
        
        # 2. Check if the file is empty or not a .txt file
        if uploaded_file.filename == '':
            return "No file selected."
            
        if not uploaded_file.filename.endswith('.txt'):
            return "Error: Please upload a .txt file."

        # 3. Read the text from the uploaded file
        try:
            resume_text = uploaded_file.read().decode('utf-8')
            
            if len(resume_text) < 50:
                return "Error: Resume file is empty or too short."
                
            # 4. Send to Gemini and render the portfolio
            portfolio_data = extract_portfolio_data(resume_text)
            
            # --- THE FIX ---
            if isinstance(portfolio_data, list):
                if len(portfolio_data) > 0:
                    portfolio_data = portfolio_data[0]
                else:
                    return "Error: The AI returned an empty list."
            # ---------------
            
            return render_template("template.html", **portfolio_data)
            
        except Exception as e:
            return f"An error occurred: {str(e)}"
            
    # If it's a GET request, just show the upload form
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
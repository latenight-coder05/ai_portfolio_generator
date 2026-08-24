# AI-Assisted Resume-to-Portfolio Generator

## 📌 Project Overview
This project is a Python-based Command Line Interface (CLI) application that automatically transforms a plain-text resume into a styled, professional HTML portfolio webpage. It uses the **Google Gemini API** to intelligently extract and structure the unstructured text into valid JSON format, which is then dynamically injected into an HTML template using **Jinja2**.

This project was built as a group submission to demonstrate API integration, JSON parsing, prompt engineering, and responsible AI practices.

---

## 🛠️ Technology Stack
- **Python 3.9+**: Core application logic and file handling.
- **Google Gemini API (`gemini-2.5-flash`)**: AI model used to extract and parse text into structured JSON.
- **JSON**: Data interchange format bridging the AI output and HTML template.
- **Jinja2**: Python templating engine used to generate the final HTML.
- **HTML5 & CSS3**: Structure and styling for the final `portfolio.html` output.

---

## 🚀 Setup & Installation Guide

Follow these steps to run the project on your local machine.

### 1. Clone the Repository
Download the project files to your local system:
```bash
git clone <your-github-repo-url>
cd resume-portfolio-generator
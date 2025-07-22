from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  
import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

app = Flask(__name__)
CORS(app)

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        print("Incoming form keys:", request.form)
        print("Incoming file keys:", request.files)
        resume_file = request.files.get("resume")
        job_role = request.form.get("job_role")

        if not resume_file or not job_role:
            return jsonify({"error": "Missing resume or job role"}), 400

        doc = fitz.open(stream=resume_file.read(), filetype="pdf")
        resume_text = ""
        for page in doc:
            resume_text += page.get_text()

        prompt = f"""
You are an expert interview coach.

The candidate has applied for the role of {job_role}.
Based on their resume provided below, generate 10 interview questions, clearly categorized into:

Technical Questions (1–5)

Behavioral Questions (6–10)

Each question should follow this format:

Question Title: Full question.
(Brief explanation of what this question assesses.)

--- RESUME ---
{resume_text}
Output Requirements:

Do NOT use any markdown formatting.

Do NOT use asterisks, hashtags, or underscores.

Add a blank line between each question.

Add a blank line between the Technical and Behavioral sections.

The response must be cleanly formatted, human-readable, and well-spaced.

If no file is provided, generate general questions based on {job_role} with a suggestion:
(Send resume as well for tailored questions).

If no {job_role} is provided, generate questions based on projects and skills in {resume_text}

Example Output:

Technical Questions

1.REST API Design: Can you explain how you would design a scalable RESTful API for an e-commerce platform?
(Assesses understanding of API principles, scalability, and best practices.)

2.React Performance Optimization: What steps would you take to improve the performance of a large React application?
(Assesses ability to analyze and optimize front-end performance.)

3.Database Selection: Given a high-traffic analytics dashboard, would you choose SQL or NoSQL and why?
(Evaluates decision-making and database architecture knowledge.)

4.Version Control Conflict: How do you resolve complex merge conflicts in Git when working on a shared codebase?
(Checks familiarity with version control systems and collaboration.)

5.Authentication Flow: Walk me through how you would implement a secure login system using JWT.
(Assesses backend security knowledge and implementation experience.)

Behavioral Questions

1.Team Collaboration: Tell me about a time when you worked closely with a team member who had a very different communication style. How did you ensure the project stayed on track?
(Assesses teamwork, adaptability, and communication.)

2.Handling Failure: Describe a situation where a project you were responsible for did not go as planned. What did you learn?
(Evaluates accountability, learning from failure, and resilience.)

3.Prioritization Skills: When multiple tasks compete for your attention, how do you prioritize?
(Assesses time management and strategic thinking.)

4.Feedback Reception: Give an example of how you handled constructive criticism and used it to improve your performance.
(Evaluates openness to feedback and self-improvement.)

5.Initiative: Tell me about a time you proactively identified a problem in a project and solved it without being asked.
(Assesses initiative, problem-solving, and leadership potential.)"""

        response = model.generate_content(prompt)
        formatted_response = response.text.strip()

        return jsonify({"questions": formatted_response})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Error processing resume and generating questions."}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)

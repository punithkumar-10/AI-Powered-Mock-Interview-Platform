import os
import io
import base64
import speech_recognition as sr
from gtts import gTTS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from config import GOOGLE_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def generate_interview_questions(job_role, job_description, interview_type):
    prompt_template = """
You are an expert interviewer. Based on the following job role, job description, and interview type, generate 5 tailored interview questions that assess a candidate's fit for the role.

Job Role: {job_role}
Job Description: {job_description}
Interview Type: {interview_type}

Provide the questions as a numbered list.
"""
    prompt = PromptTemplate(
        input_variables=["job_role", "job_description", "interview_type"],
        template=prompt_template
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    questions_output = chain.run(
        job_role=job_role,
        job_description=job_description,
        interview_type=interview_type
    )
    questions = [line.strip() for line in questions_output.split("\n")
                 if line.strip() and line.strip()[0].isdigit()]
    return questions

def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
    try:
        text = r.recognize_google(audio)
        return text
    except Exception as e:
        return f"Error recognizing speech: {e}"

def generate_feedback(transcript):
    feedback_prompt = """
You are an expert interviewer. Please review the following interview transcript and provide detailed feedback including:
- Strengths in the candidate's responses,
- Areas for improvement,
- Overall suggestions for interview improvement,
- An overall score out of 10.

Interview Transcript:
{transcript}

Provide your response in a clear, structured format.
"""
    prompt = PromptTemplate(
        input_variables=["transcript"],
        template=feedback_prompt
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    feedback = chain.run(transcript=transcript)
    return feedback
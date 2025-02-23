from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import List, Optional

# --- API Key Verification ---
VALID_API_KEY = "AIzaSyBgHX0SOzFsv6O4p-gxeoM-FCGTpcuTHmY"

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

# --- FastAPI App Initialization ---
app = FastAPI(title="Gemini API Service")

# --- Data Models ---
class InterviewDetails(BaseModel):
    job_role: str
    interview_type: str
    job_description: str
    additional_details: str = ""
    years_experience: int

class FeedbackRequest(BaseModel):
    interview_details: InterviewDetails
    answers: List[str]

# --- Endpoints ---
@app.post("/generate", dependencies=[Depends(verify_api_key)])
async def generate_interview(interview_details: InterviewDetails):
    """
    Generate interview questions based on provided interview details.
    """
    questions = [
        f"Can you elaborate on your experience as a {interview_details.job_role}?",
        "What is your approach to problem-solving?",
        "Describe a challenging work situation and how you overcame it.",
        "How do you manage multiple priorities?",
        "Where do you see yourself in five years?"
    ]
    return {"questions": questions}

@app.post("/feedback", dependencies=[Depends(verify_api_key)])
async def provide_feedback(feedback_request: FeedbackRequest):
    """
    Provide feedback on the candidate's interview answers.
    """
    overall_score = 8  # simulated score
    detailed_feedback = {str(i): f"Feedback for answer {i+1}" for i in range(len(feedback_request.answers))}
    return {"overall_score": overall_score, "detailed_feedback": detailed_feedback}

# --- Run the App ---
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

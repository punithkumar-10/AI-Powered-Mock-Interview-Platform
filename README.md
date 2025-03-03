# AI Mock Interview Platform

## 📌 Description
The AI Mock Interview Platform is an intelligent interview simulation tool that helps candidates practice and improve their interviewing skills. It generates tailored interview questions based on the user's job role and experience, records and transcribes responses, and provides AI-powered feedback.

## 🚀 Features
- **AI-Powered Interview Questions**: Generates dynamic, role-specific questions.
- **Speech Recognition**: Converts spoken answers to text.
- **Text-to-Speech (TTS)**: Reads out interview questions.
- **Real-Time Audio & Video Capture**: Supports camera and microphone input.
- **AI Feedback Analysis**: Evaluates responses and provides improvement suggestions.
- **Streamlit-Based UI**: User-friendly web interface.
- **Firebase Integration**: Stores candidate details securely.
- **Clerk Authentication**: Ensures secure user login and session handling.

---

🎥 **Demo1 Video:** [Click here to watch](https://github.com/user-attachments/assets/c1d51377-d5c9-4701-bb9f-8f50d93428f7)

🎥 **Demo2 Video:** [Click here to watch](https://github.com/user-attachments/assets/7dd5c9ed-0528-4c1c-9488-c8aa85bcc550)

## 🛠 Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/punithkumar-10/AI-Powered-Mock-Interview-Platform
   cd AI-Powered-Mock-Interview-Platform
   ```
2. **Create a Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On MacOS/Linux
   venv\Scripts\activate  # On Windows
   ```
3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set Up API Keys**
   - Replace the `GOOGLE_API_KEY` in `config.py` with your actual API key.
   
5. **Run the Application**
   ```bash
   streamlit run main.py
   ```

## 📂 Project Structure
```
├── main.py                # Landing page with navigation
pages
    ├── 1_Candidate_Details.py # Candidate details input form
    ├── 2_Interview.py         # Interview session with Q&A
├── utils.py               # Helper functions for LLM, Speech, and Feedback
├── config.py              # Configuration file for API keys
├── requirements.txt       # Dependencies list
└── README.md              # Documentation
```

## 🛠 Technologies Used
- **Streamlit**: For UI and user interaction.
- **Google Gemini API**: AI-based question generation and feedback.
- **SpeechRecognition & gTTS**: Audio processing.
- **LangChain**: Enables structured LLM-based processing for interview questions and feedback.

## 📞 Contact
For questions or contributions, contact **N PUNITH KUMAR**.


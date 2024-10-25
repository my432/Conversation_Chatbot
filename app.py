import os
import streamlit as st
from groq import Groq

# Set the Groq API key (for demo purposes; in production, avoid hardcoding it directly in the script)
os.environ["GROQ_API_KEY"] = "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"

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Arrays storing essay topics for each plan
essays_30_day_plan = [
    "Discuss a recent technological advancement and its impact on society.",
    "How does social media influence mental health in teenagers?",
    "The benefits of reading books in the digital age.",
    "Should homework be banned in schools?",
    "Impact of global warming on biodiversity.",
    # Add more topics up to 30 days
]

essays_45_day_plan = essays_30_day_plan + [
    "How can governments combat the rise of misinformation?",
    "The role of sports in character building.",
    # Add more topics up to 45 days
]

essays_60_day_plan = essays_45_day_plan + [
    "The importance of learning foreign languages in a globalized world.",
    "Should public transport be free for all citizens?",
    # Add more topics up to 60 days
]

# Function to get feedback from Groq API
def get_feedback(user_essay, level):
    # Define the system prompt for essay feedback
    system_prompt = """
    You are an experienced academic English instructor. You must provide feedback as an English teacher would, giving concise but effective advice to improve the student's writing. 
    Focus on specific, actionable feedback without lengthy explanations.

    For each error or area of improvement:
    1. Identify grammar or vocabulary mistakes by saying: "Replace 'X' with 'Y' (Type: Grammar/Vocabulary)".
    2. For cohesion, sentence structure, or other improvements, suggest: "Rephrase 'X' as 'Y' for better flow".
    3. Provide concise suggestions based on English proficiency levels (A1 to C1).
    4. Do not generate vague or lengthy answers; avoid unnecessary technical jargon.
    5. Limit feedback to 4-5 actionable points, focusing on the most important improvements.

    Essay Analysis Areas: Grammar, cohesion, sentence structure, vocabulary, and effective use of simple, compound, and complex sentences.
    """


    # Sending the essay and level to Groq API
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{system_prompt}\nEssay:\n{user_essay}\nLevel: {level}"
            }
        ],
        model="llama3-8b-8192"
    )
    
    # Extract feedback from API response
    feedback = response.choices[0].message.content
    return feedback

# Streamlit UI
st.title("Writing Assistant for IELTS/TOEFL/DET Preparation")

# Sidebar for selecting a plan
st.sidebar.title("Select Your Writing Plan")
plan = st.sidebar.radio("Choose a Plan", ("30 Days Plan", "45 Days Plan", "60 Days Plan"))

# Select the appropriate essay list based on the plan
if plan == "30 Days Plan":
    selected_plan_essays = essays_30_day_plan
elif plan == "45 Days Plan":
    selected_plan_essays = essays_45_day_plan
else:
    selected_plan_essays = essays_60_day_plan

# Dropdown to select the current day
st.subheader("Select your current day:")
current_day = st.selectbox("Choose the day:", list(range(1, len(selected_plan_essays) + 1)))

# Display the essay topic for the selected day
st.write(f"Day {current_day}: {selected_plan_essays[current_day - 1]}")

# Dropdown to show the upcoming essay topics
st.subheader("Upcoming essays:")
upcoming_essays = st.selectbox("Upcoming essay topics:", selected_plan_essays[current_day:])

# Textbox for the user to input their essay
user_essay = st.text_area("Write your essay here:", height=300)

# Dropdown to select proficiency level
level = st.selectbox("Select your proficiency level:", ["A1 (Beginner)", "A2 (Average)", "B1", "B2", "C1 (Advanced)"])

# Button to submit essay for feedback
if st.button("Submit for Feedback"):
    if user_essay.strip():
        st.write("Analyzing your essay...")

        # Get feedback using the get_feedback function
        feedback = get_feedback(user_essay, level)
        
        # Display the feedback provided by the model
        st.subheader("Feedback on your essay:")
        st.write(feedback)
    else:
        st.warning("Please write your essay before submitting!")

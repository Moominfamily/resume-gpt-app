
import streamlit as st
import openai
import docx2txt

st.set_page_config(page_title="Resume + Cover Letter Generator", layout="centered")

st.title("🎯 GPT Resume Optimizer + Cover Letter Generator")

# --- Sidebar API Key Input ---
st.sidebar.header("API Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
if api_key:
    openai.api_key = api_key

# --- Upload Resume ---
uploaded_file = st.file_uploader("Upload your resume (Word .docx file only)", type=["docx"])

# --- Job Description Input ---
st.subheader("Paste Job Description")
job_description = st.text_area("Include job title, responsibilities, and qualifications")

# --- Run GPT Analysis ---
if st.button("Generate Suggestions and Cover Letter"):
    if not uploaded_file or not job_description or not api_key:
        st.warning("Please upload resume, enter job description, and provide API key.")
    else:
        resume_text = docx2txt.process(uploaded_file)

        with st.spinner("Analyzing and generating content with GPT-4o..."):
            messages = [
                {"role": "system", "content": "You are an expert career coach helping job applicants optimize resumes and write tailored cover letters."},
                {"role": "user", "content": f"Here is the job description:\n\n{job_description}"}
{job_description}"},
                {"role": "user", "content": f"Here is my resume:

{resume_text}"},
                {"role": "user", "content": "Please provide: (1) suggestions to improve the resume to better match the job, and (2) a professional, tailored cover letter for this role."}
            ]
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.7,
                )
                output = response['choices'][0]['message']['content']
                st.success("✅ Analysis complete!")
                st.markdown("### ✏️ GPT Suggestions & Cover Letter")
                st.write(output)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

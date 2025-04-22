import streamlit as st
from openai import OpenAI
import docx2txt

st.set_page_config(page_title="Resume + Cover Letter Generator", layout="centered")

st.title("🎯 GPT Resume Optimizer + Cover Letter Generator")

# Sidebar
st.sidebar.header("Configuration 配置")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")
language = st.sidebar.radio("Select language / 选择语言", ["English", "中文"])

if api_key:
    client = OpenAI(api_key=api_key)

# Upload resume
resume_label = "Upload your resume (Word .docx file only)" if language == "English" else "上传简历（仅限 Word .docx）"
uploaded_file = st.file_uploader(resume_label, type=["docx"])

# Job description
desc_label = "Paste Job Description" if language == "English" else "粘贴职位描述"
desc_hint = "Include job title, responsibilities, and qualifications" if language == "English" else "包括职位名称、岗位职责和任职资格"
st.subheader(desc_label)
job_description = st.text_area(desc_hint)

# Process
button_label = "Generate Suggestions and Cover Letter" if language == "English" else "生成简历建议和求职信"
if st.button(button_label):
    if not uploaded_file or not job_description or not api_key:
        warn_msg = "Please upload resume, enter job description, and provide API key." if language == "English" else "请上传简历、输入职位信息，并填写 API key。"
        st.warning(warn_msg)
    else:
        resume_text = docx2txt.process(uploaded_file)

        if language == "English":
            messages = [
                {"role": "system", "content": "You are an expert career coach helping job applicants optimize resumes and write tailored cover letters."},
                {"role": "user", "content": f"Here is the job description:\n\n{job_description}"},
                {"role": "user", "content": f"Here is my resume:\n\n{resume_text}"},
                {"role": "user", "content": "Please provide: (1) suggestions to improve the resume to better match the job, and (2) a professional, tailored cover letter for this role."}
            ]
        else:
            messages = [
                {"role": "system", "content": "你是一位专业的职业顾问，擅长优化中文简历并撰写正式、得体的中文求职信。"},
                {"role": "user", "content": f"这是职位描述：\n\n{job_description}"},
                {"role": "user", "content": f"这是我的简历：\n\n{resume_text}"},
                {"role": "user", "content": "请提供：（1）简历优化建议，（2）正式、有针对性的中文求职信。"}
            ]

        with st.spinner("Generating..." if language == "English" else "正在生成..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    temperature=0.7,
                )
                result = response.choices[0].message.content
                st.success("✅ Done!" if language == "English" else "✅ 生成完成！")
                st.markdown("### ✏️ Suggestions and Cover Letter" if language == "English" else "### ✏️ 简历建议与求职信")
                st.write(result)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
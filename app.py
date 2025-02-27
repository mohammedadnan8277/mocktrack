import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adnan@8277"

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Connect to SQLite database
conn = sqlite3.connect("evaluations.db", check_same_thread=False)
c = conn.cursor()

# Create table if not exists
c.execute('''
    CREATE TABLE IF NOT EXISTS evaluations (
        trainer_name TEXT,
        student_name TEXT,
        student_roll_no TEXT,
        specialization TEXT,
        job_knowledge INTEGER,
        personality INTEGER,
        domain_knowledge INTEGER,
        interpersonal_skills INTEGER,
        attitude INTEGER,
        confidence INTEGER,
        communication INTEGER,
        business_acumen INTEGER,
        analytical_thinking INTEGER,
        leadership INTEGER,
        feedback TEXT,
        total_marks INTEGER,
        submitted_by TEXT,
        timestamp TEXT
    )
''')
conn.commit()

# Admin Login
def admin_login():
    st.title("🔑 Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login", use_container_width=True):
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")

# Admin Dashboard
def admin_dashboard():
    st.title("Admin Dashboard")
    evaluations = c.execute("SELECT * FROM evaluations").fetchall()

    if evaluations:
        df = pd.DataFrame(evaluations, columns=["Trainer Name", "Student Name", "Student Roll No", "Specialization", "Job Knowledge", "Personality", "Domain Knowledge", "Interpersonal Skills", "Attitude", "Confidence", "Communication", "Business Acumen", "Analytical Thinking", "Leadership", "Feedback", "Total Marks", "Submitted By", "Timestamp"])
        
        st.subheader("📋 Evaluation Summary")
        st.dataframe(df)

        total_students = 120  # Set actual total students count here
        completed_count = len(df)
        pending_count = max(total_students - completed_count, 0)

        col1, col2 = st.columns(2)
        col1.metric("✅ Completed Evaluations", completed_count)
        col2.metric("⏳ Pending Evaluations", pending_count)

        
        
        st.subheader("📥 Download Report")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(label="⬇️ Download CSV", data=csv, file_name="evaluation_report.csv", mime='text/csv', use_container_width=True)
        
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.info("ℹ️ No evaluations found in the database.")

# Trainer Evaluation Form
def trainer_form():
    st.title("MockTrack: Digital Interview Evaluation System")
    st.write("Streamline Mock Interviews with Seamless Digital Record-Keeping and Evaluation")

    students = {
        "2021ECE0101": {"name": "Bob Jones", "specialization": "ECE"},
        "2021CSE0102": {"name": "Frank Johnson", "specialization": "CSE"},
        "2021IT0103": {"name": "Jane Garcia", "specialization": "IT"},
        "2021CSBS0104": {"name": "Charlie Smith", "specialization": "CSBS"},
        "2021ECE0105": {"name": "Grace Smith", "specialization": "ECE"},
        "2021CSE0106": {"name": "Emma Harris", "specialization": "CSE"},
        "2021AI&DS0107": {"name": "Frank Miller", "specialization": "AI&DS"},
        "2021CSE0108": {"name": "Charlie Jones", "specialization": "CSE"},
        "2021CSE0109": {"name": "Bob Miller", "specialization": "CSE"},
        "2021CSE0110": {"name": "Emma Davis", "specialization": "CSE"},
        "2021CSBS0111": {"name": "Alice Brown", "specialization": "CSBS"},
        "2021CSBS0112": {"name": "Grace Davis", "specialization": "CSBS"},
        "2021CSE0113": {"name": "Jane Jones", "specialization": "CSE"},
        "2021AI&DS0114": {"name": "Grace Garcia", "specialization": "AI&DS"},
        "2021EEE0115": {"name": "Frank Harris", "specialization": "EEE"},
        "2021CSE0116": {"name": "Emma Miller", "specialization": "CSE"},
        "2021CSE0117": {"name": "Henry Harris", "specialization": "CSE"},
        "2021CSE0118": {"name": "David Brown", "specialization": "CSE"},
        "2021CSBS0119": {"name": "Emma Johnson", "specialization": "CSBS"},
        "2021ECE0120": {"name": "David Martinez", "specialization": "ECE"},
        "2021ECE0121": {"name": "Henry Brown", "specialization": "ECE"},
        "2021EEE0122": {"name": "Bob Johnson", "specialization": "EEE"},
        "2021CSE0123": {"name": "Frank Brown", "specialization": "CSE"},
        "2021CSBS0124": {"name": "Charlie Martinez", "specialization": "CSBS"},
        "2021CSE0125": {"name": "Jane Johnson", "specialization": "CSE"},
        "2021CSE0126": {"name": "Grace Harris", "specialization": "CSE"},
        "2021CSE0127": {"name": "Emma Williams", "specialization": "CSE"},
        "2021ECE0128": {"name": "Bob Williams", "specialization": "ECE"},
        "2021CSE0129": {"name": "Alice Smith", "specialization": "CSE"},
        "2021CSE0130": {"name": "Frank Jones", "specialization": "CSE"},
        "2021CSBS0131": {"name": "Emma Jones", "specialization": "CSBS"},
        "2021CSE0132": {"name": "John Davis", "specialization": "CSE"},
        "2021CSBS0133": {"name": "Jane Harris", "specialization": "CSBS"},
        "2021CSE0134": {"name": "Frank Smith", "specialization": "CSE"},
        "2021ECE0135": {"name": "Bob Johnson", "specialization": "ECE"},
        "2021CSBS0136": {"name": "Frank Miller", "specialization": "CSBS"},
        "2021CSE0137": {"name": "Emma Martinez", "specialization": "CSE"},
        "2021CSBS0138": {"name": "Bob Jones", "specialization": "CSBS"},
        "2021CSE0139": {"name": "David Garcia", "specialization": "CSE"},
        "2021IT0140": {"name": "John Harris", "specialization": "IT"},
        "2021CSE0141": {"name": "Bob Jones", "specialization": "CSE"},
        "2021CSE0142": {"name": "Frank Williams", "specialization": "CSE"},
        "2021CSE0143": {"name": "Alice Martinez", "specialization": "CSE"},
        "2021CSE0144": {"name": "Charlie Williams", "specialization": "CSE"},
        "2021CSE0145": {"name": "Emma Garcia", "specialization": "CSE"},
        "2021CSE0146": {"name": "Emma Garcia", "specialization": "CSE"},
        "2021CSBS0147": {"name": "Emma Miller", "specialization": "CSBS"},
        "2021ECE0148": {"name": "Frank Williams", "specialization": "ECE"},
        "2021CSE0149": {"name": "Charlie Brown", "specialization": "CSE"},
        "2021CSE0150": {"name": "Jane Johnson", "specialization": "CSE"},
        "2021CSE0151": {"name": "Emma Harris", "specialization": "CSE"},
        "2021CSE0152": {"name": "Alice Jones", "specialization": "CSE"},
        "2021CSE0153": {"name": "Grace Garcia", "specialization": "CSE"},
        "2021CSE0154": {"name": "Henry Miller", "specialization": "CSE"},
        "2021CSE0155": {"name": "Bob Jones", "specialization": "CSE"},
        "2021CSE0156": {"name": "Emma Miller", "specialization": "CSE"},
        "2021CSE0157": {"name": "Emma Davis", "specialization": "CSE"},
        "2021ECE0158": {"name": "Henry Martinez", "specialization": "ECE"},
        "2021CSE0159": {"name": "Emma Davis", "specialization": "CSE"},
        "2021IT0160": {"name": "David Smith", "specialization": "IT"},
        "2021IT0161": {"name": "Henry Harris", "specialization": "IT"},
        "2021CSBS0162": {"name": "David Johnson", "specialization": "CSBS"},
        "2021ECE0163": {"name": "Henry Smith", "specialization": "ECE"},
        "2021CSE0164": {"name": "Emma Davis", "specialization": "CSE"},
        "2021EEE0165": {"name": "Bob Garcia", "specialization": "EEE"},
        "2021CSE0166": {"name": "Jane Harris", "specialization": "CSE"},
        "2021CSE0167": {"name": "Charlie Smith", "specialization": "CSE"},
        "2021ECE0168": {"name": "Jane Martinez", "specialization": "ECE"},
        "2021ECE0169": {"name": "Jane Brown", "specialization": "ECE"},
        "2021CSE0170": {"name": "John Harris", "specialization": "CSE"},
        "2021ECE0171": {"name": "Alice Davis", "specialization": "ECE"},
        "2021ECE0172": {"name": "Bob Williams", "specialization": "ECE"},
        "2021EEE0173": {"name": "Grace Miller", "specialization": "EEE"},
        "2021ECE0174": {"name": "Alice Brown", "specialization": "ECE"},
        "2021ECE0175": {"name": "David Jones", "specialization": "ECE"},
        "2021CSE0176": {"name": "Henry Garcia", "specialization": "CSE"},
        "2021CSE0177": {"name": "Emma Brown", "specialization": "CSE"},
        "2021EEE0178": {"name": "Emma Harris", "specialization": "EEE"},
        "2021CSE0179": {"name": "David Miller", "specialization": "CSE"},
        "2021CSE0180": {"name": "Frank Garcia", "specialization": "CSE"},
        "2021CSBS0181": {"name": "Bob Davis", "specialization": "CSBS"},
        "2021ECE0182": {"name": "Charlie Davis", "specialization": "ECE"},
        "2021ECE0183": {"name": "Emma Miller", "specialization": "ECE"},
        "2021CSE0184": {"name": "John Jones", "specialization": "CSE"},
        "2021AI&DS0185": {"name": "John Smith", "specialization": "AI&DS"},
        "2021CSE0186": {"name": "Henry Davis", "specialization": "CSE"},
        "2021CSE0187": {"name": "Frank Garcia", "specialization": "CSE"},
        "2021CSE0188": {"name": "Bob Miller", "specialization": "CSE"},
        "2021CSE0189": {"name": "John Davis", "specialization": "CSE"},
        "2021ECE0190": {"name": "Grace Harris", "specialization": "ECE"},
        "2021ECE0191": {"name": "Henry Harris", "specialization": "ECE"},
        "2021CSE0192": {"name": "Jane Martinez", "specialization": "CSE"},
        "2021ECE0193": {"name": "Jane Harris", "specialization": "ECE"},
        "2021ECE0194": {"name": "David Davis", "specialization": "ECE"},
        "2021CSE0195": {"name": "Henry Smith", "specialization": "CSE"},
        "2021CSE0196": {"name": "Frank Davis", "specialization": "CSE"},
        "2021CSE0197": {"name": "Frank Jones", "specialization": "CSE"},
        "2021CSE0198": {"name": "Charlie Williams", "specialization": "CSE"},
        "2021ECE0199": {"name": "Jane Smith", "specialization": "ECE"},
        "2021CSE0200": {"name": "John Davis", "specialization": "CSE"},
        "2021CSE0201": {"name": "Grace Harris", "specialization": "CSE"},
        "2021EEE0202": {"name": "Emma Jones", "specialization": "EEE"},
        "2021IT0203": {"name": "Charlie Garcia", "specialization": "IT"},
        "2021CSE0204": {"name": "Bob Jones", "specialization": "CSE"},
        "2021IT0205": {"name": "David Davis", "specialization": "IT"},
        "2021CSE0206": {"name": "Grace Smith", "specialization": "CSE"},
        "2021CSE0207": {"name": "John Jones", "specialization": "CSE"},
        "2021AI&DS0208": {"name": "Jane Williams", "specialization": "AI&DS"},
        "2021CSBS0209": {"name": "John Garcia", "specialization": "CSBS"},
        "2021CSE0210": {"name": "John Williams", "specialization": "CSE"},
        "2021ECE0211": {"name": "Henry Garcia", "specialization": "ECE"},
        "2021ECE0212": {"name": "David Brown", "specialization": "ECE"},
        "2021ECE0213": {"name": "Alice Harris", "specialization": "ECE"},
        "2021EEE0214": {"name": "David Brown", "specialization": "EEE"},
        "2021CSBS0215": {"name": "Emma Williams", "specialization": "CSBS"},
        "2021CSE0216": {"name": "Jane Williams", "specialization": "CSE"},
        "2021AI&DS0217": {"name": "Jane Garcia", "specialization": "AI&DS"},
        "2021AI&DS0218": {"name": "Alice Jones", "specialization": "AI&DS"},
        "2021CSBS0219": {"name": "David Brown", "specialization": "CSBS"},
        "2021ECE0220": {"name": "Henry Garcia", "specialization": "ECE"}
    }

    trainers = [" Abdul ", "Zenob ", "Raj", "Ananth", "Viona", "Rajan ", "Paul ", "Arthi", "Kumar", "Sathish"]
    

    completed_students = [row[0] for row in c.execute("SELECT student_roll_no FROM evaluations").fetchall()]
    available_students = {k: v for k, v in students.items() if k not in completed_students}

    st.header("Evaluation Form")
    trainer_name = st.selectbox("Trainer Name:", trainers)
    student_roll_no = st.selectbox("Student Roll No:", list(available_students.keys()))
    student_name = available_students[student_roll_no]["name"]
    st.write(f"**Student Name:** {student_name}")
    specialization = available_students[student_roll_no]["specialization"]
    st.write(f"**Specialization:** {specialization}")
    

    st.subheader("Evaluation Criteria (Score Range: 1 to 10)")
    col1, col2 = st.columns(2)

    with col1:
        job_knowledge = st.number_input("1. Job Knowledge", min_value=1, max_value=10, value=1, step=1)
        personality = st.number_input("2. Personality", min_value=1, max_value=10, value=1, step=1)
        domain_knowledge = st.number_input("3. Domain Knowledge", min_value=1, max_value=10, value=1, step=1)
        interpersonal_skills = st.number_input("4. Interpersonal Skills", min_value=1, max_value=10, value=1, step=1)
        attitude = st.number_input("5. Attitude", min_value=1, max_value=10, value=1, step=1)

    with col2:
        confidence = st.number_input("6. Confidence", min_value=1, max_value=10, value=1, step=1)
        communication = st.number_input("7. Communication", min_value=1, max_value=10, value=1, step=1)
        business_acumen = st.number_input("8. Business Acumen", min_value=1, max_value=10, value=1, step=1)
        analytical_thinking = st.number_input("9. Analytical Thinking", min_value=1, max_value=10, value=1, step=1)
        leadership = st.number_input("10. Leadership", min_value=1, max_value=10, value=1, step=1)


    feedback = st.text_area("Interviewer Feedback / Comments:", height=150)

    # Enforcing word limit (100 to 500 words)
    if feedback:
        word_count = len(feedback.split())
        if word_count < 100:
            st.error("Feedback must be at least 100 words.")
        elif word_count > 500:
            st.error("Feedback must not exceed 500 words.")

    agree = st.checkbox("I confirm that the evaluation is accurate and complete.")
    
    if st.button("Submit Evaluation", disabled=not agree, use_container_width=True):
        total_marks = sum([job_knowledge, personality, domain_knowledge, interpersonal_skills, attitude, confidence, communication, business_acumen, analytical_thinking, leadership])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO evaluations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (trainer_name, student_name, student_roll_no, specialization, job_knowledge, personality, domain_knowledge, interpersonal_skills, attitude, confidence, communication, business_acumen, analytical_thinking, leadership, feedback, total_marks, trainer_name, timestamp))
        conn.commit()
        st.success("✅ Evaluation submitted successfully!")

if st.session_state.logged_in:
    admin_dashboard()
else:
    tab1, tab2 = st.tabs(["Trainer Evaluation", "Admin Login"])
    with tab1:
        trainer_form()
    with tab2:
        admin_login()

conn.close()

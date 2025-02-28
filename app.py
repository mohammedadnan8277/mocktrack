import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import time  # Import time for the progress bar

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "adnan@8277"

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Database Connection
conn = sqlite3.connect("evaluations.db", check_same_thread=False)
c = conn.cursor()

# Create tables if they do not exist
c.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_roll_no TEXT PRIMARY KEY,
        student_name TEXT,
        specialization TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS trainers (
        trainer_name TEXT PRIMARY KEY
    )
''')

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

# Admin Login Function
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

    if not st.session_state.logged_in:
        st.error("⛔ Access Denied. Please log in as an admin.")
        return

    # Upload Student List
    st.subheader("📄 Upload Student List")
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            required_columns = {"student_roll_no", "student_name", "specialization"}
            if required_columns.issubset(df.columns):
                c.execute("DELETE FROM students")  # Clear previous student data
                conn.commit()
                df.to_sql("students", conn, if_exists="append", index=False)
                st.success("✅ Students uploaded successfully!")

                # Display Preview of Uploaded Data
                st.subheader("👀 Student List Preview")
                st.dataframe(df)

                # Download Student List
                csv_data = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ Download Uploaded Student List",
                    data=csv_data,
                    file_name="uploaded_student_list.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            else:
                st.error(f"❌ CSV must contain columns: {', '.join(required_columns)}.")
        except Exception as e:
            st.error(f"⚠️ Error reading CSV: {e}")

    # Add Trainer
    st.subheader("👨‍🏫 Add Trainer")
    new_trainer = st.text_input("Enter Trainer Name")
    if st.button("Add Trainer", use_container_width=True):
        if new_trainer:
            try:
                c.execute("INSERT INTO trainers (trainer_name) VALUES (?)", (new_trainer,))
                conn.commit()
                st.success(f"✅ Trainer '{new_trainer}' added successfully!")
                st.rerun()
            except sqlite3.IntegrityError:
                st.error(f"❌ Trainer '{new_trainer}' already exists.")
        else:
            st.error("❌ Please enter a trainer name.")

    # Delete Trainer
    st.subheader("🗑️ Delete Trainer")
    trainers_df = pd.read_sql("SELECT * FROM trainers", conn)
    if not trainers_df.empty:
        selected_trainers = st.multiselect("Select trainers to delete", trainers_df["trainer_name"], key="delete_trainers")
        if selected_trainers and st.button("Delete Selected Trainers", use_container_width=True):
            c.executemany("DELETE FROM trainers WHERE trainer_name = ?", [(trainer,) for trainer in selected_trainers])
            conn.commit()
            st.success(f"✅ Deleted {len(selected_trainers)} trainers successfully!")
            st.rerun()
    else:
        st.info("ℹ️ No trainers found in the database.")

    # Fetch students and evaluations
    students_df = pd.read_sql("SELECT * FROM students", conn)
    evaluations_df = pd.read_sql("SELECT student_roll_no FROM evaluations", conn)

    if not students_df.empty:
        # Add Evaluation Status
        students_df["Evaluation Status"] = students_df["student_roll_no"].apply(
            lambda roll_no: "✅ Evaluated" if roll_no in evaluations_df["student_roll_no"].values else "⏳ Not Evaluated"
        )

        # Display Student List with Status
        st.subheader("📋 Student Evaluation Status")
        st.dataframe(students_df)
        
        # Multi-select delete with Select All option
        selected_students = st.multiselect("Select students to delete", students_df["student_roll_no"], key="delete_students")
        select_all = st.checkbox("Select All")
        
        if select_all:
            selected_students = students_df["student_roll_no"].tolist()

        if selected_students and st.button("🗑️ Delete Selected", use_container_width=True):
            c.executemany("DELETE FROM students WHERE student_roll_no = ?", [(roll_no,) for roll_no in selected_students])
            conn.commit()
            st.success(f"✅ Deleted {len(selected_students)} students successfully!")
            st.rerun()

        # Count Metrics
        total_students = len(students_df)
        completed_evaluations = len(evaluations_df)
        pending_evaluations = total_students - completed_evaluations

        # Display Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Total Students", total_students)
        col2.metric("✅ Evaluated", completed_evaluations)
        col3.metric("⏳ Pending", pending_evaluations)

    # Fetch and Display Evaluations
    evaluations = pd.read_sql("SELECT * FROM evaluations", conn)
    
    if not evaluations.empty:
        st.subheader("📊 Evaluation Summary")
        
        # Add date filter
        st.subheader("📅 Filter Evaluations by Date Range")
        col1, col2 = st.columns(2)
        with col1:
            from_date = st.date_input("From Date", value=pd.to_datetime(evaluations['timestamp']).min())
        with col2:
            to_date = st.date_input("To Date", value=pd.to_datetime(evaluations['timestamp']).max())
        
        # Filter evaluations based on date range
        evaluations['timestamp'] = pd.to_datetime(evaluations['timestamp'])
        filtered_evaluations = evaluations[(evaluations['timestamp'] >= pd.to_datetime(from_date)) & (evaluations['timestamp'] <= pd.to_datetime(to_date))]
        
        st.dataframe(filtered_evaluations)

        # Download Filtered Evaluation Report
        csv_eval = filtered_evaluations.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Download Evaluation Report",
            data=csv_eval,
            file_name="evaluation_report.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.info("ℹ️ No evaluations found in the database.")

    # Always Show Logout Button
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()
        
def trainer_form():
    st.title("MockTrack: Digital Interview Evaluation System")
    st.write("Streamline Mock Interviews with Seamless Digital Record-Keeping and Evaluation")

    # Initialize session state for form reset
    if "form_submitted" not in st.session_state:
        st.session_state.form_submitted = False

    # Fetch trainers from the database
    trainers_df = pd.read_sql("SELECT * FROM trainers", conn)
    trainers = trainers_df["trainer_name"].tolist()

    if not trainers:
        st.warning("No trainers available. Please add trainers from the admin panel.")
        return

    # Fetch students who haven't been evaluated
    c.execute("""
        SELECT s.student_roll_no, s.student_name, s.specialization 
        FROM students s 
        LEFT JOIN evaluations e ON s.student_roll_no = e.student_roll_no
        WHERE e.student_roll_no IS NULL
    """)
    available_students = c.fetchall()

    if not available_students:
        st.warning("All students have been evaluated. No students left for assessment.")
        return

    student_dict = {roll: {"name": name, "specialization": spec} for roll, name, spec in available_students}

    st.header("Evaluation Form")

    # Use session state to store form data
    if "trainer_name" not in st.session_state:
        st.session_state.trainer_name = trainers[0] if trainers else ""
    if "student_roll_no" not in st.session_state:
        st.session_state.student_roll_no = list(student_dict.keys())[0] if student_dict else ""

    trainer_name = st.selectbox("Trainer Name:", trainers, key="trainer_name")
    student_roll_no = st.selectbox("Student Roll No:", list(student_dict.keys()), key="student_roll_no")
    student_name = student_dict[student_roll_no]["name"]
    specialization = student_dict[student_roll_no]["specialization"]

    st.write(f"**Student Name:** {student_name}")
    st.write(f"**Specialization:** {specialization}")

    st.subheader("Evaluation Criteria (Score Range: 1 to 10)")
    col1, col2 = st.columns(2)

    with col1:
        job_knowledge = st.number_input("1. Job Knowledge", min_value=1, max_value=10, step=1, key="job_knowledge")
        personality = st.number_input("2. Personality", min_value=1, max_value=10, step=1, key="personality")
        domain_knowledge = st.number_input("3. Domain Knowledge", min_value=1, max_value=10, step=1, key="domain_knowledge")
        interpersonal_skills = st.number_input("4. Interpersonal Skills", min_value=1, max_value=10, step=1, key="interpersonal_skills")
        attitude = st.number_input("5. Attitude", min_value=1, max_value=10, step=1, key="attitude")

    with col2:
        confidence = st.number_input("6. Confidence", min_value=1, max_value=10, step=1, key="confidence")
        communication = st.number_input("7. Communication", min_value=1, max_value=10, step=1, key="communication")
        business_acumen = st.number_input("8. Business Acumen", min_value=1, max_value=10, step=1, key="business_acumen")
        analytical_thinking = st.number_input("9. Analytical Thinking", min_value=1, max_value=10, step=1, key="analytical_thinking")
        leadership = st.number_input("10. Leadership", min_value=1, max_value=10, step=1, key="leadership")

    # Feedback text area with a unique key
    feedback_key = f"feedback_{student_roll_no}"  # Unique key for each student
    feedback = st.text_area("Interviewer Feedback / Comments:", height=150, key=feedback_key)
    word_count = len(feedback.split())
    feedback_valid = 100 <= word_count <= 500

    if feedback and word_count < 100:
        st.error("Feedback must be at least 100 words.")
    elif feedback and word_count > 500:
        st.error("Feedback must not exceed 500 words.")

    agree = st.checkbox("I confirm that the evaluation is accurate and complete.", key="agree")
    submit_disabled = not (feedback_valid and agree)

    if st.button("Submit Evaluation", disabled=submit_disabled, use_container_width=True):
        total_marks = sum([
            job_knowledge, personality, domain_knowledge, interpersonal_skills,
            attitude, confidence, communication, business_acumen, analytical_thinking, leadership
        ])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Explicitly mention the correct column names
        c.execute("INSERT INTO evaluations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                  (trainer_name, student_name, student_roll_no, specialization, job_knowledge, personality, 
                   domain_knowledge, interpersonal_skills, attitude, confidence, communication, 
                   business_acumen, analytical_thinking, leadership, feedback, total_marks, 
                   trainer_name, timestamp))
        conn.commit()

        # 🎬 Unique Progress Animation
        with st.spinner("🔄 Evaluating responses..."):
            for i in range(5):
                time.sleep(0.3)

        st.success("✅ Evaluation submitted successfully!")
        
        st.session_state.form_submitted = True  # Trigger form reset

    # Reset form after submission
    if st.session_state.form_submitted:
        time.sleep(3)  # Wait for 3 seconds
        st.session_state.form_submitted = False  # Reset the flag
        st.rerun()  # Refresh the app using st.rerun()

if st.session_state.logged_in:
    admin_dashboard()
else:
    tab1, tab2 = st.tabs(["Trainer Evaluation", "Admin Login"])
    with tab1:
        trainer_form()
    with tab2:
        admin_login()

conn.close()

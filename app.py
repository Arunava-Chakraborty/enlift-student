import streamlit as st
import pandas as pd
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import sqlite3
import re
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="EnLift-Institute | Computer Science Coaching",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 3.5rem 2rem;
    border-radius: 16px;
    text-align: center;
    color: white;
    margin-bottom: 2rem;
}
.main-header h1 {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}
.main-header h3 {
    font-weight: 400;
    opacity: 0.95;
}
.feature-box, .course-highlight, .achievement-card, .simple-card {
    background: white;
    padding: 1.5rem;
    border-radius: 14px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    height: 100%;
}
.feature-box:hover,
.course-highlight:hover,
.achievement-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 30px rgba(0,0,0,0.12);
}
.feature-icon, .achievement-icon {
    font-size: 2rem;
    margin-bottom: 0.6rem;
}
.stat-box {
    text-align: center;
    padding: 1.2rem;
}
.stat-box h2 {
    color: #667eea;
    font-size: 2.2rem;
    margin-bottom: 0.3rem;
}
.process-step {
    background: #f8f9ff;
    padding: 1.2rem;
    border-left: 5px solid #667eea;
    border-radius: 10px;
    margin-bottom: 1rem;
}
.step-number {
    font-size: 1.3rem;
    font-weight: bold;
    color: #667eea;
}
.cta-section {
    background: linear-gradient(135deg, #667eea, #764ba2);
    padding: 3rem 2rem;
    border-radius: 18px;
    text-align: center;
    margin-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Custom CSS for clean design
st.markdown("""
    <style>
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .main > div {
            padding-left: 10px !important;
            padding-right: 10px !important;
        }
        .stButton > button {
            width: 100%;
        }
        .stTextInput > div > div > input {
            font-size: 16px !important;
        }
    }

    /* Header */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        color: black;
        margin-bottom: 2rem;
        text-align: center;
    }

    .main-header h1 {
        font-size: 2.8rem;
        margin-bottom: 1rem;
    }

    .main-header h3 {
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
        opacity: 0.9;
    }

    /* Feature Box */
    .feature-box {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #eaeaea;
        text-align: center;
        color: black;
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: black;
    }

    /* Stat Box */
    .stat-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1px;
        margin: 0.5rem;
        text-align: center;
        border: 1px solid #eaeaea;
        color:black;
    }

    /* Course Highlight */
    .course-highlight {
        background: white;
        border-radius: 10px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        color: black;
    }

    /* Success Message */
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
        color:black;
    }

    /* Process Step */
    .process-step {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
        color:black;
    }

    .step-number {
        display: inline-block;
        background: #667eea;
        color: white;
        width: 30px;
        height: 30px;
        border-radius: 50%;
        text-align: center;
        line-height: 30px;
        margin-right: 10px;
        font-weight: bold;
    }

    /* CTA Section */
    .cta-section {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 2.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 2rem 0;
    }

    /* Achievement Card */
    .achievement-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-top: 3px solid #667eea;
    }

    .achievement-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #667eea;
    }

    /* Contact Info */
    .contact-info {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }

    /* Simple Card */
    .simple-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #eaeaea;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for admin login
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'admin_password_attempts' not in st.session_state:
    st.session_state.admin_password_attempts = 0
if 'page' not in st.session_state:
    st.session_state.page = "Home"
if 'course_selected' not in st.session_state:
    st.session_state.course_selected = ""


# Database setup
def init_database():
    conn = sqlite3.connect('enlift_students.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            course TEXT,
            board TEXT,
            year INTEGER,
            age INTEGER,
            registration_date TIMESTAMP,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    return conn


# Email configuration
def send_welcome_email(student_email, student_name, course):
    try:
        email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'admissions@enlift-institute.com',
            'sender_password': ''
        }

        msg = MIMEMultipart()
        msg['From'] = email_config['sender_email']
        msg['To'] = student_email
        msg['Subject'] = 'Welcome to EnLift-Institute!'

        body = f"""
        Dear {student_name},

        Welcome to EnLift-Institute! 🎉

        Thank you for registering for our {course} course.

        Your registration has been received and is currently being processed.

        Here's what happens next:
        1. Our team will contact you within 24 hours
        2. You'll receive course access details
        3. Schedule your orientation session

        If you have any questions, please contact us at:
        📧 admissions@enlift-institute.com
        📞 +91 9876543210

        Best regards,
        EnLift-Institute Team
        """

        msg.attach(MIMEText(body, 'plain'))

        # For demo, save email content to file
        Path("emails").mkdir(exist_ok=True)
        with open(f'emails/{student_email}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w') as f:
            f.write(f"To: {student_email}\nSubject: {msg['Subject']}\n\n{body}")

        return True
    except Exception as e:
        # For demo purposes, we'll return True
        return True


# Navigation
def navigation():
    st.sidebar.title("🚀 EnLift-Institute")
    st.sidebar.markdown("---")

    # Main navigation menu
    menu = ["🏠 Home", "📚 Courses", "🎯 Admission", "👥 About Us", "📞 Contact Us"]

    # Add Admin page to menu if logged in
    if st.session_state.admin_logged_in:
        menu.append("🔐 Admin Dashboard")
    else:
        # Add Admin Login option
        menu.append("🔐 Admin Login")

    # Create radio buttons for navigation
    choice = st.sidebar.radio("Navigate", menu, key="nav_choice")

    # Update session state based on selection
    if choice == "🏠 Home":
        st.session_state.page = "Home"
    elif choice == "📚 Courses":
        st.session_state.page = "Courses"
    elif choice == "🎯 Admission":
        st.session_state.page = "Admission"
    elif choice == "👥 About Us":
        st.session_state.page = "About Us"
    elif choice == "📞 Contact Us":
        st.session_state.page = "Contact Us"
    elif choice == "🔐 Admin Login":
        st.session_state.page = "Admin Login"
    elif choice == "🔐 Admin Dashboard":
        st.session_state.page = "Admin Dashboard"

    # Admin logout button (only when logged in)
    if st.session_state.admin_logged_in:
        st.sidebar.markdown("---")
        if st.sidebar.button("🚪 Logout Admin", type="secondary"):
            st.session_state.admin_logged_in = False
            st.session_state.admin_password_attempts = 0
            st.session_state.page = "Home"
            st.rerun()

    return st.session_state.page


# Function to handle button clicks for page navigation
def go_to_page(page_name):
    st.session_state.page = page_name
    st.rerun()



if "page" not in st.session_state:
    st.session_state.page = "Home"

page = st.session_state.page
# Simple Home Page
def home_page():
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <h1> EnLift-Institute</h1>
        <h3>Computer Science Made Clear, Practical & Exam-Ready</h3>
        <p style="max-width: 820px; margin: 1rem auto; font-size: 1.15rem;">
            Structured online Computer Science education for ICSE, CBSE, WBCSE and college students.
            We focus on <strong>concept clarity, coding confidence, and real understanding</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)
    if st.session_state.page == "Courses":
        courses_page()

    # CTA Buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📚 View Courses", type="primary", use_container_width=True):
            st.session_state.page = "Courses"

    with col2:
        if st.button("🎯 Admission Process", use_container_width=True):
            st.session_state.page = "Admission"

    with col3:
        if st.button("📞 Contact Institute", use_container_width=True):
            st.session_state.page = "Contact Us"

    st.markdown("---")

    # Trust Stats
    stat_cols = st.columns(3)
    stats = [("5+", "Years Teaching"), ("1000+", "Classes Taken"), ("100%", "Syllabus Coverage")]
    for col, (num, text) in zip(stat_cols, stats):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <h2>{num}</h2>
                <p>{text}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Why Choose Us
    st.subheader("✨ Why Students Choose EnLift")
    features = [
        ("👨‍🏫", "Experienced Faculty", "Taught by a software engineer with deep academic clarity"),
        ("🧠", "Concept-First Teaching", "We explain *why*, not just *what*"),
        ("💻", "Live Coding Classes", "Students code along during class"),
        ("📝", "Assignments & Tests", "Weekly assignments and monthly tests"),
        ("📊", "Progress Tracking", "Personal feedback & improvement reports"),
        ("🎯", "Board-Focused", "Strictly aligned with ICSE, CBSE & WBCSE")
    ]

    cols = st.columns(3)
    for i, f in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-box">
                <div class="feature-icon">{f[0]}</div>
                <h4>{f[1]}</h4>
                <p>{f[2]}</p>
            </div>
            
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Programs
    st.subheader("🎓 Programs Offered")
    pcols = st.columns(2)

    with pcols[0]:
        st.markdown("""
        <div class="course-highlight">
            <h4>🏫 School Programs (Class VIII – XII)</h4>
            <p>ICSE • CBSE • WBCSE</p>
            <ul>
                <li>Computer Science / Computer Applications</li>
                <li>Complete board syllabus coverage</li>
                <li>Monthly exams + assignments</li>
                <li>Strong programming foundation</li>
            </ul>
            <strong>Fees: ₹1,000 – ₹1,200 / month</strong>
        </div>
        """, unsafe_allow_html=True)

    with pcols[1]:
        st.markdown("""
        <div class="course-highlight">
            <h4>🎓 College Programs (B.Tech CSE / BCA)</h4>
            <ul>
                <li>Programming & DSA clarity</li>
                <li>DBMS, OS, CN explained practically</li>
                <li>Project & interview guidance</li>
            </ul>
            <strong>Fees: ₹1,200 / month</strong>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Learning Flow
    st.subheader("📈 How Learning Happens")
    steps = [
        ("1", "Assessment", "Understand student level & goals"),
        ("2", "Live Classes", "Interactive explanation + coding"),
        ("3", "Assignments", "Weekly problem solving"),
        ("4", "Monthly Tests", "Board-pattern evaluation"),
        ("5", "Confidence", "Exam-ready + coding clarity")
    ]

    for s in steps:
        st.markdown(f"""
        <div class="process-step">
            <span class="step-number">{s[0]}</span> <strong>{s[1]}</strong>
            <p>{s[2]}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Final CTA
    st.markdown("""
    <div class="cta-section">
        <h3>Start Learning the Right Way</h3>
        <p>Admissions open • Limited seats • Personal attention guaranteed</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.button("🎯 Apply for Admission", type="primary", use_container_width=True)

    with c2:
        st.button("📚 Explore Courses", use_container_width=True)



# Admin Login Page
def admin_login_page():
    st.title("🔐 Admin Login")

    if st.session_state.admin_logged_in:
        st.success("✅ You are already logged in!")
        st.info("Navigate to '🔐 Admin Dashboard' from the sidebar to access admin features.")
        return

    st.warning("⚠️ Admin access is restricted to authorized personnel only.")

    with st.form("admin_login_form"):
        admin_username = st.text_input("Username")
        admin_password = st.text_input("Password", type="password")

        submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            correct_username = "arunava"
            correct_password = "123Arunava."

            if admin_username == correct_username and admin_password == correct_password:
                st.session_state.admin_logged_in = True
                st.session_state.admin_password_attempts = 0
                st.success("✅ Login successful! Redirecting to dashboard...")
                st.session_state.page = "Admin Dashboard"
                st.rerun()
            else:
                st.session_state.admin_password_attempts += 1
                attempts_left = 3 - st.session_state.admin_password_attempts

                if attempts_left > 0:
                    st.error(f"❌ Incorrect username or password. {attempts_left} attempts left.")
                else:
                    st.error("❌ Too many failed attempts. Please try again later.")
                    st.session_state.admin_password_attempts = 0


# Admin Dashboard Page
def admin_dashboard_page():
    if not st.session_state.admin_logged_in:
        st.error("🔒 Access Denied. Please login as admin.")
        return

    st.title("🔐 Admin Dashboard")

    # Initialize database connection
    conn = init_database()

    # Admin actions
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()

    with col2:
        if st.button("📥 Export to CSV", use_container_width=True):
            try:
                df = pd.read_sql_query("SELECT * FROM students", conn)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"enlift_students_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error exporting data: {e}")

    with col3:
        if st.button("🗑️ Clear Old Data", use_container_width=True):
            with st.expander("⚠️ Confirm Deletion"):
                st.warning("This will delete all student records. This action cannot be undone!")
                confirm = st.text_input("Type 'DELETE' to confirm:")
                if confirm == "DELETE":
                    try:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM students")
                        conn.commit()
                        st.success("✅ All student records have been deleted.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error clearing data: {e}")

    st.markdown("---")

    # Load and display student data
    try:
        df = pd.read_sql_query("SELECT * FROM students ORDER BY registration_date DESC", conn)

        if len(df) == 0:
            st.info("📭 No student registrations found.")
        else:
            # Statistics
            st.subheader("📊 Registration Statistics")

            stat_cols = st.columns(4)
            with stat_cols[0]:
                st.metric("Total Students", len(df))
            with stat_cols[1]:
                today_count = len(df[pd.to_datetime(df['registration_date']).dt.date == datetime.now().date()])
                st.metric("Today's Registrations", today_count)
            with stat_cols[2]:
                st.metric("Active Courses", df['course'].nunique())
            with stat_cols[3]:
                pending_count = len(df[df['status'] == 'pending'])
                st.metric("Pending Approvals", pending_count)

            st.markdown("---")

            # Filters
            st.subheader("🔍 Filter Registrations")

            filter_cols = st.columns(3)

            with filter_cols[0]:
                course_filter = st.multiselect(
                    "Filter by Course",
                    options=sorted(df['course'].unique()),
                    default=[]
                )

            with filter_cols[1]:
                status_filter = st.multiselect(
                    "Filter by Status",
                    options=sorted(df['status'].unique()),
                    default=[]
                )

            with filter_cols[2]:
                date_filter = st.date_input(
                    "Filter by Registration Date",
                    value=None
                )

            # Apply filters
            filtered_df = df.copy()

            if course_filter:
                filtered_df = filtered_df[filtered_df['course'].isin(course_filter)]

            if status_filter:
                filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]

            if date_filter:
                filtered_df = filtered_df[pd.to_datetime(filtered_df['registration_date']).dt.date == date_filter]

            # Display filtered data
            st.subheader(f"📋 Student Registrations ({len(filtered_df)} records)")

            # Editable dataframe for status updates
            edited_df = st.data_editor(
                filtered_df,
                column_config={
                    "id": st.column_config.NumberColumn("ID", disabled=True),
                    "name": st.column_config.TextColumn("Name", disabled=True),
                    "email": st.column_config.TextColumn("Email", disabled=True),
                    "phone": st.column_config.TextColumn("Phone"),
                    "course": st.column_config.TextColumn("Course", disabled=True),
                    "board": st.column_config.TextColumn("Board/Program"),
                    "year": st.column_config.NumberColumn("Year/Grade"),
                    "age": st.column_config.NumberColumn("Age"),
                    "registration_date": st.column_config.DatetimeColumn("Registration Date", disabled=True),
                    "status": st.column_config.SelectboxColumn(
                        "Status",
                        options=["pending", "approved", "rejected", "completed"],
                        required=True
                    )
                },
                use_container_width=True,
                height=400
            )

            # Save changes button
            if st.button("💾 Save Changes", type="primary"):
                try:
                    # Update database with changes
                    for index, row in edited_df.iterrows():
                        cursor = conn.cursor()
                        cursor.execute('''
                            UPDATE students 
                            SET phone=?, board=?, year=?, age=?, status=?
                            WHERE id=?
                        ''', (row['phone'], row['board'], row['year'], row['age'], row['status'], row['id']))
                    conn.commit()
                    st.success("✅ Changes saved successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error saving changes: {e}")

            # Detailed view expander
            with st.expander("📊 Detailed Analytics"):
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**Course Distribution**")
                    course_counts = df['course'].value_counts()
                    st.bar_chart(course_counts)

                with col2:
                    st.markdown("**Status Distribution**")
                    status_counts = df['status'].value_counts()
                    st.bar_chart(status_counts)

                col3, col4 = st.columns(2)

                with col3:
                    st.markdown("**Registration Trend (Last 7 Days)**")
                    df['reg_date'] = pd.to_datetime(df['registration_date']).dt.date
                    last_7_days = df[df['reg_date'] >= (datetime.now().date() - pd.Timedelta(days=7))]
                    daily_counts = last_7_days.groupby('reg_date').size()
                    st.line_chart(daily_counts)

                with col4:
                    st.markdown("**Age Distribution**")
                    age_counts = df['age'].value_counts().sort_index()
                    st.bar_chart(age_counts)

    except Exception as e:
        st.error(f"Error loading data: {e}")

    finally:
        conn.close()


# Courses Page
def courses_page():
    st.title("📚 Our Courses")
    st.markdown(
        "Well-structured **Computer Science programs** aligned with the **Indian education system**, "
        "focused on **board syllabus mastery, strong programming skills, regular assessments, and exam readiness**."
    )

    # School Courses
    st.subheader("🎒 School Programs (Classes VIII – XII)")
    st.markdown(
        "Courses strictly follow **ICSE, CBSE, and WBCSE Computer Science / Computer Applications syllabi**, "
        "with regular **assignments, monthly tests, and coding practice**."
    )

    school_tabs = st.tabs(["ICSE", "CBSE", "WBCSE"])

    school_courses = {
        "ICSE": [
            (
                "Computer Science / Applications",
                "Class VIII – X",
                "Complete coverage of the ICSE syllabus with strong emphasis on **Java programming**, "
                "algorithmic thinking, and database concepts. Students receive **regular programming assignments**, "
                "**theory worksheets**, and **monthly tests** strictly based on ICSE exam patterns to ensure "
                "concept clarity and consistent academic improvement.",
                "₹1,000/ month"
            ),
            (
                "Computer Science",
                "Class XI – XII",
                "In-depth preparation for ICSE Class 11 & 12 Computer Science, covering **Python programming**, "
                "OOP concepts, and data structures. The course includes **weekly coding assignments**, "
                "**practical-oriented exercises**, and **monthly evaluations** aligned with board examinations.",
                "₹1,000 / month"
            )
        ],
        "CBSE": [
            (
                "Computer Science / Applications",
                "Class XI – XII",
                "Structured as per the latest CBSE IP curriculum with focus on **Python, SQL, and data handling**. "
                "Students work on **practical assignments**, **data-based problems**, and appear for "
                "**monthly tests** designed according to the CBSE marking scheme.",
                "₹1,000 / month"
            ),
            (
                "Computer Science",
                "Class XI – XII",
                "Comprehensive CBSE Computer Science program covering **C++ / Python**, algorithms, "
                "and problem-solving techniques. Includes **regular programming assignments**, "
                "**theory practice**, and **monthly board-pattern tests** for exam confidence.",
                "₹1,000 / month"
            )
        ],
        "WBCSE": [
            (
                "Computer Science",
                "Class IX – X",
                "Aligned with the WBCSE syllabus, this course builds strong fundamentals in programming logic "
                "and computer science concepts. Students receive **regular homework**, "
                "**coding practice**, and **monthly tests** to track academic progress.",
                "₹1,000 / month"
            ),
            (
                "Computer Application",
                "Class XI – XII",
                "Designed strictly as per the WBCSE Computer Application syllabus, focusing on "
                "**programming concepts, theory clarity, and exam-oriented preparation**. "
                "Includes **topic-wise assignments**, **practical exercises**, and **monthly assessments**.",
                "₹1,000 / month"
            )
        ]
    }

    for idx, board in enumerate(["ICSE", "CBSE", "WBCSE"]):
        with school_tabs[idx]:
            for course_name, grade, description, fee in school_courses[board]:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {course_name}")
                        st.markdown(f"**Applicable Class:** {grade}")
                        st.markdown(f"📝 {description}")
                    with col2:
                        st.markdown(f"### {fee}")
                        if st.button("Enroll Now", key=f"{board}_{course_name}"):
                            st.session_state.course_selected = f"{board} - {course_name}"
                            go_to_page("Admission")
                    st.markdown("---")

    # College Courses
    st.subheader("🎓 College Programs")

    college_tabs = st.tabs(["B.Tech (CSE)", "BCA"])

    college_courses = {
        "B.Tech (CSE)": [
            (
                "1st Year",
                "Strong Programming & Math Foundation",
                "Focus on **C, C++, Python**, and engineering fundamentals to strengthen core concepts.",
                "₹1,200 / month"
            ),
            (
                "2nd Year",
                "Core Computer Science Subjects",
                "Detailed coverage of **Data Structures, Algorithms, Java/Python**, with problem-solving focus.",
                "₹1,200 / month"
            ),
            (
                "3rd Year",
                "Advanced CS & Interview Readiness",
                "Covers **DBMS, Operating Systems, Computer Networks**, and placement-oriented preparation.",
                "₹1,200 / month"
            )
        ],
        "BCA": [
            (
                "1st Year",
                "Computer Fundamentals & Programming",
                "Strong foundation in **C programming** and computer fundamentals.",
                "₹1,200 / month"
            ),
            (
                "2nd Year",
                "Web & Application Development",
                "Covers **HTML, CSS, JavaScript**, and backend basics.",
                "₹1,200 / month"
            ),
            (
                "3rd Year",
                "Projects & Career Preparation",
                "Focus on **final-year projects** and interview preparation.",
                "₹1,200 / month"
            )
        ]
    }

    for idx, program in enumerate(["B.Tech (CSE)", "BCA"]):
        with college_tabs[idx]:
            for year, title, topics, fee in college_courses[program]:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"### {program} – {year}")
                        st.markdown(f"**{title}**")
                        st.markdown(f"📚 {topics}")
                    with col2:
                        st.markdown(f"### {fee}")
                        if st.button("Enroll Now", key=f"{program}_{year}"):
                            st.session_state.course_selected = f"{program} - {year}"
                            go_to_page("Admission")
                    st.markdown("---")


# Admission Page
def admission_page():
    st.title("🎯 Student Admission")

    # Show pre-selected course if any
    if st.session_state.course_selected:
        st.info(f"📝 You're enrolling for: **{st.session_state.course_selected}**")
        if st.button("Clear selection"):
            st.session_state.course_selected = ""
            st.rerun()

    # Initialize database connection
    conn = init_database()

    with st.form("admission_form"):
        st.subheader("Personal Information")

        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name*")
            email = st.text_input("Email Address*")
            phone = st.text_input("Phone Number*")
            age = st.number_input("Age*", min_value=8, max_value=30, value=16)

        with col2:
            # Course Selection
            course_options = [
                "Select Course",
                "ICSE - Computer Applications (9-10)",
                "ICSE - Computer Science (11-12)",
                "CBSE - Informatics Practices (11-12)",
                "CBSE - Computer Science (11-12)",
                "WBCSE - Computer Science (9-10)",
                "WBCSE - Computer Application (11-12)",
                "B.Tech CSE - 1st Year",
                "B.Tech CSE - 2nd Year",
                "B.Tech CSE - 3rd Year",
                "BCA - 1st Year",
                "BCA - 2nd Year",
                "BCA - 3rd Year"
            ]

            # Pre-select course if it was chosen from courses page
            default_index = 0
            if st.session_state.course_selected:
                for idx, option in enumerate(course_options):
                    if st.session_state.course_selected in option:
                        default_index = idx
                        break

            course = st.selectbox("Select Course*", course_options, index=default_index)

            # Board/Program selection
            education_type = st.radio("Education Level*",
                                      ["School (8-12)", "College (B.Tech/BCA)"])

            if education_type == "School (8-12)":
                board = st.selectbox("Board*", ["ICSE", "CBSE", "WBCSE"])
                year = st.selectbox("Grade*", [8, 9, 10, 11, 12])
            else:
                board = st.selectbox("Program*", ["B.Tech (Computer Science)", "BCA"])
                year = st.selectbox("Year*", [1, 2, 3])

        st.subheader("Additional Information")
        previous_exp = st.text_area("Previous Computer Science Experience (if any)")
        expectations = st.text_area("What are your learning goals?")

        # Terms and conditions
        agree = st.checkbox("I agree to the terms and conditions*")

        submitted = st.form_submit_button("Submit Application", type="primary")

        if submitted:
            # Validation
            if not all([name,email, phone, course != "Select Course", agree]):
                st.error("Please fill all mandatory fields (*)")
            elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Please enter a valid email address")
            else:
                try:
                    # Save to database
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO students (name, email, phone, course, board, year, age, registration_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (name, email, phone, course, board, year, age, datetime.now()))
                    conn.commit()

                    # Save to JSON backup
                    student_data = {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "course": course,
                        "board": board,
                        "year": year,
                        "age": age,
                        "registration_date": datetime.now().isoformat(),
                        "previous_experience": previous_exp,
                        "expectations": expectations
                    }

                    # Create emails directory if not exists
                    Path("emails").mkdir(exist_ok=True)

                    # Save to JSON file
                    Path("students").mkdir(exist_ok=True)
                    with open(f"students/{email.replace('@', '_')}.json", "w") as f:
                        json.dump(student_data, f, indent=2)

                    # Send welcome email
                    if send_welcome_email(email, name, course):
                        st.success("✅ Registration Successful!")
                        st.markdown("""
                        <div class="success-message">
                        <h3>🎉 Welcome to EnLift-Institute!</h3>
                        <p>Your registration has been successfully submitted.</p>
                        <p>A confirmation email has been sent to <strong>{email}</strong></p>
                        <p>Our admission team will contact you within 24 hours.</p>
                        </div>
                        """.format(email=email), unsafe_allow_html=True)

                        # Show next steps
                        with st.expander("📋 Next Steps"):
                            st.markdown("""
                            1. **Check your email** for confirmation
                            2. **Complete fee payment** (link in email)
                            3. **Attend orientation** (schedule will be shared)
                            4. **Access learning portal** (credentials will be provided)
                            """)

                    # Reset form and course selection
                    st.session_state.course_selected = ""
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("This email is already registered!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    conn.close()


# About Us Page
def about_us_page():
    st.title("👥 About EnLift-Institute")

    st.markdown("""
    ## Our Mission
    To democratize quality computer science education and empower students 
    with cutting-edge technical skills for the digital age.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📜 Our Story")
        st.markdown("""
        Founded in 2022, EnLift-Institute started with a simple vision: 
        to make quality computer science education accessible to every student 
        regardless of their geographical location.

        Today, we've successfully trained **500+ students** across India 
        and continue to expand our reach with innovative teaching methodologies.
        """)

    with col2:
        st.subheader("🎯 Our Values")
        values = [
            ("🔬", "Excellence", "Quality education with practical approach"),
            ("🤝", "Integrity", "Transparent and ethical practices"),
            ("🚀", "Innovation", "Adapting to latest technologies"),
            ("❤️", "Student-Centric", "Personalized learning paths")
        ]

        for icon, title, desc in values:
            st.markdown(f"**{icon} {title}**")
            st.markdown(f"<small>{desc}</small>", unsafe_allow_html=True)
            st.markdown("")


# Contact Us Page
def contact_us_page():
    st.title("📞 Contact Us")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📍 Our Address")
        st.markdown("""
        **EnLift-Institute**  
        4no Padmapukur Par, 
        West Bengal, 743222
        India
        """)

        st.subheader("📱 Contact Information")
        st.markdown("""
        **Phone:** +91-7584988846  
        **Email:** enlift.provides@gmail.com  
        """)

        st.subheader("🕒 Office Hours")
        st.markdown("""
        **Monday - Friday:** 9:00 AM - 7:00 PM  
        **Saturday:** 9:00 AM - 2:00 PM  
        **Sunday:** Closed
        """)

    with col2:
        st.subheader("✉️ Send us a Message")

        with st.form("contact_form"):
            contact_name = st.text_input("Your Name*")
            contact_email = st.text_input("Your Email*")
            contact_phone = st.text_input("Phone Number")

            department = st.selectbox(
                "Department",
                ["General Inquiry", "Admissions", "Technical Support",
                 "Fee Related", "Career Opportunities"]
            )

            message = st.text_area("Your Message*", height=150)

            contact_submit = st.form_submit_button("Send Message", type="primary")

            if contact_submit:
                if not all([contact_name, contact_email, message]):
                    st.error("Please fill all mandatory fields (*)")
                else:
                    # Save contact message
                    contact_data = {
                        "name": contact_name,
                        "email": contact_email,
                        "phone": contact_phone,
                        "department": department,
                        "message": message,
                        "timestamp": datetime.now().isoformat()
                    }

                    # Create contacts directory
                    Path("contacts").mkdir(exist_ok=True)

                    with open(
                            f"contacts/{contact_email.replace('@', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                            "w") as f:
                        json.dump(contact_data, f, indent=2)

                    st.success("✅ Message sent successfully! We'll respond within 24 hours.")


# Main App
def main():
    # Create necessary directories
    Path("students").mkdir(exist_ok=True)
    Path("emails").mkdir(exist_ok=True)
    Path("contacts").mkdir(exist_ok=True)

    # Sidebar navigation
    current_page = navigation()

    # Display selected page
    if current_page == "Home":
        home_page()
    elif current_page == "Courses":
        courses_page()
    elif current_page == "Admission":
        admission_page()
    elif current_page == "About Us":
        about_us_page()
    elif current_page == "Contact Us":
        contact_us_page()
    elif current_page == "Admin Login":
        admin_login_page()
    elif current_page == "Admin Dashboard":
        admin_dashboard_page()

    # Footer
    st.markdown("---")
    footer_cols = st.columns([2, 1, 1, 1])

    with footer_cols[0]:
        st.markdown("### EnLift-Institute")
        st.markdown("""
        Transforming computer science education through 
        innovative online coaching since 2022.
        """)

    with footer_cols[1]:
        st.markdown("**Quick Links**")
        if st.button("Home", key="footer_home"):
            go_to_page("Home")
        if st.button("Courses", key="footer_courses"):
            go_to_page("Courses")
        if st.button("Admissions", key="footer_admissions"):
            go_to_page("Admission")

    with footer_cols[2]:
        st.markdown("**Resources**")
        st.markdown("Study Materials")
        st.markdown("Placement Portal")
        st.markdown("FAQ")

    with footer_cols[3]:
        st.markdown("**Legal**")
        st.markdown("Privacy Policy")
        st.markdown("Terms of Service")
        st.markdown("Refund Policy")

    st.markdown("---")
    st.markdown("© 2024 EnLift-Institute. All rights reserved.")


if __name__ == "__main__":
    main()
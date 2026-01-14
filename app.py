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

# Custom CSS for mobile responsiveness
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
            font-size: 16px !important; /* Prevents zoom on iOS */
        }
    }

    /* General styles */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .course-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        transition: transform 0.3s;
    }
    .course-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


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


# Email configuration (using Streamlit secrets for security)
def send_welcome_email(student_email, student_name, course):
    try:
        # In production, use st.secrets for email credentials
        # For demo, we'll simulate email sending
        email_config = {
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'sender_email': 'admissions@enlift-institute.com',  # Configure in Streamlit secrets
            'sender_password': ''  # Configure in Streamlit secrets
        }

        # Create message
        msg = MIMEMultipart()
        msg['From'] = email_config['sender_email']
        msg['To'] = student_email
        msg['Subject'] = 'Welcome to EnLift-Institute!'

        # Email body
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

        # Send email (commented for demo, uncomment with proper credentials)
        # server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
        # server.starttls()
        # server.login(email_config['sender_email'], email_config['sender_password'])
        # server.send_message(msg)
        # server.quit()

        # For demo, save email content to file
        with open(f'emails/{student_email}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt', 'w') as f:
            f.write(f"To: {student_email}\nSubject: {msg['Subject']}\n\n{body}")

        return True
    except Exception as e:
        st.error(f"Email configuration needed. Error: {str(e)}")
        # For demo purposes, we'll return True
        return True


# Navigation
def navigation():
    st.sidebar.title("🚀 EnLift-Institute")
    st.sidebar.markdown("---")
    menu = ["🏠 Home", "📚 Courses", "🎯 Admission", "👥 About Us", "📞 Contact Us"]
    choice = st.sidebar.radio("Navigate", menu)
    return choice


# Home Page
def home_page():
    st.markdown('<div class="header">', unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("EnLift-Institute")
        st.markdown("### Elevate Your Computer Science Journey")
        st.markdown("""
        Expert online coaching for:
        - School Students (8-12) - ICSE, CBSE, WBCSE
        - College Students (B.Tech/BCA 1st-3rd Year)
        """)
        st.button("🚀 Start Learning", type="primary")
    with col2:
        st.image("https://cdn.pixabay.com/photo/2017/10/10/21/47/laptop-2838921_1280.jpg",
                 caption="Learn Anytime, Anywhere")
    st.markdown('</div>', unsafe_allow_html=True)

    # Features
    st.subheader("🌟 Why Choose EnLift-Institute?")
    cols = st.columns(4)
    features = [
        ("👨‍🏫", "Expert Faculty", "Industry professionals"),
        ("📱", "Live Interactive Classes", "Real-time doubt solving and mentoring"),
        ("📚", "Structured Curriculum", "Board-specific & university-aligned content"),
        ("🎓", "Placement Assistance", "Career guidance and interview preparation")
    ]

    for idx, (icon, title, desc) in enumerate(features):
        with cols[idx]:
            st.markdown(f"### {icon}")
            st.markdown(f"**{title}**")
            st.markdown(f"<small>{desc}</small>", unsafe_allow_html=True)

    # Stats
    st.markdown("---")
    st.subheader("📊 Our Impact")
    stat_cols = st.columns(4)
    stats = [("500+", "Students Trained"), ("98%", "Pass Rate"), ("Online" , "1:1 Guidence"),("New-Age" , "Curriculum")]

    for idx, (number, label) in enumerate(stats):
        with stat_cols[idx]:
            st.markdown(f"## {number}")
            st.markdown(f"**{label}**")


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
                            st.switch_page("🎯 Admission")
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
                            st.switch_page("🎯 Admission")
                    st.markdown("---")




# Admission Page
def admission_page():
    st.title("🎯 Student Admission")

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

            course = st.selectbox("Select Course*", course_options)

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
            if not all([name, email, phone, course != "Select Course", agree]):
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

                    # Reset form
                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("This email is already registered!")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

    conn.close()

    # Display registration stats (admin view)
    if st.checkbox("Show Registration Stats (Admin)"):
        try:
            conn = init_database()
            df = pd.read_sql_query("SELECT * FROM students", conn)
            st.dataframe(df)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Students", len(df))
            with col2:
                st.metric("Today's Registrations",
                          len(df[pd.to_datetime(df['registration_date']).dt.date == datetime.now().date()]))
            with col3:
                st.metric("Active Courses", df['course'].nunique())
            conn.close()
        except:
            pass


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
    choice = navigation()

    # Display selected page
    if choice == "🏠 Home":
        home_page()
    elif choice == "📚 Courses":
        courses_page()
    elif choice == "🎯 Admission":
        admission_page()
    elif choice == "👥 About Us":
        about_us_page()
    elif choice == "📞 Contact Us":
        contact_us_page()

    # Footer
    st.markdown("---")
    footer_cols = st.columns([2, 1, 1, 1])

    with footer_cols[0]:
        st.markdown("### EnLift-Institute")
        st.markdown("""
        Transforming computer science education through 
        innovative online coaching since 2015.
        """)

    with footer_cols[1]:
        st.markdown("**Quick Links**")
        st.markdown("[Home](#)")
        st.markdown("[Courses](#)")
        st.markdown("[Admissions](#)")

    with footer_cols[2]:
        st.markdown("**Resources**")
        st.markdown("[Study Materials](#)")
        st.markdown("[Placement Portal](#)")
        st.markdown("[FAQ](#)")

    with footer_cols[3]:
        st.markdown("**Legal**")
        st.markdown("[Privacy Policy](#)")
        st.markdown("[Terms of Service](#)")
        st.markdown("[Refund Policy](#)")

    st.markdown("---")
    st.markdown("© 2024 EnLift-Institute. All rights reserved.")


if __name__ == "__main__":
    main()
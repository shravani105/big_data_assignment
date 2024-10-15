import streamlit as st
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB connection string
db = client['healthcare_db']
patients_collection = db['patients']

# Helper function to add a new patient
def add_patient(name, age, gender, contact, medical_history):
    patient_data = {
        'name': name,
        'age': age,
        'gender': gender,
        'contact': contact,
        'medical_history': medical_history,
    }
    patients_collection.insert_one(patient_data)
    st.success(f"Patient {name} added successfully!")

# Helper function to view patient records
def view_patients():
    patients = list(patients_collection.find())
    if patients:
        for patient in patients:
            st.write(f"**Name**: {patient['name']}")
            st.write(f"**Age**: {patient['age']}")
            st.write(f"**Gender**: {patient['gender']}")
            st.write(f"**Contact**: {patient['contact']}")
            st.write(f"**Medical History**: {patient['medical_history']}")
            st.write("---")
    else:
        st.info("No patients found.")

# Helper function to update patient information
def update_patient(name, new_contact, new_medical_history):
    query = {'name': name}
    new_values = {"$set": {'contact': new_contact, 'medical_history': new_medical_history}}
    result = patients_collection.update_one(query, new_values)
    
    if result.modified_count > 0:
        st.success(f"Patient {name}'s information updated!")
    else:
        st.warning(f"Patient {name} not found!")

# Helper function to schedule an appointment
def schedule_appointment(name, appointment_date):
    query = {'name': name}
    new_values = {"$set": {'appointment': appointment_date}}
    result = patients_collection.update_one(query, new_values)
    
    if result.modified_count > 0:
        st.success(f"Appointment scheduled for {name} on {appointment_date}!")
    else:
        st.warning(f"Patient {name} not found!")

# Streamlit UI
st.title("Patient Management System")

# Sidebar navigation
menu = ["Add Patient", "View Patients", "Update Patient", "Schedule Appointment"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Patient":
    st.subheader("Add New Patient")
    
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    contact = st.text_input("Contact Information")
    medical_history = st.text_area("Medical History")
    
    if st.button("Add Patient"):
        add_patient(name, age, gender, contact, medical_history)

elif choice == "View Patients":
    st.subheader("View All Patients")
    view_patients()

elif choice == "Update Patient":
    st.subheader("Update Patient Information")
    
    name = st.text_input("Enter Patient Name to Update")
    new_contact = st.text_input("New Contact Information")
    new_medical_history = st.text_area("New Medical History")
    
    if st.button("Update Information"):
        update_patient(name, new_contact, new_medical_history)

elif choice == "Schedule Appointment":
    st.subheader("Schedule Appointment for Patient")
    
    name = st.text_input("Enter Patient Name")
    appointment_date = st.date_input("Select Appointment Date")
    
    if st.button("Schedule Appointment"):
        schedule_appointment(name, str(appointment_date))

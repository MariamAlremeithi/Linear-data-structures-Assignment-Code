# Import necessary modules
import random
import queue
# This module creates the module unique Identifiers for the patient
import uuid


# Initialize the object with necessary attributes
class Patient:
    def __init__(self, name, insurance, medical_condition, current_condition):
        self.id = uuid.uuid4().hex[:6]  # Generate unique identifier for each patient
        self.name = name
        self.insurance = insurance
        self.medical_condition = medical_condition
        self.current_condition = current_condition
        self.selected_doctor = None
        self.appointment_details = None
        self.prescriptions = []
        self.consulted = False

    # Method to select doctor
    def select_doctor(self, doctor):
        self.selected_doctor = doctor

    # Method to set appointment details
    def set_appointment_details(self, appointment_details):
        self.appointment_details = appointment_details

    # Method to add prescription
    def add_prescription(self, prescription):
        self.prescriptions.append(prescription)

    @property
    def has_medical_condition(self):
        return self.medical_condition.lower() != "none"

    # Property to access patient information
    @property
    def patient_info(self):
        return {
            'id': self.id,
            'name': self.name,
            'insurance': self.insurance,
            'medical_condition': self.medical_condition,
            'current_condition': self.current_condition,
            'selected_doctor': self.selected_doctor,
            'appointment_details': self.appointment_details,
            'prescriptions': [prescription.name for prescription in self.prescriptions]
        }

    # Less-than method for the PriorityQueue
    def __lt__(self, other):
        return self.has_medical_condition < other.has_medical_condition


# Define the Prescription class
class Prescription:
    def __init__(self, name):
        self.name = name


# Define the Doctor class
class Doctor:
    def __init__(self, name, specialty):
        self.name = name
        self.specialty = specialty

    # Method to consult the patient
    def consult(self, patient):
        # Give prescription to the patient
        if patient.medical_condition:
            print(f"Patient {patient.id} has a medical condition. Doctor is consulting patient.")
            patient.add_prescription(Prescription("Consultation for medical condition"))
        else:
            current_prescription = prescriptions.pop(0)
            patient.add_prescription(current_prescription)
            # Store the given prescription in the stack
            prescription_stack.append(current_prescription)


# Define the Hospital class
class Hospital:
    def __init__(self):
        self.priority_patient_queue = queue.PriorityQueue()  # Use PriorityQueue for priority ordering
        self.normal_patient_queue = queue.Queue()  # Use Queue for FIFO ordering
        self.all_patients = []

    def add_patient_to_queue(self, patient):
        if patient.has_medical_condition:
            self.priority_patient_queue.put(patient)  # Add to priority queue if patient has a medical condition
        else:
            self.normal_patient_queue.put(patient)  # Add to normal queue if patient has no medical condition
            self.all_patients.append(patient)

    def search_patient(self, patient_id):
        # Search the priority queue
        while not self.priority_patient_queue.empty():
            patient = self.priority_patient_queue.get()
            if patient.id == patient_id:
                print("Patient Information:")
                print(patient.patient_info)
                return
            self.priority_patient_queue.put(patient)  # Put the patient back in the queue

        # Search the normal queue
        while not self.normal_patient_queue.empty():
            patient = self.normal_patient_queue.get()
            if patient.id == patient_id:
                print("Patient Information:")
                print(patient.patient_info)
                return
            self.normal_patient_queue.put(patient)  # Put the patient back in the queue

        print("Patient not found.")


# Initialize hospital
hospital = Hospital()

# Randomly generate patients
patients = []
for i in range(1, 16):
    name = "Patient " + str(i)
    insurance = "Insurance " + str(i)
    medical_condition = "Medical Condition " + str(i)
    current_condition = "Current Condition " + str(i)
    patients.append(Patient(name, insurance, medical_condition, current_condition))

# Initialize prescriptions
prescriptions = [Prescription("Prescription " + str(i)) for i in range(1, 16)]

# Create a stack for storing given prescriptions
prescription_stack = []

# Randomly select 2 patients
selected_patients = random.sample(patients, 2)

for patient in selected_patients:
    print(f"\nBooking in Patient {patient.id}:")
    patient.name = input("Please enter patient's name: ")
    patient.insurance = input("Please enter patient's insurance: ")
    patient.medical_condition = input("Please enter patient's medical condition if you dont have any type (none): ")
    patient.current_condition = input("Please enter patient's current condition: ")

    # Booking in process for department
    print("Which department would you like to book in?")
    print("1. General medicine ")
    print("2. Pediatric")
    print("3. Emergency ")
    department_choice = input("Enter your choice : ").strip()
    if department_choice not in ['1', '2', '3']:
        print("Invalid department choice. Transferring patient to another department.")
        continue

    # Booking appointment with doctor
    book_appointment = input("Would you like to book an appointment with available doctors? (yes/no): ").strip().lower()
    if book_appointment == "no":
        print("You need to book an appointment to see the doctors. Please say 'yes' to proceed.")
        book_appointment = input(
            "Would you like to book an appointment with available doctors? (yes/no): ").strip().lower()
    if book_appointment == "yes":
        print("Available doctors: Doctor 1, Doctor 2")
        while True:
            doctor_choice = input("Please enter the name of your preferred doctor: ").strip()
            if doctor_choice in ['Doctor 1', 'Doctor 2']:
                break  # Break out of the loop if the choice is valid
            else:
                print("Invalid doctor choice. Please choose either 'Doctor 1' or 'Doctor 2'.")
        # Select the chosen doctor for the patient
        patient.select_doctor(doctor_choice)
        appointment_details = input("Please enter the date and time of the appointment: ")
        # Set the appointment details for the patient
        patient.set_appointment_details(appointment_details)

        print(f"\nCurrent Patient Information for Patient {patient.id}:")
        # Prints the current patient information
        print(patient.patient_info)

    # Adds the patient to the hospital queue
    hospital.add_patient_to_queue(patient)

doctors = [Doctor("Doctor 1", "Family Medicine"), Doctor("Doctor 2", "Pediatrician")]

# Consult priority patients with doctors
while not hospital.priority_patient_queue.empty():
    patient = hospital.priority_patient_queue.get()
    if patient and not patient.consulted:  # Check if patient has been consulted
        for doctor in doctors:
            if patient.selected_doctor == doctor.name:
                print(f"\nConsulting Priority Patient {patient.id} with {doctor.name}...")
                doctor.consult(patient)
                print(f"Consultation for Priority Patient {patient.id} completed.")
                patient.consulted = True  # Set the flag to True after consultation

                # Prescriptions given from doctor
                prescriptions_input = input(
                    f"\nEnter prescriptions for Priority Patient {patient.id} (separated by comma): ")
                patient_prescriptions = [p.strip() for p in prescriptions_input.split(',')]
                for prescription in patient_prescriptions:
                    patient.add_prescription(Prescription(prescription))

                # Print updated patient info after consultation
                print(f"\nUpdated Patient Information for Priority Patient {patient.id}:")
                print(patient.patient_info)

# Consult normal patients with doctors
while not hospital.normal_patient_queue.empty():
    patient = hospital.normal_patient_queue.get()
    if patient and not patient.consulted:  # Check if patient has been consulted
        for doctor in doctors:
            if patient.selected_doctor == doctor.name:
                print(f"\nConsulting Normal Patient {patient.id} with {doctor.name}...")
                doctor.consult(patient)
                print(f"Consultation for Normal Patient {patient.id} completed.")
                patient.consulted = True  # Set the flag to True after consultation

                # Prescriptions given from doctor
                prescriptions_input = input(
                    f"\nEnter prescriptions for Normal Patient {patient.id} (separated by comma): ")
                patient_prescriptions = [p.strip() for p in prescriptions_input.split(',')]
                for prescription in patient_prescriptions:
                    patient.add_prescription(Prescription(prescription))

                # Print updated patient info after consultation
                print(f"\nUpdated Patient Information for Normal Patient {patient.id}:")
                print(patient.patient_info)


# Function for searching patients by ID
def search_patient_by_id(patients, patient_id):
    for patient in patients:
        if patient.id == patient_id:
            print("Patient Information:")
            print(patient.patient_info)
            return
    print("Patient not found!")


# Function for searching a specific patient
def search_patient(hospital, patients):
    patient_id = input(f"\nEnter patient ID to search for:")
    search_patient_by_id(patients, patient_id)


# Search for a patient
search_patient(hospital, patients)
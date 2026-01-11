# OpenBCI-Enabled Brain-Computer Interface (BCI) for Pediatric Neurorehabilitation

This project is an initiative by final-year engineering students at the **University of Moratuwa** to develop a Brain-Computer Interface (BCI) for children with severe motor impairments, such as **locked-in syndrome**. The system aims to restore communication and digital access by translating brain signals into commands, providing a lifeline for patients trapped in non-responsive bodies.

---

## Project Objectives

The mission is to develop a practical, EEG-based system through the following goals:

* **Develop an EEG-based BCI system**: Enabling children to control operating system interfaces using only brain signals.
* **Demonstrate proof-of-concept**: Validating usability through a real-world case study at **Lady Ridgeway Hospital**.
* **Build a scalable framework**: Creating a solution adaptable for patients with stroke, spinal cord injuries, or neurodegenerative diseases.
* **Contribute to academic knowledge**: Driving innovation through research publications.
---

## Current Progress & Technical Updates (January 2026)

As of early 2026, the project has transitioned from foundational planning to practical system validation and deployment readiness.

### Hardware & Headset Integration
* **Custom Headset Design**: Developed a ventilator-compatible headset that avoids structural parts near the chin and mouth. 
* **Mechanical Stability**: Features an elastic top and independent electrode positioning to ensure a secure fit for pediatric users.
* **Hardware Validation**: Confirmed the functionality of two out of three acquired Analog Front-End (AFE) PCBs and the '19 batch active electrode circuits.
* **Noise Mitigation**: Implemented mechanical stabilization of electrode mounts to reduce noise introduced by movement.

### Signal Processing & Firmware
* **Artifact Removal**: Successfully tested the **DeepIC Classifier**, a 51-layer pretrained DNN model, to separate clean EEG signals from artifacts.
* **Firmware Development**: Updated MCU firmware to support stable data acquisition from the **ADS1299** AFE and real-time data transmission.
* **Signal Visualization**: Integrated digital filters into the interface to balance noise reduction while preserving relevant EEG features.
* **Alpha Wave Detection**: Established a "Mid Evaluation Plan" to demonstrate alpha rhythm changes based on whether a user's eyes are open or closed.

### Ethics & Administration
* **Ethics Compliance**: Revised participant documentation to address reviewer feedback on data retention, post-trial support, and confidentiality.
* **Grant Support**: Received funding to procure high-resolution **OpenBCI Cyton** boards and **ThinkPulse™** active electrode kits.

---

## Technology: OpenBCI Hardware

The project utilizes the **OpenBCI** platform for high-quality neural signal acquisition.

![BCI Headset](../Project%20Images/Headset.jpeg)

* **High-Quality Precision**: Cyton boards capture detailed electrical signals, which is essential for accurate command interpretation.
* **Pediatric Suitability**: Ultracortex headsets are adjustable and comfortable for children.
* **Modularity**: The hardware architecture allows testing of multiple paradigms, including **SSVEP**, **P300**, and **Motor Imagery**.

---

## Project Team & Mentorship

**Final-Year Undergraduates (Group 21):**
* Chathura Nirmal Weerasinghe
* Jayamadu Gammune
* Dinujaya Wijewickrame
* Risini Dinara Kumarasinghe

**Guided by:**
* **Dr. Joshua Pranjeevan Kulasingham** (Main Supervisor)
* **Dr. Chamira Edussooriya** & **Dr. Peshala Jayasekara**
* **Prof. Jithangi Wanigasinghe** (Consultant Neurologist, LRH)
* **Mr. Kithimin Wickramsinghe** (MASc, UBC)

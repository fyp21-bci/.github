# PCB Documents for BrainNeoCare
This repository contains the PCB files for the Final Year Project "BrainNeoCare".

This FYP is a continuation of the 19th batch FYP. Therefore, the repository contains files from both FYP groups.

1. Libraries: Contains libraries used in the PCB designs
2. PCB_files_BrainNeoCare_24: Containes PCB files designed by the FYP team of batch 20
3. PCB_files_Nima_ayya: Containes PCB files designed by the FYP team of batch 19

## ECG Analog Front End
The ECG analog front end uses ADS1292 as the main IC. ECG signals are transmitted to the PCB using ECG electrodes. After processing, the digital signals are passed to the microcontroller unit via headers.

![image](https://github.com/user-attachments/assets/97b4fd13-1f2b-4085-9e67-14c4f6e9b0a1)

![image](https://github.com/user-attachments/assets/6c2b43ec-2c20-4fe4-b5c1-880354319244)

## EEG Analog Front End
The EEG analog front end uses ADS1299 as the main IC. EEG signals are transmitted to the PCB using flat electrodes. After processing, the digital signals are passed to the microcontroller unit via cables.

![image](https://github.com/user-attachments/assets/4d5e46e1-3a6d-416d-bdee-685b82e23e4a)

![image](https://github.com/user-attachments/assets/82971094-5981-417f-90c2-2178b9b07a8a)


## Microcontroller Unit
The received signals from both EEG and ECG analog front ends are wirelessly transmitted to the user computer for AI model usage and visualization

![image](https://github.com/user-attachments/assets/41068724-f751-4a83-a171-53ce124acacd)

![image](https://github.com/user-attachments/assets/32de70de-8507-4cd0-a6a2-ab9e8a1ad294)

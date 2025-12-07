# Phishing Simulation Design: Keylogger Delivery Vectors

**Date:** 07/12/2025
**Project Phase:** Phase 3 (Detection and Prevention)
[cite_start]**Task:** Week 10 - Designing Phishing Simulators [cite: 243, 290]

## 1. Objective
[cite_start]The goal of this simulation is to assess user awareness regarding social engineering tactics used to deliver malware[cite: 44]. Specifically, we aim to measure how easily a user might inadvertently download and execute the keylogger (`simple_logger.py`) believing it to be a legitimate file. [cite_start]The results will identify gaps in user training and reinforce vigilance[cite: 46].

## 2. Simulation Scenarios
[cite_start]We have designed two theoretical scenarios that mimic common attack vectors[cite: 45].

### Scenario A: The "Critical Security Update" (Fake Software Update)
* **Vector:** Email or Pop-up.
* **Pretext:** The user receives an urgent notification claiming their IT security software is outdated and requires an immediate manual patch to fix a vulnerability.
* **The Lure:** A button labeled "Download Security Patch v2.4".
* **The Payload:** Instead of a patch, the button triggers the download of a packaged version of our keylogger (e.g., renamed to `SecurityPatch_Installer.exe`).
* **User Action Required:** The user must download the file and bypass the "Unknown Publisher" warning to execute it.
* [cite_start]**Relevance:** This tests the effectiveness of the *Application Whitelisting* prevention strategy we tested in Week 9[cite: 124].

### Scenario B: Deceptive Login Page (Credential Harvesting)
* **Vector:** Email Link.
* **Pretext:** An email appearing to be from "Human Resources" regarding a mandatory policy update requiring a signature.
* **The Lure:** A link to `http://ted-university-portal-secure.com` (typosquatting domain).
* **The Payload:** The page hosts a "Sign-in" form. While this scenario typically steals credentials directly, in a keylogger context, the page could prompt the user to download a "Secure Document Viewer" to read the policy. This viewer is the keylogger.
* [cite_start]**Relevance:** Matches the project goal of understanding how attackers compromise systems[cite: 17].

## 3. Execution Flow (Theoretical)
1.  **Deployment:** A mock email campaign is sent to a test group (volunteers).
2.  **Tracking:**
    * **Metric 1 (Click Rate):** How many users clicked the malicious link?
    * **Metric 2 (Download Rate):** How many users downloaded the payload?
    * **Metric 3 (Execution Rate):** How many users attempted to run the file?
    * **Metric 4 (Report Rate):** How many users flagged the email as suspicious to IT?
3.  **Teachable Moment:** If a user runs the file, a safe pop-up appears: *"This was a simulation. In a real attack, your keystrokes would now be recorded. Please verify file signatures before running unknown applications."*

## 4. Defense & Mitigation
Based on this design, we recommend the following defenses to prevent keylogger delivery:
* [cite_start]**Technical:** Enforce strict **Software Restriction Policies** (Whitelisting) so users cannot run executables downloaded from the internet (e.g., from the `Downloads` folder)[cite: 125].
* [cite_start]**Behavioral:** Train users to inspect URL domains and verify "Urgent" requests through a secondary communication channel (e.g., calling the IT helpdesk)[cite: 38].
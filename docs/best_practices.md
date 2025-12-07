# Corporate Defense: Best Practices Against Keylogger Threats

**Project Phase:** Phase 4 (Analysis and Reporting)
**Deliverable:** Organizational Defense Guide

## 1. Introduction
Keyloggers pose a significant threat to information security by capturing sensitive data such as passwords and confidential communications . This guide outlines a multi-layered defense strategy (Defense in Depth) derived from the experimental findings of Project 4.

## 2. Preventive Controls (The First Line of Defense)
Our testing confirmed that prevention is far more effective than detection, as standard antivirus signatures often fail against custom scripts .

### A. Principle of Least Privilege (PoLP)
* **Strategy:** Enforce "Limited User" accounts for daily operations. Remove local administrator rights from standard employees.
* **Evidence:** During our testing, the keylogger script completely failed to execute when run from a non-administrator account because it lacked the permissions required for global keyboard hooking.
* **Recommendation:** Strictly limit the use of administrative accounts to IT personnel only.

### B. Application Whitelisting
* **Strategy:** Implement Software Restriction Policies (SRP) or AppLocker to block executable files from running in unauthorized directories (e.g., `C:\Users\[User]\Downloads` or `AppData`).
* **Evidence:** We successfully blocked the keylogger by enforcing a policy that prevented script execution from the user's home directory .
* **Recommendation:** Adopt a "deny-by-default" approach where only approved software can execute.

## 3. Detection & Monitoring Strategies
Since signature-based detection (like Windows Defender) proved ineffective against our custom Python script , organizations must rely on behavioral monitoring.

### A. Endpoint Detection
* **Strategy:** Monitor for unusual file handles and process behaviors rather than just file signatures.
* **Evidence:** Process Explorer was able to identify the malware by revealing an open handle to `log.txt`, whereas standard Task Manager failed to provide sufficient detail .
* **Recommendation:** Deploy Endpoint Detection and Response (EDR) tools that flag processes holding locks on suspicious log files or exhibiting continuous background input recording.

### B. Hardware-Based Security
* **Strategy:** Utilize hardware-based security modules like Trusted Platform Module (TPM) and BIOS-level protections .
* **Recommendation:** Ensure Secure Boot is enabled to prevent rootkit-type keyloggers from loading before the operating system.

## 4. The Human Element
* **Strategy:** Regular security awareness training focused on social engineering.
* **Evidence:** Our theoretical phishing simulation demonstrated that keyloggers are often delivered via deceptive emails mimicking software updates or login portals .
* **Recommendation:** Conduct quarterly phishing simulations to train users to recognize and report suspicious "urgent" downloads or unexpected email attachments.

## 5. Summary Checklist for Admins
1.  [x] **Audit Accounts:** Revoke unnecessary admin rights immediately.
2.  [x] **Restrict Paths:** Block execution from `%TEMP%` and `Downloads`.
3.  [x] **Enable EDR:** Use behavioral monitoring tools.
4.  [x] **Educate:** Train users on verifying software sources.
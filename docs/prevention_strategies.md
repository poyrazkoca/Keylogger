# Prevention Strategies

## 1. User Privilege Management (Most Effective)
[cite_start]**Finding:** When running the script under a non-administrator "Limited User" account, the script failed to execute properly due to lack of permission to hook keyboard inputs[cite: 123].
**Recommendation:** Enforce Principle of Least Privilege (PoLP) for all standard employees.

## 2. Application Whitelisting
[cite_start]**Finding:** Blocking execution from unauthorized directories (like User/Downloads) prevents the Python script from launching[cite: 125].
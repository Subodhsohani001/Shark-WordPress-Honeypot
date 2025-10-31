# 🛡️ Simple WordPress Honeypot

A lightweight and deceptive WordPress login honeypot designed to identify and log brute-force attempts. This project mimics a real `wp-admin` login page, captures attacker credentials, and stores detailed access logs — useful for cybersecurity learning, threat analysis, and portfolio demonstration.

---

## 🚀 Features

* 🎭 Realistic fake WordPress login interface
* 📝 Logs attacker attempts to `http_audits.log` (IP, timestamp, credentials)
* 👀 Helps detect brute-force bot behavior
* 🧠 Great for ethical hacking practice & security research
* 🧰 No real backend — safe to host publicly **only in controlled environments**

---

## 📂 Project Structure

```
/honeypot/
│── wp-admin-login.html    # Fake WordPress login page
│── server.py              # Logging logic (Python)
│── http_audits.log        # Attack logs (add to .gitignore before pushing)
└── README.md
```

---

## ⚙️ How It Works

1. Attacker lands on fake WP login page
2. Enters credentials (thinking it's real)
3. Submission triggers the logging script
4. Data recorded: IP 🌐 | Username 👤 | Password 🔑 | Timestamp ⏱️

---

## 🎯 Purpose

> This honeypot is intended for **ethical cybersecurity research, learning, and monitoring automated bot attacks**. Not for malicious use.

---

## 🛠️ Requirements

* Python 3.x
* Basic web hosting or local machine

---

## ▶️ Run Locally

```sh
# run the server (example)
python server.py
# then open http://localhost:5000 in your browser
```

**Deployment (free options — notes):**

* Render.com — easy deployment for simple web apps
* Replit — beginner-friendly (may have limitations)
* GitHub Pages — static HTML only (server logic won't run)
* Railway — alternative to Render

---

## 📊 Example Log Output

```
[2025-11-01 01:21:41] IP: 127.0.0.1 | USER: admin | PASS: admin@123
```

---

## ⚖️ Legal & Ethical Notice

You are responsible for how you use this project. Logging credentials or other personal data may be illegal in many jurisdictions if done outside your own, controlled environment. **Do not deploy this against third-party systems or capture data from users who haven't consented.**

If you intend to run this publicly, take steps to minimize legal risk:

* Run it on infrastructure you own or control.
* Avoid collecting or storing personally identifiable information (PII) where possible.
* Anonymize or redact logs if they include real user data.
* Consult local laws and your organization’s security/compliance team.

---

## 🔐 Security & Privacy Recommendations

* Add `http_audits.log` (and any other logs) to `.gitignore` before pushing to a public repo.
* Consider not storing raw passwords; if you must, secure the storage and rotate logs frequently.
* Prefer capturing metadata (IP, user-agent, timestamp) over PII.
* Rate-limit and sandbox the honeypot to avoid it being used as a pivot point.

---

## ✨ Future Enhancements

* Email alerting on suspicious activity
* IP reputation lookups
* Web dashboard to view and filter logs
* Docker / cloud deployment templates

---

## 📝 MIT License

Copyright (c) [2025] [SUBODH SOHANI/Subz_Cyber/Subodhsohani001]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

🔒 **Use responsibly** — this tool is for ethical cybersecurity research 🧠⚔️
📚 Learn. 🛡️ Defend. 🚫 Never exploit.

---

## 🤝 Contributing

PRs, bug reports, and suggestions are welcome. Prefer small, focused PRs and include tests where relevant.

---

*Hack smart. Hack ethically.* 🧠⚔️

# FailSafeAuth - Flask Threat Detection App

FailSafeAuth is a simple Python Flask web application deployed to Azure App Service. It features a `/login` route that logs both successful and failed login attempts, enabling security monitoring and brute-force detection using Azure Monitor and Kusto Query Language (KQL).

---

## 🔧 Features

- `/login` endpoint to simulate login attempts
- Console logs for both successful and failed logins
- Deployed to Azure App Service (Linux, Python 3.9)
- Integrated with Azure Log Analytics
- KQL queries to detect brute-force login behavior
- Configurable alert rule to notify on suspicious activity

---

## 🚀 Technologies

- Python 3.9
- Flask
- Gunicorn
- Azure App Service (Linux)
- Azure Log Analytics
- Azure Monitor
- Kusto Query Language (KQL)

---

## 📁 File Structure

```
FailSafeAuth/
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
├── startup.txt          # Azure startup command
├── test-app.http        # HTTP test cases for login
└── README.md            # This file
```

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-github-url>
cd FailSafeAuth
```

### 2. Create Virtual Environment & Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## ☁️ Azure Deployment

### 1. Create Azure Resources

```bash
az group create --name flask-lab-rg --location eastus
az appservice plan create --name flask-linux-plan --resource-group flask-lab-rg --sku B1 --is-linux
az webapp create --resource-group flask-lab-rg --plan flask-linux-plan --name FailSafeAuth --runtime "PYTHON|3.9"
```

### 2. Deploy Code to Azure

```bash
zip -r app.zip .
az webapp deployment source config-zip --resource-group flask-lab-rg --name FailSafeAuth --src app.zip
```

---

## 📊 Enable Logging

### Create Log Analytics Workspace

```bash
az monitor log-analytics workspace create --resource-group flask-lab-rg --workspace-name flask-log-ws --location eastus
```

### Enable Diagnostic Settings

```bash
az monitor diagnostic-settings create \
  --name log-settings \
  --resource "<WebApp Resource ID>" \
  --workspace "<Log Analytics Resource ID>" \
  --logs '[{"category": "AppServiceConsoleLogs","enabled": true},{"category": "AppServiceHTTPLogs","enabled": true}]'
```

---

## 🔁 Testing the App

Use the provided `test-app.http` file in VS Code with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

### `test-app.http`

```http
### Successful login
POST https://FailSafeAuth.azurewebsites.net/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=password

### Failed login
POST https://FailSafeAuth.azurewebsites.net/login
Content-Type: application/x-www-form-urlencoded

username=admin&password=wrong
```

---

## 🔍 Query Logs with KQL

In Azure Portal → Log Analytics Workspace → Logs:

```kql
AppServiceConsoleLogs
| where TimeGenerated > ago(30m)
| where ResultDescription has "login attempt"
```

> Or if using a tag in logs:
```kql
| where ResultDescription has "[LOGIN]"
```

---

## 📣 Alert Rule Configuration

1. Go to **Azure Monitor > Alerts > + Create Alert Rule**
2. Scope: your Log Analytics workspace
3. Condition: custom query above
4. Threshold: Count > 5 in 5-minute window
5. Action: Email (Action Group)
6. Severity: 2 or 3
7. Name: `BruteForceLoginAlert`

---

## 🎥 Demo

Watch a full walkthrough of FailSafeAuth on YouTube:

[![FailSafeAuth Demo](https://img.youtube.com/vi/oPWMIRpVGso/0.jpg)](https://youtu.be/oPWMIRpVGso)

📺 [Click to watch the demo](https://youtu.be/oPWMIRpVGso)

---

## ✅ Result

You now have:

- A Flask app deployed on Azure
- Login attempts being logged
- Logs searchable in KQL
- Alerts that detect brute-force login behavior

---

## 📄 License

MIT

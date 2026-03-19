# 🚀 Deployment Guide: AI Resume Matcher PRO

Follow these steps to get your app live on the web!

## 1. Create a GitHub Repository
1. Log in to [GitHub](https://github.com/).
2. Create a new repository named `resume-matcher`.
3. Copy the **HTTPS URL** (it looks like `https://github.com/your-username/resume-matcher.git`).

## 2. Push Your Code (Run these in your terminal)
Open your terminal in the `resume-matcher` folder and run:

```bash
# Add the remote (Replace YOUR_URL with the one you copied)
git remote add origin YOUR_URL

# Push the code
git push -u origin master
```

## 3. Deploy to Streamlit Community Cloud
1. Go to [Streamlit Cloud](https://share.streamlit.io/).
2. Click **"New app"**.
3. Select your `resume-matcher` repository.
4. **Important Settings:**
   - **Branch**: `master`
   - **Main file path**: `app.py`
5. Click **"Deploy!"**

---
### 🛠 Files in this project:
- `app.py`: The main application code.
- `requirements.txt`: Needed for Streamlit to install libraries.
- `README.md`: Project documentation.
- `.gitignore`: Keeps your repo clean.

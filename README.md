# 🏏 IPL Analytics Desk – Win Probability Predictor

A real-time IPL match win probability prediction app.

This project estimates the winning chances of a team based on live match inputs like target score, current score, overs completed, and wickets lost. It simulates match situations dynamically and provides instant probability insights.

---

## 🚀 Live Concept

The application works in two stages:

### 1️⃣ Front Page – Match Setup

Users select:

* Batting Team
* Bowling Team
* Match City
* Target Score
* Current Score
* Overs Completed
* Wickets Lost

After entering match details, the user clicks **"Predict Win Probability"**.

---

### 2️⃣ Result Page – Match Analysis

The app displays:

### 📊 Match Snapshot

* Target
* Runs Left
* Balls Left
* Required Run Rate
* Current Run Rate
* Wickets in Hand

### 📈 Win Probability

* Batting team winning percentage
* Bowling team winning percentage
* Visual probability bars
* Match insight summary

The probability updates dynamically based on match conditions.

---

## 🧠 Machine Learning Model

The prediction system is built using:

* Historical IPL match data
* Feature engineering:
  * Runs left
  * Balls left
  * Wickets remaining
  * Current run rate
  * Required run rate
* Logistic Regression model for probability estimation

The model outputs a winning probability between 0 and 1, converted to percentage format for display.

---

## 🛠️ Tech Stack

**Frontend**

* Streamlit
* Custom CSS styling

**Backend**

* Python
* Scikit-learn
* Pandas
* NumPy

**Model**

* Logistic Regression

---

## 📂 Project Structure

```
IPL-Analytics-Desk/
│
├── app.py
├── model.pkl
├── Data/
│   ├── matches.csv
│   └── deliveries.csv
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
```

2. Navigate to the project folder:

```bash
cd your-repo-name
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
streamlit run app.py
```

---

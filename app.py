
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import db
import json

app = Flask(__name__, template_folder="templates")
app.secret_key = 'your_secret_key'



# Define questions for each condition
stress_questions = [
    "1. How often do you feel overwhelmed by stress?",
    "2. How often do you have trouble sleeping due to stress?",
    "3. How often do you experience physical symptoms like headaches or stomachaches due to stress?",
    "4. How often do you find it hard to make decisions or think clearly due to stress?",
    "5. How often do you feel irritable or short-tempered due to stress?",
    "6. How often do you have difficulty relaxing or unwinding at the end of the day due to stress?",
    "7. How often do you experience changes in your appetite due to stress?",
    "8. How often do you experience muscle tension or pain due to stress?",
    "9. How often do you have racing thoughts or constant worrying due to stress?",
    "10. How often do you feel emotionally drained or exhausted due to stress?"
]

depression_questions = [
    "1. How often do you feel sad or hopeless?",
    "2. How often do you find it difficult to enjoy activities you once enjoyed?",
    "3. How often do you isolate yourself from others?",
    "4. How often do you have persistent physical symptoms like body aches or tension?",
    "5. How often do you have trouble concentrating or making decisions due to sadness?",
    "6. How often do you experience changes in your sleep patterns (e.g., sleeping too much or too little) due to sadness?",
    "7. How often do you feel like you've lost interest or pleasure in most things you used to enjoy?",
    "8. How often do you feel a sense of worthlessness or excessive guilt?",
    "9. How often do you have changes in appetite or weight due to depression?",
    "10. How often do you have thoughts of self-harm or suicide?"
]

anxiety_questions = [
    "1. How often do you feel nervous or anxious?",
    "2. How often do you have difficulty concentrating due to anxiety?",
    "3. How often do you experience excessive worry about various aspects of your life?",
    "4. How often do you feel fatigued or lack energy due to anxiety?",
    "5. How often do you have restlessness or a feeling of being on edge due to anxiety?",
    "6. How often do you have muscle tension or body aches due to anxiety?",
    "7. How often do you avoid situations or places due to anxiety?",
    "8. How often do you experience a racing heart or palpitations due to anxiety?",
    "9. How often do you have trouble falling or staying asleep due to anxiety?",
    "10. How often do you experience shortness of breath or a choking sensation due to anxiety?"
]


# Create global variables to keep track of responses for each condition
stress_responses = []
depression_responses = []
anxiety_responses = []

# Assign weights to questions for each condition
question_weights = [
    # Stress
    [3, 3, 2, 2, 1, 1, 1, 1, 1, 2],

    # Depression
    [2, 3, 2, 1, 1, 2, 1, 2, 1, 1],

    # Anxiety
    [3, 2, 3, 2, 1, 2, 2, 3, 1, 1]
]


def calculate_score(responses, weights):
    return sum([int(response) * weight for response, weight in zip(responses, weights)])


# login condition

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template("signin.html")


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")



@app.route('/signin', methods = ['GET', 'POST'])
def signin():
    status, username = db.check_user()

    data = {
        "username": username,
        "status": status
    }

    return json.dumps(data)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    status = db.insert_data()
    return json.dumps(status)


#  login end


@app.route('/greet')
def greet():
     return render_template('greeting.html')

# Stress assessment
@app.route('/stress')
def stress():
    return render_template('stress.html', question=stress_questions[0])

@app.route('/stress-answer', methods=['POST'])
def stress_answer():
    response = request.form.get('response')
    stress_responses.append(response)

    if len(stress_responses) < len(stress_questions):
        return render_template('stress.html', question=stress_questions[len(stress_responses)])
    else:
        stress_score = calculate_score(stress_responses, question_weights[0])
        # Determine stress level based on the score
        print(stress_score)
        if stress_score < 8:
            session['stress_level'] = "Your stress level is low. Continue practicing stress management techniques and maintain a balanced lifestyle."
        elif stress_score < 15 and stress_score >= 8:
            session['stress_level'] = "Your stress level is within the normal range. Keep up with self-care and stress reduction methods."
        else:
            session['stress_level'] = "Your stress level is high. Consider consulting with a mental health professional for guidance and support."

        # Redirect to the depression assessment
        return redirect(url_for('depression'))


# Depression assessment
@app.route('/depression')
def depression():
    # Clear stress responses and start depression assessment
    stress_responses.clear()
    return render_template('depression.html', question=depression_questions[0])

@app.route('/depression-answer', methods=['POST'])
def depression_answer():
    response = request.form.get('response')
    depression_responses.append(response)

    if len(depression_responses) < len(depression_questions):
        return render_template('depression.html', question=depression_questions[len(depression_responses)])
    else:
        depression_score = calculate_score(depression_responses, question_weights[1])
        # Determine depression level based on the score
        print(depression_score)
        if depression_score < 8:
            session['depression_level'] = "Your depression level is low. Stay connected with your support network and focus on positive activities."
        elif depression_score < 15 and depression_score >= 8:
            session['depression_level'] = "Your depression level is normal. Continue self-care and consider talking to a counselor if needed."
        else:
            session['depression_level'] = "Your depression level is high. Seek professional help to address your symptoms and develop a treatment plan."

        # Redirect to the anxiety assessment
        return redirect(url_for('anxiety'))

# Anxiety assessment
@app.route('/anxiety')
def anxiety():
    # Clear depression responses and start anxiety assessment
    depression_responses.clear()
    return render_template('anxiety.html', question=anxiety_questions[0])

@app.route('/anxiety-answer', methods=['POST'])
def anxiety_answer():
    response = request.form.get('response')
    anxiety_responses.append(response)

    if len(anxiety_responses) < len(anxiety_questions):
        return render_template('anxiety.html', question=anxiety_questions[len(anxiety_responses)])
    else:
        anxiety_score = calculate_score(anxiety_responses, question_weights[2])
        # Determine anxiety level based on the score
        print(anxiety_score)
        if anxiety_score < 8:
            session['anxiety_level'] = "Your anxiety level is low. Practice relaxation techniques and maintain a stress-reducing lifestyle."
        elif anxiety_score < 15 and anxiety_score >= 8:
            session['anxiety_level'] = "Your anxiety level is normal. Keep up with stress management and consider therapy for further assistance."
        else:
            session['anxiety_level'] = "Your anxiety level is high. Consult with a mental health specialist for coping strategies and treatment options."

        # Get stress and depression levels from the session
        stress_level = session.get('stress_level', 'Not assessed')
        depression_level = session.get('depression_level', 'Not assessed')
        # Display the final result
        return render_template('result.html', stress_level=stress_level, depression_level=depression_level, anxiety_level=session['anxiety_level'])

if __name__ == '__main__':
    app.run(debug=True)

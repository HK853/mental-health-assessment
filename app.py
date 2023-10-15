from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, template_folder="templates")

# Set the secret key to enable sessions
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Define questions for each condition
stress_questions = [
    "How often do you feel overwhelmed by stress?",
    "How often do you have trouble sleeping due to stress?",
    "How often do you experience physical symptoms like headaches or stomachaches due to stress?",
    "How often do you find it hard to make decisions or think clearly due to stress?"
]

depression_questions = [
    "How often do you feel sad or hopeless?",
    "How often do you find it difficult to enjoy activities you once enjoyed?",
    "How often do you isolate yourself from others?",
    "How often do you have persistent physical symptoms like body aches or tension?"
]

anxiety_questions = [
    "How often do you feel nervous or anxious?",
    "How often do you have difficulty concentrating due to anxiety?",
    "How often do you experience excessive worry about various aspects of your life?",
    "How often do you feel fatigued or lack energy due to anxiety?"
]

# Create global variables to keep track of responses for each condition
stress_responses = []
depression_responses = []
anxiety_responses = []

# Assign weights to questions for each condition
question_weights = [
    # Stress
    [3, 3, 2, 2],

    # Depression
    [2, 3, 2, 1],

    # Anxiety
    [3, 2, 3, 2]
]

def calculate_score(responses, weights):
    return sum([int(response) * weight for response, weight in zip(responses, weights)])
# Stress assessment
@app.route('/')
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
        if stress_score < 8:
            session['stress_level'] = "Low"
        elif stress_score < 15 and stress_score >= 8:
            session['stress_level'] = "Normal"
        else:
            session['stress_level'] = "High"

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
        if depression_score < 8:
            session['depression_level'] = "Low"
        elif depression_score < 15 and depression_score >= 8:
            session['depression_level'] = "Normal"
        else:
            session['depression_level'] = "High"

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
        if anxiety_score < 8:
            session['anxiety_level'] = "Low"
        elif anxiety_score < 15 and anxiety_score >= 8:
            session['anxiety_level'] = "Normal"
        else:
            session['anxiety_level'] = "High"

        # Get stress and depression levels from the session
        stress_level = session.get('stress_level', 'Not assessed')
        depression_level = session.get('depression_level', 'Not assessed')
        # Display the final result
        return render_template('result.html', stress_level=stress_level, depression_level=depression_level, anxiety_level=session['anxiety_level'])

if __name__ == '__main__':
    app.run(debug=True)

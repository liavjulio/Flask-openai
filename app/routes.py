from flask import Blueprint, request, jsonify
from openai import OpenAIError
from .models import db, QnA
from . import openai_client

bp = Blueprint('main', __name__)

@bp.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    print("Received question:", question)  # Debugging line

    try:
        if openai_client is None:
            raise ValueError("OpenAI client is not initialized")

        response = openai_client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=question,
            max_tokens=150,
            stop=None
        )
        print("OpenAI raw response:", response)  # Debugging line

        if response.choices:
            answer = response.choices[0].text.strip()
            print("Parsed answer:", answer)  # Debugging line

            # Save to database
            save_to_db(question, answer)

            return jsonify({'question': question, 'answer': answer}), 200
        else:
            return jsonify({'error': 'No response choices from OpenAI'}), 500

    except OpenAIError as e:
        # Handle OpenAI API errors
        print("OpenAI Error:", e)  # Debugging line
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        print("General Error:", e)  # Debugging line
        return jsonify({'error': str(e)}), 500

def save_to_db(question, answer):
    try:
        new_qna = QnA(question=question, answer=answer)
        db.session.add(new_qna)
        db.session.commit()
        print("Saved to DB: question={}, answer={}".format(question, answer))  # Debugging line
    except Exception as e:
        print("Error saving to DB:", e)  # Debugging line
        db.session.rollback()
        raise e

from flask import Blueprint, request, jsonify, render_template, Response
from openai import OpenAIError
from .models import db, QnA, Conversation, Message
from . import openai_client
import json
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@bp.route('/api/conversations', methods=['GET'])
def get_conversations():
    """Get all conversations"""
    conversations = Conversation.query.order_by(Conversation.updated_at.desc()).all()
    return jsonify([{
        'id': conv.id,
        'title': conv.title or 'New Chat',
        'created_at': conv.created_at.isoformat(),
        'updated_at': conv.updated_at.isoformat()
    } for conv in conversations])

@bp.route('/api/conversations', methods=['POST'])
def create_conversation():
    """Create a new conversation"""
    conversation = Conversation()
    db.session.add(conversation)
    db.session.commit()
    
    return jsonify({
        'id': conversation.id,
        'title': 'New Chat',
        'created_at': conversation.created_at.isoformat(),
        'updated_at': conversation.updated_at.isoformat()
    }), 201

@bp.route('/api/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_messages(conversation_id):
    """Get all messages for a conversation"""
    messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()
    
    return jsonify([{
        'id': msg.id,
        'role': msg.role,
        'content': msg.content,
        'created_at': msg.created_at.isoformat()
    } for msg in messages])

@bp.route('/api/conversations/<int:conversation_id>/chat', methods=['POST'])
def chat(conversation_id):
    """Send a message and get AI response"""
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        conversation = Conversation.query.get_or_404(conversation_id)
        
        # Save user message
        user_msg = Message(
            conversation_id=conversation_id,
            role='user',
            content=user_message
        )
        db.session.add(user_msg)
        
        # Get conversation history for context
        messages = Message.query.filter_by(conversation_id=conversation_id).order_by(Message.created_at).all()
        
        # Prepare messages for OpenAI (including the new user message)
        openai_messages = []
        for msg in messages:
            openai_messages.append({
                'role': msg.role,
                'content': msg.content
            })
        openai_messages.append({
            'role': 'user',
            'content': user_message
        })
        
        if openai_client is None:
            raise ValueError("OpenAI client is not initialized")

        # Check if we're in mock mode
        mock_mode = os.getenv('MOCK_MODE', 'false').lower() == 'true'
        
        if mock_mode:
            # Mock response for development/testing
            ai_response = f"🤖 Mock AI Response: I understand you asked '{user_message}'. This is a simulated response since we're in mock mode due to API quota limits. Please add credits to your OpenAI account to get real AI responses!"
        else:
            # Use the chat completions API (modern approach)
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=openai_messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            if response.choices:
                ai_response = response.choices[0].message.content.strip()
            else:
                return jsonify({'error': 'No response from AI'}), 500
        
        # Save AI response
        ai_msg = Message(
            conversation_id=conversation_id,
            role='assistant',
            content=ai_response
        )
        db.session.add(ai_msg)
        
        # Update conversation title if it's the first message
        if not conversation.title and len(openai_messages) <= 2:
            # Generate a title based on the first user message
            title = user_message[:50] + "..." if len(user_message) > 50 else user_message
            conversation.title = title
        
        db.session.commit()
        
        return jsonify({
            'user_message': {
                'id': user_msg.id,
                'role': 'user',
                'content': user_message,
                'created_at': user_msg.created_at.isoformat()
            },
            'ai_message': {
                'id': ai_msg.id,
                'role': 'assistant',
                'content': ai_response,
                'created_at': ai_msg.created_at.isoformat()
            }
        }), 200

    except OpenAIError as e:
        print("OpenAI Error:", e)
        return jsonify({'error': f'AI service error: {str(e)}'}), 500
    except Exception as e:
        print("General Error:", e)
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/api/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete a conversation"""
    conversation = Conversation.query.get_or_404(conversation_id)
    db.session.delete(conversation)
    db.session.commit()
    return '', 204

# Keep the old ask endpoint for backward compatibility
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

# long_term_memory_app/app/api/routes.py

from flask import request, jsonify, Blueprint
from ..services.summary_service import summarize_conversation
from ..models.models import db, ConversationSummary

api = Blueprint('api', __name__)


@api.route('/summarize', methods=['POST'])
def create_summary():
    data = request.get_json()
    conversation_text = data.get('conversation_text')
    summary_length = data.get('summary_length', 5)  # Default summary length to 5 sentences

    if not conversation_text:
        return jsonify({"error": "No conversation text provided"}), 400

    summary = summarize_conversation(conversation_text, summary_length)

    new_summary = ConversationSummary(summary=summary)
    db.session.add(new_summary)
    db.session.commit()

    return jsonify({"summary": summary}), 200


@api.route('/conversations', methods=['POST'])
def store_conversation():
    data = request.get_json()
    summary = data.get('summary')
    conversation_text = data.get('conversation_text')

    if not summary or not conversation_text:
        return jsonify({'error': 'Missing data'}), 400

    new_summary = ConversationSummary(summary=summary, conversation_text=conversation_text)
    db.session.add(new_summary)
    db.session.commit()

    return jsonify({'id': new_summary.id, 'message': 'Conversation summary stored successfully.'}), 201


@api.route('/conversations/<int:id>', methods=['GET'])
def get_conversation(id):
    conversation_summary = ConversationSummary.query.get(id)

    if conversation_summary is None:
        return jsonify({'error': 'Conversation summary not found'}), 404

    return jsonify({
        'id': conversation_summary.id,
        'conversation_text': conversation_summary.conversation_text,
        'summary': conversation_summary.summary,
        'created_at': conversation_summary.created_at.isoformat()
    }), 200

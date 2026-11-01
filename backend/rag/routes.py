from flask import Blueprint, request, jsonify, session
from backend.services.rag_service import rag_engine
from backend.models import KnowledgeDocument
from backend.database import db
import os
import uuid

rag_bp = Blueprint('rag', __name__, url_prefix='/api/rag')

@rag_bp.route('/documents', methods=['GET'])
def list_documents():
    docs = KnowledgeDocument.query.order_by(KnowledgeDocument.id.desc()).all()
    if not docs:
        # Return currently indexed chunks info from memory
        unique_titles = list(set(c['title'] for c in rag_engine.chunks))
        return jsonify({
            'documents': [
                {
                    'id': 1,
                    'title': t,
                    'category': 'Handbook / Policy',
                    'num_chunks': sum(1 for c in rag_engine.chunks if c['title'] == t),
                    'created_at': 'Official Policy'
                } for t in unique_titles
            ]
        })

    return jsonify({'documents': [{
        'id': d.id,
        'title': d.title,
        'filename': d.filename,
        'category': d.category,
        'num_chunks': d.num_chunks,
        'uploaded_by': d.uploaded_by,
        'created_at': d.created_at.strftime("%b %d, %Y")
    } for d in docs]})

@rag_bp.route('/query', methods=['POST'])
def query_knowledge_base():
    data = request.get_json(silent=True) or {}
    q = data.get('query', '').strip()
    top_k = int(data.get('top_k', 3))

    if not q:
        return jsonify({'error': 'Query string required'}), 400

    results = rag_engine.search(q, top_k=top_k, min_similarity=0.10)
    return jsonify({
        'query': q,
        'results_count': len(results),
        'results': results
    })

@rag_bp.route('/upload', methods=['POST'])
def upload_document():
    data = request.get_json(silent=True) or {}
    title = data.get('title', 'Campus Regulation Document')
    category = data.get('category', 'Handbook')
    content = data.get('content', '')
    filename = data.get('filename', f"doc_{uuid.uuid4().hex[:6]}.txt")

    if not content or len(content.strip()) < 50:
        return jsonify({'error': 'Document content must contain at least 50 characters of valid text.'}), 400

    num_chunks = rag_engine.add_document(title, filename, category, content)

    doc = KnowledgeDocument(
        title=title,
        filename=filename,
        category=category,
        file_path=filename,
        num_chunks=num_chunks,
        uploaded_by=session.get('role', 'Administrator')
    )
    db.session.add(doc)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Document "{title}" ingested and indexed successfully into RAG knowledge base ({num_chunks} chunks).',
        'document_id': doc.id,
        'chunks_created': num_chunks
    }), 201

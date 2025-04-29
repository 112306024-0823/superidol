from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models.idol import Idol
from ..models.user import User
from . import bp

@bp.route('/idols', methods=['GET'])
def get_idols():
    idols = Idol.query.all()
    return jsonify([{
        'id': idol.id,
        'name': idol.name,
        'birthday': idol.birthday.isoformat(),
        'height': idol.height,
        'weight': idol.weight,
        'blood_type': idol.blood_type,
        'hobbies': idol.hobbies,
        'specialties': idol.specialties,
        'description': idol.description
    } for idol in idols])

@bp.route('/idols/<int:id>', methods=['GET'])
def get_idol(id):
    idol = Idol.query.get_or_404(id)
    return jsonify({
        'id': idol.id,
        'name': idol.name,
        'birthday': idol.birthday.isoformat(),
        'height': idol.height,
        'weight': idol.weight,
        'blood_type': idol.blood_type,
        'hobbies': idol.hobbies,
        'specialties': idol.specialties,
        'description': idol.description
    })

@bp.route('/idols/<int:id>/favorite', methods=['POST'])
@jwt_required()
def favorite_idol(id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    idol = Idol.query.get_or_404(id)
    
    if idol in user.favorite_idols:
        return jsonify({'message': 'Idol already in favorites'}), 400
    
    user.favorite_idols.append(idol)
    db.session.commit()
    return jsonify({'message': 'Idol added to favorites'})

@bp.route('/idols/<int:id>/favorite', methods=['DELETE'])
@jwt_required()
def unfavorite_idol(id):
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    idol = Idol.query.get_or_404(id)
    
    if idol not in user.favorite_idols:
        return jsonify({'message': 'Idol not in favorites'}), 400
    
    user.favorite_idols.remove(idol)
    db.session.commit()
    return jsonify({'message': 'Idol removed from favorites'}) 
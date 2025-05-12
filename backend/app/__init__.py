# backend/app/__init__.py
import os
from flask import Flask
from flask_cors import CORS
from app.db.models import db
from app.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    
    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:postgres@localhost:5432/rag_app_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    
    # Health check route
    @app.route('/api/health')
    def health_check():
        return {'status': 'OK'}, 200
    
    return app

# For running with Flask CLI
app = create_app()

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
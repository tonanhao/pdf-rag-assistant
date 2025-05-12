# backend/manage.py
import os
import click
from flask.cli import FlaskGroup
from app import create_app
from app.db.models import db, User, Role, Permission, Profile

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command('create-tables')
def create_tables():
    """Create database tables"""
    with app.app_context():
        db.create_all(schema='rag_app')
        click.echo('Tables created')

@cli.command('init-db')
def init_db():
    """Initialize database with required data"""
    from app.services.auth_service import AuthService
    
    with app.app_context():
        # Create roles if they don't exist
        roles = {
            1: 'admin',
            2: 'user',
            3: 'guest'
        }
        
        for role_id, role_name in roles.items():
            if not Role.query.get(role_id):
                role = Role(role_id=role_id, role_name=role_name)
                db.session.add(role)
        
        # Create permissions
        permissions = [
            'document:read', 'document:write',
            'chat:read', 'chat:write',
            'user:manage'
        ]
        
        for perm_name in permissions:
            if not Permission.query.filter_by(name=perm_name).first():
                perm = Permission(name=perm_name)
                db.session.add(perm)
        
        db.session.commit()
        
        # Create admin user if it doesn't exist
        admin_email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
        admin_password = os.environ.get('ADMIN_PASSWORD', 'Admin@123')
        
        admin = User.query.filter_by(email=admin_email).first()
        if not admin:
            admin = User(
                email=admin_email,
                password_hash=AuthService.hash_password(admin_password),
                role_id=1  # Admin role
            )
            db.session.add(admin)
            db.session.commit()
            
            # Create admin profile
            profile = Profile(
                user_id=admin.user_id,
                full_name='Admin User'
            )
            db.session.add(profile)
            db.session.commit()
            
            click.echo(f'Admin user created: {admin_email}')
        else:
            click.echo(f'Admin user already exists: {admin_email}
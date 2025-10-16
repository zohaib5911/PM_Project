from flask import Flask, render_template, request, jsonify, send_file, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pm_standards.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/documents/standards'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import models after db initialization
from models.standard import Standard
from models.section import Section
from models.comparison import Comparison
from models.process import ProcessTemplate
from models.bookmark import Bookmark

# Import and register blueprints
from routes import standards_bp, comparison_bp, process_bp, search_bp

app.register_blueprint(standards_bp, url_prefix='/standards')
app.register_blueprint(comparison_bp, url_prefix='/comparison')
app.register_blueprint(process_bp, url_prefix='/process')
app.register_blueprint(search_bp, url_prefix='/search')

@app.before_request
def before_request():
    """Set session user_id if not exists"""
    if 'user_id' not in session:
        session['user_id'] = 'guest_' + os.urandom(8).hex()

@app.route('/')
def index():
    """Landing page"""
    standards = Standard.query.all()
    return render_template('index.html', standards=standards)

@app.route('/dashboard')
def dashboard():
    """User dashboard with recent activity"""
    recent_bookmarks = Bookmark.query.filter_by(
        user_session=session.get('user_id', 'guest')
    ).order_by(Bookmark.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', bookmarks=recent_bookmarks)

@app.context_processor
def utility_processor():
    """Add utility functions to templates"""
    def get_standard_color(standard_name):
        colors = {
            'PMBOK': '#0066CC',
            'PRINCE2': '#6B2C91',
            'ISO21500': '#00843D',
            'ISO21502': '#00843D'
        }
        return colors.get(standard_name, '#333333')
    
    return dict(get_standard_color=get_standard_color)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
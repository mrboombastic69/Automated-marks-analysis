from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, desc

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'departments'
    
    code = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    files = db.relationship('File', backref='department', lazy=True)

    def __repr__(self):
        return f'<Department {self.name}>'

class File(db.Model):
    __tablename__ = 'files'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    department_code = db.Column(db.String(10), db.ForeignKey('departments.code'), nullable=False)

    def __repr__(self):
        return f'<File {self.name}>'

def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()

def add_department(code, name):
    new_department = Department(code=code, name=name)
    db.session.add(new_department)
    db.session.commit()

def add_file(name, created_on, department_code):
    new_file = File(name=name, created_on=created_on, department_code=department_code)
    db.session.add(new_file)
    db.session.commit()

def get_files(page=1, per_page=10, sort_by='created_on', order='asc'):
    sort_order = asc(sort_by) if order == 'asc' else desc(sort_by)
    files_query = File.query.order_by(sort_order)
    return files_query.paginate(page=page, per_page=per_page, error_out=False)

# Usage example:
# init_db(app)
# add_department('CSE', 'Computer Science and Engineering')
# add_file('example.txt', datetime.now(), 'CSE')
# files = get_files(page=1, per_page=10, sort_by='name', order='desc')

from flask import Flask, render_template, request, redirect, session, url_for, send_from_directory, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import time, os, uuid, json
from datetime import datetime
from national import nationalities
from sqlalchemy import text
from flask import Flask, after_this_request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['LAST_UPDATE'] = int(time.time())
app.secret_key = "aries_vincent_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///luma.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db = SQLAlchemy(app)

class Tickets(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False) #/checked
    standard_tickets = db.Column(db.Integer, nullable=False) #/checked
    premium_tickets = db.Column(db.Integer, nullable=False) #/checked
    
class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    venue_name = db.Column(db.String(100), nullable=False) #/checked
    location = db.Column(db.String(200), nullable=False) #/checked
    seating_capacity = db.Column(db.Integer, nullable=False) #/checked
    venue_image = db.Column(db.String(1000), nullable=False) #/checked
    schedule_open = db.Column(db.String(1000), nullable=False) #/checked
    venue_linkMap = db.Column(db.String(1000), nullable=False) #/checked
    
class Libraries(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    library_name = db.Column(db.String(100), nullable=False) #/checked
    user_id = db.Column(db.String(200), nullable=False) #/checked
    seating_capacity = db.Column(db.Integer, nullable=False) #/checked
    library_image = db.Column(db.String(1000), nullable=False) #/checked
    schedule_open = db.Column(db.String(1000), nullable=False) #/checked
    library_linkMap = db.Column(db.String(1000), nullable=False) #/checked

class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.Text, nullable=False) #/checked
    description = db.Column(db.Text, nullable=False) #/checked
    movie_image = db.Column(db.String(1000), nullable=False) #/checked
    movie_trailer = db.Column(db.String(1000), nullable=False) #/checked
    movie_date = db.Column(db.String(50), nullable=False) #/checked
    status = db.Column(db.String(50), nullable=False) #/checked
    age_rating = db.Column(db.String(10), nullable=False) #/checked
    language = db.Column(db.String(50), nullable=False) #/checked
    duration = db.Column(db.String(20), nullable=False) #/checked
    genre = db.Column(db.String(50), nullable=False) #/checked
    movie_schedule = db.Column(db.String(1000), nullable=False) #/checked
    scheduled_date = db.Column(db.String(1000), nullable=False) #/checked
    
    tickets = db.relationship('Tickets', backref='movie', lazy=True)
    venue = db.relationship('Venue', backref='movie', lazy=True)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    access = db.Column(db.String(50), nullable=False, default='active')
    role = db.Column(db.String(50), default='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

def inject_now():
    """Adds a changing timestamp to all templates."""
    return {'now': int(time.time())}

@app.route('/gotologin')
def gotologin():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('landingpage.html')

# @app.route('/dashboard', methods=['GET', 'POST'])
# def dashboard():
#     if 'username' not in session:
#         return redirect(url_for('index'))

#     if request.method == 'POST':
#         name = f"{request.form.get('last', '').capitalize()} {request.form.get('first', '').capitalize()} {request.form.get('initial', '').capitalize()}".strip()
#         age = int(request.form['age'])
#         gender = request.form['gender']
#         nationality = request.form['nationality']

#         security_level_num = int(request.form['security_level'])
#         SECURITY_LEVELS = {
#             1: "Low Security Inmate",
#             2: "Medium Security Inmate",
#             3: "High Security Inmate",
#             4: "Maximum Security Inmate",
#             5: "Death Row Inmate"
#         }
#         security_level_str = SECURITY_LEVELS.get(security_level_num, "Unknown")

#         date_apprehended_str = request.form.get('Apprehended')
#         date_apprehended = (
#             datetime.strptime(date_apprehended_str, "%Y-%m-%d").date()
#             if date_apprehended_str else None
#         )

#         current_date_str = request.form.get('current_date')
#         date_added = (
#             datetime.strptime(current_date_str, "%Y-%m-%d").date()
#             if current_date_str else datetime.utcnow().date()
#         )

#         bail_fund = request.form.get('bail_fund') or "Unbailable"
#         marital_status = request.form.get('marital_status')
#         inmate_status = request.form.get('inmate_status', 'In Custody')

#         mother_name = f"{request.form.get('mother_last', '').capitalize()} {request.form.get('mother_first', '').capitalize()} {request.form.get('mother_initial', '').capitalize()}".strip()
#         father_name = f"{request.form.get('father_last', '').capitalize()} {request.form.get('father_first', '').capitalize()} {request.form.get('father_initial', '').capitalize()}".strip()

#         home_address = request.form.get('home-address')
#         mugshot_file = request.files.get('mugshot')
#         mugshot_filename = None

#         if mugshot_file and mugshot_file.filename != '':
#             ext = os.path.splitext(mugshot_file.filename)[1]
#             mugshot_filename = f"{uuid.uuid4().hex}{ext}"
#             mugshot_file.save(os.path.join(app.config['UPLOAD_FOLDER'], mugshot_filename))

#         inmate = Inmate(
#             name=name, 
#             age=age,
#             gender=gender, 
#             nationality=nationality,
#             security_level=security_level_str, 
#             date_apprehended=date_apprehended,
#             date_added=date_added, 
#             bail_fund=bail_fund, 
#             marital_status=marital_status,
#             inmate_status=inmate_status, 
#             mother_name=mother_name, 
#             father_name=father_name,
#             home_address=home_address,
#             mugshot=mugshot_filename
#         )
#         db.session.add(inmate)
#         db.session.commit()

#         record_descriptions = request.form.getlist('crime_description[]')
#         conviction_years_list = request.form.getlist('conviction_years[]')
#         evidence_files = request.files.getlist('evidence_file[]')

#         for i in range(len(record_descriptions)):
#             evidence_file = evidence_files[i] if i < len(evidence_files) else None
#             filename = None

#             if evidence_file and evidence_file.filename != '':
#                 ext = os.path.splitext(evidence_file.filename)[1]
#                 filename = f"{uuid.uuid4().hex}{ext}"
#                 evidence_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#             record = InmateRecord(
#                 inmate_id=inmate.id,
#                 crime_description=record_descriptions[i],
#                 conviction_years=int(conviction_years_list[i]),
#                 evidence_file=filename
#             )
#             db.session.add(record)

#         db.session.commit()
#         flash('Inmate added successfully!', 'success')
#         return redirect(url_for('dashboard'))

#     inmates = Inmate.query.order_by(Inmate.date_added.desc()).all()

#     posts = []
#     for inmate in inmates:
#         total_years = sum([r.conviction_years for r in inmate.records])

#         posts.append({
#             "id": inmate.id,
#             "name": inmate.name,
#             "security_level": inmate.security_level,
#             "date_added": inmate.date_added,
#             "mugshot": inmate.mugshot,
#             "total_years": total_years,
#             "evidence_file": inmate.evidence_file
#         })

#     return render_template("dashboard.html", posts=posts)

# @app.route('/add', methods=['GET', 'POST'])
# def add_inmate():
#     if 'username' not in session:
#         return redirect(url_for('index'))
    
#     if request.method == 'POST':
#         name_parts = [request.form.get('last', ''), request.form.get('first', ''), request.form.get('initial', '')]
#         name = " ".join([p.capitalize() for p in name_parts if p.strip()]).strip()
        
#         age = int(request.form.get('age', 0))
#         gender = request.form.get('gender')
#         nationality = request.form.get('nationality')
#         security_level_num = int(request.form.get('security_level', 1))
#         SECURITY_LEVELS = {1: "Low Security", 2: "Medium Security", 3: "High Security", 4: "Maximum Security", 5: "Death Row"}
#         security_level_str = SECURITY_LEVELS.get(security_level_num, "Unknown")
        
#         date_apprehended_str = request.form.get('Apprehended')
#         date_apprehended = datetime.strptime(date_apprehended_str, "%Y-%m-%d").date() if date_apprehended_str else None
        
#         current_date = datetime.utcnow().date()
#         marital_status = request.form.get('marital_status')
#         inmate_status = request.form.get('inmate_status', 'In Custody')
#         home_address = request.form.get('home-address')
        
#         mother_name_parts = [request.form.get('mother_last', ''), request.form.get('mother_first', ''), request.form.get('mother_initial', '')]
#         mother_name = " ".join([p.capitalize() for p in mother_name_parts if p.strip()]) or None
#         mother_contact = request.form.get('mother_contact') or None
#         mother_occupation = request.form.get('mother_occupation') or None
#         mother_age = request.form.get('mother_age') or None
#         mother_birthdate = request.form.get('mother_birthdate') or None
#         mother_origin_address = request.form.get('mother_origin') or None
        
#         father_name_parts = [request.form.get('father_last', ''), request.form.get('father_first', ''), request.form.get('father_initial', '')]
#         father_name = " ".join([p.capitalize() for p in father_name_parts if p.strip()]) or None
#         father_contact = request.form.get('father_contact') or None
#         father_occupation = request.form.get('father_occupation') or None
#         father_age = request.form.get('father_age') or None
#         father_birthdate = request.form.get('father_birthdate') or None
#         father_origin_address = request.form.get('father_origin') or None
        
#         mugshot_file = request.files.get('mugshot')
#         mugshot_filename = None
#         if mugshot_file and mugshot_file.filename != '':
#             ext = os.path.splitext(mugshot_file.filename)[1]
#             mugshot_filename = f"{uuid.uuid4().hex}{ext}"
#             mugshot_file.save(os.path.join(app.config['UPLOAD_FOLDER'], mugshot_filename))
            
#         evidence_file = request.files.get('fileInput')
#         evidence_filename = None
#         evidence_original_name = None

#         if evidence_file and evidence_file.filename != '':
#             evidence_original_name = evidence_file.filename
#             ext = os.path.splitext(evidence_file.filename)[1]
#             evidence_filename = f"{uuid.uuid4().hex}{ext}"
#             evidence_file.save(os.path.join(app.config['UPLOAD_FOLDER'], evidence_filename))
        
#         inmate = Inmate(
#             name=name,
#             age=age,
#             gender=gender,
#             nationality=nationality,
#             security_level=security_level_str,
#             date_apprehended=date_apprehended,
#             date_added=current_date,
#             marital_status=marital_status,
#             inmate_status=inmate_status,
#             mother_name=mother_name,
#             mother_birthdate=mother_birthdate,
#             mother_occupation=mother_occupation,
#             mother_origin_address=mother_origin_address,
#             mother_contact=mother_contact,
#             mother_age=mother_age,
#             father_name=father_name,
#             father_birthdate=father_birthdate,
#             father_occupation=father_occupation,
#             father_origin_address=father_origin_address,
#             father_age=father_age,
#             father_contact=father_contact,
#             home_address=home_address,
#             mugshot=mugshot_filename,
#             evidence_file=evidence_filename,
#         )
        
#         db.session.add(inmate)
#         db.session.commit()
        
#         case_records_json = request.form.get('case_records_json')
#         total_fine = 0
#         if case_records_json:
#             case_records = json.loads(case_records_json)
#             for record in case_records:
#                 conviction_years = int(record.get('years', 0))
#                 fine_amount = float(record.get('fine', 0))
#                 total_fine += fine_amount

#                 new_record = InmateRecord(
#                     inmate_id=inmate.id,
#                     crime_description=record.get('crime', ''),
#                     conviction_years=conviction_years,
#                     address_convicted=record.get('addressCommitted', ''),
#                     fine=str(fine_amount),
#                     court=record.get('court', ''),
#                     status=record.get('status', 'Pending'),
#                     remarks=record.get('remarks', ''),
#                     date_of_record=datetime.strptime(record.get('currentDate'), "%Y-%m-%d").date() if record.get('currentDate') else datetime.utcnow().date()
#                 )
#                 db.session.add(new_record)

#         inmate.bail_fund = total_fine if total_fine > 0 else 0
        
#         db.session.commit()
#         flash('Inmate added successfully!', 'success')
#         return redirect(url_for('dashboard'))
    
#     return render_template('add.html', nationalities=nationalities)


# @app.route('/system_description')
# def system_description():
#     if 'username' not in session:
#         return redirect(url_for('dashboard'))
#     return render_template('system_description.html')

# @app.route('/user_approval', methods=['GET', 'POST'])
# def user_approval():
#     if session.get('approved', 0) < 2:
#         flash("Access denied: Admins only.", "danger")
#         return redirect(url_for('dashboard'))

#     current_user_id = session.get('user_id')

#     if request.method == 'POST':
#         if 'delete_user' in request.form:
#             user_id = int(request.form['delete_user'])
#             user_to_delete = User.query.get(user_id)
#             if user_to_delete and user_to_delete.id != current_user_id:
#                 db.session.delete(user_to_delete)
#                 db.session.commit()
#                 flash(f"User '{user_to_delete.username}' deleted successfully.", "success")
#             else:
#                 flash("Cannot delete your own account or invalid user.", "warning")
#             return redirect(url_for('user_approval'))
        
#         users = User.query.all()

#         for user in users:
#             if user.id == current_user_id:
#                 continue 

#             if f'approved_{user.id}' in request.form:
#                 user.approved = 0
#             else:
#                 user.approved = 1

#             admin_level = request.form.get(f'admin_level_{user.id}')
#             if admin_level and session.get('approved', 0) == 2:
#                 user.approved = int(admin_level)

#             access_value = request.form.get(f'access_{user.id}')
#             if access_value is not None:
#                 user.system_access = int(access_value)

#         db.session.commit()
#         flash("User updates saved successfully.", "success")
#         return redirect(url_for('user_approval'))

#     pending_users = User.query.order_by(User.approved.asc()).all()
#     return render_template('user_approval.html', pending_users=pending_users)


# @app.route('/search', methods=['GET'])
# def search_inmates():
#     if 'username' not in session:
#         return redirect(url_for('index'))

#     query = request.args.get('q', '').strip().lower()
#     all_inmates = Inmate.query.order_by(Inmate.date_added.desc()).all()

#     if query:
#         matches = []
#         non_matches = []
#         for inmate in all_inmates:
#             if (query.isdigit() and int(query) == inmate.id) or (query in inmate.name.lower()):
#                 matches.append(inmate)
#             else:
#                 non_matches.append(inmate)
#         inmates = matches + non_matches
#     else:
#         inmates = all_inmates

#     return render_template('dashboard.html', posts=inmates, nationalities=nationalities)

@app.route('/admin_dashboard')
def admin_dashboard():
    if 'user_id' not in session or session.get('role') != 'admin':
        flash("Unauthorized access", "danger")
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    return render_template('admin_dashboard.html', user=user)

@app.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    email = request.form['email']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Account does not exist!.", "danger")
        return render_template('login.html', error="User not found. Please register first.")

    if user.access == "Inactive":
        flash("Account disable contact support, or make a new account!", "danger")
        return render_template('login.html', error="Your account is disabled ask for access.")

    if not user.check_password(password):
        flash("Incorrect password or email!", "danger")
        return render_template('login.html', error="Incorrect password or email. Please try again.")

    session['user_id'] = user.id
    session['email'] = email
    session['role'] = user.role
    session['username'] = user.username

    if user.role == "admin":
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

@app.route('/register', methods=['POST'])
def register():
    
    name_parts = [request.form.get('last', ''), request.form.get('first', '')]
    username = " ".join([p.capitalize() for p in name_parts if p.strip()]).strip()
    password = request.form['password']
    email = request.form['email']

    existing_user = User.query.filter_by(email=email).first()
    
    if existing_user:
        flash("Email already exists. Please choose a different one.", "danger")
        return render_template('login.html', error="Email already exists. Please choose a different one.")

    new_user = User(username=username, email=email, access='active')
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful!", "success")
    return render_template('user_dashboard.html', alert_message="Registration successful!")
    

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('index'))

# @app.route('/view/<int:inmate_id>')
# def view_inmate(inmate_id):
#     if 'username' not in session:
#         return redirect(url_for('index'))

#     inmate = Inmate.query.get_or_404(inmate_id)
#     return render_template('view.html', inmate=inmate)

# @app.route('/inmate/delete/<int:inmate_id>', methods=['POST'])
# def delete_inmate(inmate_id):
#     if 'username' not in session:
#         return redirect(url_for('index'))

#     inmate = Inmate.query.get_or_404(inmate_id)

#     if inmate.evidence_file:
#         file_path = os.path.join(app.config['UPLOAD_FOLDER'], inmate.evidence_file)
#         if os.path.exists(file_path):
#             os.remove(file_path)

#     db.session.delete(inmate)
#     db.session.commit()
#     flash('Inmate deleted successfully!', 'success')
#     return redirect(url_for('dashboard'))

# @app.route('/inmate/edit/<int:inmate_id>', methods=['GET', 'POST'])
# def edit_inmate(inmate_id):
#     if 'username' not in session:
#         return redirect(url_for('index'))

#     inmate = Inmate.query.get_or_404(inmate_id)

#     SECURITY_LEVELS = {
#         1: "Low Security",
#         2: "Medium Security",
#         3: "High Security",
#         4: "Maximum Security",
#         5: "Death Row"
#     }

#     if request.method == 'POST':
#         try:
#             last = request.form.get("last", "").capitalize()
#             first = request.form.get("first", "").capitalize()
#             initial = request.form.get("initial", "").capitalize()
#             inmate.name = f"{last} {first} {initial}".strip()

#             inmate.age = int(request.form.get("age", inmate.age))
#             inmate.gender = request.form.get("gender", inmate.gender)
#             inmate.nationality = request.form.get("nationality", inmate.nationality)

#             sec_num = int(request.form.get("security_level", 1))
#             inmate.security_level = SECURITY_LEVELS.get(sec_num, inmate.security_level)

#             apprehended_str = request.form.get("Apprehended")
#             if apprehended_str:
#                 inmate.date_apprehended = datetime.strptime(apprehended_str, "%Y-%m-%d").date()

#             inmate.marital_status = request.form.get("marital_status") or inmate.marital_status or "Single"
#             inmate.inmate_status = request.form.get("inmate_status") or inmate.inmate_status or "Active"
#             inmate.home_address = request.form.get("home_address") or inmate.home_address or "N/A"
            
#             mugshot_file = request.files.get("mugshot")
#             if mugshot_file and mugshot_file.filename:

#                 filename = secure_filename(mugshot_file.filename)
#                 upload_folder = app.config.get("UPLOAD_FOLDER", "static/uploads")

#                 os.makedirs(upload_folder, exist_ok=True)
#                 file_path = os.path.join(upload_folder, filename)
#                 mugshot_file.save(file_path)

#                 inmate.mugshot = filename

#             with db.session.no_autoflush:
#                 existing_records = {str(r.id): r for r in inmate.records}

#                 record_ids = request.form.getlist("record_id[]")
#                 crimes = request.form.getlist("crime_description[]")
#                 addresses = request.form.getlist("address_committed[]")
#                 convictions = request.form.getlist("conviction_years[]")
#                 fines = request.form.getlist("fine[]")
#                 courts = request.form.getlist("court_branch[]")
#                 statuses = request.form.getlist("status[]")
#                 record_dates = request.form.getlist("record_date[]")
#                 remarks_list = request.form.getlist("remarks[]")

#                 received_ids = set()

#                 for i in range(len(crimes)):
#                     rid = record_ids[i]

#                     if not crimes[i].strip():
#                         continue

#                     if rid and rid in existing_records:
#                         rec = existing_records[rid]
#                         received_ids.add(rid)
#                         rec.crime_description = crimes[i]
#                         rec.address_convicted = addresses[i]
#                         rec.conviction_years = int(convictions[i] or 0)
#                         rec.fine = str(fines[i] or 0)
#                         rec.court = courts[i]
#                         rec.status = statuses[i]
#                         rec.date_of_record = datetime.strptime(record_dates[i], "%Y-%m-%d").date()
#                         rec.remarks = remarks_list[i]
#                     else:
#                         new_rec = InmateRecord(
#                             inmate_id=inmate.id,
#                             crime_description=crimes[i],
#                             address_convicted=addresses[i],
#                             conviction_years=int(convictions[i] or 0),
#                             fine=str(fines[i] or 0),
#                             court=courts[i],
#                             status=statuses[i],
#                             date_of_record=datetime.strptime(record_dates[i], "%Y-%m-%d").date(),
#                             remarks=remarks_list[i]
#                         )
#                         db.session.add(new_rec)

#                 if record_ids:
#                     for rid, record in existing_records.items():
#                         if rid not in received_ids:
#                             db.session.delete(record)
#                 else:
#                     print("⚠️ No record_id[] received; preserving existing records.")

#             db.session.commit()
#             flash("✅ Inmate updated successfully!", "success")
#             return redirect(url_for("dashboard"))

#         except IntegrityError as e:
#             db.session.rollback()
#             flash(f"⚠️ Database integrity error: {e}", "danger")
#         except Exception as e:
#             db.session.rollback()
#             flash(f"⚠️ Unexpected error: {e}", "danger")

#     name_parts = inmate.name.split()

#     if len(name_parts) == 3:
#         last, first, initial = name_parts
#     elif len(name_parts) == 2:
#         last, first = name_parts
#         initial = ""
#     elif len(name_parts) == 1:
#         last = name_parts[0]
#         first = ""
#         initial = ""
#     else:
#         last = first = initial = ""

#     sec_map = {v: k for k, v in SECURITY_LEVELS.items()}
#     current_security_level = sec_map.get(inmate.security_level, 1)

#     case_records = InmateRecord.query.filter_by(inmate_id=inmate.id).all()
#     case_records_data = [
#         {
#             "id": rec.id,
#             "case_number": getattr(rec, "case_number", ""),
#             "crime": rec.crime_description,
#             "addressCommitted": rec.address_convicted,
#             "convictionYears": rec.conviction_years,
#             "fine": rec.fine,
#             "court": rec.court,
#             "status": rec.status,
#             "recordDate": rec.date_of_record.strftime("%Y-%m-%d") if rec.date_of_record else "",
#             "remarks": rec.remarks,
#         }
#         for rec in case_records
#     ]

#     return render_template(
#         "edit_inmate.html",
#         inmate=inmate,
#         last=last,
#         first=first,
#         initial=initial,
#         case_records=case_records_data,
#         nationalities=nationalities,
#         current_security_level=current_security_level
#     )

# @app.route("/inmate/<int:inmate_id>/add_record", methods=["POST"])
# def add_inmate_record(inmate_id):
#     inmate = Inmate.query.get_or_404(inmate_id)

#     try:
#         crime = request.json.get("crime")
#         address = request.json.get("addressCommitted")
#         years = int(request.json.get("convictionYears") or 0)
#         fine = str(request.json.get("fine") or 0)
#         court = request.json.get("court")
#         status = request.json.get("status")
#         record_date_str = request.json.get("recordDate")
#         record_date = datetime.strptime(record_date_str, "%Y-%m-%d").date() if record_date_str else datetime.today().date()
#         remarks = request.json.get("remarks") or ""

#         new_rec = InmateRecord(
#             inmate_id=inmate.id,
#             crime_description=crime,
#             address_convicted=address,
#             conviction_years=years,
#             fine=fine,
#             court=court,
#             status=status,
#             date_of_record=record_date,
#             remarks=remarks
#         )
#         db.session.add(new_rec)
#         db.session.commit()

#         return jsonify({
#             "success": True,
#             "record": {
#                 "id": new_rec.id,
#                 "crime": new_rec.crime_description,
#                 "addressCommitted": new_rec.address_convicted,
#                 "convictionYears": new_rec.conviction_years,
#                 "fine": new_rec.fine,
#                 "court": new_rec.court,
#                 "status": new_rec.status,
#                 "recordDate": new_rec.date_of_record.strftime("%Y-%m-%d"),
#                 "remarks": new_rec.remarks
#             }
#         })
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"success": False, "error": str(e)}), 500
    
# @app.route("/inmate/<int:inmate_id>/delete_record/<int:record_id>", methods=["POST"])
# def delete_inmate_record(inmate_id, record_id):
#     inmate = Inmate.query.get_or_404(inmate_id)
#     record = InmateRecord.query.filter_by(id=record_id, inmate_id=inmate.id).first()
#     if not record:
#         return jsonify({"success": False, "error": "Record not found"}), 404
#     try:
#         db.session.delete(record)
#         db.session.commit()
#         return jsonify({"success": True})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"success": False, "error": str(e)}), 500

    
# @app.route("/inmate/<int:inmate_id>/edit_record/<int:record_id>", methods=["PATCH"])
# def edit_inmate_record(inmate_id, record_id):
#     inmate = Inmate.query.get_or_404(inmate_id)
#     record = InmateRecord.query.filter_by(id=record_id, inmate_id=inmate.id).first()
#     if not record:
#         return jsonify({"success": False, "error": "Record not found"}), 404

#     data = request.json
#     try:
#         record.crime_description = data.get("crime", record.crime_description)
#         record.address_convicted = data.get("addressCommitted", record.address_convicted)
#         record.conviction_years = int(data.get("convictionYears", record.conviction_years))
#         record.fine = str(data.get("fine", record.fine))
#         record.court = data.get("court", record.court)
#         record.status = data.get("status", record.status)
#         record.date_of_record = datetime.strptime(data.get("recordDate"), "%Y-%m-%d").date() if data.get("recordDate") else record.date_of_record
#         record.remarks = data.get("remarks", record.remarks)

#         db.session.commit()
#         return jsonify({"success": True})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':

    with app.app_context():
        db.create_all()
        db.session.commit()

    app.run(debug=True)
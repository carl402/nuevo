from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name or ''}".strip()

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    iterations = db.Column(db.Integer, default=1000)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    variables = db.relationship("Variable", backref="project", cascade="all, delete-orphan")
    reports = db.relationship("Report", backref="project", cascade="all, delete-orphan")


class Variable(db.Model):
    __tablename__ = "project_variables"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    distribution = db.Column(db.String(50), nullable=False)
    mean = db.Column(db.Numeric(15, 6))
    std_dev = db.Column(db.Numeric(15, 6))
    min_value = db.Column(db.Numeric(15, 6))
    max_value = db.Column(db.Numeric(15, 6))
    mode_value = db.Column(db.Numeric(15, 6))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def params(self):
        if self.distribution == "normal":
            return {"mean": float(self.mean or 0), "std": float(self.std_dev or 1)}
        elif self.distribution == "uniform":
            return {"low": float(self.min_value or 0), "high": float(self.max_value or 1)}
        elif self.distribution == "triangular":
            return {"left": float(self.min_value or 0), "mode": float(self.mode_value or 0.5), "right": float(self.max_value or 1)}
        return {}


class Report(db.Model):
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    deleted_at = db.Column(db.DateTime, nullable=True)

    @property
    def results(self):
        result = SimulationResult.query.filter_by(report_id=self.id).first()
        if result:
            return {
                "summary": {
                    "mean": float(result.mean_value or 0),
                    "std": float(result.std_dev or 0),
                    "variance": float(result.variance_value or 0),
                    "min": float(result.min_value or 0),
                    "max": float(result.max_value or 0),
                    "median": float(result.median_value or 0),
                    "percentile_5": float(result.percentile_5 or 0),
                    "percentile_95": float(result.percentile_95 or 0)
                }
            }
        return {"summary": {}}


class SimulationResult(db.Model):
    __tablename__ = "simulation_results"
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable=False)
    mean_value = db.Column(db.Numeric(15, 6))
    std_dev = db.Column(db.Numeric(15, 6))
    variance_value = db.Column(db.Numeric(15, 6))
    min_value = db.Column(db.Numeric(15, 6))
    max_value = db.Column(db.Numeric(15, 6))
    percentile_5 = db.Column(db.Numeric(15, 6))
    percentile_95 = db.Column(db.Numeric(15, 6))
    median_value = db.Column(db.Numeric(15, 6))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
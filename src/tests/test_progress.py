import sys
import os
import joblib

# Add parent directory to path so we can import the model class
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from model_training import EqualFeatureImportanceClassifier

# Load the model using relative path
script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "..", "models", "student_performance_model.pkl")

try:
    model = joblib.load(model_path)
    print("[OK] Model loaded successfully!")
except Exception as e:
    print(f"[ERROR] Error loading model: {e}")

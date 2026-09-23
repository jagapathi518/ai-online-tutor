# Student_Progress_Tracking_System.py
import pandas as pd
import os
from typing import Dict, Optional

# Get the directory of the current script for relative paths
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_SCRIPT_DIR, "data")

def get_student_progress(student_id: str, subject: str) -> Dict[str, float]:
    """
    Get student progress for a subject from progress tracking CSV.
    Returns completion rate and average score.
    """
    try:
        # Read progress data (create empty DataFrame if file doesn't exist)
        try:
            progress_df = pd.read_csv(os.path.join(_DATA_DIR, "student_progress.csv"))
        except FileNotFoundError:
            return {"completion_rate": 0.0, "average_score": 0.0}
        
        # Filter by student and subject
        student_progress = progress_df[
            (progress_df["student_id"] == student_id) & 
            (progress_df["subject"] == subject)
        ]
        
        if not student_progress.empty:
            return {
                "completion_rate": student_progress["completion_rate"].values[0],
                "average_score": student_progress["average_score"].values[0],
                "completed_materials": student_progress["completed_materials"].values[0].split("|")
            }
        return {"completion_rate": 0.0, "average_score": 0.0, "completed_materials": []}
    
    except Exception as e:
        print(f"Error reading progress: {e}")
        return {"completion_rate": 0.0, "average_score": 0.0, "completed_materials": []}

def update_progress(student_id: str, subject: str, score: float, completed_material: str):
    """
    Update or create student progress record
    """
    try:
        # Try to read existing data
        try:
            progress_df = pd.read_csv(os.path.join(_DATA_DIR, "student_progress.csv"))
        except FileNotFoundError:
            progress_df = pd.DataFrame(columns=[
                "student_id", "subject", "completion_rate", 
                "average_score", "completed_materials"
            ])
        
        # Update or add record
        mask = (progress_df["student_id"] == student_id) & (progress_df["subject"] == subject)
        if mask.any():
            # Update existing
            idx = mask.idxmax()
            progress_df.at[idx, "average_score"] = score
            completed = set(progress_df.at[idx, "completed_materials"].split("|"))
            completed.add(completed_material)
            progress_df.at[idx, "completed_materials"] = "|".join(completed)
            progress_df.at[idx, "completion_rate"] = len(completed) / 10.0  # Assuming 10 materials per subject
        else:
            # Add new
            new_record = {
                "student_id": student_id,
                "subject": subject,
                "average_score": score,
                "completed_materials": completed_material,
                "completion_rate": 0.1  # 1/10 completed
            }
            progress_df = pd.concat([progress_df, pd.DataFrame([new_record])], ignore_index=True)
        
        progress_df.to_csv(os.path.join(_DATA_DIR, "student_progress.csv"), index=False)
        return True
    
    except Exception as e:
        print(f"Error updating progress: {e}")
        return False
# recommendation_engine.py
from typing import Dict, List, Optional, Union
from study_materials import get_study_materials
from Adaptive_Learning_Content_Generator import AdaptiveLearningContentGenerator

# At the top of recommendation_engine.py
try:
    from Student_Progress_Tracking_System import get_student_progress
except ImportError:
    # Fallback for development
    def get_student_progress(student_id: str, subject: str) -> dict:
        return {
            "completion_rate": 0.0,
            "average_score": 0.0,
            "completed_materials": []
        }
        
class StudyMaterialRecommender:
    def __init__(self):
        self.content_generator = AdaptiveLearningContentGenerator()
        self.study_materials = get_study_materials()
        self._initialize_default_materials()
        
    def _initialize_default_materials(self) -> None:
        """Ensure default subjects and materials exist."""
        if 'English' not in self.study_materials:
            self.study_materials['English'] = {
                'beginner': [
                    {'title': 'Basic Grammar', 'description': 'Fundamentals of English grammar', 
                     'url': 'https://uniathena.com/lms/student-dashboard/course-landing/1075/fundamentals-of-english-grammar'},
                    {'title': 'Vocabulary Building', 'description': 'Essential vocabulary for beginners', 
                     'url': 'https://123bien.com/vocabulary/'}
                ],
                'intermediate': [
                    {'title': 'Intermediate Composition', 'description': 'Improve your writing skills', 
                     'url': 'https://www.cambridgeenglish.org/learning-english/free-resources/write-and-improve/'},
                    {'title': 'Reading Comprehension', 'description': 'Techniques for better understanding', 
                     'url': 'https://learnenglish.britishcouncil.org/english-levels/improve-your-english-level'}
                ],
                'advanced': [
                    {'title': 'Advanced Literature', 'description': 'Analysis of complex literary works', 
                     'url': 'https://writing.wisc.edu/handbook/closereading/'},
                    {'title': 'Academic Writing', 'description': 'Professional and scholarly writing techniques', 
                     'url': 'https://slc.berkeley.edu/writing-worksheets-and-other-writing-resources/nine-basic-ways-improve-your-style-academic-writing'}
                ]
            }
    
    def map_learning_speed_to_level(self, learning_speed: str) -> str:
        """Maps learning speed to a difficulty level with validation."""
        speed_to_level = {
            'slow': 'beginner',
            'medium': 'intermediate',
            'fast': 'advanced'
        }
        return speed_to_level.get(learning_speed.lower(), 'intermediate')
    
    def _get_student_learning_speed(self, student_id: str, subject: str) -> str:
        """Determine learning speed based on student progress."""
        progress = get_student_progress(student_id, subject)
        
        if not progress:
            return 'medium'  # Default if no progress data
        
        completion_rate = progress.get('completion_rate', 0.5)
        avg_score = progress.get('average_score', 70)
        
        if completion_rate > 0.8 and avg_score > 85:
            return 'fast'
        elif completion_rate < 0.5 or avg_score < 60:
            return 'slow'
        return 'medium'
    
    def recommend_materials(
        self, 
        subject: str, 
        learning_speed: Optional[str] = None, 
        student_id: Optional[str] = None
    ) -> Optional[Dict[str, Union[str, List[Dict]]]]:
        """
        Recommends study materials with adaptive content.
        
        Args:
            subject: The subject area (e.g., 'Mathematics')
            learning_speed: Optional manual override ('slow', 'medium', 'fast')
            student_id: Optional student ID for personalized recommendations
            
        Returns:
            Dictionary with recommendations or None if subject not found
        """
        # Validate subject exists
        if subject not in self.study_materials:
            available_subjects = list(self.study_materials.keys())
            raise ValueError(
                f"Subject '{subject}' not found. Available subjects: {', '.join(available_subjects)}"
            )
        
        # Determine learning speed (priority: manual > student progress > default)
        if learning_speed is None and student_id:
            learning_speed = self._get_student_learning_speed(student_id, subject)
        elif learning_speed is None:
            learning_speed = 'medium'
        
        level = self.map_learning_speed_to_level(learning_speed)
        
        # Get base materials and filter by completion if student_id provided
        materials = self.study_materials[subject].get(level, [])
        if student_id:
            completed = get_student_progress(student_id, subject).get('completed_materials', [])
            materials = [m for m in materials if m['url'] not in completed]
        
        # Generate adaptive content
        adaptive_content = self.content_generator.generate_adaptive_content(
            subject=subject, 
            learning_speed=learning_speed,
            student_level=level
        )
        
        return {
            "student_level": level,
            "learning_speed": learning_speed,
            "subject": subject,
            "recommended_materials": materials,
            "adaptive_content": {
                "topic": subject,
                "subject": subject,
                "complexity_level": adaptive_content['complexity_level'],
                "content": adaptive_content['content']
            }
        }
    
    def batch_recommend(
        self, 
        subjects: List[str], 
        student_id: str
    ) -> Dict[str, Dict[str, Union[str, List[Dict]]]]:
        """Get recommendations for multiple subjects."""
        return {
            subject: self.recommend_materials(subject, student_id=student_id)
            for subject in subjects
        }

# Usage examples
def main():
    recommender = StudyMaterialRecommender()
    

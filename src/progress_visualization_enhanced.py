import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Get the directory of the current script for relative paths
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DATA_DIR = os.path.join(_SCRIPT_DIR, "data")
_ASSETS_DIR = os.path.join(_SCRIPT_DIR, "..", "assets")

class EnhancedProgressVisualizer:
    def __init__(self, student_id):
        self.student_id = student_id
        self.progress_file = os.path.join(_DATA_DIR, f'student_progress_{student_id}.csv')
    
    def comprehensive_progress_analysis(self):
        """
        Perform comprehensive progress analysis with multiple visualizations
        """
        # Read the progress data
        df = pd.read_csv(self.progress_file)
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Create a multi-panel visualization
        plt.figure(figsize=(15, 10))
        
        # 1. Score Progression with Trend Line
        plt.subplot(2, 2, 1)
        plt.plot(df['date'], df['test_score'], marker='o')
        plt.title('Test Score Progression')
        plt.xlabel('Date')
        plt.ylabel('Test Score')
        plt.xticks(rotation=45)
        
        # Add trend line
        z = np.polyfit(range(len(df)), df['test_score'], 1)
        p = np.poly1d(z)
        plt.plot(df['date'], p(range(len(df))), "r--", label='Trend Line')
        
        # 2. Subjects Distribution Pie Chart
        plt.subplot(2, 2, 2)
        subjects = df['subjects_tested'].str.split(', ', expand=True).stack()
        subject_counts = subjects.value_counts()
        plt.pie(subject_counts, labels=subject_counts.index, autopct='%1.1f%%')
        plt.title('Subjects Tested Distribution')
        
        # 3. Study Time vs Test Score Scatter Plot
        plt.subplot(2, 2, 3)
        plt.scatter(df['time_spent_studying'], df['test_score'])
        plt.title('Study Time vs Test Score')
        plt.xlabel('Time Spent Studying (Hours)')
        plt.ylabel('Test Score')
        
        # 4. Level Progression Bar Chart
        plt.subplot(2, 2, 4)
        level_progression = df['predicted_level'].value_counts()
        level_progression.plot(kind='bar')
        plt.title('Learning Level Progression')
        plt.xlabel('Learning Level')
        plt.ylabel('Number of Tests')
        
        plt.tight_layout()
        output_dir = os.path.join(_ASSETS_DIR)
        os.makedirs(output_dir, exist_ok=True)
        plt.savefig(os.path.join(output_dir, f'comprehensive_analysis_{self.student_id}.png'))
        plt.close()
        
        # Generate detailed statistical report
        report = {
            'total_tests': len(df),
            'average_score': df['test_score'].mean(),
            'score_improvement': self.calculate_score_improvement(df),
            'study_time_correlation': self.calculate_study_time_correlation(df)
        }
        
        return report
    
    def calculate_score_improvement(self, df):
        """
        Calculate overall score improvement
        """
        if len(df) < 2:
            return 0
        first_score = df.iloc[0]['test_score']
        last_score = df.iloc[-1]['test_score']
        improvement_percentage = ((last_score - first_score) / first_score) * 100
        return improvement_percentage
    
    def calculate_study_time_correlation(self, df):
        """
        Calculate correlation between study time and test score
        """
        correlation = df['time_spent_studying'].corr(df['test_score'])
        return correlation

# Example Usage
def main():
    # Create visualizer for a student
    visualizer = EnhancedProgressVisualizer('ST001')
    
    # Generate comprehensive analysis
    analysis_report = visualizer.comprehensive_progress_analysis()
    
    # Print detailed report
    print("Comprehensive Progress Analysis Report:")
    for key, value in analysis_report.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
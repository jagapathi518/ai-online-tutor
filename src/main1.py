import streamlit as st
import joblib
import os
import pandas as pd
import numpy as np
from recommendation_engine import StudyMaterialRecommender
from model_training import EqualFeatureImportanceClassifier

# Load the trained model and encoders
@st.cache_resource
def load_model_and_encoders():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        models_dir = os.path.join(script_dir, "models")
        model = joblib.load(os.path.join(models_dir, "student_performance_model.pkl"))
        encoders = joblib.load(os.path.join(models_dir, "label_encoders.pkl"))
        return model, encoders
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None, None

# Function to predict the student's next level
def predict_next_level(model, encoders, age, test_score, learning_speed, knowledge_level):
    if model is None or encoders is None:
        return "Error: Model could not be loaded."
    
    # Get the encoders and scaler
    knowledge_encoder = encoders['knowledge_encoder']
    learning_encoder = encoders['learning_encoder']
    target_encoder = encoders['target_encoder']
    scaler = encoders['scaler']
    
    # Build a DataFrame matching the training format
    input_df = pd.DataFrame([{
        'Age': age,
        'Last_Test_Score': test_score,
        'Knowledge_Level': knowledge_level,
        'Learning_Speed': learning_speed
    }])
    
    # Encode categorical variables (string -> number)
    input_df['Knowledge_Level'] = knowledge_encoder.transform(input_df['Knowledge_Level'])
    input_df['Learning_Speed'] = learning_encoder.transform(input_df['Learning_Speed'])
    
    # Scale numerical features
    input_df[['Age', 'Last_Test_Score']] = scaler.transform(input_df[['Age', 'Last_Test_Score']])
    
    # Predict and decode back to label
    prediction = model.predict(input_df)
    predicted_level = target_encoder.inverse_transform(prediction)[0]
    
    return predicted_level

# Function to provide study material based on subject & level
def get_study_material(subject, level):
    study_materials = {
        "Mathematics": {
            "Beginner": "Math Basics.pdf",
            "Intermediate": "Algebra & Geometry.pdf",
            "Advanced": "Calculus & Trigonometry.pdf",
        },
        "Science": {
            "Beginner": "Science Fundamentals.pdf",
            "Intermediate": "Physics & Chemistry.pdf",
            "Advanced": "Advanced Biology & Physics.pdf",
        },
        "English": {
            "Beginner": "Grammar Basics.pdf",
            "Intermediate": "Essay Writing.pdf",
            "Advanced": "Advanced Literature.pdf",
        },
    }
    return study_materials.get(subject, {}).get(level, "No study material available.")

def main():
    st.set_page_config(page_title="Adaptive Learning System", layout="wide")
    
    # Load model and encoders
    model, encoders = load_model_and_encoders()
    
    st.title("🎓 Adaptive Learning System")
    st.markdown("This system provides personalized study materials and adaptive content.")
    
    # Create columns for layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Student Information")
        
        # Student inputs
        subject = st.selectbox(
            "Select Subject",
            ["Mathematics", "Science", "English"],
            index=1
        )
        
        learning_speed = st.selectbox(
            "Learning Speed",
            ["Slow", "Medium", "Fast"],
            index=0
        )
        
        age = st.slider("Age", 5, 15, 12)  # Updated age range to 5-15
        test_score = st.slider("Last Test Score (0-100)", 0, 100, 45)
        
        knowledge_level = st.selectbox(
            "Current Knowledge Level",
            ["Beginner", "Intermediate", "Advanced"],
            index=1
        )
        
        if st.button("Get Recommendations"):
            with st.spinner("Generating personalized recommendations..."):
                try:
                    # Predict student's next learning level
                    predicted_level = predict_next_level(model, encoders, age, test_score, learning_speed, knowledge_level)
                    
                    # Get study material
                    study_material = get_study_material(subject, predicted_level)
                    
                    # Initialize the recommendation engine
                    recommender = StudyMaterialRecommender()
                    
                    # Get recommendations
                    recommendations = recommender.recommend_materials(
                        subject=subject,
                        learning_speed=learning_speed.lower(),
                        student_id="sample_student"
                    )
                    
                    # Display results in col2
                    with col2:
                        st.header("Recommendation Results")
                        
                        # Basic prediction
                        st.subheader("📚 Learning Level Prediction")
                        st.success(f"Your predicted next study level is: **{predicted_level}**")
                        
                        # Basic study material
                        st.subheader("📖 Basic Study Material")
                        st.info(f"Recommended resource: **{study_material}**")
                        
                        # Personalized recommendations
                        st.subheader("🌟 Personalized Recommendations")
                        st.write(f"- **Learning speed:** {recommendations['learning_speed'].capitalize()}")
                        st.write(f"- **Recommended level:** {recommendations['student_level'].capitalize()}")
                        
                        # Recommended materials
                        st.subheader("📚 Recommended Materials")
                        for material in recommendations['recommended_materials']:
                            with st.expander(f"🔗 {material['title']}"):
                                st.write(material['description'])
                                st.markdown(f"[Open Resource]({material['url']})", unsafe_allow_html=True)
                        
                        # Adaptive learning content
                        st.subheader("🧠 Adaptive Learning Content")
                        adaptive_content = recommendations['adaptive_content']
                        with st.expander(f"📖 {adaptive_content['topic']} ({adaptive_content['complexity_level']} level)"):
                            st.write(adaptive_content['content'])
                
                except Exception as e:
                    st.error(f"Error generating recommendations: {e}")
                    st.warning("Showing basic recommendations only...")
                    
                    with col2:
                        st.header("Basic Recommendation")
                        predicted_level = predict_next_level(model, encoders, age, test_score, learning_speed, knowledge_level)
                        study_material = get_study_material(subject, predicted_level)
                        st.success(f"Your predicted next study level is: **{predicted_level}**")
                        st.info(f"Recommended resource: **{study_material}**")

if __name__ == "__main__":
    main()
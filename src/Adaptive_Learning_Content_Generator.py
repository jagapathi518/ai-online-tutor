import nltk
from nltk.tokenize import sent_tokenize
import random
import os

class AdaptiveLearningContentGenerator:
    def __init__(self):
        # Ensure necessary NLTK resources are available
        self.ensure_nltk_data()
        
        # Initialize dictionaries for word substitution
        self.initialize_dictionaries()
        
        # Initialize content database
        self.initialize_content_database()

    def initialize_dictionaries(self):
        """Initialize the dictionaries for word simplification and enhancement."""
        self.simple_words = {
            "polygon": "shape",
            "classified": "grouped",
            "metabolic": "body process",
            "generate": "make",
            "photosynthesis": "plant food-making process",
            "chloroplasts": "plant cells",
            "interior": "inside",
            "sum": "total",
            "chemical": "special",
            "carbon dioxide": "air",
            "glucose": "sugar",
            "oxygen": "air",
            "reactions": "changes",
            "chlorophyll": "green part",
            "metaphor": "comparison",
            "symbolism": "hidden meaning",
            "protagonist": "main character",
            "antagonist": "bad character",
            "narrative": "story",
            "literary": "book-related",
            "analyze": "look at closely",
            "interpret": "explain meaning",
            "alliteration": "same-sounding words",
            "syntax": "word order",
            "quadratic": "U-shaped",
            "equation": "math problem",
            "mitochondria": "energy parts",
            "eukaryotic": "complex cells",
            "prokaryotic": "simple cells",
            "metaphorically": "in a comparing way",
            "foreshadowing": "hints about the future",
            "imagery": "word pictures",
            "personification": "giving human traits",
            "hyperbole": "big exaggeration"
        }
        
        self.enhanced_words = {
            "shape": "geometrical structure",
            "grouped": "categorized based on properties",
            "body process": "biochemical reaction in living organisms",
            "make": "synthesize using complex mechanisms",
            "plant food-making process": "photosynthesis involving complex biochemical reactions",
            "angles": "interior angles",
            "sides": "line segments",
            "plants": "photosynthetic organisms",
            "sunlight": "electromagnetic radiation",
            "water": "H₂O molecules",
            "air": "atmospheric gases",
            "food": "carbohydrates and energy-rich compounds",
            "comparison": "metaphorical representation",
            "hidden meaning": "symbolic representation of abstract concepts",
            "main character": "central figure of the narrative",
            "story": "narrative structure with complex plot elements",
            "look at": "critically examine and deconstruct",
            "meaning": "thematic significance and contextual implications",
            "character": "literary figure with psychological depth",
            "writing": "composition with rhetorical techniques",
            "math problem": "mathematical equation",
            "energy parts": "mitochondria (the powerhouse of the cell)",
            "complex cells": "eukaryotic cells with membrane-bound organelles",
            "simple cells": "prokaryotic cells lacking nucleus",
            "U-shaped": "quadratic parabolic curve",
            "hints": "foreshadowing narrative devices",
            "word pictures": "vivid sensory imagery",
            "human traits": "anthropomorphic personification",
            "big exaggeration": "hyperbolic expression"
        }

    def initialize_content_database(self):
        """Initialize the content database with topics and their complexity levels."""
        self.content_database = {
            "Mathematics": {
                "basic": "Math is about numbers and shapes. You can add, subtract, multiply and divide numbers.",
                "intermediate": "Mathematics includes algebra, geometry, and calculus. It helps solve real-world problems.",
                "advanced": "Mathematics is the abstract science of number, quantity, and space, with rigorous proofs and theoretical frameworks."
            },
            "Science": {
                "basic": "Science is learning about the world. It includes plants, animals, and stars.",
                "intermediate": "Science covers biology, chemistry, and physics. It explains natural phenomena through experiments.",
                "advanced": "Science is a systematic enterprise that builds and organizes knowledge through testable explanations and predictions."
            },
            "English": {
                "basic": "English is about reading and writing. You learn words and how to make sentences.",
                "intermediate": "English includes grammar, literature, and composition. It develops communication skills.",
                "advanced": "English studies language structure, literary analysis, and rhetorical strategies across genres and periods."
            }
        }

    def ensure_nltk_data(self):
        """Ensure that required NLTK data is downloaded."""
        try:
            nltk.data.find('tokenizers/punkt_tab')
        except LookupError:
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                pass
            print("Downloading required NLTK data...")
            home_dir = os.path.expanduser("~")
            nltk_data_dir = os.path.join(home_dir, "nltk_data")
            os.makedirs(nltk_data_dir, exist_ok=True)
            try:
                nltk.download('punkt_tab', download_dir=nltk_data_dir, quiet=True)
            except Exception:
                nltk.download('punkt', download_dir=nltk_data_dir, quiet=True)
            print(f"Downloaded NLTK tokenizer to {nltk_data_dir}")

    def generate_adaptive_content(self, subject, learning_speed, student_level=None):
        """
        Generate adaptive learning content based on subject and learning speed.
        
        Args:
            subject (str): The subject area (e.g., 'Mathematics')
            learning_speed (str): 'slow', 'medium', or 'fast'
            student_level (str, optional): The student's current level
            
        Returns:
            dict: Dictionary containing topic, complexity level, and processed content
        """
        speed_map = {
            'slow': 'basic',
            'medium': 'intermediate',
            'fast': 'advanced'
        }

        # Normalize subject name to match database keys
        normalized_subject = subject.capitalize()
        if normalized_subject not in self.content_database:
            available_subjects = list(self.content_database.keys())
            normalized_subject = random.choice(available_subjects)
            print(f"Subject '{subject}' not found. Using '{normalized_subject}' instead.")

        complexity_level = speed_map.get(learning_speed.lower(), 'intermediate')
        
        try:
            content = self.content_database[normalized_subject][complexity_level]
            processed_content = self.process_content(content, learning_speed)
            
            return {
                "subject": normalized_subject,
                "complexity_level": complexity_level,
                "content": processed_content,
                "learning_speed": learning_speed,
                "student_level": student_level
            }
            
        except KeyError as e:
            print(f"Error generating content: {e}")
            return {
                "error": f"Could not generate content for {normalized_subject} at {complexity_level} level"
            }

    def process_content(self, content, learning_speed):
        """Process content to match the student's learning speed."""
        try:
            sentences = sent_tokenize(content)
            if not sentences:
                sentences = [content]
        except Exception as e:
            print(f"Error in sentence tokenization: {e}")
            sentences = [content]

        if learning_speed.lower() == 'slow':
            processed_sentences = [self.simplify_sentence(sentence) for sentence in sentences]
        elif learning_speed.lower() == 'fast':
            processed_sentences = [self.enhance_sentence(sentence) for sentence in sentences]
        else:
            processed_sentences = sentences

        return " ".join(processed_sentences)

    def simplify_sentence(self, sentence):
        """Simplify a sentence by reducing complex words."""
        result = sentence.lower()
        for complex_word, simple_word in self.simple_words.items():
            complex_word_lower = complex_word.lower()
            if complex_word_lower in result:
                result = result.replace(complex_word_lower, simple_word)
        if result:
            result = result[0].upper() + result[1:]
        return result

    def enhance_sentence(self, sentence):
        """Enhance a sentence by adding complexity and details."""
        result = sentence
        for simple_word, enhanced_word in self.enhanced_words.items():
            result = result.replace(simple_word, enhanced_word)
        return result

    def get_available_subjects(self):
        """Return a list of available subjects in the content database."""
        return list(self.content_database.keys())

    def add_subject(self, subject, basic_content, intermediate_content, advanced_content):
        """Add a new subject to the content database."""
        self.content_database[subject.capitalize()] = {
            "basic": basic_content,
            "intermediate": intermediate_content,
            "advanced": advanced_content
        }
        print(f"Added subject '{subject}' to the content database.")

def main():
    print("Initializing Adaptive Learning Content Generator...")
    generator = AdaptiveLearningContentGenerator()
    
    subjects = generator.get_available_subjects()
    print(f"Available subjects: {', '.join(subjects)}")
    
    speeds = ['slow', 'medium', 'fast']
    
    for subject in subjects:
        for speed in speeds:
            try:
                print(f"\n--- Generating {subject} Content for {speed.capitalize()} Learner ---")
                adaptive_content = generator.generate_adaptive_content(subject, speed)
                print(f"Complexity Level: {adaptive_content['complexity_level']}")
                print(adaptive_content['content'])
            except Exception as e:
                print(f"Error generating content for subject '{subject}' at speed '{speed}': {e}")

if __name__ == "__main__":
    main()
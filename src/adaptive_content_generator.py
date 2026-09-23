import nltk
import re

# Ensure these are downloaded
try:
    nltk.download('punkt', quiet=True)
except Exception:
    pass

class AdaptiveLearningContentGenerator:
    def __init__(self):
        """
        Initialize the adaptive learning content generator
        """
        self.complexity_levels = {
            'Beginner': {
                'sentence_length': (5, 10),
                'vocabulary_complexity': 'simple'
            },
            'Intermediate': {
                'sentence_length': (10, 15),
                'vocabulary_complexity': 'moderate'
            },
            'Advanced': {
                'sentence_length': (15, 25),
                'vocabulary_complexity': 'complex'
            }
        }
    
    def _custom_sentence_tokenize(self, text):
        """
        Custom sentence tokenization method
        
        Args:
        text (str): Input text
        
        Returns:
        list: List of sentences
        """
        # Split text into sentences using regex
        sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
        return [sentence.strip() for sentence in sentences if sentence.strip()]
    
    def simplify_content(self, text, learning_level):
        """
        Simplify content based on learning level
        
        Args:
        text (str): Original text
        learning_level (str): Student's learning level
        
        Returns:
        str: Simplified text
        """
        # Get complexity parameters
        complexity = self.complexity_levels[learning_level]
        
        # Tokenize sentences
        sentences = self._custom_sentence_tokenize(text)
        
        # Simplified sentences
        simplified_sentences = []
        
        for sentence in sentences:
            # Tokenize words
            words = sentence.split()
            
            # Adjust sentence length
            min_length, max_length = complexity['sentence_length']
            
            # Simplify based on complexity
            if complexity['vocabulary_complexity'] == 'simple':
                # Keep only most basic words
                words = [word for word in words if len(word) <= 6]
            elif complexity['vocabulary_complexity'] == 'moderate':
                # Keep medium-length words
                words = [word for word in words if 4 <= len(word) <= 8]
            
            # Truncate or pad to meet length requirements
            if len(words) < min_length:
                # Add simple filler words
                filler_words = ['is', 'are', 'a', 'the', 'of', 'in']
                while len(words) < min_length:
                    words.insert(0, filler_words[len(words) % len(filler_words)])
            
            if len(words) > max_length:
                words = words[:max_length]
            
            # Reconstruct sentence
            simplified_sentence = ' '.join(words)
            simplified_sentences.append(simplified_sentence)
        
        return ' '.join(simplified_sentences)
    
    def generate_adaptive_content(self, original_content, learning_level):
        """
        Generate adaptive content for different learning levels
        
        Args:
        original_content (str): Original study material
        learning_level (str): Student's learning level
        
        Returns:
        str: Adaptive content
        """
        # Simplify the content
        adaptive_content = self.simplify_content(original_content, learning_level)
        
        return adaptive_content

# Example Usage
def main():
    # Create an instance of the adaptive content generator
    content_generator = AdaptiveLearningContentGenerator()
    
    # Original content about triangles
    original_content = """
    A triangle is a polygon with three edges and three vertices. 
    The sum of the internal angles of a triangle is always 180 degrees. 
    Triangles can be classified based on their angles and side lengths into 
    equilateral, isosceles, and scalene triangles. Advanced geometric 
    principles demonstrate that the area of a triangle can be calculated 
    using various formulas depending on the known parameters.
    """
    
    # Generate adaptive content for different learning levels
    print("--- Beginner Level Content ---")
    beginner_content = content_generator.generate_adaptive_content(
        original_content, 
        'Beginner'
    )
    print(beginner_content)
    
    print("\n--- Intermediate Level Content ---")
    intermediate_content = content_generator.generate_adaptive_content(
        original_content, 
        'Intermediate'
    )
    print(intermediate_content)
    
    print("\n--- Advanced Level Content ---")
    advanced_content = content_generator.generate_adaptive_content(
        original_content, 
        'Advanced'
    )
    print(advanced_content)

if __name__ == "__main__":
    main()
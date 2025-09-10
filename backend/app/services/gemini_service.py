from typing import List, Dict
from dotenv import load_dotenv
import os
import json
import httpx

# Mock Gemini API for now as it requires actual API key
load_dotenv()

async def get_ai_analysis(weak_topics: List[Dict[str, str]]):
    """
    Get AI analysis for weak topics.
    
    For now, this is a mock implementation that returns predefined study plans.
    In a production environment, you would use a real AI API like Gemini.
    """
    # Format weak topics for better presentation
    formatted_topics = []
    for topic in weak_topics:
        formatted_topics.append(f"{topic['subject']}: {topic['topic']}")
    
    # Basic template responses for common subjects
    study_plans = {
        "Physics": {
            "Electromagnetism": """
# Study Plan for Electromagnetism

## Key Concepts to Review:
1. **Electric Fields and Forces**
   - Coulomb's Law
   - Electric field calculations
   - Field lines and their interpretation

2. **Magnetic Fields and Forces**
   - Magnetic field due to moving charges
   - Magnetic force on moving charges
   - Biot-Savart Law

3. **Electromagnetic Induction**
   - Faraday's Law
   - Lenz's Law
   - Self-inductance and mutual inductance

## Recommended Practice:
- Solve 10 problems on Coulomb's Law and superposition of electric forces
- Practice drawing field lines for different charge configurations
- Review the relationship between electricity and magnetism

## Resources:
- Chapter 21-24 in your textbook
- Online simulations for visualizing fields
- Practice tests focusing on quantitative problems
            """,
            "Optics": """
# Study Plan for Optics

## Key Concepts to Review:
1. **Reflection and Refraction**
   - Laws of reflection
   - Snell's Law
   - Total internal reflection

2. **Lenses and Mirrors**
   - Thin lens equation
   - Magnification
   - Ray diagrams

3. **Wave Optics**
   - Interference
   - Diffraction
   - Polarization

## Recommended Practice:
- Draw ray diagrams for converging and diverging lenses
- Solve numerical problems involving the lens equation
- Practice problems on interference and diffraction patterns

## Resources:
- Chapter 34-36 in your textbook
- Online simulations for ray tracing
- Video tutorials on wave optics phenomena
            """
        },
        "Chemistry": {
            "Organic Chemistry": """
# Study Plan for Organic Chemistry

## Key Concepts to Review:
1. **Functional Groups**
   - Identification and properties
   - Reactions of alcohols, aldehydes, ketones
   - Carboxylic acids and derivatives

2. **Reaction Mechanisms**
   - Nucleophilic substitution (SN1 & SN2)
   - Elimination reactions (E1 & E2)
   - Addition reactions

3. **Stereochemistry**
   - Chirality and optical activity
   - R/S configuration
   - Geometric isomerism

## Recommended Practice:
- Practice drawing mechanisms for common reactions
- Convert between different representations (skeletal, condensed, etc.)
- Identify stereochemical relationships between compounds

## Resources:
- Chapter 10-14 in your organic chemistry textbook
- Molecular model kits for 3D visualization
- Practice problems focusing on mechanisms
            """
        },
        "Mathematics": {
            "Integration": """
# Study Plan for Integration Techniques

## Key Concepts to Review:
1. **Basic Integration Methods**
   - Substitution technique
   - Integration by parts
   - Partial fractions

2. **Special Integrals**
   - Trigonometric integrals
   - Rational functions
   - Improper integrals

3. **Applications**
   - Area between curves
   - Volumes of revolution
   - Arc length

## Recommended Practice:
- Solve 20 problems covering different integration techniques
- Practice recognizing which technique to apply
- Work through applied problems involving physical scenarios

## Resources:
- Chapter 7-8 in your calculus textbook
- Online practice problems with solutions
- Video tutorials on complex integration examples
            """
        }
    }
    
    # Generate a custom study plan based on weak topics
    custom_plan = "# Personalized Study Plan\n\n"
    custom_plan += "Based on your test results, here's a personalized study plan to help you improve:\n\n"
    
    for topic_str in formatted_topics:
        parts = topic_str.split(": ")
        if len(parts) == 2:
            subject, topic = parts
            if subject in study_plans and topic in study_plans[subject]:
                custom_plan += study_plans[subject][topic]
            else:
                custom_plan += f"## {subject}: {topic}\n\n"
                custom_plan += "- Review the fundamental concepts in this area\n"
                custom_plan += "- Practice with sample problems of increasing difficulty\n"
                custom_plan += "- Consider forming a study group for this topic\n\n"
    
    custom_plan += "\n\n## General Study Tips:\n\n"
    custom_plan += "1. **Spaced Repetition**: Review these topics at increasing intervals\n"
    custom_plan += "2. **Active Recall**: Test yourself frequently, don't just read passively\n"
    custom_plan += "3. **Teach Others**: Explaining concepts solidifies your understanding\n"
    custom_plan += "4. **Connect Ideas**: Look for relationships between different topics\n"
    
    return {
        "study_plan": custom_plan,
        "weak_topics": formatted_topics
    }

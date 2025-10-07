#!/usr/bin/env python3
"""
CLI test script for Resume Gap Analyzer.
Use this to test the analysis function directly without MCP.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the analysis function
from server import analyze_resume_gaps


def main():
    """Run a test analysis."""

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment")
        print("Please set it in .env file or export it")
        sys.exit(1)

    # Example usage with sample resume
    sample_resumes_dir = Path(__file__).parent / "sample-resumes"

    # Find first .docx file in sample-resumes
    sample_files = list(sample_resumes_dir.glob("*.docx"))
    if not sample_files:
        print("Error: No .docx files found in sample-resumes/")
        print("Please add a resume file to test with")
        sys.exit(1)

    resume_path = str(sample_files[0].absolute())

    # Example job description
    job_description = """
    Senior Software Engineer

    We are seeking a Senior Software Engineer with 5+ years of experience in:
    - Python and Django/FastAPI
    - AWS cloud services (EC2, S3, Lambda, RDS)
    - React or Vue.js frontend development
    - CI/CD pipelines and DevOps practices
    - Leading technical projects and mentoring junior developers

    Required qualifications:
    - Bachelor's degree in Computer Science or related field
    - Strong problem-solving and communication skills
    - Experience with microservices architecture
    - Knowledge of containerization (Docker, Kubernetes)

    Preferred:
    - AWS certification
    - Experience with machine learning/AI
    - Open source contributions
    """

    print(f"Analyzing resume: {resume_path}")
    print(f"Against job description: Senior Software Engineer")
    print("-" * 60)

    try:
        # Run the analysis
        result = analyze_resume_gaps(resume_path, job_description)

        # Print results
        print(f"\n📊 Overall Match Score: {result.overall_match_score}%\n")

        print("🔴 Critical Gaps:")
        for gap in result.critical_gaps:
            print(f"  - [{gap.category}] {gap.gap}")
            print(f"    💡 {gap.recommendation}")

        print(f"\n🔑 Missing Keywords:")
        print(f"  Technical: {', '.join(result.missing_keywords.get('technical', []))}")
        print(f"  Soft Skills: {', '.join(result.missing_keywords.get('soft_skills', []))}")

        print(f"\n💪 Strengths to Highlight:")
        for strength in result.strengths_to_highlight:
            print(f"  - {strength.strength}: {strength.recommendation}")

        print(f"\n⚡ Quick Wins:")
        for win in result.quick_wins:
            print(f"  - {win}")

        print(f"\n📝 Summary:")
        print(f"  {result.summary}")

    except Exception as e:
        print(f"Error during analysis: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

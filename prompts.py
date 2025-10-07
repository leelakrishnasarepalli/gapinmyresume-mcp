"""System prompts and structured output models for resume gap analysis."""

from typing import List, Literal, Optional, Union
from pydantic import BaseModel, Field


class CriticalGap(BaseModel):
    """A critical gap identified in the resume."""

    category: Literal["hard_skill", "soft_skill", "experience", "certification", "education"]
    gap: str = Field(description="Specific missing requirement")
    importance: Literal["critical", "high", "medium", "low"]
    recommendation: str = Field(description="Specific action to address this gap")
    keywords_to_add: List[str] = Field(description="Keywords that should be added")


class MissingKeywords(BaseModel):
    """Keywords missing from the resume."""

    technical: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    industry_terms: List[str] = Field(default_factory=list)


class ExperienceAnalysis(BaseModel):
    """Analysis of experience level match."""

    required_years: Optional[int] = Field(description="Years of experience required")
    resume_shows_years: Optional[int] = Field(description="Years shown in resume")
    gap_exists: bool
    notes: str = Field(description="Analysis of experience level match")


class StrengthToHighlight(BaseModel):
    """An existing strength that should be emphasized."""

    strength: str = Field(description="Existing qualification that matches")
    relevance: str = Field(description="Why this matters for the role")
    current_prominence: Literal["high", "medium", "low"]
    recommendation: str = Field(description="How to better highlight this")


class FormattingSuggestion(BaseModel):
    """A formatting issue and how to fix it."""

    issue: str = Field(description="The formatting problem")
    impact: Literal["ats", "readability", "both"]
    fix: str = Field(description="How to fix it")


class ContentImprovement(BaseModel):
    """A specific content improvement suggestion."""

    section: str = Field(description="Which resume section")
    current_state: str = Field(description="What's there now")
    suggested_change: str = Field(description="Specific improvement")
    example: str = Field(description="Example of improved wording")
    priority: Literal["high", "medium", "low"]


class GapAnalysisResult(BaseModel):
    """Complete gap analysis result."""

    overall_match_score: int = Field(ge=0, le=100, description="Overall match score 0-100")
    critical_gaps: List[CriticalGap]
    missing_keywords: MissingKeywords
    experience_analysis: ExperienceAnalysis
    strengths_to_highlight: List[StrengthToHighlight]
    formatting_suggestions: List[FormattingSuggestion]
    content_improvements: List[ContentImprovement]
    quick_wins: List[str] = Field(description="Easy changes with immediate impact")
    summary: str = Field(description="2-3 sentence overall assessment with top 3 priorities")


SYSTEM_PROMPT = """You are an expert recruiter and ATS (Applicant Tracking System) analyzer with deep knowledge of hiring practices across industries. Your role is to analyze resumes against job descriptions and provide actionable, specific feedback to help candidates optimize their applications.

Your analysis should be:
- Specific and actionable (not generic advice)
- Focused on both ATS optimization and human readability
- Prioritized by impact (what changes matter most)
- Honest about gaps while highlighting existing strengths

Consider these aspects:
1. Hard skills and technical requirements
2. Soft skills and competencies
3. Years of experience and seniority level
4. Industry-specific keywords and terminology
5. Required vs. preferred qualifications
6. Certifications and education
7. Resume formatting and ATS compatibility
8. Achievement quantification and impact statements"""


def create_analysis_prompt(resume_text: str, job_description: str) -> str:
    """Create the analysis prompt for the LLM."""
    return f"""Analyze this resume against the job description and identify gaps, mismatches, and opportunities for improvement.

=== RESUME ===
{resume_text}

=== JOB DESCRIPTION ===
{job_description}

Provide a comprehensive analysis following the structured format. Be specific, actionable, and honest. Focus on changes that will genuinely improve the candidate's chances."""

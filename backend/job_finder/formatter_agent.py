"""
Formatter Agent for Job Finder recommendations.
Phase 3: AI Logic scaffolding
"""

from __future__ import annotations

from .models import JobRecommendation


class FormatterAgent:
    """Applies presentation rules to recommendations."""

    MAX_LENGTH = 220

    def format_recommendation(
        self,
        recommendation: JobRecommendation,
    ) -> JobRecommendation:
        explanation = recommendation.explanation.strip()
        if len(explanation) > self.MAX_LENGTH:
            explanation = explanation[: self.MAX_LENGTH].rstrip() + "…"

        if not explanation.endswith("."):
            explanation += "."

        recommendation.explanation = explanation
        return recommendation

    def format_recommendations(self, recommendations):
        return [self.format_recommendation(rec) for rec in recommendations]


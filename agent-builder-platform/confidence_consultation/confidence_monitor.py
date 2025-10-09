"""
Confidence Monitoring Dashboard

Tracks confidence metrics throughout the workflow and correlates with user satisfaction.
Provides real-time monitoring and alerts when confidence drops below thresholds.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ConfidenceStatus(Enum):
    """Confidence status levels"""
    EXCELLENT = "excellent"  # >= 98%
    GOOD = "good"  # >= 95%
    ACCEPTABLE = "acceptable"  # >= 90%
    LOW = "low"  # < 90%


@dataclass
class ConfidenceMetrics:
    """Metrics for confidence tracking"""
    session_id: str
    phase: str
    timestamp: str
    
    # Confidence scores
    current_confidence: float
    minimum_confidence: float
    average_confidence: float
    peak_confidence: float
    
    # Trend
    confidence_trend: str  # "increasing", "stable", "decreasing"
    
    # User feedback
    user_satisfaction: Optional[float] = None  # 0.0 to 1.0
    user_feedback: Optional[str] = None
    
    # Alerts
    alerts: List[str] = field(default_factory=list)


class MonitoringDashboard:
    """
    Real-time confidence monitoring dashboard.
    
    Features:
    - Tracks confidence throughout workflow
    - Identifies trends and patterns
    - Alerts when confidence drops below 90%
    - Correlates confidence with user satisfaction
    - Provides actionable insights
    """
    
    ENHANCEMENT_THRESHOLD = 0.90  # Trigger enhancement at 90%
    BASELINE_THRESHOLD = 0.95  # Baseline requirement
    EXCELLENT_THRESHOLD = 0.98  # Excellent confidence
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.session_history: Dict[str, List[ConfidenceMetrics]] = {}
    
    def track_confidence(
        self,
        session_id: str,
        phase: str,
        confidence_score: float
    ) -> ConfidenceMetrics:
        """
        Track confidence for a session.
        
        Args:
            session_id: Session identifier
            phase: Current workflow phase
            confidence_score: Current confidence score (0.0 to 1.0)
            
        Returns:
            ConfidenceMetrics with tracking data
        """
        # Get or create session history
        if session_id not in self.session_history:
            self.session_history[session_id] = []
        
        history = self.session_history[session_id]
        
        # Calculate metrics
        all_scores = [m.current_confidence for m in history] + [confidence_score]
        
        metrics = ConfidenceMetrics(
            session_id=session_id,
            phase=phase,
            timestamp=datetime.utcnow().isoformat(),
            current_confidence=confidence_score,
            minimum_confidence=min(all_scores),
            average_confidence=sum(all_scores) / len(all_scores),
            peak_confidence=max(all_scores),
            confidence_trend=self._calculate_trend(history, confidence_score)
        )
        
        # Check for alerts
        metrics.alerts = self._check_alerts(metrics)
        
        # Add to history
        history.append(metrics)
        
        # Log metrics
        self.logger.info(
            f"Confidence tracked: {int(confidence_score * 100)}% "
            f"(trend: {metrics.confidence_trend}, alerts: {len(metrics.alerts)})"
        )
        
        return metrics
    
    def _calculate_trend(
        self,
        history: List[ConfidenceMetrics],
        current: float
    ) -> str:
        """Calculate confidence trend"""
        if len(history) < 2:
            return "stable"
        
        # Look at last 3 data points
        recent = [m.current_confidence for m in history[-3:]] + [current]
        
        # Calculate trend
        if len(recent) >= 3:
            first_half = sum(recent[:len(recent)//2]) / (len(recent)//2)
            second_half = sum(recent[len(recent)//2:]) / (len(recent) - len(recent)//2)
            
            diff = second_half - first_half
            
            if diff > 0.02:  # 2% increase
                return "increasing"
            elif diff < -0.02:  # 2% decrease
                return "decreasing"
        
        return "stable"
    
    def _check_alerts(self, metrics: ConfidenceMetrics) -> List[str]:
        """Check for confidence alerts"""
        alerts = []
        
        # Below baseline
        if metrics.current_confidence < self.BASELINE_THRESHOLD:
            alerts.append(
                f"⚠️  Confidence below baseline: {int(metrics.current_confidence * 100)}% "
                f"(baseline: {int(self.BASELINE_THRESHOLD * 100)}%)"
            )
        
        # Below enhancement threshold
        if metrics.current_confidence < self.ENHANCEMENT_THRESHOLD:
            alerts.append(
                f"💡 Consider confidence enhancement: {int(metrics.current_confidence * 100)}% "
                f"(threshold: {int(self.ENHANCEMENT_THRESHOLD * 100)}%)"
            )
        
        # Decreasing trend
        if metrics.confidence_trend == "decreasing":
            alerts.append(
                "📉 Confidence decreasing - investigate uncertainties"
            )
        
        # Low minimum
        if metrics.minimum_confidence < 0.85:
            alerts.append(
                f"⚠️  Minimum confidence very low: {int(metrics.minimum_confidence * 100)}%"
            )
        
        return alerts
    
    def get_status(self, confidence: float) -> ConfidenceStatus:
        """Get confidence status"""
        if confidence >= self.EXCELLENT_THRESHOLD:
            return ConfidenceStatus.EXCELLENT
        elif confidence >= self.BASELINE_THRESHOLD:
            return ConfidenceStatus.GOOD
        elif confidence >= self.ENHANCEMENT_THRESHOLD:
            return ConfidenceStatus.ACCEPTABLE
        else:
            return ConfidenceStatus.LOW
    
    def record_user_feedback(
        self,
        session_id: str,
        satisfaction: float,
        feedback: Optional[str] = None
    ):
        """
        Record user satisfaction feedback.
        
        Args:
            session_id: Session identifier
            satisfaction: Satisfaction score (0.0 to 1.0)
            feedback: Optional text feedback
        """
        if session_id in self.session_history:
            history = self.session_history[session_id]
            if history:
                # Update most recent metrics
                history[-1].user_satisfaction = satisfaction
                history[-1].user_feedback = feedback
                
                self.logger.info(
                    f"User feedback recorded: {int(satisfaction * 100)}% satisfaction"
                )
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Get summary of session confidence metrics.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Summary dictionary
        """
        if session_id not in self.session_history:
            return {}
        
        history = self.session_history[session_id]
        if not history:
            return {}
        
        # Calculate summary
        all_scores = [m.current_confidence for m in history]
        all_satisfaction = [m.user_satisfaction for m in history if m.user_satisfaction is not None]
        
        summary = {
            "session_id": session_id,
            "total_phases": len(history),
            "confidence": {
                "current": history[-1].current_confidence,
                "minimum": min(all_scores),
                "average": sum(all_scores) / len(all_scores),
                "peak": max(all_scores),
                "trend": history[-1].confidence_trend
            },
            "status": self.get_status(history[-1].current_confidence).value,
            "total_alerts": sum(len(m.alerts) for m in history)
        }
        
        # Add satisfaction if available
        if all_satisfaction:
            summary["user_satisfaction"] = {
                "average": sum(all_satisfaction) / len(all_satisfaction),
                "latest": all_satisfaction[-1]
            }
        
        return summary
    
    def format_dashboard(self, session_id: str) -> str:
        """
        Format monitoring dashboard for display.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Formatted dashboard
        """
        summary = self.get_session_summary(session_id)
        
        if not summary:
            return "No confidence data available"
        
        conf = summary["confidence"]
        status = summary["status"]
        
        # Status emoji
        status_emoji = {
            "excellent": "🌟",
            "good": "✅",
            "acceptable": "⚠️",
            "low": "🔴"
        }
        
        output = [
            f"\n{'='*60}",
            f"CONFIDENCE MONITORING DASHBOARD",
            f"{'='*60}\n",
            f"Session: {session_id}",
            f"Status: {status_emoji.get(status, '•')} {status.upper()}",
            f"Phases Completed: {summary['total_phases']}",
            "",
            "Confidence Metrics:",
            f"  Current:  {int(conf['current'] * 100)}%",
            f"  Average:  {int(conf['average'] * 100)}%",
            f"  Peak:     {int(conf['peak'] * 100)}%",
            f"  Minimum:  {int(conf['minimum'] * 100)}%",
            f"  Trend:    {conf['trend'].upper()}",
            ""
        ]
        
        # Add satisfaction if available
        if "user_satisfaction" in summary:
            sat = summary["user_satisfaction"]
            output.extend([
                "User Satisfaction:",
                f"  Latest:   {int(sat['latest'] * 100)}%",
                f"  Average:  {int(sat['average'] * 100)}%",
                ""
            ])
        
        # Add alerts
        if summary["total_alerts"] > 0:
            output.append(f"⚠️  Total Alerts: {summary['total_alerts']}")
            output.append("")
        
        output.append(f"{'='*60}\n")
        
        return "\n".join(output)
    
    def get_correlation_analysis(self, session_id: str) -> Dict[str, Any]:
        """
        Analyze correlation between confidence and user satisfaction.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Correlation analysis
        """
        if session_id not in self.session_history:
            return {}
        
        history = self.session_history[session_id]
        
        # Get pairs of confidence and satisfaction
        pairs = [
            (m.current_confidence, m.user_satisfaction)
            for m in history
            if m.user_satisfaction is not None
        ]
        
        if len(pairs) < 2:
            return {"correlation": "insufficient_data"}
        
        # Simple correlation analysis
        conf_scores = [p[0] for p in pairs]
        sat_scores = [p[1] for p in pairs]
        
        avg_conf = sum(conf_scores) / len(conf_scores)
        avg_sat = sum(sat_scores) / len(sat_scores)
        
        return {
            "correlation": "positive" if avg_conf > 0.95 and avg_sat > 0.8 else "needs_improvement",
            "average_confidence": avg_conf,
            "average_satisfaction": avg_sat,
            "sample_size": len(pairs)
        }

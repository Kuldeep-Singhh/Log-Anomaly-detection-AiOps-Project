def get_runbook_actions(anomaly_reason: str) -> list:
    """Map detected anomaly reasons to actionable DevOps steps."""
    actions = []
    reason_lower = str(anomaly_reason).lower()
    
    if "high latency" in reason_lower:
        actions.extend([
            "Check database connection pool utilization.",
            "Analyze query performance (e.g., slow query logs).",
            "Verify CPU and memory usage on application servers.",
            "Check upstream API latency if applicable."
        ])
    
    if "5xx" in reason_lower or "server error" in reason_lower:
        actions.extend([
            "Check application stack traces for fatal exceptions.",
            "Verify if required backend services are down.",
            "Check disk space and inode availability.",
            "Inspect web server (Nginx/Apache) error logs."
        ])
        
    if "text anomaly" in reason_lower:
        actions.extend([
            "Review the specific log message for unexpected errors or exceptions.",
            "Check if a new deployment introduced unexpected logging patterns.",
            "Investigate for potential security scanning or malicious payloads (e.g., SQL injection attempts)."
        ])
        
    if not actions:
        actions.append("Review log entry manually and monitor system metrics.")
        
    # Remove duplicates but preserve order
    return list(dict.fromkeys(actions))

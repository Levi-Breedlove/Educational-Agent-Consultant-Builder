#!/usr/bin/env python3
"""
Minimal Export Service for Testing
"""

from enum import Enum

class ExportFormat(str, Enum):
    """Export format types"""
    CODE = "code"
    IAC = "iac"
    CONTAINER = "container"
    STRANDS = "strands"
    COMPLETE = "complete"


class ExportService:
    """Service for exporting and deploying agents"""
    
    def __init__(self):
        """Initialize export service"""
        print("ExportService initialized")


if __name__ == "__main__":
    print("Testing minimal export service...")
    service = ExportService()
    print(f"Export formats: {list(ExportFormat)}")

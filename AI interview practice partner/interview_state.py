from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class InterviewState:
    """Manages the state of the interview, including dynamic roles and transcripts."""
    
    # Dynamic configurations (set by user at start)
    role: str = "General Candidate" 
    experience_level: str = "Entry-Level"
    focus_areas: str = "General Fit"
    
    # Interview Progress
    is_active: bool = False
    
    # Updated generic stages that fit ANY job type
    stages: List[str] = field(default_factory=lambda: [
        "Introduction",
        "Role-Specific Knowledge",
        "Situational/Behavioral",
        "Conclusion & Feedback"
    ])
    
    current_stage_index: int = 0
    transcript: List[Dict[str, str]] = field(default_factory=list)
    final_report_content: str = "" 
    
    # Audio handling for Voice Feature
    last_audio_file: str = None

    @property
    def current_stage(self) -> str:
        if self.current_stage_index < len(self.stages):
            return self.stages[self.current_stage_index]
        return "Interview Complete"

    def start_interview(self, role, level, focus):
        """Initializes the interview with specific settings."""
        self.role = role
        self.experience_level = level
        self.focus_areas = focus
        self.is_active = True
        self.current_stage_index = 0
        self.transcript = []
        self.final_report_content = ""

    def add_message(self, speaker: str, text: str):
        self.transcript.append({"speaker": speaker, "text": text})

    def advance_stage(self):
        if self.current_stage_index < len(self.stages):
            self.current_stage_index += 1
            
    def reset_state(self):
        self.is_active = False
        self.current_stage_index = 0
        self.transcript = []
        self.final_report_content = ""
        self.last_audio_file = None
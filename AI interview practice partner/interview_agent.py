import os
import time
import json
import re  # <--- Added Regex module for smarter cleaning
import streamlit as st
from google import genai 
from google.genai import types
from gtts import gTTS 

class InterviewAgent:
    def __init__(self, client, model_name, state):
        self.client = client
        self.model_name = model_name
        self.state = state
        
    def generate_system_prompt(self):
        # Dynamic System Prompt based on User Selection
        is_final_stage = self.state.current_stage == "Conclusion & Feedback"
        
        base_prompt = f"""
        You are an expert Hiring Manager conducting a mock interview for a **{self.state.experience_level} {self.state.role}** position.
        The candidate wants to focus on: {self.state.focus_areas}.
        
        Your goal is to assess the candidate realistically.
        
        --- YOUR PERSONA ---
        * Tone: Professional, inquisitive, yet encouraging.
        * Role Context: If interviewing an Engineer, be technical. If Sales, be energetic and scenario-focused.
        
        --- INTERVIEW STAGE: {self.state.current_stage} ---
        1.  **Ask ONE question at a time.**
        2.  **Dig Deeper:** If the user's answer is shallow, ask a follow-up. Do not just accept it.
        3.  **Be Human:** React to what they say (e.g., "That's an interesting approach...") before asking the next question.
        
        --- TRANSITION RULES ---
        You are currently in the '{self.state.current_stage}' stage.
        Engage for 2-3 turns per stage. When you feel you have enough info, include the phrase "MOVING_ON" in your response (hidden from user) to signal the system to advance.
        
        --- TRANSCRIPT ---
        {json.dumps(self.state.transcript)}
        """
        
        if is_final_stage:
             base_prompt += """
        --- FINAL STAGE ---
        The interview is over. Say a polite goodbye and tell the user their feedback report is being generated.
        """
        
        return base_prompt

    def _make_api_call(self, contents, config, retries=0):
        try:
            return self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )
        except Exception as e:
            if retries < 3:
                time.sleep(2)
                return self._make_api_call(contents, config, retries + 1)
            raise e

    def generate_audio(self, text):
        """Generates TTS audio for the agent's response."""
        try:
            # Create a temporary file for audio
            tts = gTTS(text=text, lang='en')
            filename = f"temp_audio_{int(time.time())}.mp3"
            tts.save(filename)
            return filename
        except Exception:
            return None

    def generate_next_response(self, user_input: str):
        # 1. Prepare context
        full_history = self.state.transcript + [{'speaker': 'user', 'text': user_input}]
        contents = [{'role': 'user' if m['speaker'] == 'user' else 'model', 'parts': [{'text': m['text']}]} for m in full_history]

        # 2. Gemini API Call
        response = self._make_api_call(
            contents=contents,
            config={
                'temperature': 0.7, 
                'system_instruction': self.generate_system_prompt()
            }
        )
        
        agent_text = response.text
        terminated = False

        # 3. Check for stage transition signal
        if "MOVING_ON" in agent_text:
            agent_text = agent_text.replace("MOVING_ON", "").strip() # Remove the keyword
            if self.state.current_stage != "Conclusion & Feedback":
                self.state.advance_stage()
        
        if self.state.current_stage == "Conclusion & Feedback":
             # Force termination logic if we are at the end
             if len(self.state.transcript) > 2 and self.state.transcript[-1]['speaker'] == 'model':
                 terminated = True

        # 4. Generate Audio (Voice Feature)
        audio_file = self.generate_audio(agent_text)
        self.state.last_audio_file = audio_file

        return agent_text, terminated

    def generate_feedback_report(self):
        """Generates the JSON report using robust Regex cleaning."""
        
        system_instruction = f"""
        You are an expert AI Recruiter. Analyze this transcript for a {self.state.role} role.
        Generate a JSON report. Do NOT use Markdown formatting.
        
        JSON Schema:
        {{
            "overall_score": (int 1-5),
            "summary": (string),
            "strengths": [(string)],
            "weaknesses": [(string)],
            "communication_score": (int 1-5),
            "technical_score": (int 1-5),
            "sections": [
                {{ "name": (string), "feedback": (string), "score": (int 1-5) }}
            ],
            "next_steps": (string)
        }}
        """
        
        prompt = f"Generate report for:\n{json.dumps(self.state.transcript)}"
        
        # Safety settings
        safety_settings = [
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
        ]

        response = self._make_api_call(
            contents=[{'role': 'user', 'parts': [{'text': prompt}]}],
            config={
                'temperature': 0.2, 
                'system_instruction': system_instruction,
                'response_mime_type': "application/json",
                'safety_settings': safety_settings
            }
        )
        
        # --- SMART CLEANING (REGEX) ---
        text_response = response.text
        
        # Look for the first opening brace { and the last closing brace }
        # This ignores "Here is your JSON" or markdown ticks completely
        match = re.search(r"\{.*\}", text_response, re.DOTALL)
        
        if match:
            return match.group(0) # Return only the JSON part
        else:
            return text_response # Fallback if no JSON found
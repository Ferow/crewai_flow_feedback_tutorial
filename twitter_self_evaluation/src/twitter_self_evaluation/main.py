#!/usr/bin/env python
from typing import Optional
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, router
from .crews.shakesphere_crew import shakesphere_crew
from .crews.x_post_review_crew import x_post_review_crew

class TwitterPostState(BaseModel):
    x_post: str =""
    feedback: Optional[str] = None
    valid: bool = False
    retry_count: int = 0

class TwitterPostFlow(Flow[TwitterPostState]):
    @start("retry")
    def generate_shakespeare_x_post(self):
        #TODO: Add Shakespeare Crew
        pass
   
    @router(generate_shakespeare_x_post)
    def evaluate_x_post(self):
        #TODO: Add evaluation crew
        #Option 1: completed
        #Option 2; Max retry exceeded
        #option 3: retry
        pass
   
    @listen("completed")
    def save_results(self):
       pass

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        pass

def kickoff():
    twitter_flow = TwitterPostFlow()
    twitter_flow.kickoff()
    
def plot():
    post_flow = TwitterPostFlow()
    post_flow.plot()


if __name__ == "__main__":
    kickoff()

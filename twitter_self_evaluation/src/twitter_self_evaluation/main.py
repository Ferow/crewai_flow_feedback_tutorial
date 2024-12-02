#!/usr/bin/env python
from typing import Optional
from pydantic import BaseModel
from crewai.flow.flow import Flow, listen, start, router

from twitter_self_evaluation.crews.shakespeare_crew.shakespeare_crew import ShakespeareCrew
from twitter_self_evaluation.crews.x_post_review_crew.x_post_review_crew import XPostReviewCrew

class TwitterPostState(BaseModel):
    x_post: str =""
    feedback: Optional[str] = None
    valid: bool = False
    retry_count: int = 0

class TwitterPostFlow(Flow[TwitterPostState]):
    @start("retry")
    def generate_shakespeare_x_post(self):
        result = (ShakespeareCrew().crew().kickoff(
            inputs={"topic": "Flying cars", "feedback": self.state.feedback})
        )
        print("result", result.raw)
        self.state.x_post = result.raw
   
    @router(generate_shakespeare_x_post)
    def evaluate_x_post(self):
        
        if self.state.retry_count > 3:
            return "max_retry_exceeded"
        
        result = XPostReviewCrew().crew().kickoff(inputs={"x_post": self.state.x_post})
        self.state.valid = result["valid"]
        self.state.feedback = result["feedback"]
        
        print("valid", self.state.valid)
        print("feedback", self.state.feedback)
        self.state.retry_count += 1
        
        if self.state.valid:
            return "completed"
        
        return "retry"
   
    @listen("completed")
    def save_results(self):
       print("X post is valid")
       print("X post:", self.state.x_post)
       
       #Save the valid X post to a file
       with open("x_post.txt", "w") as file:
           file.write(self.state.x_post)

    @listen("max_retry_exceeded")
    def max_retry_exceeded_exit(self):
        print("Max retry count exceeded")
        print("X Post:", self.state.x_post)
        print("Feedback:", self.state.x_post)

def kickoff():
    twitter_flow = TwitterPostFlow()
    twitter_flow.kickoff()
    
def plot():
    post_flow = TwitterPostFlow()
    post_flow.plot()


if __name__ == "__main__":
    kickoff()

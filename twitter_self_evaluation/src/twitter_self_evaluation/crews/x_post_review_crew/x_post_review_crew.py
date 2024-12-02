from typing import Optional
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from pydantic import BaseModel
from twitter_self_evaluation.tools.CharacterCounterTool import ToolCharacterCounter

class XPostVerification(BaseModel):
	valid: bool
	feedback: Optional[str]


@CrewBase
class XPostReviewCrew:
    """XPostReviewCrew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def x_post_verifier(self) -> Agent:
        return Agent(
            config=self.agents_config["x_post_verifier"],
            tools=[ToolCharacterCounter()],
        )

    @task
    def verify_x_post(self) -> Task:
        return Task(
            config=self.tasks_config["verify_x_post"],
            output_pydantic=XPostVerification,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the XPostReviewCrew crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
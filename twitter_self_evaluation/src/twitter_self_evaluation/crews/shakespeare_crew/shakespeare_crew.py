from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from twitter_self_evaluation.tools.CharacterCounterTool import ToolCharacterCounter

@CrewBase
class ShakespeareCrew():
	"""ShakespeareCrew crew"""

	agents_config = "config/agents.yaml"
	tasks_config = "config/tasks.yaml"

	@agent
	def shakespearean_bard(self) -> Agent:
		return Agent(
            config=self.agents_config["shakespearean_bard"],
            tools=[ToolCharacterCounter()],
        )

	@task
	def write_x_post(self) -> Task:
		return Task(
            config=self.tasks_config["write_x_post"],
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
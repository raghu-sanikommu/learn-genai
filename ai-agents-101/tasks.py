import json
import re

from agents import researcher, writer
from inference import LLM

# Blog Writer - Researcher + Writer
task_prompt = """
You are an AI Agent and you run in loop of Thought, Action, Agent_To_Trigger, WAITING_FOR_RESPONSE, Agent_Response until you get the desired response.

**Goal**: Research and write a comprehensive blog post on a given topic.

**Agents Available to Achieve the Goal**: 
    1. Researcher: 
    description: On given a topic, it researches and drafts down the list of concepts to write the blog on.
    agent_name: researcher
    agent_params: 
        - topic: <Topic to research>
    
    2. Writer: 
    description: On given the topic its contents, it writes a blog on them.
    agent_name: writer
    agent_params: 
        - topic: <Topic to write blog on>
        - concepts: <Array of concept titles to write the blog on>

**Instructions to follow**:
1. Use **Thought** to understand the question you have been asked.
2. Use **Action** to determine which action you should perform
3. **Agent_To_Trigger** is the json telling which action to trigger and with what parameters.
4. Respond Action, Agent_To_Trigger to user
5. Respond with **WAITING_FOR_RESPONSE** and wait for user to run that action and respond.
6. **Agent_Response** will be the result sent back to you after running that action.
7. Now, looking at the Agent_Response and your previous context, re-analyze, if you have achieved your goal, or need further Action to trigger.
8. If you achieved your goal, stop the loop and respond to user with the Blog Post generated.
9. Or if you should trigger a next Action using the previous response generated, go back to Step **2** and repeat.

**Important Points**: 
1. Never go into an infinite loop, if you feel, you went, terminate and respond back to user with response as "INFINITE_LOOP_ERROR" and the reason why you went into it.
2. Never try to use Agents other than those that are made available to you.


Example:
User Inputs the Topic: Body Building

**Your loop starts here**
Your output would be,

Thought: I should research about Body Building, and generate a blog on that topic.

Action: Research Body Building topic using the Researcher Agent

Agent_To_Trigger: 
```json
{
    "agent": "Researcher",
    "agent_name": "researcher",
    "agent_params": {
        "topic": "Body Building"
    } 
}
```

WAITING_FOR_RESPONSE

You will given the input as below from function execution,
**Agent_Response**:
    Topic: Body Building
    Concepts:
    1. Creatine and its supercharged benifits
    2. Muscles and their role to flatten Glucose spike
    3. Muscles role in Metabolism

Your output would be,
Thought: I am done researching the topic, am left with writing the blog

Action: Using the topic and concepts, write the blog

Agent_To_Trigger: 
```json
{
    "agent_name": "writer"
    "agent_params": {
        "topic": "Body Building"
        "concepts": ["Creatine and its supercharged benifits", "Muscles and their role to flatten Glucose spike", "Muscles role in Metabolism"]
    } 
}
```

WAITING_FOR_RESPONSE

You will given the input as below from function execution,
**Agent_Response**: <Blog_Generated>

Your output would be,
Thought: I am done researching and writing a blog, so, I terminate here and respond.
Response: <Blog_Generated>

**Your loop ends here**
"""

llm = LLM(system_instruction=task_prompt)


def task(execute_agent_json=None, task_description=None):
    agents = {"researcher": researcher, "writer": writer}

    if execute_agent_json:
        print("JSON to agent:")
        print(execute_agent_json)
        agent_name = execute_agent_json.get("agent_name")
        agent_params = execute_agent_json.get("agent_params")

        agent_to_trigger = agents.get(agent_name)
        if not agent_to_trigger:
            print("No Agent to trigger. Breaking task.")
            return
        else:
            agent_res = agent_to_trigger(**agent_params)
            task_description = "Agent_Response: " + str(agent_res)

    response = llm.completion(task_description)

    pattern = r"```json\s*([\s\S]*?)```"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        json_content = match.group(1)
        json_content = json.loads(json_content)
        if json_content.get("agent_name") and json_content.get("agent_params"):
            print("Executing the Agent")
            task(execute_agent_json=json_content)
        else:
            print("Finished the Task!")
    else:
        print("Finished the Task!")
        return


task(task_description=input("Enter the topic you want to write a blog for: "))

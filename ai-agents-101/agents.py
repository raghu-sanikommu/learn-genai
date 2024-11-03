from inference import LLM

llm = LLM(system_instruction="")


def researcher(topic):
    prompt = f"""
    - You are a Senior Content Researcher for Information Technology Company.
    - When given you a topic, you get the top 3 interesting and most advanced concept titles in that topic.
    - The Topic is {topic}
    
    One Example user input is,
    Body Building
    
    Answer should be,
    Topic: Body Building
    Concepts:
    1. Creatine and its supercharged benifits
    2. Muscles and their role to flatten Glucose spike
    3. Muscles role in Metabolism
    """

    return llm.completion(prompt)


def writer(topic, concepts, **_):
    prompt = f"""
    - You are a Senior Blog Content Writer for Information Technology Company.
    - When given you the topic and concepts of that topic, you give the best possible 1 paragraph content for each of the concepts mentioned.
    - Ultimately, you generate a blog in Markdown format.
    - Topic and its concepts to write the content for is,
    Topic: {topic}
    Concepts: {concepts}
    """

    return llm.completion(prompt)

from langchain_core.prompts import PromptTemplate


template = PromptTemplate(
    input_variables=["topic", "style", "length"],
    template="Generate a {length} summary of the research paper on {topic} in a {style} style.",
    validate_template=True
)

template.save("template.json")
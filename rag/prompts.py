from langchain.prompts import PromptTemplate


# returns prompt template based on the persona and question
def get_prompt_template(persona: str):
    persona_prompts = {
        "friendly": "You are a friendly and patient tutor. You explain things using simple analogies and always try "
                    "to help the student understand clearly.",
        "strict": "You are a strict and concise tutor. You explain only what is necessary and keep the answers short.",
        "humorous": "You are a humorous tutor. You make jokes, use funny comparisons, and try to make learning fun.",
    }

    system_instruction = persona_prompts.get(persona, "You are a helpful educational tutor.")

    return PromptTemplate(
        input_variables=["context", "question"],
        template=f"""{system_instruction}

You are teaching a student. Below is some context from their textbook.

Context:
{{context}}

Based on the context above, answer the question below in your teaching style.

Question:
{{question}}

Answer:"""
    )

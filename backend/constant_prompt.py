qa_promt_tmpl_en = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"

    "Question information is below. \n"
    "---------------------\n"
    "{query_str}"
    "\n---------------------\n"
    "If the Context information is empty, than try to answer the question without consider context information."
    "If the Context information in not empty, given the context information and not prior knowledge.\n"
)

qa_promt_tmpl_zh = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"

    "Question information is below. \n"
    "---------------------\n"
    "{query_str}"
    "\n---------------------\n"
    "If the Context information is empty, than try to answer the question without consider context information."
    "If the Context information in not empty, given the context information and not prior knowledge.\n"
    "Using traditional Chinese to answer the question.\n"
)

qa_promt_tmpl_cn = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"

    "Question information is below. \n"
    "---------------------\n"
    "{query_str}"
    "\n---------------------\n"
    "If the Context information is empty, than try to answer the question without consider context information."
    "If the Context information in not empty, given the context information and not prior knowledge.\n"
    "Using Simplified Chinese to answer the question.\n"
)

qa_gen_promt_tmpl_en = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"

    "Question information is below. \n"
    "---------------------\n"
    "{query_str}"
    "\n---------------------\n"
    "If the Context information is empty, than try to answer the question without consider context information."
    "If the Context information in not empty, given the context information and not prior knowledge.\n"
)

qa_gen_promt_tmpl_zh = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"

    "Question information is below. \n"
    "---------------------\n"
    "{query_str}"
    "\n---------------------\n"
    "If the Context information is empty, than try to answer the question without consider context information."
    "If the Context information in not empty, given the context information and not prior knowledge.\n"
    "Using traditional Chinese to answer the question.\n"
)

qa_gen_promt_tmpl_cn = (
    "Context information is below. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"

    "Question information is below. \n"
    "---------------------\n"
    "{query_str}"
    "\n---------------------\n"
    "If the Context information is empty, than try to answer the question without consider context information."
    "If the Context information in not empty, given the context information and not prior knowledge.\n"
    "Using Simplified Chinese to answer the question.\n"
)


pre_promt =  f"You are a personal assistant for Synergies company, your job is to answer questions. First check index as reference."

noact_prompt = """
"Your job is to continue the conversation as a chatbot.\n"
"When asked a question, try to use the context provided to directly answer that question.\n"
"Given this information, please respond to or answer the question: {query}
""" 

yes_no_prompt = """
"I want you to act as a simple AI which only answer by "Yes" or "No" to my questions."
"Do no write explanations. If you can't answer by Yes or No, type"I can't answer","
"but do not type anythins else.\n"
"The questio is: {query}""" 

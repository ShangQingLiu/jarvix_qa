qa_promt_tmpl_en_bk = (
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

qa_promt_tmpl_en = (
"以下是背景資訊。 \n"
"---------------------\n"
"{context_str}"
"\n---------------------\n"

"以下是問題資訊。 \n"
"---------------------\n"
"{query_str}"
"\n---------------------\n"
"如果背景資訊是空的，那麼嘗試不考慮背景資訊來回答問題。"
"如果背景資訊不是空的，則在給出背景資訊的情況下，並不考慮先前的知識。\n"
    "使用英文來回答問題。\n"
)


qa_promt_tmpl_zh_bk = (
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

qa_promt_tmpl_zh = (
"以下是背景資訊。 \n"
"---------------------\n"
"{context_str}"
"\n---------------------\n"

"以下是問題資訊。 \n"
"---------------------\n"
"{query_str}"
"\n---------------------\n"
"如果背景資訊是空的，那麼嘗試不考慮背景資訊來回答問題。"
"如果背景資訊不是空的，則在給出背景資訊的情況下，並不考慮先前的知識。\n"
"使用繁體中文來回答問題。\n"
)

qa_promt_tmpl_cn_bk = (
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

qa_promt_tmpl_cn = (
"以下是背景信息。 \n"
"---------------------\n"
"{context_str}"
"\n---------------------\n"

"以下是问题信息。 \n"
"---------------------\n"
"{query_str}"
"\n---------------------\n"
"如果背景信息为空，那么尝试不考虑背景信息来回答问题。"
"如果背景信息不为空，那么给出背景信息，不考虑先前的知识。\n"
"使用简体中文来回答问题。\n"
)

# qa_gen_promt_tmpl_en = (
#     "Context information is below. \n"
#     "---------------------\n"
#     "{context_str}"
#     "\n---------------------\n"

#     "Question information is below. \n"
#     "---------------------\n"
#     "{query_str}"
#     "\n---------------------\n"
#     "If the Context information is empty, than try to answer the question without consider context information."
#     "If the Context information in not empty, given the context information and not prior knowledge.\n"
# )

# qa_gen_promt_tmpl_zh = (
#     "Context information is below. \n"
#     "---------------------\n"
#     "{context_str}"
#     "\n---------------------\n"

#     "Question information is below. \n"
#     "---------------------\n"
#     "{query_str}"
#     "\n---------------------\n"
#     "If the Context information is empty, than try to answer the question without consider context information."
#     "If the Context information in not empty, given the context information and not prior knowledge.\n"
#     "Using traditional Chinese to answer the question.\n"
# )

# qa_gen_promt_tmpl_cn = (
#     "Context information is below. \n"
#     "---------------------\n"
#     "{context_str}"
#     "\n---------------------\n"

#     "Question information is below. \n"
#     "---------------------\n"
#     "{query_str}"
#     "\n---------------------\n"
#     "If the Context information is empty, than try to answer the question without consider context information."
#     "If the Context information in not empty, given the context information and not prior knowledge.\n"
#     "Using Simplified Chinese to answer the question.\n"
# )


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


# Add record as json.dumps() in the back
continuous_prompt = """
I have following querie and response pairs, help me complete the latest response text, only give completion text of response to complete the sentence as answer and do not generate any other text espeacially the exist content:
"""
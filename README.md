# AI-Portfolio-Reviewer
This is RAG based AI Portfolio Reviewer, which helps users in summarizing, reviewing any candidates Portfolio.
The **Architecture** comprises following modules
  -  Knowledge Base / List of Source Files
  -  Metdata Filter to Narrow down Knowledge Base to Specific candidate
  -  Vector Store/Database
  -  Prompt Template for System Instructions
  -  LLM to Generate Answers
  -  Parser to Parse output
  -  Memory Module to feed previous conversations

**RAGChain Structure - Feed | Prompt | Model | Parser**

**WorkFlow**
  -  As Conversation Inititated, Feed Module is provided with Knowledge Base, User's Question and Conversation History
  -  Based on User's Question & Conversation History Knowledge Base is Narrow down to Specific Candidate through Metadata Filter
  -  Vector Store is built across queried Candidate Name
  -  LLM Generate Answer using provided Vector Store and as per System Instruction Provided in Prompt Template
  -  LLM's response is Parsed through Output Pareser

**Future Scope**
  - Provide Citation for RAG response
  - Summarize & Evaluate Candidates Portofolio against Organizations Job Description for ATS Scoring
  - Summarize & Evaluate Candidates Portfolio against another candidate

Response
<img width="952" height="332" alt="Response 1" src="https://github.com/user-attachments/assets/e050412c-a24b-4a16-a7c7-e457c2833b4d" />
<img width="913" height="430" alt="Response 2" src="https://github.com/user-attachments/assets/b698fa8d-7858-4cb8-9eaa-fe8f0bea99de" />

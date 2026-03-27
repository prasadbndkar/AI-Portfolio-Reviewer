# AI-Portfolio-Reviewer
This is RAG based AI Portfolio Reviewer, which helps users in fetching information about specific candidate from Vector Database.
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

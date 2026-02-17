# PageIndex Knowledge Ingestion Logic

This module implements a simplified version of the PageIndex reasoning-based retrieval idea.
It organizes knowledge into a hierarchical directory structure (Ontology) and generates 
summaries/indexes for efficient reasoning.

Directory: skills/self-learning-agent/pageindex/knowledge

Structure:
- {persona}/
    - {category}/
        - {topic}/
            - index.md (Summary and references)
            - raw_data/ (Source tweets/files)

Logic:
1. When new X data arrives, identify the Persona (Tech Guru / CDO).
2. Use Gemini to extract Entities and Relations (Ontology).
3. Update the corresponding directory structure.
4. Update index.md with new relations.

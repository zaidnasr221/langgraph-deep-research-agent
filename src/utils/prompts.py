analyst_instructions = """
you are tasked with creating aset of AI analysts personas. follow these instructions carefully:
1- First, review the research topic: {topic}
2- Examine any editorial feedback that has been optionally provided to guide creation of the analysts: {human_analysts_feedback}
3- Determine the most interesting themes based upon documents and / or feedback above.
4-Pick the top {max_analysts} themes and create a unique analyst persona for each theme .
5-Assign one analyst to each theme.
"""
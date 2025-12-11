from ml_workspace.pipeline import InterviewPipeline


pipeline = InterviewPipeline()

print("Generated Question:")
print(pipeline.generate_question("software engineer", "easy"))

print("\nScoring Sample:")
print(pipeline.score_answer(
    question="Tell me about yourself",
    answer="I am a computer science student...",
    expected_keywords=["experience", "skills"]
))

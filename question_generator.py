# ml/question_generator.py

def generate_question(job_role: str, difficulty: str = "easy") -> str:
    job_role = job_role.lower().strip()
    difficulty = difficulty.lower().strip()

    questions_easy = {
        "software engineer": [
            "What programming languages are you most comfortable with?",
            "Explain a project you recently worked on."
        ],
        "data analyst": [
            "What tools do you use for data cleaning?",
            "Explain the difference between data analysis and data analytics."
        ]
    }

    questions_medium = {
        "software engineer": [
            "How do you ensure code quality in a large project?",
            "Explain the concept of multithreading."
        ],
        "data analyst": [
            "How do you handle missing values in a dataset?",
            "Explain the purpose of A/B testing."
        ]
    }

    questions_hard = {
        "software engineer": [
            "Explain how a compiler works internally.",
            "Design a scalable logging service for millions of users."
        ],
        "data analyst": [
            "How would you design an end-to-end data pipeline?",
            "Explain how to detect statistical anomalies in real-time data."
        ]
    }

    bank = {
        "easy": questions_easy,
        "medium": questions_medium,
        "hard": questions_hard
    }

    if job_role not in bank[difficulty]:
        return f"Give me details about your experience as a {job_role}."

    import random
    return random.choice(bank[difficulty][job_role])

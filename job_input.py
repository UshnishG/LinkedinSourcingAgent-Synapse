def get_job_description():
    """Get job description from user input or use default"""
    print("\n=== Job Description Input ===")
    print("Enter the job description below (or press Enter to use default):")
    print("Default: Software Engineer ML Research at Windsurf (Codeium) - Forbes AI 50 company building AI-powered developer tools. Train LLMs for code generation, $140-300k + equity, Mountain View. Machine learning, neural networks, large language models, code generation, developer tools.")
    print("-" * 80)
    
    user_input = input("Job Description: ").strip()
    
    if user_input:
        return user_input
    else:
        default_description = """Software Engineer ML Research at Windsurf (Codeium) - Forbes AI 50 company building AI-powered developer tools. Train LLMs for code generation, $140-300k + equity, Mountain View. Machine learning, neural networks, large language models, code generation, developer tools."""
        print(f"\nUsing default job description: {default_description}")
        return default_description

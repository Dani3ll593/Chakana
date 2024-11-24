def get_model_feedback(text, temperature=0.7, max_tokens=1000, criteria=None):
    """
    Sends text to the AI/ML API and retrieves AI feedback as a single paragraph.
    """
    # Define default criteria if none provided
    if criteria is None:
        criteria = [
            "writing quality (grammar, clarity, and conciseness)",
            "coherence and logical structure",
            "alignment with research objectives and theoretical framework",
            "recommendations for improvement"
        ]

    # Construct the system prompt
    criteria_str = ", ".join(criteria)
    system_prompt = (
        "You are an advanced AI assistant specializing in research analysis. Your task is to provide "
        "clear, detailed, and constructive feedback on research text. Focus on the following aspects: "
        f"{criteria_str}. "
        "Ensure the feedback is organized into a single cohesive paragraph with specific examples or suggestions."
    )

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    response = requests.post(f"{API_BASE_URL}/chat/completions", headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    # Return the feedback as a single paragraph
    return response.json()["choices"][0]["message"]["content"].strip()
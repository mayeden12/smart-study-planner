import ollama
import os


def get_client():
    host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    return ollama.Client(host=host)


def generate_study_hack(topic_name: str) -> str:
    client = get_client()
    
    # TinyLlama struggles with instructions, so we use a "1-shot" example to force the output format
    system_prompt = "You are a strict, concise AI. Never use greetings, introductions, or lists. Output ONLY a single-sentence technique."
    
    prompt = f"""Subject: Mathematics
Hack: Use interleaved practice by mixing different types of equations to train your brain to recognize patterns.

Subject: {topic_name}
Hack:"""

    try:
        response = client.generate(
            model='tinyllama',
            prompt=prompt,
            system=system_prompt,
            options={
                "temperature": 0.1,
                "num_predict": 100
            }
        )
        
        result = response.get("response", "").strip()
        return result if result else "⚠️ Could not generate a hack. Please try again."
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"
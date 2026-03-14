import ollama
import os


def get_client():
    host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
    return ollama.Client(host=host)


def generate_study_hack(topic_name: str) -> str:
    client = get_client()
    
    prompt = f"Provide a Quick Study Hack (maximum 2 sentences) for mastering this topic: '{topic_name}'."

    try:
        response = client.generate(
            model='tinyllama',
            prompt=prompt,
            options={
                "temperature": 0.2,
                "num_predict": 80
            }
        )
        
        result = response.get("response", "").strip()
        return result if result else "⚠️ Could not generate a hack. Please try again."
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}"
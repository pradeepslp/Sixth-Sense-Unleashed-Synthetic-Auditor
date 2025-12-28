import requests
import json

def analyze_vulnerability(finding, context_note="Client is a financial bank with strict compliance needs."):
    """
    Sends the finding to local Ollama API for contextual analysis.
    """
    
    prompt = f"""
    You are a Cyber Security Expert. Analyze the following vulnerability for this specific client context.
    
    Client Context: {context_note}
    Vulnerability: {finding['title']}
    Severity: {finding['severity']}
    Technical Detail: {finding['description']}
    
    Task: Write a short paragraph explaining why this is dangerous specifically for this client. 
    Keep it under 3 sentences. Do not hallucinate.
    """

    # 1. API Call to local Ollama
    url = "http://localhost:11434/api/generate"
    
    # IMPORTANT: Ensure 'stream' is False so we get one complete JSON response
    data = {
        "model": "llama3",   # <--- MAKE SURE THIS MATCHES YOUR INSTALLED MODEL
        "prompt": prompt,
        "stream": False
    }

    try:
        print(f"[*] Sending request to Ollama for: {finding['title']}...") # Debug print
        response = requests.post(url, json=data)
        
        # 2. Check for HTTP Errors (like 404 Model Not Found)
        if response.status_code != 200:
            print(f"[!] Ollama Error {response.status_code}: {response.text}")
            return f"AI Error: Ollama returned status {response.status_code}. Check terminal for details."

        # 3. Parse JSON
        result = response.json()
        
        # 4. Check if 'response' key exists
        if 'response' in result:
            return result['response']
        else:
            print(f"[!] Unexpected JSON format: {result}")
            return "AI Error: Valid JSON received, but no 'response' key found."

    except Exception as e:
        print(f"[!] Connection Exception: {str(e)}")
        return f"Connection Error: Is Ollama running? Details: {str(e)}"
    # ... (Keep your existing imports and analyze_vulnerability function) ...

def generate_attack_path_summary(findings, context_note):
    """
    Sends ALL findings to Ollama for a holistic threat analysis.
    """
    # --- CHANGE: Removed filter for ['High', 'Critical'] ---
    # Now we include EVERYTHING, but we truncate the list if it's too long
    # to prevent crashing the local AI.
    
    summary_findings = []
    for f in findings:
        summary_findings.append(f"{f['title']} on {f['host']} ({f['severity']})")

    # Safety: If there are more than 15 findings, only take the top 15 
    # so Llama3 doesn't get overwhelmed.
    if len(summary_findings) > 15:
        summary_findings = summary_findings[:15]
        summary_findings.append("... [and more truncated]")

    if not summary_findings:
        return "No vulnerabilities identified."

    findings_list_str = "\n".join([f"- {item}" for item in summary_findings])

    prompt = f"""
    You are a Senior Red Team Strategist.
    
    Client Context: {context_note}
    
    Vulnerabilities Found:
    {findings_list_str}
    
    Task:
    Write a cohesive "Security Posture Overview" paragraph (max 4 sentences). 
    Discuss the overall risk level. If there are only Low/Medium risks, mention that the posture is decent but needs hardening. 
    If there are High/Critical, explain the attack chain.
    """

    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3", 
        "prompt": prompt,
        "stream": False
    }

    try:
        print("[*] Generating Holistic Summary (All Severities)...")
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            return result.get('response', 'AI Analysis Failed')
        return "Error: Local AI did not respond correctly."
    except Exception as e:
        return f"AI Connection Error: {str(e)}"
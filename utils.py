import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
import json
import requests  

load_dotenv()
openai_api_key = os.getenv("OPENROUTER_API_KEY")
openai_api_base = "https://openrouter.ai/api/v1"

def search_web_with_serper(query, num_results=5):
    """Uses Serper.dev to perform Google-like web search."""
    serper_api_key = os.getenv("SERPER_API_KEY")
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        results = response.json()
        formatted = ""
        for item in results.get("organic", [])[:num_results]:
            formatted += f"- {item['title']} ({item['link']})\n"
        return formatted or "No results found."
    except Exception as e:
        return f"(Search failed: {str(e)})"


def generate_roadmap(user_info, goal, preferred_platforms=None):
    """Generates a career roadmap using LangChain and RAG via Serper."""

    # 1. Define LLM (Mistral via OpenRouter)
    llm = ChatOpenAI(
        model_name="mistralai/mistral-7b-instruct",
        openai_api_key=openai_api_key,
        openai_api_base=openai_api_base,
    )

    # 2. Prompt Template
    prompt_template = ChatPromptTemplate.from_template(
        """
        Act as a friendly and professional career roadmap mentor.

        The student has the following background: {user_info}
        Their career goal is: {goal}

        Your job is to generate a realistic and personalized career roadmap to help the student.

        **Instructions**:
        * Do NOT fix the roadmap to 8 weeks. Use your best judgment...
        * For each week, include topic, description, resources, and estimated time commitment.
        * ONLY use verified learning resources.  Check links to make sure they work.

        **VERIFIED RESOURCES (from search):**
        {search_results}

        📍 At the end, include a **Final Milestone** titled
        - This should feel like a personal note to the student.
        - Explain what they’ve accomplished and how they can now apply for jobs, internships, or freelance gigs.
        - Be supportive and motivating, as if you're celebrating their journey and encouraging them to take the leap.

        Avoid generic or robotic tone. Be helpful, uplifting, and practical.
        """
    )

    # 3. Extract Topics
    topics = extract_topics(goal)

    # 4. Search and Compile Results using Serper
    search_results = ""
    for topic in topics:
        search_output = search_web_with_serper(f"learning resources for {topic}")
        search_results += f"Topic: {topic}\n{search_output}\n\n"

    # 5. Invoke the LLM
    chain = prompt_template | llm
    response = chain.invoke({
        "user_info": user_info,
        "goal": goal,
        "search_results": search_results
    })

    return response.content if hasattr(response, "content") else response



def extract_topics(user_goal):
    """Extract key topics from user's career goal using OpenRouter"""

    prompt = f"""
    Extract 5-8 key learning topics/skills needed for someone pursuing this career goal: "{user_goal}"
    Return only a simple JSON array of strings. For example:
    ["Python", "SQL", "Data Visualization", "Statistics", "Machine Learning"]
    """

    headers = {
        "Authorization": f"Bearer {openai_api_key}",
        "HTTP-Referer": "http://localhost",  
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": "You extract key learning topics from career goals."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(f"{openai_api_base}/chat/completions", headers=headers, json=payload)

    if response.status_code != 200:
        return [user_goal]  
    result = response.json()["choices"][0]["message"]["content"]

    try:
        return json.loads(result)
    except json.JSONDecodeError:
        try:
            start = result.find("[")
            end = result.rfind("]") + 1
            return json.loads(result[start:end])
        except:
            return [user_goal]

def logout_button():
    with st.container():
        col1, col2 = st.columns([9, 1])  
        with col2:
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()

import google.generativeai as genai
from supabase import create_client, Client
import os


# --- CONFIGURATION (Replace with your actual keys) ---
SUPABASE_URL = "https://zmvprrhayjmgxvahbjny.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InptdnBycmhheWptZ3h2YWhiam55Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE3NTU4MjgsImV4cCI6MjA4NzMzMTgyOH0.-jLcYh69RsIqroQVwgDqwscthQ84Gme75AaoNNlt79M"
GEMINI_API_KEY = "AIzaSyBQ6PH6DzNrdErksG3NWUJIoJP6-eSk5cg"
# ----------------------------------------------------

# Initialize Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # 1. Save User Message to Supabase
        supabase.table("messages").insert({"role": "user", "content": user_message}).execute()

        # 2. Get AI Response
        response = model.generate_content(user_message)
        bot_reply = response.text

        # 3. Save Bot Response to Supabase
        supabase.table("messages").insert({"role": "bot", "content": bot_reply}).execute()

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/history', methods=['GET'])
def get_history():
    try:
        response = supabase.table("messages").select("*").order("created_at", desc=False).execute()
        return jsonify(response.data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)


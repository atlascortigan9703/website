from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'smart_tourism_secret_key_2024'

# Sample data for demonstration
SAMPLE_HERITAGE_SITES = {
    "taj_mahal": {
        "name": "Taj Mahal",
        "location": "Agra, India",
        "description": "An ivory-white marble mausoleum on the right bank of the Yamuna river",
        "history": "Built by Mughal emperor Shah Jahan in memory of his wife Mumtaz Mahal. Construction started in 1632 and completed in 1653.",
        "architectural_style": "Mughal architecture",
        "fun_facts": [
            "It took approximately 22 years and 20,000 artisans to complete",
            "The marble changes color throughout the day",
            "It's one of the Seven Wonders of the World"
        ],
        "languages": ["English", "Hindi", "Spanish", "French", "German", "Japanese"]
    },
    "colosseum": {
        "name": "Colosseum",
        "location": "Rome, Italy",
        "description": "An oval amphitheatre in the centre of the city of Rome",
        "history": "Built between 72 AD and 80 AD under the emperors Vespasian and Titus. Could hold 50,000-80,000 spectators.",
        "architectural_style": "Roman architecture",
        "fun_facts": [
            "Used for gladiatorial contests and public spectacles",
            "Had a retractable awning to protect spectators from sun",
            "80 entrances allowed quick entry and exit"
        ],
        "languages": ["English", "Italian", "Spanish", "French", "German"]
    },
    "great_wall": {
        "name": "Great Wall of China",
        "location": "Northern China",
        "description": "Series of fortifications made of stone, brick, and other materials",
        "history": "Originally built as early as the 7th century BC, with major construction during the Ming dynasty (1368-1644).",
        "architectural_style": "Military architecture",
        "fun_facts": [
            "Total length is approximately 21,196 km",
            "Contrary to myth, it cannot be seen from space with naked eye",
            "Built over 2,000 years by various dynasties"
        ],
        "languages": ["English", "Mandarin", "Spanish", "French", "Japanese"]
    }
}

SAMPLE_NEARBY_ATTRACTIONS = {
    "taj_mahal": [
        {"name": "Agra Fort", "type": "Historical Fort", "distance": "2.5 km"},
        {"name": "Mehtab Bagh", "type": "Gardens", "distance": "1 km"},
        {"name": "Local Bazaar", "type": "Shopping", "distance": "3 km"}
    ],
    "colosseum": [
        {"name": "Roman Forum", "type": "Archaeological Site", "distance": "0.5 km"},
        {"name": "Palatine Hill", "type": "Historical Site", "distance": "0.8 km"},
        {"name": "Trevi Fountain", "type": "Landmark", "distance": "1.2 km"}
    ],
    "great_wall": [
        {"name": "Mutianyu Section", "type": "Wall Section", "distance": "70 km"},
        {"name": "Ming Tombs", "type": "Historical Site", "distance": "50 km"},
        {"name": "Beijing City Center", "type": "Urban Area", "distance": "60 km"}
    ]
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/discover')
def discover():
    return render_template('discover.html', sites=SAMPLE_HERITAGE_SITES)

@app.route('/site/<site_id>')
def site_detail(site_id):
    site = SAMPLE_HERITAGE_SITES.get(site_id)
    if not site:
        return "Site not found", 404
    
    nearby = SAMPLE_NEARBY_ATTRACTIONS.get(site_id, [])
    return render_template('site_detail.html', site=site, site_id=site_id, nearby_attractions=nearby)

@app.route('/ar_experience')
def ar_experience():
    return render_template('ar_experience.html')

@app.route('/voice_assistant')
def voice_assistant():
    return render_template('voice_assistant.html')

@app.route('/api/site_info/<site_id>')
def api_site_info(site_id):
    site = SAMPLE_HERITAGE_SITES.get(site_id)
    if site:
        return jsonify(site)
    return jsonify({"error": "Site not found"}), 404

@app.route('/api/nearby_attractions/<site_id>')
def api_nearby_attractions(site_id):
    attractions = SAMPLE_NEARBY_ATTRACTIONS.get(site_id, [])
    return jsonify(attractions)

@app.route('/api/ask_question', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')
    site_id = data.get('site_id', '')
    
    # Simple AI response simulation
    responses = {
        "history": f"Here's more about the history of {SAMPLE_HERITAGE_SITES.get(site_id, {}).get('name', 'this site')}...",
        "architecture": f"The architectural style is {SAMPLE_HERITAGE_SITES.get(site_id, {}).get('architectural_style', 'unique and historically significant')}.",
        "construction": "The construction involved skilled artisans and took many years to complete.",
        "significance": "This site holds great cultural and historical importance for the region.",
        "visit": "The best time to visit is during morning hours to avoid crowds."
    }
    
    # Simple keyword matching for demo
    answer = "I'd be happy to tell you more about this heritage site. It represents rich cultural heritage and historical significance."
    for key, response in responses.items():
        if key in question.lower():
            answer = response
            break
    
    return jsonify({
        "question": question,
        "answer": answer,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })

@app.route('/api/change_language', methods=['POST'])
def change_language():
    data = request.get_json()
    language = data.get('language', 'English')
    session['language'] = language
    return jsonify({"message": f"Language changed to {language}", "language": language})

@app.route('/offline_mode')
def offline_mode():
    return render_template('offline_mode.html')

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Create all HTML templates
    create_templates()
    
    app.run(debug=True, host='0.0.0.0', port=5000)

def create_templates():
    templates = {
        'index.html': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart Cultural Tourism Assistant</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }
        
        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #4a5568;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        
        .nav-links a {
            text-decoration: none;
            color: #4a5568;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: #667eea;
        }
        
        .hero {
            text-align: center;
            padding: 4rem 2rem;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero p {
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 2rem;
        }
        
        .btn {
            display: inline-block;
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: 600;
            transition: transform 0.3s, box-shadow 0.3s;
            border: none;
            cursor: pointer;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }
        
        .feature-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: #667eea;
        }
        
        .feature-card h3 {
            margin-bottom: 1rem;
            color: #4a5568;
        }
        
        footer {
            text-align: center;
            padding: 2rem;
            color: white;
            margin-top: 3rem;
        }
        
        @media (max-width: 768px) {
            .nav-links {
                flex-direction: column;
                gap: 1rem;
            }
            
            .hero h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo">🌍 Cultural Explorer</div>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/discover">Discover</a>
                <a href="/ar_experience">AR Experience</a>
                <a href="/voice_assistant">Voice Assistant</a>
                <a href="/offline_mode">Offline Mode</a>
            </div>
        </nav>
    </header>

    <div class="container">
        <section class="hero">
            <h1>Smart Cultural Tourism Assistant</h1>
            <p>Experience cultural heritage sites like never before with AI-powered guidance, augmented reality, and personalized tours.</p>
            <a href="/discover" class="btn">Start Exploring</a>
        </section>

        <section class="features">
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3>Smart Discovery</h3>
                <p>Find and learn about cultural heritage sites with detailed information and historical context.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📱</div>
                <h3>AR Experience</h3>
                <p>View historical reconstructions and information through augmented reality.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🎤</div>
                <h3>Voice Assistant</h3>
                <p>Ask questions and get instant answers about cultural sites in multiple languages.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📶</div>
                <h3>Offline Mode</h3>
                <p>Access site information and guides without internet connection.</p>
            </div>
        </section>
    </div>

    <footer>
        <p>&copy; 2024 Smart Cultural Tourism Assistant. All rights reserved.</p>
    </footer>
</body>
</html>
        ''',
        
        'discover.html': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discover Heritage Sites</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }
        
        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #4a5568;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        
        .nav-links a {
            text-decoration: none;
            color: #4a5568;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: #667eea;
        }
        
        .page-header {
            text-align: center;
            color: white;
            margin-bottom: 3rem;
        }
        
        .page-header h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .sites-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 2rem;
            margin-bottom: 3rem;
        }
        
        .site-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }
        
        .site-card:hover {
            transform: translateY(-5px);
        }
        
        .site-image {
            height: 200px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 4rem;
        }
        
        .site-content {
            padding: 1.5rem;
        }
        
        .site-content h3 {
            color: #4a5568;
            margin-bottom: 0.5rem;
        }
        
        .site-location {
            color: #667eea;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .site-description {
            color: #666;
            margin-bottom: 1rem;
        }
        
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            border-radius: 20px;
            font-weight: 600;
            transition: transform 0.3s;
            border: none;
            cursor: pointer;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        footer {
            text-align: center;
            padding: 2rem;
            color: white;
            margin-top: 3rem;
        }
        
        @media (max-width: 768px) {
            .nav-links {
                flex-direction: column;
                gap: 1rem;
            }
            
            .sites-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo">🌍 Cultural Explorer</div>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/discover">Discover</a>
                <a href="/ar_experience">AR Experience</a>
                <a href="/voice_assistant">Voice Assistant</a>
                <a href="/offline_mode">Offline Mode</a>
            </div>
        </nav>
    </header>

    <div class="container">
        <div class="page-header">
            <h1>Discover Cultural Heritage</h1>
            <p>Explore amazing heritage sites from around the world</p>
        </div>

        <div class="sites-grid">
            {% for site_id, site in sites.items() %}
            <div class="site-card">
                <div class="site-image">
                    {{ site.name[0] }}{{ site.name.split()[-1][0] if site.name.split()|length > 1 else site.name[1] }}
                </div>
                <div class="site-content">
                    <h3>{{ site.name }}</h3>
                    <div class="site-location">{{ site.location }}</div>
                    <p class="site-description">{{ site.description }}</p>
                    <a href="/site/{{ site_id }}" class="btn">Explore Site</a>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>

    <footer>
        <p>&copy; 2024 Smart Cultural Tourism Assistant. All rights reserved.</p>
    </footer>
</body>
</html>
        ''',
        
        'site_detail.html': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ site.name }} - Cultural Explorer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }
        
        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #4a5568;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        
        .nav-links a {
            text-decoration: none;
            color: #4a5568;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: #667eea;
        }
        
        .site-header {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .site-header h1 {
            color: #4a5568;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        
        .site-location {
            color: #667eea;
            font-size: 1.2rem;
            font-weight: 600;
        }
        
        .content-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 2rem;
            margin-bottom: 2rem;
        }
        
        .main-content {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
        }
        
        .sidebar {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
        }
        
        .section {
            margin-bottom: 2rem;
        }
        
        .section h2 {
            color: #4a5568;
            margin-bottom: 1rem;
            border-bottom: 2px solid #667eea;
            padding-bottom: 0.5rem;
        }
        
        .fun-facts {
            list-style: none;
        }
        
        .fun-facts li {
            background: #f7fafc;
            padding: 1rem;
            margin-bottom: 0.5rem;
            border-left: 4px solid #667eea;
            border-radius: 5px;
        }
        
        .attraction-card {
            background: #f7fafc;
            padding: 1rem;
            margin-bottom: 1rem;
            border-radius: 10px;
            border-left: 4px solid #764ba2;
        }
        
        .attraction-name {
            font-weight: 600;
            color: #4a5568;
        }
        
        .attraction-type {
            color: #667eea;
            font-size: 0.9rem;
        }
        
        .attraction-distance {
            color: #666;
            font-size: 0.9rem;
        }
        
        .ai-assistant {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
        }
        
        .chat-container {
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 1rem;
            padding: 1rem;
            background: #f7fafc;
            border-radius: 10px;
        }
        
        .message {
            margin-bottom: 1rem;
            padding: 0.5rem 1rem;
            border-radius: 10px;
        }
        
        .user-message {
            background: #667eea;
            color: white;
            margin-left: 2rem;
        }
        
        .ai-message {
            background: #e2e8f0;
            margin-right: 2rem;
        }
        
        .chat-input {
            display: flex;
            gap: 1rem;
        }
        
        .chat-input input {
            flex: 1;
            padding: 0.5rem 1rem;
            border: 1px solid #cbd5e0;
            border-radius: 20px;
            outline: none;
        }
        
        .btn {
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 20px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        footer {
            text-align: center;
            padding: 2rem;
            color: white;
        }
        
        @media (max-width: 768px) {
            .nav-links {
                flex-direction: column;
                gap: 1rem;
            }
            
            .content-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo">🌍 Cultural Explorer</div>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/discover">Discover</a>
                <a href="/ar_experience">AR Experience</a>
                <a href="/voice_assistant">Voice Assistant</a>
                <a href="/offline_mode">Offline Mode</a>
            </div>
        </nav>
    </header>

    <div class="container">
        <div class="site-header">
            <h1>{{ site.name }}</h1>
            <div class="site-location">{{ site.location }}</div>
        </div>

        <div class="content-grid">
            <div class="main-content">
                <div class="section">
                    <h2>About</h2>
                    <p>{{ site.description }}</p>
                </div>
                
                <div class="section">
                    <h2>History</h2>
                    <p>{{ site.history }}</p>
                </div>
                
                <div class="section">
                    <h2>Architecture</h2>
                    <p><strong>Style:</strong> {{ site.architectural_style }}</p>
                </div>
                
                <div class="section">
                    <h2>Fun Facts</h2>
                    <ul class="fun-facts">
                        {% for fact in site.fun_facts %}
                        <li>{{ fact }}</li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            <div class="sidebar">
                <div class="section">
                    <h2>Nearby Attractions</h2>
                    {% for attraction in nearby_attractions %}
                    <div class="attraction-card">
                        <div class="attraction-name">{{ attraction.name }}</div>
                        <div class="attraction-type">{{ attraction.type }}</div>
                        <div class="attraction-distance">{{ attraction.distance }} away</div>
                    </div>
                    {% endfor %}
                </div>
                
                <div class="section">
                    <h2>Available Languages</h2>
                    <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;">
                        {% for language in site.languages %}
                        <span style="background: #667eea; color: white; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.9rem;">
                            {{ language }}
                        </span>
                        {% endfor %}
                    </div>
                </div>
            </div>
        </div>

        <div class="ai-assistant">
            <h2>AI Cultural Assistant</h2>
            <p>Ask me anything about {{ site.name }}</p>
            
            <div class="chat-container" id="chatContainer">
                <div class="message ai-message">
                    Hello! I'm your cultural assistant. Ask me anything about {{ site.name }} - its history, architecture, or significance!
                </div>
            </div>
            
            <div class="chat-input">
                <input type="text" id="questionInput" placeholder="Ask a question about {{ site.name }}...">
                <button class="btn" onclick="askQuestion()">Ask</button>
            </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2024 Smart Cultural Tourism Assistant. All rights reserved.</p>
    </footer>

    <script>
        function askQuestion() {
            const input = document.getElementById('questionInput');
            const question = input.value.trim();
            const chatContainer = document.getElementById('chatContainer');
            
            if (!question) return;
            
            // Add user message
            const userMessage = document.createElement('div');
            userMessage.className = 'message user-message';
            userMessage.textContent = question;
            chatContainer.appendChild(userMessage);
            
            // Clear input
            input.value = '';
            
            // Show loading
            const loadingMessage = document.createElement('div');
            loadingMessage.className = 'message ai-message';
            loadingMessage.textContent = 'Thinking...';
            chatContainer.appendChild(loadingMessage);
            
            // Scroll to bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;
            
            // Send request to backend
            fetch('/api/ask_question', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    question: question,
                    site_id: '{{ site_id }}'
                })
            })
            .then(response => response.json())
            .then(data => {
                // Remove loading message
                chatContainer.removeChild(loadingMessage);
                
                // Add AI response
                const aiMessage = document.createElement('div');
                aiMessage.className = 'message ai-message';
                aiMessage.innerHTML = `<strong>Answer:</strong> ${data.answer}<br><small>${data.timestamp}</small>`;
                chatContainer.appendChild(aiMessage);
                
                // Scroll to bottom
                chatContainer.scrollTop = chatContainer.scrollHeight;
            })
            .catch(error => {
                console.error('Error:', error);
                chatContainer.removeChild(loadingMessage);
                
                const errorMessage = document.createElement('div');
                errorMessage.className = 'message ai-message';
                errorMessage.textContent = 'Sorry, I encountered an error. Please try again.';
                chatContainer.appendChild(errorMessage);
            });
        }
        
        // Allow pressing Enter to send message
        document.getElementById('questionInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                askQuestion();
            }
        });
    </script>
</body>
</html>
        ''',
        
        'ar_experience.html': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AR Experience - Cultural Explorer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }
        
        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #4a5568;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        
        .nav-links a {
            text-decoration: none;
            color: #4a5568;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: #667eea;
        }
        
        .page-header {
            text-align: center;
            color: white;
            margin-bottom: 3rem;
        }
        
        .page-header h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .ar-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .ar-view {
            width: 100%;
            height: 400px;
            background: linear-gradient(135deg, #e2e8f0, #cbd5e0);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        .ar-overlay {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            color: white;
        }
        
        .ar-controls {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-bottom: 2rem;
        }
        
        .btn {
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 25px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn-outline {
            background: transparent;
            border: 2px solid #667eea;
            color: #667eea;
        }
        
        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }
        
        .feature-card {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        footer {
            text-align: center;
            padding: 2rem;
            color: white;
        }
        
        @media (max-width: 768px) {
            .nav-links {
                flex-direction: column;
                gap: 1rem;
            }
            
            .ar-controls {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo">🌍 Cultural Explorer</div>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/discover">Discover</a>
                <a href="/ar_experience">AR Experience</a>
                <a href="/voice_assistant">Voice Assistant</a>
                <a href="/offline_mode">Offline Mode</a>
            </div>
        </nav>
    </header>

    <div class="container">
        <div class="page-header">
            <h1>Augmented Reality Experience</h1>
            <p>Bring cultural heritage to life with AR technology</p>
        </div>

        <div class="ar-container">
            <div class="ar-view">
                <div class="ar-overlay">
                    <div style="font-size: 4rem; margin-bottom: 1rem;">📱</div>
                    <h2 style="color: #333; margin-bottom: 1rem;">AR View</h2>
                    <p style="color: #666; text-align: center; max-width: 500px;">
                        Point your camera at a heritage site or use the demo mode to experience augmented reality reconstructions and information overlays.
                    </p>
                </div>
            </div>
            
            <div class="ar-controls">
                <button class="btn" onclick="startAR()">Start AR Camera</button>
                <button class="btn btn-outline" onclick="startDemo()">Demo Mode</button>
                <button class="btn btn-outline" onclick="showInfo()">Show Information</button>
            </div>
            
            <div id="arInfo" style="display: none;">
                <h3>Historical Reconstruction</h3>
                <p>This AR view shows how this site would have looked in its original state, with detailed information about architectural features and historical context.</p>
            </div>
        </div>

        <div class="features-grid">
            <div class="feature-card">
                <div class="feature-icon">🏛️</div>
                <h3>3D Reconstructions</h3>
                <p>View accurate 3D models of historical structures as they originally appeared.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>Interactive Info</h3>
                <p>Tap on different parts of the structure to learn about their significance and history.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <h3>Color Restoration</h3>
                <p>See how buildings and artifacts would have looked with their original colors and decorations.</p>
            </div>
            
            <div class="feature-card">
                <div class="feature-icon">📷</div>
                <h3>Photo Mode</h3>
                <p>Take pictures with AR elements and share your cultural discoveries.</p>
            </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2024 Smart Cultural Tourism Assistant. All rights reserved.</p>
    </footer>

    <script>
        function startAR() {
            alert('AR Camera would start here. In a real app, this would access your device camera and overlay AR content.');
        }
        
        function startDemo() {
            alert('Starting AR Demo Mode. Showing sample reconstructions and information overlays.');
            document.getElementById('arInfo').style.display = 'block';
        }
        
        function showInfo() {
            const infoDiv = document.getElementById('arInfo');
            infoDiv.style.display = infoDiv.style.display === 'none' ? 'block' : 'none';
        }
    </script>
</body>
</html>
        ''',
        
        'voice_assistant.html': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Voice Assistant - Cultural Explorer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }
        
        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #4a5568;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        
        .nav-links a {
            text-decoration: none;
            color: #4a5568;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: #667eea;
        }
        
        .page-header {
            text-align: center;
            color: white;
            margin-bottom: 3rem;
        }
        
        .page-header h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .assistant-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
        }
        
        .voice-interface {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .voice-circle {
            width: 150px;
            height: 150px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            margin: 0 auto 2rem;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: transform 0.3s;
            position: relative;
        }
        
        .voice-circle:hover {
            transform: scale(1.05);
        }
        
        .voice-circle.listening {
            animation: pulse 1.5s infinite;
        }
        
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        .voice-icon {
            font-size: 3rem;
            color: white;
        }
        
        .chat-container {
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 2rem;
            padding: 1rem;
            background: #f7fafc;
            border-radius: 10px;
        }
        
        .message {
            margin-bottom: 1rem;
            padding: 1rem;
            border-radius: 10px;
            max-width: 80%;
        }
        
        .user-message {
            background: #667eea;
            color: white;
            margin-left: auto;
            text-align: right;
        }
        
        .ai-message {
            background: #e2e8f0;
            margin-right: auto;
        }
        
        .language-selector {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .language-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
            margin-top: 1rem;
        }
        
        .lang-btn {
            padding: 8px 16px;
            background: #e2e8f0;
            border: none;
            border-radius: 15px;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .lang-btn.active {
            background: #667eea;
            color: white;
        }
        
        .suggested-questions {
            margin-top: 2rem;
        }
        
        .suggestions {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }
        
        .suggestion-card {
            background: #f7fafc;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .suggestion-card:hover {
            background: #e2e8f0;
        }
        
        footer {
            text-align: center;
            padding: 2rem;
            color: white;
        }
        
        @media (max-width: 768px) {
            .nav-links {
                flex-direction: column;
                gap: 1rem;
            }
            
            .language-buttons {
                flex-direction: column;
                align-items: center;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo">🌍 Cultural Explorer</div>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/discover">Discover</a>
                <a href="/ar_experience">AR Experience</a>
                <a href="/voice_assistant">Voice Assistant</a>
                <a href="/offline_mode">Offline Mode</a>
            </div>
        </nav>
    </header>

    <div class="container">
        <div class="page-header">
            <h1>Voice Assistant</h1>
            <p>Ask questions about cultural sites using voice commands</p>
        </div>

        <div class="assistant-container">
            <div class="language-selector">
                <h3>Select Language</h3>
                <div class="language-buttons">
                    <button class="lang-btn active" onclick="changeLanguage('English')">English</button>
                    <button class="lang-btn" onclick="changeLanguage('Spanish')">Spanish</button>
                    <button class="lang-btn" onclick="changeLanguage('French')">French</button>
                    <button class="lang-btn" onclick="changeLanguage('German')">German</button>
                    <button class="lang-btn" onclick="changeLanguage('Japanese')">Japanese</button>
                </div>
            </div>

            <div class="voice-interface">
                <div class="voice-circle" id="voiceCircle" onclick="toggleListening()">
                    <div class="voice-icon">🎤</div>
                </div>
                <p id="statusText">Click the microphone to start speaking</p>
            </div>

            <div class="chat-container" id="chatContainer">
                <div class="message ai-message">
                    Hello! I'm your cultural voice assistant. Ask me anything about heritage sites, history, or architecture in your preferred language.
                </div>
            </div>

            <div class="suggested-questions">
                <h3>Suggested Questions</h3>
                <div class="suggestions">
                    <div class="suggestion-card" onclick="askQuestion('Tell me about the history')">
                        "Tell me about the history"
                    </div>
                    <div class="suggestion-card" onclick="askQuestion('What is the architectural style?')">
                        "What is the architectural style?"
                    </div>
                    <div class="suggestion-card" onclick="askQuestion('How was it constructed?')">
                        "How was it constructed?"
                    </div>
                    <div class="suggestion-card" onclick="askQuestion('What is the cultural significance?')">
                        "What is the cultural significance?"
                    </div>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2024 Smart Cultural Tourism Assistant. All rights reserved.</p>
    </footer>

    <script>
        let isListening = false;
        let currentLanguage = 'English';
        
        function toggleListening() {
            const voiceCircle = document.getElementById('voiceCircle');
            const statusText = document.getElementById('statusText');
            
            if (!isListening) {
                // Start listening
                isListening = true;
                voiceCircle.classList.add('listening');
                statusText.textContent = 'Listening... Speak now';
                
                // Simulate voice recognition
                setTimeout(() => {
                    const questions = [
                        "Tell me about the history of this place",
                        "What is the architectural style?",
                        "How old is this structure?",
                        "Who built this monument?",
                        "What is the cultural significance?"
                    ];
                    const randomQuestion = questions[Math.floor(Math.random() * questions.length)];
                    processVoiceInput(randomQuestion);
                }, 2000);
                
            } else {
                // Stop listening
                isListening = false;
                voiceCircle.classList.remove('listening');
                statusText.textContent = 'Click the microphone to start speaking';
            }
        }
        
        function processVoiceInput(question) {
            const chatContainer = document.getElementById('chatContainer');
            
            // Add user message
            const userMessage = document.createElement('div');
            userMessage.className = 'message user-message';
            userMessage.textContent = question;
            chatContainer.appendChild(userMessage);
            
            // Show AI response
            setTimeout(() => {
                const responses = {
                    "history": "This site has a rich history dating back centuries. It was constructed during a significant period and has witnessed many historical events.",
                    "architecture": "The architecture represents a unique blend of styles from different eras, showcasing excellent craftsmanship and cultural influences.",
                    "construction": "It took many years and skilled artisans to construct this magnificent structure using traditional techniques and materials.",
                    "significance": "This site holds immense cultural and historical importance, representing the heritage and traditions of the region."
                };
                
                let answer = "This is a culturally significant site with amazing historical value and architectural beauty.";
                for (const [key, response] of Object.entries(responses)) {
                    if (question.toLowerCase().includes(key)) {
                        answer = response;
                        break;
                    }
                }
                
                const aiMessage = document.createElement('div');
                aiMessage.className = 'message ai-message';
                aiMessage.innerHTML = `<strong>Assistant:</strong> ${answer}`;
                chatContainer.appendChild(aiMessage);
                
                // Stop listening
                isListening = false;
                document.getElementById('voiceCircle').classList.remove('listening');
                document.getElementById('statusText').textContent = 'Click the microphone to start speaking';
                
                // Scroll to bottom
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }, 1000);
            
            // Scroll to bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function changeLanguage(language) {
            currentLanguage = language;
            
            // Update active button
            document.querySelectorAll('.lang-btn').forEach(btn => {
                btn.classList.remove('active');
                if (btn.textContent === language) {
                    btn.classList.add('active');
                }
            });
            
            // Show confirmation
            const chatContainer = document.getElementById('chatContainer');
            const message = document.createElement('div');
            message.className = 'message ai-message';
            message.textContent = `Language changed to ${language}. You can now speak in ${language}.`;
            chatContainer.appendChild(message);
            
            // Send to backend
            fetch('/api/change_language', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ language: language })
            });
            
            // Scroll to bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function askQuestion(question) {
            processVoiceInput(question);
        }
    </script>
</body>
</html>
        ''',
        
        'offline_mode.html': '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Offline Mode - Cultural Explorer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background: rgba(255, 255, 255, 0.95);
            padding: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        
        nav {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 2rem;
        }
        
        .logo {
            font-size: 1.8rem;
            font-weight: bold;
            color: #4a5568;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
        }
        
        .nav-links a {
            text-decoration: none;
            color: #4a5568;
            font-weight: 500;
            transition: color 0.3s;
        }
        
        .nav-links a:hover {
            color: #667eea;
        }
        
        .page-header {
            text-align: center;
            color: white;
            margin-bottom: 3rem;
        }
        
        .page-header h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        
        .offline-container {
            background: rgba(255, 255, 255, 0.95);
            padding: 2rem;
            border-radius: 15px;
            margin-bottom: 2rem;
        }
        
        .status-card {
            background: #f7fafc;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 2rem;
            border-left: 4px solid #48bb78;
        }
        
        .status-offline {
            border-left-color: #ed8936;
        }
        
        .downloads-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin: 3rem 0;
        }
        
        .download-card {
            background: #f7fafc;
            padding: 2rem;
            border-radius: 10px;
            text-align: center;
            border: 2px solid #e2e8f0;
            transition: border-color 0.3s;
        }
        
        .download-card:hover {
            border-color: #667eea;
        }
        
        .download-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        .btn {
            padding: 10px 20px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 20px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s;
            margin-top: 1rem;
        }
        
        .btn:hover {
            transform: translateY(-2px);
        }
        
        .btn-outline {
            background: transparent;
            border: 2px solid #667eea;
            color: #667eea;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #e2e8f0;
            border-radius: 4px;
            margin: 1rem 0;
            overflow: hidden;
        }
        
        .progress {
            height: 100%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 4px;
            transition: width 0.3s;
        }
        
        .feature-list {
            list-style: none;
            margin: 2rem 0;
        }
        
        .feature-list li {
            padding: 0.5rem 0;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .feature-list li:before {
            content: "✓";
            color: #48bb78;
            font-weight: bold;
            margin-right: 0.5rem;
        }
        
        footer {
            text-align: center;
            padding: 2rem;
            color: white;
        }
        
        @media (max-width: 768px) {
            .nav-links {
                flex-direction: column;
                gap: 1rem;
            }
        }
    </style>
</head>
<body>
    <header>
        <nav>
            <div class="logo">🌍 Cultural Explorer</div>
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/discover">Discover</a>
                <a href="/ar_experience">AR Experience</a>
                <a href="/voice_assistant">Voice Assistant</a>
                <a href="/offline_mode">Offline Mode</a>
            </div>
        </nav>
    </header>

    <div class="container">
        <div class="page-header">
            <h1>Offline Mode</h1>
            <p>Access cultural information without internet connection</p>
        </div>

        <div class="offline-container">
            <div class="status-card" id="statusCard">
                <h2>Online Mode</h2>
                <p>You are currently connected to the internet. Download content for offline access.</p>
                <button class="btn" onclick="toggleOfflineMode()">Switch to Offline Mode</button>
            </div>

            <div class="downloads-grid">
                <div class="download-card">
                    <div class="download-icon">🏛️</div>
                    <h3>Heritage Sites Guide</h3>
                    <p>Complete information about major cultural heritage sites</p>
                    <div class="progress-bar">
                        <div class="progress" style="width: 100%"></div>
                    </div>
                    <button class="btn" onclick="downloadContent('sites')">Download (25 MB)</button>
                </div>
                
                <div class="download-card">
                    <div class="download-icon">🗺️</div>
                    <h3>Offline Maps</h3>
                    <p>Interactive maps and navigation for heritage sites</p>
                    <div class="progress-bar">
                        <div class="progress" style="width: 75%"></div>
                    </div>
                    <button class="btn" onclick="downloadContent('maps')">Download (50 MB)</button>
                </div>
                
                <div class="download-card">
                    <div class="download-icon">🎧</div>
                    <h3>Audio Guides</h3>
                    <p>Multilingual audio tours and descriptions</p>
                    <div class="progress-bar">
                        <div class="progress" style="width: 60%"></div>
                    </div>
                    <button class="btn" onclick="downloadContent('audio')">Download (100 MB)</button>
                </div>
                
                <div class="download-card">
                    <div class="download-icon">📸</div>
                    <h3>AR Content</h3>
                    <p>Augmented reality models and experiences</p>
                    <div class="progress-bar">
                        <div class="progress" style="width: 40%"></div>
                    </div>
                    <button class="btn" onclick="downloadContent('ar')">Download (150 MB)</button>
                </div>
            </div>

            <div style="margin-top: 3rem;">
                <h2>Offline Features</h2>
                <ul class="feature-list">
                    <li>Access to downloaded site information and history</li>
                    <li>Interactive offline maps with navigation</li>
                    <li>Multilingual audio guides and descriptions</li>
                    <li>AR experiences without internet connection</li>
                    <li>Basic voice assistant functionality</li>
                    <li>Photo gallery and saved content</li>
                </ul>
            </div>

            <div style="text-align: center; margin-top: 2rem;">
                <button class="btn" onclick="downloadAll()">Download All Content (325 MB)</button>
                <button class="btn btn-outline" onclick="clearDownloads()" style="margin-left: 1rem;">Clear Downloads</button>
            </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2024 Smart Cultural Tourism Assistant. All rights reserved.</p>
    </footer>

    <script>
        let isOfflineMode = false;
        
        function toggleOfflineMode() {
            isOfflineMode = !isOfflineMode;
            const statusCard = document.getElementById('statusCard');
            
            if (isOfflineMode) {
                statusCard.innerHTML = `
                    <h2>Offline Mode Active</h2>
                    <p>You are now in offline mode. All downloaded content is available.</p>
                    <button class="btn" onclick="toggleOfflineMode()">Switch to Online Mode</button>
                `;
                statusCard.classList.add('status-offline');
            } else {
                statusCard.innerHTML = `
                    <h2>Online Mode</h2>
                    <p>You are currently connected to the internet. Download content for offline access.</p>
                    <button class="btn" onclick="toggleOfflineMode()">Switch to Offline Mode</button>
                `;
                statusCard.classList.remove('status-offline');
            }
        }
        
        function downloadContent(type) {
            alert(`Starting download of ${type} content...`);
            // Simulate download progress
            simulateDownloadProgress(type);
        }
        
        function downloadAll() {
            alert('Starting download of all offline content (325 MB)...');
            // Simulate download progress for all types
            ['sites', 'maps', 'audio', 'ar'].forEach(type => {
                simulateDownloadProgress(type);
            });
        }
        
        function clearDownloads() {
            if (confirm('Are you sure you want to clear all downloaded content?')) {
                alert('All downloaded content has been cleared.');
                // Reset progress bars
                document.querySelectorAll('.progress').forEach(progress => {
                    progress.style.width = '0%';
                });
            }
        }
        
        function simulateDownloadProgress(type) {
            const progressBars = {
                'sites': document.querySelector('.download-card:nth-child(1) .progress'),
                'maps': document.querySelector('.download-card:nth-child(2) .progress'),
                'audio': document.querySelector('.download-card:nth-child(3) .progress'),
                'ar': document.querySelector('.download-card:nth-child(4) .progress')
            };
            
            const progressBar = progressBars[type];
            if (progressBar) {
                let width = parseInt(progressBar.style.width) || 0;
                const interval = setInterval(() => {
                    if (width >= 100) {
                        clearInterval(interval);
                        alert(`${type} content downloaded successfully!`);
                    } else {
                        width += 10;
                        progressBar.style.width = width + '%';
                    }
                }, 200);
            }
        }
    </script>
</body>
</html>
        '''
    }
    
    for filename, content in templates.items():
        with open(f'templates/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)

# Create requirements.txt
requirements_content = '''Flask==2.3.3
Werkzeug==2.3.7
'''

with open('requirements.txt', 'w') as f:
    f.write(requirements_content)

# Create README.md
readme_content = '''# Smart Cultural Tourism Assistant

A Flask-based web application that provides an intelligent cultural tourism experience with AI-powered guidance, augmented reality features, and multilingual support.

## Features

- **Smart Discovery**: Explore cultural heritage sites with detailed information
- **AI Assistant**: Ask questions about sites and get intelligent responses
- **Augmented Reality**: AR experiences for historical reconstructions
- **Voice Assistant**: Voice-controlled interface in multiple languages
- **Offline Mode**: Access content without internet connection
- **Multilingual Support**: Available in multiple languages

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd smart-cultural-tourism
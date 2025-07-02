from django.shortcuts import render
from django.http import JsonResponse

# Conversation tree definition - Fixed with proper nesting
conversation_tree = {
    "hello": {
        "response": "Welcome! Please choose an option:\n1. Web Development\n2. Internship\n3. AI/ML\n4. Mobile App",
        "next": {
            "1": {
                "response": "Great! Choose a track:\n1. Full Stack Dev\n2. Frontend\n3. Backend",
                "next": {
                    "1": {
                        "response": "Full Stack Development: Learn both frontend and backend technologies like React, Node.js, databases, and deployment."
                    },
                    "2": {
                        "response": "Frontend Development: Master HTML, CSS, JavaScript, React, Vue.js, and responsive design."
                    },
                    "3": {
                        "response": "Backend Development: Learn server-side programming with Python/Django, Node.js, databases, and APIs."
                    }
                }
            },
            "2": {
                "response": "Internship Info:\n1. Eligibility\n2. Duration\n3. Apply Now",
                "next": {
                    "1": {
                        "response": "Eligibility: Students in final year or recent graduates with basic programming knowledge."
                    },
                    "2": {
                        "response": "Duration: Our internship program runs for 3-6 months with flexible timings."
                    },
                    "3": {
                        "response": "Apply Now: Please visit our careers page or send your resume to hr@company.com"
                    }
                }
            },
            "3": {
                "response": "AI/ML Paths:\n1. Machine Learning\n2. Deep Learning\n3. Data Science",
                "next": {
                    "1": {
                        "response": "Machine Learning: Learn algorithms, supervised/unsupervised learning, and practical ML applications."
                    },
                    "2": {
                        "response": "Deep Learning: Master neural networks, TensorFlow, PyTorch, and advanced AI models."
                    },
                    "3": {
                        "response": "Data Science: Learn data analysis, visualization, statistics, and predictive modeling."
                    }
                }
            },
            "4": {
                "response": "Mobile App Dev Options:\n1. Android\n2. iOS\n3. Flutter",
                "next": {
                    "1": {
                        "response": "Android Development: Learn Java/Kotlin, Android Studio, and Google Play Store deployment."
                    },
                    "2": {
                        "response": "iOS Development: Master Swift, Xcode, and App Store guidelines for iPhone/iPad apps."
                    },
                    "3": {
                        "response": "Flutter Development: Build cross-platform apps with Dart and Flutter framework."
                    }
                }
            }
        }
    }
}

# Session-based conversation handler - Fixed logic
def get_bot_response(user_input, session):
    # Initialize session
    if 'conversation_path' not in session:
        session['conversation_path'] = []
    
    path = session['conversation_path']
    current_node = conversation_tree

    # Start of conversation
    if not path and user_input.lower() == "hello":
        session['conversation_path'] = ["hello"]
        session.modified = True
        return conversation_tree["hello"]["response"]
    
    # Navigate through conversation tree
    try:
        for step in path:
            if step in current_node:
                current_node = current_node[step]
            elif 'next' in current_node and step in current_node['next']:
                current_node = current_node['next'][step]
            else:
                raise KeyError("Invalid path step")

        # Handle user input
        if 'next' in current_node and user_input in current_node['next']:
            session['conversation_path'].append(user_input)
            session.modified = True
            next_node = current_node['next'][user_input]
            response = next_node['response']

            # End node
            if 'next' not in next_node:
                session['conversation_path'] = []  # Clear for restart
                session.modified = True
                response += "\n\nSay 'hello' to start over."

            return response
        else:
            valid_keys = list(current_node.get('next', {}).keys())
            return f"Invalid choice. Valid options: {', '.join(valid_keys)}"
        
    except Exception as e:
        session['conversation_path'] = []
        session.modified = True
        return "Something went wrong. Please say 'hello' to restart."

# Views
def chatbot_view(request):
    return render(request, "blog/index.html")

def get_response(request):
    if request.method == "POST":
        user_input = request.POST.get("message", "").strip()
        if user_input:
            response = get_bot_response(user_input, request.session)
            return JsonResponse({"message": response})
        else:
            return JsonResponse({"message": "Please enter a message."})
    
    return JsonResponse({"error": "Invalid request method"})
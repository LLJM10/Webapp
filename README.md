# Webapp
Entire Code for the webapp

🚀 Setup Instructions
1. Clone the repository
git clone https://github.com/yourusername/yourrepo.git
cd yourrepo

2. Backend Setup (Django)

Create & activate virtual environment

Windows (PowerShell):

py -m venv venv
.\venv\Scripts\activate


Git Bash / WSL:

python3 -m venv venv
source venv/bin/activate


Install dependencies

pip install -r requirements.txt


Run database migrations

cd backend
py manage.py migrate


Start backend server

py manage.py runserver


✅ Now backend runs at: http://127.0.0.1:8000

3. Frontend Setup (Nuxt)

Navigate to frontend folder

cd frontend


Install dependencies

npm install


Start development server

npm run dev


✅ Now frontend runs at: http://localhost:3000
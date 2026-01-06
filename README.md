Setup Instructions

1. Installations
    Install git
    Install Node.js


1. Clone the repository
    naviagte to folder you want the repository (projetct) to be in
    git clone https://github.com/LLJM10/Webapp.git
    git clone https://github.com/LLJM10/Webapp.git -b branch-name

2. Create virtual environment
    Open Git Bash Terminal
    navigate to Webapp Folder
    #LINUX: source venv/bin/activate #WINDOWS: 
source venv/Scripts/activate
3. Start Backend Server
    cd backend
    (pip install python) #pip install django djangorestframework django-cors-headers djangorestframework-simplejwt
    python manage.py runserver
    
    Now backend runs at: http://127.0.0.1:8000

4. Start frontend
    Open new terminal
    cd frontend
    (pip install npm) #npm install
    npm run dev

    
    Now frontend runs at: http://localhost:3000

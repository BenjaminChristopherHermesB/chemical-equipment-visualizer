# Chemical Equipment Parameter Visualizer - Developer Guide

This document contains technical details, setup instructions, and architecture information for developers working on the project.

## 🚀 Features

- **CSV Upload & Processing**: Upload CSV files with equipment data (Equipment Name, Type, Flowrate, Pressure, Temperature)
- **Statistical Analysis**: Automatic computation of summary statistics (mean, min, max, standard deviation)
- **Data Visualizations**: Interactive charts for flowrate, pressure, temperature, and equipment type distribution
- **History Management**: Automatic storage and retrieval of last 5 uploaded datasets
- **PDF Reports**: Generate downloadable PDF reports with statistics and equipment data
- **Token Authentication**: Secure user authentication for both web and desktop clients
- **Cross-Platform**: Web app (React) and desktop app (PyQt5) consuming the same backend API

## 📁 Project Structure

```
chemical-equipment-visualizer/
├── backend/                      # Django REST API
│   ├── equipment_visualizer/     # Django project settings
│   ├── api/                      # REST API app
│   │   ├── models.py            # EquipmentDataset model
│   │   ├── views.py             # API endpoints
│   │   ├── serializers.py       # DRF serializers
│   │   ├── utils.py             # CSV processing & PDF generation
│   │   └── urls.py              # API routing
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── Procfile                 # Render deployment
│   └── build.sh                 # Render build script
│
├── frontend-web/                # React web frontend
│   ├── src/
│   │   ├── components/          # React components
│   │   │   ├── Login.jsx       # Login/Register
│   │   │   ├── Dashboard.jsx   # Main dashboard
│   │   │   ├── CSVUpload.jsx   # CSV upload with drag-and-drop
│   │   │   ├── Charts.jsx      # Chart.js visualizations
│   │   │   ├── DataTable.jsx   # Data grid
│   │   │   ├── SummaryStats.jsx # Statistics display
│   │   │   └── History.jsx     # Dataset history
│   │   ├── services/
│   │   │   └── api.js          # Axios API client
│   │   └── App.jsx              # Main app component
│   ├── package.json
│   ├── vercel.json              # Vercel deployment config
│   └── .env.example
│
└── frontend-desktop/            # PyQt5 desktop frontend
    ├── ui/                       # PyQt5 UI components
    │   ├── main_window.py       # Main application window
    │   ├── login_dialog.py      # Login/Register dialog
    │   ├── data_table_widget.py # Data table widget
    │   ├── charts_widget.py     # Matplotlib charts
    │   ├── summary_widget.py    # Statistics widget
    │   └── history_widget.py    # History list widget
    ├── api/
    │   └── client.py            # Backend API client
    ├── main.py                   # Application entry point
    ├── requirements.txt
    └── ChemicalEquipmentVisualizer.spec  # PyInstaller config
```

## 🛠️ Tech Stack

### Backend
- **Django 4.2** - Web framework
- **Django REST Framework** - REST API
- **Pandas** - CSV processing and data analysis
- **ReportLab** - PDF generation
- **SQLite** (local) / **PostgreSQL** (production)
- **CORS Headers** - Cross-origin support
- **Token Authentication** - User authentication

### Web Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **CSS3** - Modern styling with gradients

### Desktop Frontend
- **PyQt5** - GUI framework
- **Matplotlib** - Data visualization
- **Requests** - HTTP client
- **PyInstaller** - Executable packaging

## 📦 Installation & Setup

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (create `.env` file):
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create superuser** (optional, for admin panel):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**:
   ```bash
   python manage.py runserver
   ```

   Backend will be available at `http://localhost:8000`

### Web Frontend Setup

1. **Navigate to web frontend directory**:
   ```bash
   cd frontend-web
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment** (create `.env` file):
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

4. **Run development server**:
   ```bash
   npm run dev
   ```

   Web app will be available at `http://localhost:5173`

### Desktop Frontend Setup

1. **Navigate to desktop frontend directory**:
   ```bash
   cd frontend-desktop
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

   On first launch, you'll be prompted to enter the API URL (default: `http://localhost:8000/api`)

## 🚀 Deployment

### Backend Deployment (Render)

1. **Create account** on [Render.com](https://render.com)

2. **Create new Web Service**:
   - Connect your GitHub repository
   - Select `backend` directory
   - Environment: Python 3
   - Build Command: `./build.sh`
   - Start Command: `gunicorn equipment_visualizer.wsgi:application`

3. **Set environment variables**:
   ```
   DEBUG=False
   SECRET_KEY=<generate-strong-key>
   ALLOWED_HOSTS=.onrender.com
   DATABASE_URL=<provided-by-render>
   CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
   ```

4. **Deploy** - Render will auto-deploy on push to main branch

### Web Frontend Deployment (Vercel)

1. **Install Vercel CLI** (optional):
   ```bash
   npm install -g vercel
   ```

2. **Deploy via CLI**:
   ```bash
   cd frontend-web
   vercel
   ```

3. **Or connect GitHub** to Vercel dashboard for automatic deployments

4. **Set environment variable**:
   ```
   VITE_API_BASE_URL=https://your-backend.onrender.com/api
   ```

### Desktop App Packaging (PyInstaller)

1. **Navigate to desktop directory**:
   ```bash
   cd frontend-desktop
   ```

2. **Build executable**:
   ```bash
   pyinstaller ChemicalEquipmentVisualizer.spec
   ```

3. **Find executable** in `dist/` folder

## 📊 CSV Format

Required columns:
- **Equipment Name** - String
- **Type** - String (e.g., Pump, Valve, Tank)
- **Flowrate** - Numeric
- **Pressure** - Numeric
- **Temperature** - Numeric

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump A,Pump,150.5,45.2,68.3
Valve B,Valve,120.3,38.7,72.1
Tank C,Tank,200.8,50.1,65.4
```

## 🐛 Troubleshooting

### Backend Issues
- **Port already in use**: Change port with `python manage.py runserver 8001`
- **Database locked**: Delete `db.sqlite3` and run migrations again
- **CORS errors**: Update `CORS_ALLOWED_ORIGINS` in settings.py

### Web Frontend Issues
- **API connection failed**: Check `.env` file has correct `VITE_API_BASE_URL`
- **Build errors**: Delete `node_modules` and run `npm install` again
- **Charts not displaying**: Ensure Chart.js is properly installed

### Desktop App Issues
- **Import errors**: Reinstall dependencies with `pip install -r requirements.txt`
- **API connection failed**: Check API URL in settings dialog
- **PyInstaller errors**: Ensure all dependencies are in requirements.txt

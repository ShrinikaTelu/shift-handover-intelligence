# 🔄 Shift Handover Intelligence

AI-powered shift handover report generation system using Google Gemini AI. Transform unstructured shift notes, alarms, and trends into professional, structured handover documents.

![Shift Handover Intelligence](frontend/src/assets/background.png)

## 🌐 Live Demo

- **Frontend**: [https://shrinikatelu.github.io/shift-handover-intelligence/](https://shrinikatelu.github.io/shift-handover-intelligence/)
- **Backend API**: [https://shift-handover-intelligence-production.up.railway.app/](https://shift-handover-intelligence-production.up.railway.app/)
- **API Documentation**: [https://shift-handover-intelligence-production.up.railway.app/docs](https://shift-handover-intelligence-production.up.railway.app/docs)

## ✨ Features

- 🤖 **AI-Powered Analysis**: Uses Google Gemini AI to intelligently parse and structure shift notes
- 📝 **Multiple Input Formats**: Accepts plain text notes, JSON alarms, and CSV trend data
- 📄 **PDF Generation**: Download professional PDF reports of handover summaries
- 🎨 **Modern UI**: Clean, responsive Angular frontend with industrial-themed design
- 🔒 **Session Management**: Each handover is saved with a unique session ID for retrieval
- 🚀 **Production Ready**: Deployed on Railway (backend) and GitHub Pages (frontend)

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Angular 18)                     │
│                    GitHub Pages Deployment                       │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Handover Form│  │ Result View  │  │ PDF Download         │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────┬───────────────────────────────────┘
                              │ HTTPS API Calls
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Backend (FastAPI + Python)                   │
│                      Railway Deployment                          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ REST API     │  │ Gemini AI    │  │ PDF Generator        │  │
│  │ Endpoints    │  │ Client       │  │ (ReportLab)          │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │   SQLite Database  │                        │
│                    └───────────────────┘                        │
└─────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- Google Gemini API Key ([Get one here](https://ai.google.dev))

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/ShrinikaTelu/shift-handover-intelligence.git
   cd shift-handover-intelligence
   ```

2. **Start the Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Set your Gemini API key
   export GEMINI_API_KEY="your_api_key_here"
   
   # Run the server
   python main.py
   ```
   Backend will be available at `http://localhost:8000`

3. **Start the Frontend**
   ```bash
   cd frontend
   npm install
   npm start
   ```
   Frontend will be available at `http://localhost:4200`

## 📁 Project Structure

```
shift-handover-intelligence/
├── backend/                    # FastAPI Python backend
│   ├── main.py                # Main application & API routes
│   ├── gemini_client.py       # Google Gemini AI integration
│   ├── pdf_generator.py       # PDF report generation
│   ├── database.py            # SQLite database operations
│   ├── schemas.py             # Pydantic models
│   └── requirements.txt       # Python dependencies
│
├── frontend/                   # Angular 18 frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/    # UI components
│   │   │   ├── services/      # API services
│   │   │   └── models/        # TypeScript interfaces
│   │   ├── environments/      # Environment configs
│   │   └── assets/            # Static assets
│   └── package.json           # Node dependencies
│
├── sample-data/               # Sample input files for testing
│   ├── sample-notes-1.txt
│   ├── pharma-notes.txt
│   ├── refinery-notes.txt
│   └── ...
│
├── Dockerfile                 # Docker config for Railway
├── deploy.sh                  # GitHub Pages deployment script
└── README.md                  # This file
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/handover/generate` | Generate handover report |
| GET | `/api/handover/{session_id}` | Retrieve saved handover |
| POST | `/api/handover/download-pdf` | Generate & download PDF |
| GET | `/api/handover/{session_id}/download-pdf` | Download PDF by session |

### Example Request

```bash
curl -X POST "https://shift-handover-intelligence-production.up.railway.app/api/handover/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "shiftNotes": "Morning shift started at 6 AM. Tank T-101 level at 85%. Pump P-201 showing vibration alerts. Maintenance called for inspection.",
    "alarmsJson": "[{\"time\": \"06:15\", \"tag\": \"P-201\", \"description\": \"High vibration\", \"priority\": \"High\"}]",
    "trendsCsv": "time,tag,value\n06:00,T-101,85\n06:30,T-101,87"
  }'
```

## 🚢 Deployment

### Backend (Railway)

1. Connect your GitHub repo to Railway
2. Set environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `ALLOWED_ORIGINS`: `https://shrinikatelu.github.io` (or `*` for testing)
3. Railway auto-deploys from the configured branch

### Frontend (GitHub Pages)

```bash
# Run the deployment script
chmod +x deploy.sh
./deploy.sh

# When prompted, enter your Railway backend URL
# Example: https://shift-handover-intelligence-production.up.railway.app
```

## 🧪 Testing

### Sample Data

The `sample-data/` folder contains test files:
- `sample-notes-1.txt` - Basic shift notes
- `pharma-notes.txt` - Pharmaceutical industry example
- `refinery-notes.txt` - Oil refinery example
- `alarms.json` - Sample alarm data
- `trends.csv` - Sample trend data

### Manual Testing

1. Open the frontend application
2. Paste shift notes in the text area
3. Optionally add alarms JSON and trends CSV
4. Click "Generate Handover"
5. View the structured output
6. Download as PDF if needed

## 🛠️ Technologies

### Backend
- **FastAPI** - Modern Python web framework
- **Google Gemini AI** - Large language model for text analysis
- **SQLAlchemy** - Database ORM with async support
- **ReportLab** - PDF generation
- **Pydantic** - Data validation

### Frontend
- **Angular 18** - TypeScript framework
- **RxJS** - Reactive programming
- **Angular CLI** - Build tooling

### Deployment
- **Railway** - Backend hosting with Docker
- **GitHub Pages** - Frontend static hosting
- **angular-cli-ghpages** - Deployment automation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Shrinika Telu**
- GitHub: [@ShrinikaTelu](https://github.com/ShrinikaTelu)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:
1. Check the [API Documentation](https://shift-handover-intelligence-production.up.railway.app/docs)
2. Review the [Implementation Guide](IMPLEMENTATION_GUIDE.md)
3. Open an issue on GitHub

---

⭐ If you find this project useful, please give it a star on GitHub!

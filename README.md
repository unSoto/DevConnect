# 🤖 DevConnect - IT Job Search Telegram Bot

**DevConnect** is a modern Telegram bot designed to help with job searching and employee hiring in the IT field. The platform provides a convenient interface for creating profiles, viewing vacancies and resumes, and managing your career.

![Bot Preview](assets/welcome.png)

## ✨ Features

### For Job Seekers 🔍
- **Resume Creation** - convenient form for entering personal information
- **Vacancy Viewing** - navigation through available job offers
- **Profile Management** - editing and deleting resumes
- **User-Friendly Interface** - intuitive menu with buttons

### For Employers 🏢
- **Vacancy Creation** - detailed job description and requirements
- **Resume Viewing** - searching for suitable candidates
- **Vacancy Management** - editing and deleting job postings
- **Contact Information** - direct contacts for communication

## 🚀 Quick Start

### ⚙️ Setup After Upload

1. **Get bot token:**
   - Write to [@BotFather](https://t.me/botfather) in Telegram
   - Send `/newbot` and follow instructions
   - Save the received token

2. **Create config.py file:**
   ```python
   # Main configuration
   import os
   API_TOKEN = os.getenv("API_TOKEN", "YOUR_TOKEN_HERE")
   ```

3. **Or use environment variables:**
   ```bash
   export API_TOKEN="your_token"
   python src/main.py
   ```

### Prerequisites
- Python 3.11+
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd DevConnect
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the bot:**
   - Open `src/config.py`
   - Replace `API_TOKEN` with your token from BotFather

5. **Run the bot:**
   ```bash
   python src/main.py
   ```

## 📁 Project Structure

```
DevConnect/
├── assets/                 # Graphic resources
│   ├── welcome.png        # Welcome image
│   ├── resume.png         # Resume image
│   └── vacancy.png        # Vacancy image
├── src/
│   ├── main.py           # Application entry point
│   ├── config.py         # Configuration (API token)
│   ├── db.py            # Database operations
│   ├── utils.py         # Helper functions
│   └── handlers/        # Command handlers
│       ├── welcome.py   # Welcome menu
│       ├── seeker.py    # Job seeker functionality
│       └── employer.py  # Employer functionality
├── requirements.txt     # Python dependencies
├── devconnect.db       # SQLite database
└── README.md           # Documentation
```

## 🎯 Usage

### Getting Started
1. Start the bot with `/start` command
2. Choose role: **"🔎 Find Work"** or **"🧑‍💼 Find Employee"**
3. Follow the menu instructions

### For Job Seekers

**Creating Resume:**
- Click "📝 Create Resume"
- Fill in information:
  - Name
  - Specialization
  - Work experience
  - Skills
  - Contacts

**Viewing Vacancies:**
- Click "📋 View Vacancies"
- Use navigation buttons ⬅️➡️ to browse
- Each vacancy contains:
  - Company name
  - Position
  - Job requirements
  - Work conditions
  - Contacts

### For Employers

**Creating Vacancy:**
- Click "📝 Create Vacancy"
- Fill in information:
  - Company name
  - Position
  - Candidate requirements
  - Work conditions
  - Contacts

**Viewing Resumes:**
- Click "👥 View Resumes"
- Browse candidate profiles
- Each profile contains:
  - Specialist name
  - Specialization
  - Work experience
  - Skills
  - Contacts

## ⚙️ Configuration

### Getting API Token
1. Write to [@BotFather](https://t.me/botfather) in Telegram
2. Send `/newbot` command
3. Choose bot name
4. Copy the received token
5. Paste token into `src/config.py`

### Database Setup
SQLite database is created automatically on first launch. It contains:
- `resumes` table for job seeker resumes
- `vacancies` table for employer vacancies
- Test data for demonstration

## 🛠️ Technologies

- **Python 3.11+** - main programming language
- **aiogram 3.22.0** - framework for Telegram bots
- **SQLite** - built-in database
- **magic-filter** - for message filtering
- **aiofiles** - asynchronous file operations
- **aiohttp** - HTTP client
- **pydantic** - data validation

## 📊 Development Opportunities

- [ ] **Matching** - automatic job/candidate matching
- [ ] **Filters** - search by technologies, experience, salary
- [ ] **Notifications** - alerts about new vacancies/resumes
- [ ] **Admin Panel** - web interface for bot management
- [ ] **Statistics** - usage analytics
- [ ] **Multilingual** - support for multiple languages
- [ ] **Integrations** - connection with HH.ru, LinkedIn and other platforms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push changes (`git push origin feature/new-feature`)
5. Create Pull Request

## 📄 License

This project is distributed under the **DevConnect License** with restrictions.

### ✅ **ALLOWED FOR FREE:**
- Downloading and personal use
- Studying code for educational purposes
- Demonstrating in portfolio (with author attribution)
- Distributing original version

### ❌ **PROHIBITED WITHOUT AUTHOR CONSENT:**
- Commercial use
- Code modification
- Creating derivative products
- Attribution theft

**Details in `LICENSE` file.**

## 📞 Contacts

- **Telegram:** [@worksoto](https://t.me/worksoto)
- **Email:** vlskrauch@mail.ru

---

**DevConnect** - your reliable assistant in the world of IT career! 🚀

# Contributing to Japanese Foods IR System

Thank you for your interest in contributing to the Japanese Foods Information Retrieval System!

## Development Workflow

1. **Fork & Clone**
   ```bash
   git clone https://github.com/dechatorn-L/Japan_FoodsIR.git
   cd Japan_FoodsIR
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux / macOS:
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Local Server**
   ```bash
   python server.py --port 8000
   ```
   Open `http://localhost:8000` in your browser.

5. **Code Style & Guidelines**
   - Clean, readable Python with standard library first.
   - Minimalist, accessible web styling without unnecessary heavy frameworks.
   - Keep dataset files clean under `data/processed/`.

6. **Submit a Pull Request**
   - Create a feature branch (`git checkout -b feature/my-feature`).
   - Commit your changes with clear commit messages.
   - Push and open a Pull Request.

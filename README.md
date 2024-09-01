# DarkForest HCVS Demo

This repository contains a demonstration of the DarkForest Human Content Verification System (HCVS). The demo consists of three main components:

1. DarkForest API
2. TruthBlog (User Interface)
3. DarkFoest Dashboard (Admin Interface)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/muzz-yasir/darkforest-hcvs-demo.git
   cd darkforest-hcvs-demo
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install fastapi uvicorn streamlit nltk plotly pandas requests
   ```

## Running the Demo

### 1. DarkForest API

1. Navigate to the API directory:
   ```
   cd hcvs_api
   ```

2. Run the API:
   ```
   uvicorn hcvs_api:app --reload
   ```

The API will be available at `http://localhost:8000`.

### 2. TruthBlog (User Interface)

1. Open a new terminal window and navigate to the TruthBlog directory:
   ```
   cd truthblog
   ```

2. Run the TruthBlog Streamlit app:
   ```
   streamlit run truthblog.py
   ```

TruthBlog will be accessible at `http://localhost:8501`.

### 3. DarkForest Dashboard (Admin Interface)

1. Open another terminal window and navigate to the HCVS Dashboard directory:
   ```
   cd hcvs_dashboard
   ```

2. Run the HCVS Dashboard Streamlit app:
   ```
   streamlit run hcvs_dashboard.py
   ```

The HCVS Dashboard will be available at `http://localhost:8502`.

## Usage

1. Start by creating some posts on the TruthBlog interface.
2. Observe how the HCVS API verifies the content.
3. Use the HCVS Dashboard to explore the verification results and blockchain data.

## Troubleshooting

If you encounter any issues with NLTK data, you can manually download the required datasets:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Note

This is a demonstration project and should not be used in production without further development and security considerations.



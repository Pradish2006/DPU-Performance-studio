# Dependency Resolution - Python 3.14 Compatibility

## Changes Made

### 1. Updated requirements.txt
**Before:** Fixed versions that may not be compatible with Python 3.14
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
numpy==1.26.2
torch==2.1.0
torchaudio==2.1.0
scipy==1.11.4
psutil==5.9.6
python-multipart==0.0.6
aiofiles==23.2.1
pyyaml==6.0.1
jinja2==3.1.2
```

**After:** Flexible version ranges for Python 3.12-3.14 compatibility
```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
numpy>=1.26.0
scipy>=1.11.0
psutil>=5.9.0
python-multipart>=0.0.6
aiofiles>=23.0.0
pyyaml>=6.0.0
jinja2>=3.1.0
```

**Changes:**
- Removed PyTorch and TorchAudio (not needed for simulation/demo)
- Changed all fixed versions (`==`) to minimum versions (`>=`)
- This allows pip to install the latest compatible versions for Python 3.14

### 2. Updated Dockerfile
**Before:** `FROM python:3.12-slim`
**After:** `FROM python:3.13-slim`

**Reason:** Python 3.13 is the latest stable version and has better compatibility with current package versions.

### 3. Removed requirements-docker.txt
- Deleted the separate Docker requirements file
- Docker now uses the same requirements.txt as local development
- Simplifies maintenance and reduces confusion

### 4. Updated Documentation
- Updated SETUP.md with flexible installation instructions
- Updated README.md prerequisites to mention Python 3.12+
- Updated DOCKER_DOCUMENTATION.md to reflect Python 3.13 base image

## Why These Changes?

### Python 3.14 Compatibility
Python 3.14 is very new (released late 2024), and some older package versions don't have pre-built wheels for it. By using `>=` instead of `==`, pip can:
1. Install the latest version that supports Python 3.14
2. Avoid compilation errors from missing C compilers
3. Get better performance and security updates

### Removed PyTorch
- PyTorch is heavy (~2GB download)
- Requires complex installation on Windows
- Not needed for the simulation/demo functionality
- The platform simulates DPU performance without running actual AI models
- Can be added later if real model execution is needed

### Flexible Versions
- `>=` allows pip to pick the best version for your Python version
- Avoids version conflicts
- Gets security updates automatically
- Still ensures minimum functionality requirements

## Installation Instructions

### Local Development (Python 3.14)
```bash
cd backend
pip install -r requirements.txt
python main.py
```

If you encounter any issues with specific packages:
```bash
pip install fastapi uvicorn[standard] pydantic numpy scipy psutil python-multipart aiofiles pyyaml jinja2
```

### Docker
```bash
docker-compose up --build
```

The Dockerfile now uses Python 3.13-slim which has excellent package compatibility.

## Testing Your Installation

After installing dependencies, verify:
```bash
# Check FastAPI
python -c "import fastapi; print(fastapi.__version__)"

# Check Uvicorn
uvicorn --version

# Check other packages
python -c "import numpy, scipy, psutil; print('All packages OK')"
```

## Troubleshooting

### NumPy Installation Issues on Windows
If you still have issues with NumPy on Windows:

```bash
# Install from wheel (pre-compiled)
pip install numpy --prefer-binary

# Or use conda instead
conda install numpy scipy
```

### Package Version Conflicts
If you get version conflicts:
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt --upgrade
```

### Virtual Environment (Recommended)
Always use a virtual environment to avoid system-wide conflicts:

```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install
pip install -r requirements.txt
```

## Current Compatibility

- **Python:** 3.12, 3.13, 3.14
- **FastAPI:** >=0.104.0
- **Uvicorn:** >=0.24.0
- **Pydantic:** >=2.5.0
- **NumPy:** >=1.26.0
- **SciPy:** >=1.11.0
- **psutil:** >=5.9.0

All packages now support Python 3.14 with flexible version ranges.

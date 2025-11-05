#!/bin/bash
# Setup script for NLM Web Applications

set -e

echo "🚀 NLM Web Applications Setup"
echo "=============================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python version
echo -e "${BLUE}Checking Python version...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.11"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo -e "${RED}❌ Python 3.11+ is required (found $PYTHON_VERSION)${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python $PYTHON_VERSION${NC}"

# Check if nlm is installed
echo -e "${BLUE}Checking nlm CLI...${NC}"
if ! command -v nlm &> /dev/null; then
    echo -e "${YELLOW}⚠️  nlm CLI not found${NC}"
    echo "Install with: go install github.com/tmc/nlm/cmd/nlm@latest"
    echo "Then run: nlm auth"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✅ nlm CLI found${NC}"
fi

# Check nlm credentials
echo -e "${BLUE}Checking nlm credentials...${NC}"
if [ -f "$HOME/.nlm/env" ]; then
    echo -e "${GREEN}✅ Credentials found${NC}"
else
    echo -e "${YELLOW}⚠️  No credentials found${NC}"
    echo "Run: nlm auth"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "Which implementation do you want to setup?"
echo "1) FastAPI + HTMX (Python + HTML, best for public sites)"
echo "2) NiceGUI (100% Python, best for internal tools)"
echo "3) Both"
echo ""
read -p "Enter choice (1-3): " choice

setup_fastapi() {
    echo ""
    echo -e "${BLUE}Setting up FastAPI + HTMX...${NC}"
    
    cd nlm-web-fastapi
    
    # Create virtual environment
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements-dev.txt
    
    # Setup .env
    if [ ! -f .env ]; then
        echo "Creating .env file..."
        cp .env.example .env
        
        # Try to populate from ~/.nlm/env
        if [ -f "$HOME/.nlm/env" ]; then
            echo "Populating credentials from ~/.nlm/env..."
            source "$HOME/.nlm/env"
            sed -i.bak "s|NLM_AUTH_TOKEN=|NLM_AUTH_TOKEN=$NLM_AUTH_TOKEN|" .env
            sed -i.bak "s|NLM_COOKIES=|NLM_COOKIES=$NLM_COOKIES|" .env
            rm .env.bak
        fi
    fi
    
    # Run tests
    echo "Running tests..."
    pytest
    
    echo ""
    echo -e "${GREEN}✅ FastAPI + HTMX setup complete!${NC}"
    echo ""
    echo "To start the server:"
    echo "  cd nlm-web-fastapi"
    echo "  source venv/bin/activate"
    echo "  python -m app.main"
    echo ""
    echo "Then visit: http://localhost:8000"
    echo ""
    
    cd ..
}

setup_nicegui() {
    echo ""
    echo -e "${BLUE}Setting up NiceGUI...${NC}"
    
    cd nlm-web-nicegui
    
    # Create virtual environment
    echo "Creating virtual environment..."
    python3 -m venv venv
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install dependencies
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements-dev.txt
    
    # Setup .env
    if [ ! -f .env ]; then
        echo "Creating .env file..."
        cp .env.example .env
        
        # Try to populate from ~/.nlm/env
        if [ -f "$HOME/.nlm/env" ]; then
            echo "Populating credentials from ~/.nlm/env..."
            source "$HOME/.nlm/env"
            sed -i.bak "s|NLM_AUTH_TOKEN=|NLM_AUTH_TOKEN=$NLM_AUTH_TOKEN|" .env
            sed -i.bak "s|NLM_COOKIES=|NLM_COOKIES=$NLM_COOKIES|" .env
            rm .env.bak
        fi
    fi
    
    # Run tests
    echo "Running tests..."
    pytest
    
    echo ""
    echo -e "${GREEN}✅ NiceGUI setup complete!${NC}"
    echo ""
    echo "To start the server:"
    echo "  cd nlm-web-nicegui"
    echo "  source venv/bin/activate"
    echo "  python -m app.main"
    echo ""
    echo "Then visit: http://localhost:8080"
    echo ""
    
    cd ..
}

case $choice in
    1)
        setup_fastapi
        ;;
    2)
        setup_nicegui
        ;;
    3)
        setup_fastapi
        setup_nicegui
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Review the .env file and ensure credentials are correct"
echo "2. Start the development server"
echo "3. Open the URL in your browser"
echo ""
echo "Documentation:"
echo "  - WEB_APPS_README.md - Overview and quick start"
echo "  - WEB_APPS_COMPARISON.md - Detailed comparison"
echo "  - WEBAPP_SPECS.md - Full specifications"
echo "  - nlm-web-fastapi/README.md - FastAPI documentation"
echo "  - nlm-web-nicegui/README.md - NiceGUI documentation"
echo ""

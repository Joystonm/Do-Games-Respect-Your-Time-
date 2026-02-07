#!/bin/bash

echo "🎮 Do Games Respect Your Time?"
echo "================================"
echo ""
echo "Launching Streamlit editorial experience..."
echo ""

streamlit run app.py --server.port 8501 --server.headless true

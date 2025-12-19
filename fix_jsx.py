"""
Quick fix for CropRecommendation.jsx - Remove escaped backslash character
"""

# Read file
file_path = r"c:\Users\hi\KisanMitra-AI\src\pages\CropRecommendation.jsx"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix escaped character
content = content.replace('\\u003cdiv className="rec-tip"', '<div className="rec-tip"')

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fixed JSX syntax error")



def clean_text(text):
    if not text:
        return ""
    return " ".join(text.replace("\n", " ").split())
    
    

    

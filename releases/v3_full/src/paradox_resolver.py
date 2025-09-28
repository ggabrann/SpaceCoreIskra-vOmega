
def resolve(text:str)->dict:
    c1="быстро и медленно" in text
    c2="без давления и обязательно" in text
    classes=[k for k,v in {"speed":c1,"pressure":c2}.items() if v]
    return {"paradox": bool(classes), "classes": classes}

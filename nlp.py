import en_core_web_sm

nlp = en_core_web_sm.load()

doc = nlp("My name is john and")
XA = [(X.text, X.label_) for X in doc.ents]

(name, type) = XA[0]
print(name)

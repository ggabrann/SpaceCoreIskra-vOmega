PRESETS={"коротко":{"temp":0.5},"подробно":{"temp":0.9}}
def route(name): return PRESETS.get(name,{})

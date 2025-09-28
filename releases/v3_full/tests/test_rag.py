
from src.rag_panel import rosette_index, rosette_search
def test_rag():
    idx = rosette_index({"a":["дыхание ритм"],"b":["волна связка"]})
    res = rosette_search(idx, "ритм дыхание", top_k=3)
    assert res and res[0][0].startswith("a:")

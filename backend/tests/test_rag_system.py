from backend.app.rag_system import rag_system

def test_generate_response():
    response = rag_system.generate_response("What are the dietary preferences?")
    assert "dietary" in response.lower()

from vector_database import VectorDatabase

class ToolShed:
    def __init__(self, client, tools):
        self.client = client
        self.tools = tools
        self.vector_db = self.create_tool_embeddings()

    def create_tool_embeddings(self):
        tool_descriptions = [tool.__doc__ for tool in self.tools]
        embeddings_response = self.client.embeddings.create(
            input=tool_descriptions,
            model="text-embedding-3-small"
        )
        db = VectorDatabase()
        for i, tool in enumerate(self.tools):
            db.add_entity(embeddings_response.data[i].embedding, tool)
        return db
    
    def add_tool(self, tool):
        tool_descriptions = [tool.__doc__]
        embeddings_response = self.client.embeddings.create(
            input=tool_descriptions,
            model="text-embedding-3-small"
        )
        self.vector_db.add_entity(embeddings_response.data[0].embedding, tool)


    def retrieve_relevant_tools(self, question, top_k=5):
        question_embedding_response = self.client.embeddings.create(
            input=[question],
            model="text-embedding-3-small"
        )
        question_embedding = question_embedding_response.data[0].embedding
        relevant_tools = self.vector_db.search(question_embedding, top_k=top_k)
        return relevant_tools

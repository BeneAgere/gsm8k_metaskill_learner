import numpy as np

class VectorDatabase:
    def __init__(self):
        self.vectors = []
        self.values = []

    def add_entity(self, vector, value):
        """
        Add a Python list or NumPy array as a vector to the database,
        along with its corresponding tool.
        """
        self.vectors.append(np.array(vector))
        self.values.append(value)

    def search(self, query_vector, top_k=5):
        """
        Search the database for the most similar vectors based on the dot product.

        Parameters:
            query_vector (list or np.ndarray): The query vector.

        Returns:
            The top_k most similar tools from the database.
            If the database is empty, returns an empty list.
        """
        query_vector = np.array(query_vector)
        similarities = [(tool, np.dot(query_vector, vector)) for tool, vector in zip(self.values, self.vectors)]
        similarities.sort(key=lambda x: x[1], reverse=True)
        return [tool for tool, _ in similarities[:top_k]]

def main():
    # Example usage:
    db = VectorDatabase()
    db.add_vector([1, 2, 3])
    db.add_vector([2, 3, 4])
    db.add_vector([3, 4, 5])

    query = [1, 1, 1]
    result = db.search(query)
    print("Most similar vector to", query, "is", result)

if __name__ == "__main__":
    main()

class Books:

    def __init__(self):

        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        import pandas as pd 

        tf=TfidfVectorizer()
        
        self.df=pd.read_csv("bookdata.csv")
        tf_matrix=tf.fit_transform(self.df["text"])
        self.tf_cosine_sim=cosine_similarity(tf_matrix)


    def get_title_from_index(self,id):
        """
        Returns the title of the bOOK given the index
        """
        return self.df[self.df["Id"]==id]["Book_Title"].values[0]

    def get_index_from_title(self,title):
        """
        Returns the index of the Book given the title
        """
        return self.df[self.df.Book_Title == title].Id.values[0]

    def get_recommendations(self,book_id, sim_matrix):
        """
        -Store the recommendations in a list
        -Get the title of book using get_title_from_index
        -Genarate cosine similarity matrix for the book and enumerate it
        -Sort the list based on the similarity
        -Get the index of the book (due to enumeration) 
        and get corresponding title
        -Retrun the list of recs
        """
        recommendations = list()
        
        podcast_title = self.get_title_from_index(book_id)
        similar_books =  list(enumerate(sim_matrix[book_id]))
        sorted_similar_books = sorted(similar_books,key=lambda x:x[1],reverse=True)
        
        for i in range(11):
            title = self.get_title_from_index(sorted_similar_books[i][0])
            recommendations.append(title)
        
        return recommendations[1:]

    def get_dissimilar_recommendations(self,book_id, sim_matrix):
        """
        -Store the recommendations in a list
        -Get the title of book using get_title_from_index
        -Genarate cosine similarity matrix for the book and enumerate it
        -Sort the list based on the similarity
        -Get the index of the book (due to enumeration) 
        and get corresponding title
        -Retrun the list of recs
        """
        recommendations = list()
        
        podcast_title = self.get_title_from_index(book_id)
        similar_books =  list(enumerate(sim_matrix[book_id]))
        sorted_similar_books = sorted(similar_books,key=lambda x:x[1])
        
        for i in range(11):
            title = self.get_title_from_index(sorted_similar_books[i][0])
            recommendations.append(title)
        
        return recommendations[1:]
    
#b=Books()
#print(b.get_recommendations(b.get_index_from_title("Divergent"),b.tf_cosine_sim))
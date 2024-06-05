import helpers
import pandas as pd

def load_movie_data():
    dynamo_resource = helpers.start_dynamo_session()
    tables = []
    
    for table in dynamo_resource.tables.all():
        print(table.name)
        tables.append(table)
    movies = dynamo_resource.Table('doc-example-table-movies')
    return movies
    
    
def query_movies_from_year(movies, year):
    result = movies.get_item(Key={'year': year, 'title': '2 Guns'})
    return result
    


def need_answer(): 
    print(helpers.get_answer())
    
def main():
    movies = load_movie_data()
    helpers.save_data(movies, "raw_data.csv")
    lastMayaYear = query_movies_from_year(movies, 2012)
    helpers.save_query_data(input=lastMayaYear, filename="movies2013.csv")


if __name__ == "__main__":
    main()
import streamlit as st
import pandas as pd
import random

# Cargar datos
file_path = "df_web.csv"  # Ruta correcta del archivo
df = pd.read_csv(file_path)

# Obtener promedio de ratings para usarlo como umbral
avg_rating = df['rating'].mean()

# Calcular la frecuencia de cada género y ordenarlos
genres_0_counts = df['genres_0'].value_counts()
genres_0_sorted = genres_0_counts.index.tolist()

# Eliminar 'Other' si está presente y agregarlo al final
if 'Other' in genres_0_sorted:
    genres_0_sorted.remove('Other')
genres_0_sorted.append('Other')

# Insertar '-Choose the genre of your book-' al principio de la lista
genres_0_sorted.insert(0, '-Choose the genre of your book-')

# Título de la aplicación
st.markdown("<h1 style='text-align: center; color: #FFA500;'>You don't know what book to read this summer?</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: #008080;'>Don't worry, we'll help you</h2>", unsafe_allow_html=True)

# Primera pregunta sobre el género
selected_genre_0 = st.selectbox('What would you like to read?', genres_0_sorted)

if selected_genre_0 and selected_genre_0 != '-Choose the genre of your book-':
    # Calcular la frecuencia de cada subgénero dentro del género seleccionado y ordenarlos
    subgenres_counts = df[df['genres_0'] == selected_genre_0]['genre_2'].value_counts()
    subgenres_sorted = subgenres_counts.index.tolist()
    
    # Mostrar subgéneros
    selected_subgenre = st.selectbox('Could you be more specific? Give us a subgenre to make the search more precise', subgenres_sorted)
    
    if selected_subgenre:
        # Pregunta sobre si planea leer en la playa
        on_beach = st.radio('Are you planning to read on the beach?', ('Yes', 'No'), index=None)

        if on_beach:
            if on_beach == 'Yes':
                # Filtrar libros que cumplan con los criterios para leer en la playa
                beach_books = df[(df['genres_0'] == selected_genre_0) & 
                                 (df['genre_2'] == selected_subgenre) & 
                                 (df['bookformat'] == 'Paperback') & 
                                 (df['pages_binned_300'] == '-300') & 
                                 (df['rating'] > avg_rating)]
                
                if not beach_books.empty:
                    def display_book(book):
                        st.markdown("<h3 style='color: #FF4500;'>Then we recommend a book with less than 300 pages and paperback book format</h3>", unsafe_allow_html=True)
                        st.write(f"**{book['title']}**")
                        st.write(f"by {book['author']}")
                        st.write(book['desc'])
                        st.image(book['img'])
                        st.write(f"**{book['totalratings']:.0f} people** have rated **{book['title']}** with a rating of **{book['rating']:.2f}/5**")
                        st.write(f"Which means it is **better** rated than **{book['worse_rating_percentage']*100:.2f}%** of the books")

                    recommended_book = beach_books.sample(n=1)
                    display_book(recommended_book.iloc[0])

                    if st.button('Randomize'):
                        print("")
                else:
                    st.write("**Sorry, no books match your criteria.**")
            else:
                # Pregunta sobre el tamaño del libro si no va a leer en la playa
                book_size = st.radio('So are you ready for a big challenge? Or do you prefer short or medium book?', 
                                     ('Short book', 'Medium book', 'Challenge accepted'), index=None)

                if book_size:
                    if book_size == 'Short book':
                        size_filter = '-300'
                    elif book_size == 'Medium book':
                        size_filter = '300-599'
                    else:
                        size_filter = '+600'
                    
                    # Filtrar libros que cumplan con los criterios seleccionados
                    filtered_books = df[(df['genres_0'] == selected_genre_0) & 
                                        (df['genre_2'] == selected_subgenre) & 
                                        (df['pages_binned_300'] == size_filter) & 
                                        (df['rating'] > avg_rating)]
                    
                    if not filtered_books.empty:
                        def display_book(book):
                            st.markdown("<h3 style='color: #FF4500;'>Then we recommend the following book</h3>", unsafe_allow_html=True)
                            st.write(f"**{book['title']}**")
                            st.write(f"by {book['author']}")
                            st.write(book['desc'])
                            st.image(book['img'])
                            st.write(f"**{book['totalratings']:.0f} people** have rated **{book['title']}** with a rating of **{book['rating']:.2f}/5**")
                            st.write(f"Which means it is **better** rated than **{book['worse_rating_percentage']*100:.2f}%** of the books")

                        recommended_book = filtered_books.sample(n=1)
                        display_book(recommended_book.iloc[0])

                        if st.button('Randomize'):  
                            print("")
                    else:
                        st.write("**Sorry, no books match your criteria.**")

# Aplicar un diseño de página inspirado en la playa
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e");
        background-size: cover;
    }
    .stMarkdown h3 {
        color: #FF4500;
    }
    .stMarkdown h1, .stMarkdown h2 {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

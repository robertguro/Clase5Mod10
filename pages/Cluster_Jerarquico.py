#Importamos las librerias necesarias
import pandas as pd
import numpy as np
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.cluster.hierarchy import dendrogram, linkage, fcluster

#Condifuración de la página
st.set_page_config(page_title='Cluster Jerarquico', page_icon=':bar_chart:', layout='wide', initial_sidebar_state='expanded')
#Página principal
st.title('Bienvenido a la aplicación de análisis de datos')
#Menu de opciones
st.sidebar.title('Menú de opciones')
#Lista de opciones
opciones = ['Cargar Datos', 'Cluster Jerarquico']
#Selección de la opción
opcion = st.sidebar.selectbox('Seleccione una opción', opciones)

@st._cache_data
def cargar_datos(archivo):
    if archivo:
        if archivo.name.endswith('csv'):
            df = pd.read_csv(archivo)
        elif archivo.name.endswith('xlsx'):
            df = pd.read_excel(archivo)
        else:
            raise ValueError('Formato de archivo no soportado')
        return df
    else:
        return None

if opcion == 'Cargar Datos':
    st.subheader('Cargar datos')
    archivo = st.sidebar.file_uploader('Seleccione un archivo', type=['csv', 'xlsx'])
    if archivo:
        df = cargar_datos(archivo)
        st.session_state.df = df
        st.info('Datos cargados correctamente')
    else:
        st.write('No hay datos para mostrar')
elif opcion == 'Cluster Jerarquico':
    st.subheader('Cluster Jerarquico')
    if 'df' not in st.session_state:
        st.warning('No hay datos para mostrar')
    else:
        df = st.session_state.df
        st.write('El archivo contiene {} filas y {} columnas'.format(df.shape[0], df.shape[1]))
        #Agregar lista de columnas
        lista_columnas = df.columns
        columnas = st.sidebar.multiselect('Seleccione las columnas', lista_columnas)

        if columnas:
            X = df[columnas]
            st.write(X.head())

            #Seleccionar el tipo de enlace
            enlace = st.sidebar.selectbox('Seleccione el tipo de enlace', ['ward', 'complete', 'average', 'single'])
            #Calcular la matriz de enlace
            Z = linkage(X, enlace)
            st.write(Z)
            #Graficar el dendrograma
            fig = plt.figure(figsize=(6,6))
            #Agregar la línea de corte del dendrograma
            corte = st.sidebar.slider('Corte', 0, 10, 3)
            dendrogram(Z)
            plt.axhline(y=corte, color='r', linestyle='--')            
            st.pyplot(fig)
            #Crear una lista de criterios
            criterios = ['maxclust', 'distance']
            critetio = st.sidebar.selectbox('Seleccione el criterio', criterios)
            k=st.sidebar.slider('Número de clusters', 2, 10, 2)
            #Asignar clusters
            clusters = fcluster(Z, k, criterion=critetio)
            df['Cluster'] = clusters
            st.write(df.head())
            fig = plt.figure(figsize=(6,6))
            sns.scatterplot(x=X.iloc[:,0], y=X.iloc[:,1], c=clusters, s=250, markers='8', palette='Set1')
            st.pyplot(fig)
        else:
            st.warning('Seleccione al menos una columna')

    


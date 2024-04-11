# chatBot-rag-playground
## Clonar el Repositorio de GitHub
#### 1. Abrir la Terminal o Línea de Comandos
Dependiendo de tu sistema operativo, abre la terminal (Linux o macOS) o la línea de comandos/PowerShell (Windows).

#### 2. Navegar al Directorio
Usa el comando cd para navegar al directorio donde deseas clonar el repositorio. Por ejemplo:
```console
cd path/to/directory
```

#### 3. Clonar el repositorio
Puedes clonar el repositorio via HTTP o SSH:
###### HTTP
```console
git clone https://github.com/jp-rp/chatBot-rag-playground.git
```

###### SSH
```console
git clone git@github.com:jp-rp/chatBot-rag-playground.git
```

## Seleccionar versión

Este repositorio implementa un chatbot con differentes especificaciones. De momento, las versiones están funcionales son:
###### chatBot_gpt3.5t_hfst-MiniLM-L6-v2_t
- LLM: OpenAI's GPT 3.5 Turbo
- Embeddings: HuggingFace all-MiniLM-L6-v2 Sentence Transformers 
- Vector Store: ChromaDB
- Formatos acceptados para Data Ingestion: PDF

###### chatBot_gpt-4-0125-preview_hfst-MiniLM-L6-v2_t
- LLM: OpenAI's GPT 4 Turbo (Preview)
- Embeddings: HuggingFace all-MiniLM-L6-v2 Sentence Transformers 
- Vector Store: ChromaDB
- Formatos acceptados para Data Ingestion: PDF

Cada versión está implementada en differentes branches. Si no estás ya en el directorio del repositorio clonado, muévete a él con:
```console
cd chatBot-rag-playground
```
Para cambiar implementaciones, utiliza el siguiente comando:
```console
git checkout <branch-name>
```
sustituyendo '<branch-name>' por el nombre de la implementación deseada. e.g.
```
git checkout chatBot_gpt3.5t_hfst-MiniLM-L6-v2_t
```

## Instalar librerías
Una vez clonado el repositorio y seleccionada una implementación. El siguiente paso es instalar las librerías necesarias para el proyecto.
###### Recomiendo utilizar diferentes evnironments para cada branch. Así podemos evitar incompatibilidad entre paquetes (si llegasen a surgir) y podemos manetener environments limpios entre proyectos. Para más información sobre como crear, activar y eliminar environments revisa la documentación de [Conda]() o [Pyenv](https://github.com/pyenv/pyenv).

#### 1. Instalar Dependencias
###### Si estás utilizando una distribución de Conda (Anaconda, Miniconda), asegurate de que pip este instalado en tu virtual environment. Puedes instalarlo con:
```console
conda install pip
```

Para instalar las depndencias, utiliza el siguiente comando:
```console
pip install -r requirements.txt
```

#### 2 .env 
Por seguridad y practicidad, el proyecto utiliza environment variables para almacenar strings de manera globalm, entre ellos, tu OpenAI API key. Para activar estas environment variables, crea un archivo .env con:
```console
touch .env
```
y abre el archivo en cualquier text editor y añade la siguiente línea:
```python
OPENAI_API_KEY ='{tu API key}'
```

## 4. Vectorización
Para añadir información al Knowledge Base, crea un directorio con:
```console
mkdir data
```
y añade los documentos a este folder. Para vectorizar la información, corre el programa con directamente desde tu IDE o con:
```console
python3 vector_db.py
```
o 
```console
python vector_db.py
```
Se tardará un poco en vectorizar la información dependiendo de la cantidad de información a vectorizar y la capacidad de tu hardware.

### 4. Chat
Finalmente, puede iniciar el chat de manera local con:
```console
chainlit run chat.py -w
```
Automaticamente tu browser debería abrir una ventana interactiva para Q&A. Una vez que termine la inicialización, el chat mostrará un prompt para hacerle una pregunta. 
La sesión se mantendrá activa en localhost:8080.

Para terminar la sesión, abre la terminal en donde está corriendo el programa y presiona *ctrl + c* en Windows/Linux o *cmd + c* en MacOS.

### Notas adicionales
- Prompts
  Puedes editar el prompt utilizado para retrieval en chat.py. Por default, 
- RetrievalQA Chain
  Por default, el chat muestra las fuentes utilizadas para generar la respuesta. Esta opción se puede desactivar eliminando 'return_soruce_documents=True' en qa_chain:
```python
def retrieval_qa_chain(llm, prompt, vector_db):
  qa_chain = RetrievalQA.from_chain_type(
    ...
    return_source_documents=True,
    ...
``` 
  




import os
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate 
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

from dotenv import load_dotenv

load_dotenv()



#API keys loading
hf_api_key = os.getenv('HF_TOKEN')

mistral_api_key = os.getenv('MISTRAL_API_KEY')



#embeddings
embeddings =HuggingFaceEmbeddings(model_name='sentence-transformers/multi-qa-MiniLM-L6-cos-v1')


#bdv
db = FAISS.load_local(
    "faiss_bible_bdv", embeddings, allow_dangerous_deserialization=True)


# Connect query to FAISS index using a retriever
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={'k':1},
)



# Define LLM

model = ChatMistralAI(
    model_name="mistral-large-latest",
    temperature=0.0,
    mistral_api_key=mistral_api_key
)


template ="""Tu es Thomas, un bot expert en théologie et en histoire de la Bible. Ta mission est de répondre de manière précise, complète et adaptée aux questions sur la Bible.
Réponds en Français

 **Gestion des sources** : Utilise à la fois les informations fournies dans le document et tes connaissances approfondies en théologie pour formuler une réponse pertinente et bien étayée. Si le document et tes connaissances ne suffisent pas, demande des précisions.

 **Adaptation du ton** : Adopte un ton jovial et sympathique si la situation le permet, mais reste respectueux et solennel pour les sujets sensibles ou graves. Assure-toi que ta réponse est adaptée au niveau de compréhension de l'utilisateur (débutant, intermédiaire, expert).

 **Gestion des erreurs et des questions hors sujet** : 
   - Si la question n’est pas claire ou semble incomplète, demande des clarifications avant de répondre.
   - Si la question est hors du domaine de la Bible, réponds par:  "Je ne maîtrise par ce sujet".
   - Si la question n'a aucun rapport avec le contexte et est une question simple comme (bonjour, comment ça va, etc), réponds de manière joviale et sympathique sans faire référence à la Bible.

   ** Cite des passages bibliques s'il le faut

**Contexte** : {context}

**Voici la question** : {input}

**Réponse** :
"""


prompt = PromptTemplate(
    template=template,
    input_variables=['input', 'context'] 
)



#Chain LLM, prompt and retriever
combine_docs_chain = create_stuff_documents_chain(model, prompt)
retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)




#Let's write a function to retrieve with llm

def ask(question: str):
  response = retrieval_chain.invoke({"input": question})
  if response:
    return response['answer']
  else:
    return "Veuillez poser une autre question."



 

#print(ask("QUe dit la Bible de la polygamie"))

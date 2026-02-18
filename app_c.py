import chainlit as cl
import time
from main import ask
import asyncio
# from main import ask

@cl.on_message
async def main(message: cl.Message):
    loading_element = cl.Image(path="public/loading.gif", name="image1", display="inline", size="small")
    load = cl.Message(content="Thomas réfléchit...", elements=[loading_element])
    await load.send()
    
    await asyncio.sleep(3)
    response = ask(message.content)
    # response = "HELLOOOO"
    
    await load.remove()
    
    # Envoyer la réponse à l'utilisateur
    await cl.Message(
        content=response,
        author="Thomas"
    ).send()

# Pour exécuter: chainlit run app.py
#asyncio.queue()
import asyncio
import random

async def productor(queue, n):
    for i in range(n):
        value = random.randint(1, 100)
        print(f"Productor puso: {value}")
        await queue.put(value)
        await asyncio.sleep(random.uniform(0.1, 0.5)) # Simula algo de trabajo

async def consumidor(queue, id):
    while True:
        item = await queue.get()
        print(f"Consumidor {id} obtuvo: {item}, procesando...")
        await asyncio.sleep(random.uniform(0.2, 0.7)) # Simula procesamiento
        queue.task_done() # Indica que la tarea se completó

async def main():
    cola = asyncio.Queue(maxsize=5) # Cola con capacidad máxima de 5
    num_productores = 2
    num_consumidores = 3
    num_items = 10

    productores = [asyncio.create_task(productor(cola, num_items // num_productores)) for _ in range(num_productores)]
    consumidores = [asyncio.create_task(consumidor(cola, i + 1)) for i in range(num_consumidores)]

    await asyncio.gather(*productores)
    await cola.join() # Espera hasta que todos los elementos de la cola hayan sido procesados

    # Cancelar los consumidores (ya que el productor terminó)
    for consumidor_task in consumidores:
        consumidor_task.cancel()
    await asyncio.gather(*consumidores, return_exceptions=True)

if __name__ == "__main__":
    asyncio.run(main())

import React, { useState } from "react";
import Textarea from "../../components/textarea/Textarea";
import Navbar from "../../components/navbar/Navbar";
import "../app.css";

/**
 * Represents the ReadersWriters component.
 * This component simulates the Readers-Writers problem in concurrency.
 * It allows multiple readers and writers to access a shared resource,
 * ensuring that only one writer can modify the resource at a time and
 * allowing multiple readers to access the resource simultaneously.
 */
export default function ProducerConsumer() {
  const [readers, setReaders] = useState(3);
  const [writers, setWriters] = useState(2);
  const [maxReadTime, setMaxReadTime] = useState(3);
  const [maxWriteTime, setmaxWriteTime] = useState(3);
  const [output, setOutput] = useState("");
  const [textareaContent, setTextareaContent] = useState("");
  const [intervalId, setIntervalId] = useState(null);

  const clearTextArea = () => {
    setTextareaContent("");
  };

  const startSimulation = () => {
    fetch("/readers_writers/start/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ readers, writers, maxReadTime, maxWriteTime }),
    })
      .then((response) => response.json())
      .then((data) => {
        setTextareaContent("") // Limpiar el contenido del textarea al iniciar la simulación
        setOutput(data.status);
        // Iniciar el intervalo para obtener el log cada 3 segundos
        const id = setInterval(getEventLog, 3000);
        setIntervalId(id); // Guardar el ID del intervalo en el estado
      })
      .catch((error) => setOutput(error.message));
  };

  const stopSimulation = () => {
    clearInterval(intervalId); // Limpiar el intervalo al detener la simulación
    setIntervalId(null); // Limpiar el estado del ID del intervalo
    fetch("/readers_writers/stop/")
      .then((response) => response.json())
      .then((data) => setOutput(data.status))
      .catch((error) => setOutput(error.message));
  };

  const getEventLog = () => {
    fetch("/readers_writers/log/")
      .then((response) => response.json())
      .then((data) => {
        processOutput(data);
      })
      .catch((error) => setOutput(error.message));
  };

  const processOutput = async (data) => {
    for (const message of data) {
      const formattedMessage = `${message.reader ? "Lector" : "Escritor"} ${
        message.id
      } ${message.reader ? "leyó" : "escribió"} durante ${message.time} s`;

      await new Promise((resolve) => setTimeout(resolve, message.time * 1000));

      setTextareaContent(
        (prevContent) => `${prevContent}\n${formattedMessage}`
      );
    }
  };

  return (
    <div className="main">
      <Navbar readersWriters={false}></Navbar>
      <div className="container">
        <div className="container-left">
          <h2>Lectores - Escritores</h2>
          <p>
            El problema de los lectores-escritores es ejemplo de un problema
            informático común en concurrencia. Existen al menos tres variaciones
            de los problemas, que tratan situaciones en las que muchos hilos de
            ejecución concurrentes intentan acceder al mismo recurso compartido
            a la vez. Algunos hilos pueden leer y otros escribir, con la
            restricción de que ningún hilo puede acceder al recurso compartido
            para leer o escribir mientras otro hilo está escribiendo en él. En
            particular, queremos evitar que más de un hilo modifique el recurso
            compartido simultáneamente y permitir que dos o más lectores accedan
            al recurso compartido al mismo tiempo.
          </p>
          <div className="entry-values">
            <label htmlFor="">Cantidad de lectores</label>
            <input
              type="number"
              id="readers"
              value={readers}
              min={1}
              onChange={(e) => setReaders(parseInt(e.target.value))}
            />
            <label htmlFor="">Cantidad de escritores</label>
            <input
              type="number"
              id="writers"
              value={writers}
              min={1}
              onChange={(e) => setWriters(parseInt(e.target.value))}
            />
            <label htmlFor="">Tiempo máximo de escritura</label>
            <input
              type="number"
              id="maxReadTime"
              value={maxReadTime}
              min={1}
              onChange={(e) => setMaxReadTime(parseInt(e.target.value))}
            />
            <label htmlFor="">Tiempo máximo de lectura</label>
            <input
              type="number"
              id="maxWriteTime"
              value={maxWriteTime}
              min={1}
              onChange={(e) => setmaxWriteTime(parseInt(e.target.value))}
            />
          </div>
          <button onClick={startSimulation}>Iniciar</button>
          <button onClick={stopSimulation}>Detener</button>
          <button onClick={clearTextArea}>Limpiar</button>
        </div>
        <div className="container-right">
          <Textarea content={textareaContent}></Textarea>
        </div>
      </div>
      <h2 className="output">{output}</h2>
    </div>
  );
}

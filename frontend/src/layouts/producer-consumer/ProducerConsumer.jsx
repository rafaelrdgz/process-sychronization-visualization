import { useState, useEffect } from "react";
import Textarea from "../../components/textarea/Textarea";
import Navbar from "../../components/navbar/Navbar";
import "../app.css";
import { Link } from "react-router-dom";
// import ReloadPage from "../../components/ReloadPage";


/**
 * Represents the ProducerConsumer component.
 * 
 * @returns {JSX.Element} The ProducerConsumer component.
 */
export default function ProducerConsumer() {
  const [producers, setProducers] = useState(2);
  const [consumers, setConsumers] = useState(2);
  const [output, setOutput] = useState("");
  const [textareaContent, setTextareaContent] = useState("");
  const [intervalId, setIntervalId] = useState(null); // State para almacenar el ID del intervalo

  const clearTextArea = () => {
    setTextareaContent("");
  };

  const startSimulation = () => {
    fetch("/prodcon/start/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ producers, consumers }),
    })
      .then((response) => response.json())
      .then((data) => {
        setTextareaContent(""); // Limpiar el contenido del textarea al iniciar la simulación
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
    fetch("/prodcon/stop/")
      .then((response) => response.json())
      .then((data) => setOutput(data.status))
      .catch((error) => setOutput(error.message));
  };

  const getEventLog = () => {
    fetch("/prodcon/log/")
      .then((response) => response.json())
      .then((data) => {
        processOutput(data);
      })
      .catch((error) => setOutput(error.message));
  };

  const processOutput = async (data) => {
    for (const message of data) {
      const formattedMessage = `${
        message.producer ? "Productor" : "Consumidor"
      } ${message.id} ${message.producer ? "creó" : "consumió"} el item ${
        message.item
      } en ${message.time} s`;

      await new Promise((resolve) => setTimeout(resolve, message.time * 1000));

      setTextareaContent(
        (prevContent) => `${prevContent}\n${formattedMessage}`
      );
    }
  };

  // Limpia el intervalo cuando el componente se desmonta o cuando se detiene la simulación
  useEffect(() => {
    return () => {
      clearInterval(intervalId);
    };
  }, [intervalId]);

  return (
    <div className="main">
      <Navbar producerConsumer={false}></Navbar>
      <Link to={"/prodcon/animated_version/"}>
        <button className="linkButton">Animated version</button>
      </Link>
      <div className="container">
        <div className="container-left">
          <h2>Productor - Consumidor</h2>
          <p>
            El problema del productor-consumidor es un ejemplo clásico de
            problema de sincronización de multiprocesos. El problema describe
            dos procesos, productor y consumidor, ambos comparten un búfer de
            tamaño finito. La tarea del productor es generar un producto,
            almacenarlo y comenzar nuevamente; mientras que el consumidor toma
            (simultáneamente) productos uno a uno. El problema consiste en que
            el productor no añada más productos que la capacidad del buffer y
            que el consumidor no intente tomar un producto si el buffer está
            vacío.
          </p>
          <div className="entry-values">
            <label htmlFor="producers">Cantidad de productores</label>
            <input
              type="number"
              id="producers"
              value={producers}
              min={1}
              onChange={(e) => setProducers(parseInt(e.target.value))}
            />
            <label htmlFor="consumers">Cantidad de consumidores</label>
            <input
              type="number"
              id="consumers"
              value={consumers}
              min={1}
              onChange={(e) => setConsumers(parseInt(e.target.value))}
            />
          </div>
          <button onClick={startSimulation}>Iniciar</button>
          <button onClick={stopSimulation}>Detener</button>
          <button onClick={clearTextArea}>Limpiar</button>
          <h2>{output}</h2>
        </div>
        <div className="container-right">
          <Textarea content={textareaContent}></Textarea>
        </div>
      </div>
    </div>
  );
}

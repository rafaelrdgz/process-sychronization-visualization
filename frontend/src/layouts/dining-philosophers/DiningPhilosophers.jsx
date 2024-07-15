import React, { useEffect, useState } from "react";
import Navbar from "../../components/navbar/Navbar";
import Textarea from "../../components/textarea/Textarea";
import "../app.css";
import { Link } from "react-router-dom";

/**
 * Component for the Dining Philosophers simulation.
 * @returns {JSX.Element} The DiningPhilosophers component.
 */
export default function DiningPhilosophers() {
  const [philosophers, setPhilosophers] = useState(5);
  const [actionTime, setActionTime] = useState(5);
  const [output, setOutput] = useState("");
  const [textareaContent, setTextareaContent] = useState("");
  const [intervalId, setIntervalId] = useState(null); // State para almacenar el ID del intervalo

  const clearTextArea = () => {
    setTextareaContent("");
  };

  const startSimulation = () => {
    fetch("/philosophers/start/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ philosophers, actionTime }),
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
    fetch("/philosophers/stop/")
      .then((response) => response.json())
      .then((data) => setOutput(data.status))
      .catch((error) => setOutput(error.message));
  };

  const getEventLog = () => {
    fetch("/philosophers/log/")
      .then((response) => response.json())
      .then((data) => {
        processOutput(data);
      })
      .catch((error) => setOutput(error.message));
  };

  const processOutput = async (data) => {
    for (const message of data) {
      const formattedMessage = `Filósofo ${message.id} está ${message.action} y demora ${message.time} s`;

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
      <Navbar philosophersDiners={false}></Navbar>
      <Link to={"/philosophers/animated_version/"}>
        <button className="linkButton">Animated version</button>
      </Link>
      <div className="container">
        <div className="container-left">
          <h2>Filósofos comensales</h2>
          <p>
            El problema de la cena de los filósofos o problema de los filósofos
            cenando (dining philosophers problem) es un problema clásico de las
            ciencias de la computación propuesto por Edsger Dijkstra en 1965
            para representar el problema de la sincronización de procesos en un
            sistema operativo. Cabe aclarar que la interpretación está basada en
            pensadores chinos, quienes comían con dos palillos, donde es más
            lógico que se necesite el del comensal que se siente al lado para
            poder comer. El problema de los 5 filósofos presenta una situación
            hipotética donde cinco filósofos se sientan alrededor de una mesa
            redonda, cada uno con un plato de pasta y un tenedor entre cada par
            de filósofos adyacentes. La dificultad radica en permitir que cada
            filósofo alterne entre dos estados, pensamiento y comer, sin que se
            produzcan bloqueos mutuos mientras intentan adquirir los tenedores
            adyacentes necesarios para comer.
          </p>
          <div className="entry-values">
            <label htmlFor="">Cantidad de filósofos</label>
            <input
              type="number"
              value={philosophers}
              min={5}
              onChange={(e) => setPhilosophers(parseInt(e.target.value))}
            />
            <label htmlFor="">Tiempo maximo en proceso</label>
            <input
              type="number"
              value={actionTime}
              min={1}
              onChange={(e) => setActionTime(parseInt(e.target.value))}
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

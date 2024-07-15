import React from "react";
import "./Home.css";
import { Link } from "react-router-dom";

/**
 * Renders the Home component.
 * 
 * @returns {JSX.Element} The rendered Home component.
 */
export default function Home() {
  return (
    <div className="home">
      <h1 className="tittle">
        Visualización de Problemas de Sincronización de Procesos
      </h1>
      <p className="description">
        Explora la sincronización de procesos con este programa que te muestra
        gráficamente cómo funcionan los problemas clásicos.
      </p>
      <div className="button-container">
        <Link to={'prodcon'}><button>Productor - Consumidor</button></Link>
        <Link to={'philosophers'}><button>Filósofos - Comensales</button></Link>
        <Link to={'readers_writers'}><button>Lectores - Escritores</button></Link>
      </div>
    </div>
  );
}

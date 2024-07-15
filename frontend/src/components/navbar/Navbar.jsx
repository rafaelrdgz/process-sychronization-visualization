import React from "react";
import "./Navbar.css";
import { Link } from "react-router-dom";


export default function Navbar({producerConsumer = true, philosophersDiners = true, readersWriters = true}) {

  return (
    <div>
      <nav className="nav">
        <div className="nav-left">
          <Link to={'/'}>Home</Link>
        </div>
        <div className="nav-right">
            {producerConsumer && <Link to={'/prodcon'}>Productor - Consumidor</Link>}
            {philosophersDiners && <Link to={'/philosophers'}>Filósofos - Comensales</Link>}
            {readersWriters && <Link to={'/readers_writers'}>Lectores - Escritores</Link>}
        </div>
      </nav>
    </div>
  );
}

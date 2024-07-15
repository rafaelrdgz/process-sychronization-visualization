import React from "react";
import ReactDOM from "react-dom/client";
import Home from "./layouts/home/Home";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import ProducerConsumer from "./layouts/producer-consumer/ProducerConsumer";
import DiningPhilosophers from "./layouts/dining-philosophers/DiningPhilosophers";
import ReadersWriters from "./layouts/readers-writers/ReadersWriters";
import ReloadPage from "./components/ReloadPage";

/**
 * The router object for handling routing in the application.
 *
 * @type {BrowserRouter}
 */
const router = createBrowserRouter([
  {
    path: "/",
    element: <Home></Home>,
  },
  {
    path: "/prodcon",
    element: <ProducerConsumer></ProducerConsumer>,
  },
  {
    path: "/prodcon/animated_version",
    element: <ReloadPage />,
  },
  {
    path: "/philosophers",
    element: <DiningPhilosophers></DiningPhilosophers>,
  },
  {
    path: "/philosophers/animated_version",
    element: <ReloadPage />,
  },
  {
    path: "/readers_writers",
    element: <ReadersWriters></ReadersWriters>,
  },
]);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

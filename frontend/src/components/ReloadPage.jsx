import { useEffect } from 'react';

const ReloadPage = () => {
  useEffect(() => {
    window.location.reload();
  }, []); // El array vacío asegura que esta función se ejecute solo al montar el componente
};

export default ReloadPage;

import { useEffect, useState } from "react";
import axios from "axios";

const API_BASE_URL = "http://3.222.161.109:8080";

function App() {
  const [user, setUser] = useState(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    axios.get(`${API_BASE_URL}/api/me/`, {
      withCredentials: true, // <-- para que mande la cookie de sesión
    })
      .then((res) => {
        setUser(res.data);
        setChecking(false);
      })
      .catch((err) => {
        setUser(null);
        setChecking(false);
      });
  }, []);

  if (checking) {
    return <p>Verificando sesión...</p>;
  }

  if (!user) {
    return (
      <div style={{ padding: 20 }}>
        <h1>WMS Provesi</h1>
        <p>No has iniciado sesión.</p>
        <a href={`${API_BASE_URL}/login/auth0/`}>
          Iniciar sesión con Auth0
        </a>
      </div>
    );
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>WMS Provesi</h1>
      <p>Hola, {user.username} ({user.email})</p>
      <a href={`${API_BASE_URL}/logout/`}>Cerrar sesión</a>

      {/* Aquí ya puedes renderizar tus componentes de pedidos/productos */}
      {/* Por ejemplo: <Pedidos /> que haga GET a /api/pedidos/listar/ */}
    </div>
  );
}

export default App;


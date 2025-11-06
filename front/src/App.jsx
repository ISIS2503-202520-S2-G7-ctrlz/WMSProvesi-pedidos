import { useAuth0 } from "@auth0/auth0-react";
import axios from "axios";

function App() {
  const { loginWithRedirect, logout, user, isAuthenticated, getAccessTokenSilently } = useAuth0();

  const getPedidos = async () => {
  try {
    const token = await getAccessTokenSilently({
      audience: import.meta.env.VITE_AUTH0_AUDIENCE,
    });

    console.log("Token:", token);
    const res = await axios.get(
      `${import.meta.env.VITE_API_BASE_URL}/pedidos/listar/`,
      { headers: { Authorization: `Bearer ${token}` } }
    );

    alert(JSON.stringify(res.data, null, 2));
  } catch (err) {
    console.error(err);
    alert("Error accediendo al backend");
  }
};


  return (
    <div style={{ padding: 30 }}>
      <h1>🚀 WMSProvesi</h1>
      {!isAuthenticated ? (
        <button onClick={() => loginWithRedirect()}>Iniciar sesión</button>
      ) : (
        <>
          <p>Bienvenido, {user.name}</p>
          <button onClick={() => logout({ returnTo: window.location.origin })}>Cerrar sesión</button>
          <br /><br />
          <button onClick={getPedidos}>Consultar pedidos (API protegida)</button>
        </>
      )}
    </div>
  );
}

export default App;

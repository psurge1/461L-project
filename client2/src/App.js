import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from "react-router-dom";
import ProjectSelection from "./components/ProjectSelection";
import ResourceManagement from "./components/ResourceManagement";
import axios from "axios";

function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);

  // Check if already logged in on reload
  useEffect(() => {
    const storedId = localStorage.getItem("userId");
    if (storedId) {
      setUserId(storedId);
      setLoggedIn(true);
    }
  }, []);

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/login", { userId, password }, {
        headers: { "Content-Type": "application/json" }
      });

      if (response.data.status === "success") {
        localStorage.setItem("userId", userId);
        setLoggedIn(true);
      }
    } catch (error) {
      alert("Invalid Login!");
      console.log(error);
    }
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:5000/add_user", { userId, password }, {
        headers: { "Content-Type": "application/json" }
      });

      if (response.data.status === "success") {
        setIsLogin(true);
      } else {
        alert("Try a different username and/or password!");
      }
    } catch (error) {
      alert("Try a different username and/or password!");
      console.log(error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("userId");
    setUserId('');
    setPassword('');
    setLoggedIn(false);
  };

  return (
    <Router>
      <div style={{ textAlign: "center", marginTop: "50px" }}>
        <nav style={{ marginBottom: "20px" }}>
          <Link to="/">Home</Link> |{" "}
          <Link to="/projects">Project Selection</Link> |{" "}
          <Link to="/resources">Resource Management</Link>
          {loggedIn && (
            <>
              {" "} | <span style={{ fontWeight: "bold" }}>Welcome, {userId}!</span>
              {" "} <button onClick={handleLogout} style={{ marginLeft: "10px" }}>
                Log Out
              </button>
            </>
          )}
        </nav>

        <Routes>
          <Route
            path="/"
            element={
              !loggedIn ? (
                <div>
                  {isLogin ? (
                    <form onSubmit={handleLogin}>
                      <h2>Login</h2>
                      <input
                        type="text"
                        placeholder="Username"
                        value={userId}
                        onChange={(e) => setUserId(e.target.value)}
                      />
                      <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                      />
                      <button type="submit">Login</button>
                    </form>
                  ) : (
                    <form onSubmit={handleSignup}>
                      <h2>Signup</h2>
                      <input
                        type="text"
                        placeholder="Username"
                        value={userId}
                        onChange={(e) => setUserId(e.target.value)}
                      />
                      <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                      />
                      <button type="submit">Signup</button>
                    </form>
                  )}
                  <button onClick={() => setIsLogin(!isLogin)}>
                    {isLogin ? "No account? Signup here" : "Have an account? Login here"}
                  </button>
                </div>
              ) : (
                <div>
                  <ProjectSelection />
                </div>
              )
            }
          />
          <Route path="/projects" element={<ProjectSelection />} />
          <Route path="/resources" element={<ResourceManagement />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

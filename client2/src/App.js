import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ProjectSelection from "./components/ProjectSelection"; // Import ProjectSelection

function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  // Function to handle login form submission
  const handleLogin = async (e) => {
    e.preventDefault();
    alert("Mock: Logging in...");
    setUser({ username });
    setLoggedIn(true);
  };

  // Function to handle signup form submission
  const handleSignup = async (e) => {
    e.preventDefault();
    alert("Mock: Signing up...");
    setIsLogin(true);
  };

  return (
    <Router>
      <div style={{ textAlign: "center", marginTop: "50px" }}>
        <nav>
          <Link to="/">Home</Link> | <Link to="/projects">Project Selection</Link>
        </nav>

        <Routes>
          {/* Home Route (Login/Signup) */}
          <Route
            path="/"
            element={
              !loggedIn ? (
                <div>
                  {isLogin ? (
                    <form onSubmit={handleLogin}>
                      <h2>Login</h2>
                      <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                      <button type="submit">Login</button>
                    </form>
                  ) : (
                    <form onSubmit={handleSignup}>
                      <h2>Signup</h2>
                      <input type="text" placeholder="Username" value={username} onChange={(e) => setUsername(e.target.value)} />
                      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                      <button type="submit">Signup</button>
                    </form>
                  )}
                  <button onClick={() => setIsLogin(!isLogin)}>{isLogin ? "No account? Signup here" : "Have an account? Login here"}</button>
                </div>
              ) : (
                <div>
                  <h2>Welcome, {user?.username || username}!</h2>
                  <ProjectSelection />
                </div>
              )
            }
          />

          {/* Separate Project Selection Route */}
          <Route path="/projects" element={<ProjectSelection />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

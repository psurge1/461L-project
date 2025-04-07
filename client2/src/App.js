import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import ProjectSelection from "./components/ProjectSelection"; // Import ProjectSelection
import ResourceManagement from "./components/ResourceManagement"; // Import ResourceManagement
import backendServerUrl from "./components/ProjectSelection"; // Import ProjectSelection
import axios from "axios";


function App() {
  const [isLogin, setIsLogin] = useState(true);
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  // Function to handle login form submission
  const handleLogin = async (e) => {
    e.preventDefault();
    // alert("Mock: Logging in...");
    // POST
    axios.post(backendServerUrl + "/login", {params: { userId, password}}).then(response => {
      console.log(response.data);
      if (response.data["status"] === "success") {
        setUser(userId);
        setLoggedIn(true);
      }
    }).catch(error => {
      alert("Invalid Login!");
      console.log(error);
    })
  };

  // Function to handle signup form submission
  const handleSignup = async (e) => {
    e.preventDefault();
    // alert("Mock: Signing up...");
    // POST
    axios.post(backendServerUrl + "/add_user", {params: { userId, password}}).then(response => {
      console.log(response.data);
      if (response.data["status"] === "success") {
        console.log("SUCCESS");
        setIsLogin(true);
      }
      else {
        alert("Try a different username and/or password!");
      }
    }).catch(error => {
      alert("Try a different username and/or password!");
      console.log(error);
    })
  };

  return (
    <Router>
      <div style={{ textAlign: "center", marginTop: "50px" }}>
        <nav>
          <Link to="/">Home</Link> | <Link to="/projects">Project Selection</Link> | <Link to="/resources">Resource Management</Link>
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
                      <input type="text" placeholder="Username" value={userId} onChange={(e) => setUserId(e.target.value)} />
                      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                      <button type="submit">Login</button>
                    </form>
                  ) : (
                    <form onSubmit={handleSignup}>
                      <h2>Signup</h2>
                      <input type="text" placeholder="Username" value={userId} onChange={(e) => setUserId(e.target.value)} />
                      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
                      <button type="submit">Signup</button>
                    </form>
                  )}
                  <button onClick={() => setIsLogin(!isLogin)}>{isLogin ? "No account? Signup here" : "Have an account? Login here"}</button>
                </div>
              ) : (
                <div>
                  <h2>Welcome, {user?.username || userId}!</h2>
                  <ProjectSelection />
                </div>
              )
            }
          />

          {/* Separate Project Selection Route */}
          <Route path="/projects" element={<ProjectSelection />} />
          
          {/* Separate Resource Management Route */}
          <Route path="/resources" element={<ResourceManagement />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

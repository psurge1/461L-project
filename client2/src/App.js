import React, { useState } from 'react';

function App() {
  // State to toggle between Login and Signup forms
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loggedIn, setLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  // Function to handle login form submission
  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();
      if (data.status === 'success') {
        setUser(data.user);
        setLoggedIn(true);
        setMessage('Logged in successfully!');
      } else {
        setMessage(data.message || 'Login failed');
      }
    } catch (error) {
      console.error('Error during login:', error);
      setMessage('An error occurred. Please try again.');
    }
  };

  // Function to handle signup form submission
  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:5000/add_user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();
      if (data.status === 'success') {
        setMessage('Signup successful! You can now log in.');
        // Optionally clear the form fields or switch to login view
        setIsLogin(true);
      } else {
        setMessage(data.message || 'Signup failed');
      }
    } catch (error) {
      console.error('Error during signup:', error);
      setMessage('An error occurred. Please try again.');
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      {!loggedIn ? (
        <div>
          {isLogin ? (
            <form onSubmit={handleLogin}>
              <h2>Login</h2>
              <div>
                <input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  style={{ padding: '8px', margin: '5px' }}
                />
              </div>
              <div>
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  style={{ padding: '8px', margin: '5px' }}
                />
              </div>
              <button type="submit" style={{ padding: '8px 16px', margin: '10px' }}>
                Login
              </button>
            </form>
          ) : (
            <form onSubmit={handleSignup}>
              <h2>Signup</h2>
              <div>
                <input
                  type="text"
                  placeholder="Username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  style={{ padding: '8px', margin: '5px' }}
                />
              </div>
              <div>
                <input
                  type="password"
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  style={{ padding: '8px', margin: '5px' }}
                />
              </div>
              <button type="submit" style={{ padding: '8px 16px', margin: '10px' }}>
                Signup
              </button>
            </form>
          )}

          <button
            onClick={() => {
              setIsLogin(!isLogin);
              setMessage('');
            }}
            style={{ marginTop: '20px' }}
          >
            {isLogin ? 'No account? Signup here' : 'Have an account? Login here'}
          </button>
        </div>
      ) : (
        <div>
          <h2>Welcome, {user?.username || username}!</h2>
          {/* Additional components and functionality can be added here */}
        </div>
      )}
      {message && <p>{message}</p>}
    </div>
  );
}

export default App;

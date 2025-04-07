import React, { useState, useEffect } from "react";
import axios from "axios";

//change this to backend 
const backendServerUrl = "http://localhost:5000"; 

const ResourceManagement = () => {
    const [resources, setResources] = useState({});
    const [hwSet1Amount, setHwSet1Amount] = useState("");
    const [hwSet2Amount, setHwSet2Amount] = useState("");
    const [loading, setLoading] = useState(true);
    const [message, setMessage] = useState("");
  
    // Fetch resources on component mount
    useEffect(() => {
      const fetchResources = async () => {
        try {
          const response = await axios.get(`${backendServerUrl}/resources`);
          setResources(response.data);
          setLoading(false);
        } catch (error) {
          setMessage("Failed to load resources.");
          setLoading(false);
        }
      };
  
      fetchResources();
    }, []);
  
    // Checkout resources
    const handleCheckout = async (setNumber, amount) => {
      try {
        const response = await axios.post(`${backendServerUrl}/checkout`, { setNumber, amount: Number(amount) });
        setResources(response.data);
        setMessage(`Checked out ${amount} from ${setNumber}`);
      } catch (error) {
        setMessage("Checkout failed!");
      }
    };
  
    // Checkin resources
    const handleCheckin = async (setNumber, amount) => {
      try {
        const response = await axios.post(`${backendServerUrl}/checkin`, { setNumber, amount: Number(amount) });
        setResources(response.data);
        setMessage(`Checked in ${amount} to ${setNumber}`);
      } catch (error) {
        setMessage("Check-in failed!");
      }
    };

    const logOut = () => {
      alert("Logged out successfully!");
      window.location.reload(); // Or redirect to login page if needed
    };
  
    return (
      <div style={{ textAlign: "center", marginTop: "50px" }}>
        <h2>Resource Management</h2>
        {message && <p>{message}</p>}
        {loading ? (
          <p>Loading resources...</p>
        ) : (
          <div>
            <div>
              <h3>HW Set 1</h3>
              <p>Available: {resources.hwSet1?.available || 0}</p>
              <p>Capacity: {resources.hwSet1?.capacity || 200}</p>
              <input
                type="number"
                value={hwSet1Amount}
                onChange={(e) => setHwSet1Amount(e.target.value)}
                placeholder="Enter amount"
              />
              <button onClick={() => handleCheckout("hwSet1", hwSet1Amount)}>Check Out</button>
              <button onClick={() => handleCheckin("hwSet1", hwSet1Amount)}>Check In</button>
            </div>
  
            <div style={{ marginTop: "20px" }}>
              <h3>HW Set 2</h3>
              <p>Available: {resources.hwSet2?.available || 0}</p>
              <p>Capacity: {resources.hwSet2?.capacity || 200}</p>              <input
                type="number"
                value={hwSet2Amount}
                onChange={(e) => setHwSet2Amount(e.target.value)}
                placeholder="Enter amount"
              />
              <button onClick={() => handleCheckout("hwSet2", hwSet2Amount)}>Check Out</button>
              <button onClick={() => handleCheckin("hwSet2", hwSet2Amount)}>Check In</button>
            </div>

            <div style={{ marginTop: "30px" }}>
              <button onClick={logOut}>Log Out</button>
            </div>

          </div>
          
        )}
      </div>

    );
  };
  
  export default ResourceManagement;